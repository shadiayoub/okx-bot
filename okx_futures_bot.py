#!/usr/bin/env python3
"""
OKX Futures ML Trading Bot
Uses your trained models with OKX Futures API
"""

import asyncio
import logging
import os
import sys
import time
import json
import redis
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import numpy as np
from okx.api import Account, Trade, Market
from dotenv import load_dotenv

# Add strategies to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'strategies'))

from enhanced_strategy import EnhancedStrategy
from prediction_models import PricePredictor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/okx_trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class OKXFuturesBot:
    """OKX Futures ML-based trading bot using your trained models"""
    
    def __init__(self):
        self.api_key = os.getenv('OKX_API_KEY')
        self.api_secret = os.getenv('OKX_API_SECRET')
        self.passphrase = os.getenv('OKX_PASSPHRASE')
        
        # Trading parameters
        self.leverage = int(os.getenv('LEVERAGE', '10'))
        self.risk_per_trade = float(os.getenv('RISK_PER_TRADE', '0.05'))
        self.min_signal_strength = float(os.getenv('MIN_SIGNAL_STRENGTH', '0.3'))
        self.stop_loss_pct = float(os.getenv('STOP_LOSS_PCT', '0.02'))
        self.take_profit_pct = float(os.getenv('TAKE_PROFIT_PCT', '0.04'))
        
        # Trading pairs (OKX format)
        self.symbols = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BNB-USDT-SWAP', 'ADA-USDT-SWAP', 'SOL-USDT-SWAP']
        
        # Initialize OKX clients
        self.account_api = None
        self.trade_api = None
        self.market_api = None
        
        # Initialize components
        self.strategies = {}
        self.predictors = {}
        self.positions = {}
        self.running = False
        
        # Initialize Redis connection
        self.redis_client = redis.Redis.from_url(
            os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        )
        
        logger.info(f"🤖 OKX Futures Bot initialized")
        logger.info(f"⚡ Leverage: {self.leverage}x")
        logger.info(f"🎯 Risk per trade: {self.risk_per_trade*100}%")
    
    async def initialize(self):
        """Initialize the bot"""
        try:
            # Initialize OKX APIs
            self.account_api = Account(
                key=self.api_key,
                secret=self.api_secret,
                passphrase=self.passphrase,
                flag="0"  # 0: live trading, 1: demo
            )
            
            self.trade_api = Trade(
                key=self.api_key,
                secret=self.api_secret,
                passphrase=self.passphrase,
                flag="0"
            )
            
            self.market_api = Market(
                key=self.api_key,
                secret=self.api_secret,
                passphrase=self.passphrase,
                flag="0"
            )
            
            # Test connection
            account_info = self.account_api.get_balance()
            if account_info.get('code') == '0':
                logger.info("✅ Connected to OKX Futures")
            else:
                logger.error(f"❌ OKX connection failed: {account_info}")
                return False
            
            # Initialize strategies and models
            await self._initialize_components()
            
            # Get account balance
            balance = await self._get_balance()
            logger.info(f"💰 OKX Futures balance: ${balance:.2f}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize: {e}")
            return False
    
    async def _initialize_components(self):
        """Initialize ML models and strategies"""
        # Map OKX symbols to model symbols
        symbol_mapping = {
            'BTC-USDT-SWAP': 'BTCUSDT',
            'ETH-USDT-SWAP': 'ETHUSDT',
            'BNB-USDT-SWAP': 'BNBUSDT',
            'ADA-USDT-SWAP': 'ADAUSDT',
            'SOL-USDT-SWAP': 'SOLUSDT'
        }
        
        for okx_symbol, model_symbol in symbol_mapping.items():
            try:
                # Initialize strategy
                config_dict = {
                    "LEVERAGE": self.leverage,
                    "RISK_PER_TRADE": self.risk_per_trade,
                    "MIN_SIGNAL_STRENGTH": self.min_signal_strength,
                    "STOP_LOSS_PCT": self.stop_loss_pct,
                    "TAKE_PROFIT_PCT": self.take_profit_pct
                }
                self.strategies[okx_symbol] = EnhancedStrategy(config_dict)
                
                # Load ML model
                model_path = os.path.join('models', f'{model_symbol}_gradient_boosting.joblib')
                if os.path.exists(model_path):
                    self.predictors[okx_symbol] = PricePredictor()
                    self.predictors[okx_symbol].load_model(model_path)
                    logger.info(f"✅ ML model loaded for {okx_symbol}")
                else:
                    logger.warning(f"⚠️ No ML model found for {okx_symbol}")
                    
            except Exception as e:
                logger.error(f"❌ Failed to initialize {okx_symbol}: {e}")
    
    async def _get_balance(self) -> float:
        """Get OKX Futures account balance"""
        try:
            account_info = self.account_api.get_balance()
            if account_info.get('code') == '0':
                for balance in account_info.get('data', []):
                    # Look in the details array for USDT balance
                    details = balance.get('details', [])
                    for detail in details:
                        if detail.get('ccy') == 'USDT':
                            return float(detail.get('availBal', 0))
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return 0.0

    def _get_auto_trading_status(self) -> bool:
        """Get auto trading status from Redis"""
        try:
            settings = self.redis_client.get("trading:settings")
            if settings:
                settings_data = json.loads(settings)
                return settings_data.get("auto_trading", True)  # Default to True
            return True  # Default to True if no settings found
        except Exception as e:
            logger.error(f"Failed to get auto trading status: {e}")
            return True  # Default to True on error

    def _get_trading_status(self) -> str:
        """Get trading status from Redis"""
        try:
            status = self.redis_client.get("trading:status")
            if status:
                status_data = json.loads(status)
                return status_data.get("status", "stopped")
            return "stopped"
        except Exception as e:
            logger.error(f"Failed to get trading status: {e}")
            return "stopped"
    
    async def _get_market_data(self, symbol: str) -> pd.DataFrame:
        """Get market data for analysis"""
        try:
            # Get recent klines from OKX
            klines = self.market_api.get_candles(
                instId=symbol,
                bar='1H',
                limit='100'
            )
            
            if klines.get('code') == '0':
                data = klines.get('data', [])
                if data:
                    df = pd.DataFrame(data, columns=[
                        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'volCcy', 'volCcyQuote', 'confirm'
                    ])
                    
                    # Convert to numeric
                    for col in ['open', 'high', 'low', 'close', 'volume']:
                        df[col] = pd.to_numeric(df[col])
                    
                    return df
            else:
                logger.error(f"Failed to get market data: {klines}")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Failed to get market data for {symbol}: {e}")
            return pd.DataFrame()
    
    async def _generate_signal(self, symbol: str, df: pd.DataFrame) -> tuple:
        """Generate trading signal using ML model"""
        try:
            if symbol not in self.strategies:
                return None, 0.0
            
            # Generate signal using your strategy
            signal, strength, signal_data = self.strategies[symbol].generate_signal(df)
            
            # Get current real-time price from ticker
            ticker_info = self.market_api.get_ticker(instId=symbol)
            if ticker_info.get('code') == '0':
                current_price = float(ticker_info['data'][0]['last'])
            else:
                # Fallback to candlestick close price
                current_price = float(df['close'].iloc[-1])
            
            # Log detailed analysis
            logger.info(f"[{symbol}] Price: ${current_price:.2f}, Signal: {signal}, Strength: {strength:.2f}")
            
            # Log detailed analysis if signal_data is available
            if signal_data and 'technical_signals' in signal_data:
                tech_signals = signal_data['technical_signals']
                ml_pred = signal_data.get('ml_prediction', 0)
                ml_conf = signal_data.get('ml_confidence', 0)
                
                logger.info(f"[{symbol}] Technical Analysis:")
                logger.info(f"  EMA Signal: {tech_signals.get('ema_signal', 0):.2f}")
                logger.info(f"  RSI Signal: {tech_signals.get('rsi_signal', 0):.2f}")
                logger.info(f"  BB Signal: {tech_signals.get('bb_signal', 0):.2f}")
                logger.info(f"  MACD Signal: {tech_signals.get('macd_signal', 0):.2f}")
                logger.info(f"  Volume Signal: {tech_signals.get('volume_signal', 0):.2f}")
                logger.info(f"  Momentum Signal: {tech_signals.get('momentum_signal', 0):.2f}")
                logger.info(f"[{symbol}] ML Analysis:")
                logger.info(f"  ML Prediction: {ml_pred:.4f}")
                logger.info(f"  ML Confidence: {ml_conf:.2f}")
                
                # Calculate what the combined score would be
                if hasattr(self.strategies[symbol], 'combine_signals'):
                    tech_score = sum([
                        tech_signals.get('ema_signal', 0) * 0.3,
                        tech_signals.get('rsi_signal', 0) * 0.2,
                        tech_signals.get('bb_signal', 0) * 0.15,
                        tech_signals.get('macd_signal', 0) * 0.15,
                        tech_signals.get('volume_signal', 0) * 0.1,
                        tech_signals.get('momentum_signal', 0) * 0.1
                    ])
                    ml_weight = min(ml_conf, 0.8)
                    tech_weight = 1.0 - ml_weight
                    combined_score = (tech_score * tech_weight + np.sign(ml_pred) * ml_weight)
                    logger.info(f"[{symbol}] Combined Score: {combined_score:.3f} (Threshold: 0.3)")
            
            return signal, strength
            
        except Exception as e:
            logger.error(f"Failed to generate signal for {symbol}: {e}")
            return None, 0.0
    
    async def _execute_trade(self, symbol: str, signal: str, price: float, strength: float):
        """Execute trade based on signal"""
        try:
            # Check if we already have a position
            if symbol in self.positions:
                logger.info(f"Already have position in {symbol}, skipping")
                return
            
            # Calculate position size
            balance = await self._get_balance()
            position_size = balance * self.risk_per_trade * self.leverage
            
            # Determine order side
            side = 'buy' if signal == 'BUY' else 'sell'
            
            # Calculate quantity
            quantity = position_size / price
            
            # Place order
            order = self.trade_api.set_order(
                instId=symbol,
                tdMode='cross',
                side=side,
                ordType='market',
                sz=str(quantity)
            )
            
            if order.get('code') == '0':
                # Store position info
                self.positions[symbol] = {
                    'side': side,
                    'entry_price': price,
                    'quantity': quantity,
                    'order_id': order.get('data', [{}])[0].get('ordId', ''),
                    'signal_strength': strength,
                    'timestamp': datetime.now()
                }
                
                logger.info(f"✅ {signal} order placed for {symbol}")
                logger.info(f"   Price: ${price:.2f}")
                logger.info(f"   Position Size: ${position_size:.2f}")
                logger.info(f"   Signal Strength: {strength:.2f}")
                
                # Place stop loss and take profit
                await self._place_stop_orders(symbol, side, price, quantity)
                
        except Exception as e:
            logger.error(f"Failed to execute trade for {symbol}: {e}")
    
    async def _place_stop_orders(self, symbol: str, side: str, entry_price: float, quantity: float):
        """Place stop loss and take profit orders"""
        try:
            if side == 'buy':
                # Long position
                stop_price = entry_price * (1 - self.stop_loss_pct)
                take_profit_price = entry_price * (1 + self.take_profit_pct)
                stop_side = 'sell'
            else:
                # Short position
                stop_price = entry_price * (1 + self.stop_loss_pct)
                take_profit_price = entry_price * (1 - self.take_profit_pct)
                stop_side = 'buy'
            
            # Place stop loss
            self.trade_api.set_order(
                instId=symbol,
                tdMode='cross',
                side=stop_side,
                ordType='conditional',
                sz=str(quantity),
                slTriggerPx=str(stop_price),
                slOrdPx=str(stop_price)
            )
            logger.info(f"Stop loss placed for {symbol} @ ${stop_price:.2f}")
            
            # Place take profit
            self.trade_api.set_order(
                instId=symbol,
                tdMode='cross',
                side=stop_side,
                ordType='conditional',
                sz=str(quantity),
                tpTriggerPx=str(take_profit_price),
                tpOrdPx=str(take_profit_price)
            )
            logger.info(f"Take profit placed for {symbol} @ ${take_profit_price:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to place stop orders for {symbol}: {e}")
    
    async def run(self):
        """Main trading loop"""
        logger.info("🚀 Starting OKX Futures ML Trading Bot...")
        self.running = True
        
        while self.running:
            try:
                # Check trading status from Redis
                trading_status = self._get_trading_status()
                auto_trading_enabled = self._get_auto_trading_status()
                
                if trading_status != "running":
                    logger.info(f"Trading status: {trading_status}, waiting...")
                    await asyncio.sleep(10)  # Check every 10 seconds
                    continue
                
                for symbol in self.symbols:
                    # Get market data
                    df = await self._get_market_data(symbol)
                    if df.empty:
                        continue
                    
                    # Generate signal
                    signal, strength = await self._generate_signal(symbol, df)
                    
                    # Execute trade if signal is strong enough and auto-trading is enabled
                    if signal and strength > self.min_signal_strength:
                        current_price = float(df['close'].iloc[-1])
                        
                        if auto_trading_enabled:
                            logger.info(f"🤖 Auto-trading enabled - Executing {signal} trade for {symbol}")
                            await self._execute_trade(symbol, signal, current_price, strength)
                        else:
                            logger.info(f"📊 Signal detected but auto-trading disabled - {signal} for {symbol} (Strength: {strength:.2f})")
                
                # Wait before next iteration
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(30)
    
    async def stop(self):
        """Stop the bot"""
        logger.info("🛑 Stopping OKX Futures ML Trading Bot...")
        self.running = False
        
        # Close all positions
        for symbol in self.positions:
            try:
                position = self.positions[symbol]
                close_side = 'sell' if position['side'] == 'buy' else 'buy'
                
                self.trade_api.set_order(
                    instId=symbol,
                    tdMode='cross',
                    side=close_side,
                    ordType='market',
                    sz=str(position['quantity'])
                )
                logger.info(f"Closing position for {symbol}")
                
            except Exception as e:
                logger.error(f"Failed to close position for {symbol}: {e}")

async def main():
    """Main function"""
    bot = OKXFuturesBot()
    
    # Initialize bot
    if not await bot.initialize():
        logger.error("Failed to initialize bot")
        return
    
    try:
        # Run the bot
        await bot.run()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    finally:
        # Stop the bot
        await bot.stop()

if __name__ == "__main__":
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Run the bot
    asyncio.run(main())
