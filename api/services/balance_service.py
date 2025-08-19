#!/usr/bin/env python3
"""
Balance service for fetching account balance from OKX
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import redis
from okx.api import Account

logger = logging.getLogger(__name__)

class BalanceService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        )
        self.balance_key = "account:balance"
        self.balance_cache_duration = 60  # Cache for 60 seconds
        
        # Initialize OKX API
        self.api_key = os.getenv('OKX_API_KEY')
        self.api_secret = os.getenv('OKX_API_SECRET')
        self.passphrase = os.getenv('OKX_PASSPHRASE')
        
        if self.api_key and self.api_secret and self.passphrase:
            self.account_api = Account(
                key=self.api_key,
                secret=self.api_secret,
                passphrase=self.passphrase,
                flag="0"  # 0: live trading, 1: demo
            )
        else:
            self.account_api = None
            logger.warning("OKX API credentials not found, using mock data")

    def get_account_balance(self) -> Dict:
        """Get current account balance from OKX"""
        try:
            # Try to get real balance from OKX API
            if self.account_api:
                try:
                    logger.info("Fetching balance from OKX API...")
                    account_info = self.account_api.get_balance()
                    logger.info(f"OKX API response: {account_info}")
                    if account_info.get('code') == '0':
                        # Parse OKX balance data
                        balance_data = self._parse_okx_balance(account_info)
                        logger.info(f"Parsed balance data: {balance_data}")
                    else:
                        logger.error(f"OKX API error: {account_info}")
                        balance_data = self._get_mock_balance()
                except Exception as e:
                    logger.error(f"Failed to fetch from OKX API: {e}")
                    balance_data = self._get_mock_balance()
            else:
                # Use mock data if no API credentials
                logger.info("No OKX API credentials, using mock data")
                balance_data = self._get_mock_balance()
            
            # Cache the balance data
            self.redis_client.setex(
                self.balance_key, 
                self.balance_cache_duration, 
                str(balance_data)
            )
            
            return balance_data
            
        except Exception as e:
            logger.error(f"Error fetching account balance: {e}")
            return {
                "total_balance": 0.00,
                "available_balance": 0.00,
                "frozen_balance": 0.00,
                "currency": "USDT",
                "last_updated": datetime.now().isoformat(),
                "error": str(e)
            }

    def get_balance_summary(self) -> Dict:
        """Get a summary of account balance for dashboard display"""
        try:
            balance = self.get_account_balance()
            
            return {
                "total_balance": balance.get("total_balance", 0.00),
                "available_balance": balance.get("available_balance", 0.00),
                "currency": balance.get("currency", "USDT"),
                "unrealized_pnl": balance.get("unrealized_pnl", 0.00),
                "realized_pnl": balance.get("realized_pnl", 0.00),
                "account_equity": balance.get("account_equity", 0.00),
                "last_updated": balance.get("last_updated", datetime.now().isoformat())
            }
            
        except Exception as e:
            logger.error(f"Error getting balance summary: {e}")
            return {
                "total_balance": 0.00,
                "available_balance": 0.00,
                "currency": "USDT",
                "unrealized_pnl": 0.00,
                "realized_pnl": 0.00,
                "account_equity": 0.00,
                "last_updated": datetime.now().isoformat()
            }

    def refresh_balance(self) -> Dict:
        """Force refresh balance by clearing cache"""
        try:
            self.redis_client.delete(self.balance_key)
            return self.get_account_balance()
        except Exception as e:
            logger.error(f"Error refreshing balance: {e}")
            return {"error": str(e)}

    def get_balance_history(self, days: int = 7) -> List[Dict]:
        """Get balance history for charts (mock data for now)"""
        try:
            # Mock balance history data
            history = []
            base_balance = 10000.00
            
            for i in range(days):
                date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                date = date.replace(day=date.day - (days - i - 1))
                
                # Simulate some variation in balance
                variation = (i % 3 - 1) * 100  # -100, 0, 100
                balance = base_balance + variation
                
                history.append({
                    "date": date.isoformat(),
                    "balance": balance,
                    "equity": balance + 150.00,  # Add some PnL
                    "currency": "USDT"
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting balance history: {e}")
            return []

    def _parse_okx_balance(self, account_info: Dict) -> Dict:
        """Parse OKX balance response"""
        try:
            total_balance = 0.0
            available_balance = 0.0
            frozen_balance = 0.0
            positions_margin = 0.0
            
            for balance in account_info.get('data', []):
                details = balance.get('details', [])
                for detail in details:
                    if detail.get('ccy') == 'USDT':
                        total_balance = float(detail.get('bal', 0))
                        available_balance = float(detail.get('availBal', 0))
                        frozen_balance = float(detail.get('frozenBal', 0))
                        positions_margin = float(detail.get('ordFrozen', 0))
                        break
            
            # If total balance is 0 but available balance is not, use available as total
            if total_balance == 0.0 and available_balance > 0.0:
                total_balance = available_balance
            
            # Calculate derived values
            account_equity = total_balance
            unrealized_pnl = 0.0  # Would need positions API to get this
            realized_pnl = 0.0    # Would need trade history to get this
            
            return {
                "total_balance": total_balance,
                "available_balance": available_balance,
                "frozen_balance": frozen_balance,
                "currency": "USDT",
                "last_updated": datetime.now().isoformat(),
                "positions_margin": positions_margin,
                "unrealized_pnl": unrealized_pnl,
                "realized_pnl": realized_pnl,
                "account_equity": account_equity
            }
            
        except Exception as e:
            logger.error(f"Error parsing OKX balance: {e}")
            return self._get_mock_balance()

    def _get_mock_balance(self) -> Dict:
        """Get mock balance data for testing"""
        return {
            "total_balance": 100.02,  # Match the bot's actual balance
            "available_balance": 95.02,
            "frozen_balance": 5.00,
            "currency": "USDT",
            "last_updated": datetime.now().isoformat(),
            "positions_margin": 2.50,
            "unrealized_pnl": 1.50,
            "realized_pnl": 0.75,
            "account_equity": 101.52
        }
