# OKX Futures ML Trading Bot

A clean, production-ready ML-based trading bot for OKX Futures using your trained models.

## 🚀 Features

- **ML-Powered Trading**: Uses your trained gradient boosting models for price prediction
- **Multi-Symbol Support**: Trades BTC, ETH, BNB, ADA, and SOL simultaneously
- **Real-Time Pricing**: Accurate price feeds from OKX Futures API
- **Risk Management**: Configurable leverage, stop-loss, and take-profit
- **Live Trading**: Ready for production with proper risk controls

## 📁 Clean Structure

```
clean_hummingbot_bot/
├── okx_futures_bot.py      # Main trading bot
├── start_okx_bot.sh        # Startup script
├── env.example             # Environment template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── strategies/            # Trading strategies
│   ├── enhanced_strategy.py
│   └── prediction_models.py
├── models/                # Your trained ML models
│   ├── BTCUSDT_gradient_boosting.joblib
│   ├── ETHUSDT_gradient_boosting.joblib
│   ├── BNBUSDT_gradient_boosting.joblib
│   ├── ADAUSDT_gradient_boosting.joblib
│   └── SOLUSDT_gradient_boosting.joblib
└── logs/                  # Trading logs
    └── okx_trading_bot.log
```

## 🛠️ Setup

1. **Copy environment template**:
   ```bash
   cp env.example .env
   ```

2. **Configure your API credentials** in `.env`:
   ```bash
   # OKX API Configuration
   OKX_API_KEY=your_okx_api_key
   OKX_API_SECRET=your_okx_api_secret
   OKX_PASSPHRASE=your_okx_passphrase
   
   # Trading Parameters
   LEVERAGE=10
   RISK_PER_TRADE=0.05
   MIN_SIGNAL_STRENGTH=0.3
   STOP_LOSS_PCT=0.02
   TAKE_PROFIT_PCT=0.04
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

**Start the bot**:
```bash
./start_okx_bot.sh
```

**Monitor logs**:
```bash
tail -f logs/okx_trading_bot.log
```

## ⚙️ Configuration

### Trading Parameters

- **Leverage**: 10x (configurable)
- **Risk per Trade**: 5% of account balance
- **Minimum Signal Strength**: 30% confidence required
- **Stop Loss**: 2% from entry
- **Take Profit**: 4% from entry

### Supported Symbols

- BTC-USDT-SWAP
- ETH-USDT-SWAP  
- BNB-USDT-SWAP
- ADA-USDT-SWAP
- SOL-USDT-SWAP

## 📊 Performance

The bot uses your trained ML models to:
- Analyze market data in real-time
- Generate buy/sell signals with confidence scores
- Execute trades with proper risk management
- Monitor positions and apply stop-loss/take-profit

## 🔒 Safety Features

- **Balance Verification**: Confirms account balance before trading
- **Signal Validation**: Only trades on strong signals (≥30% confidence)
- **Risk Limits**: Maximum 5% risk per trade
- **Stop Orders**: Automatic stop-loss and take-profit placement
- **Error Handling**: Graceful handling of API errors and network issues

## 📝 Logging

All trading activity is logged to `logs/okx_trading_bot.log`:
- Price updates
- Signal generation
- Trade executions
- Error messages
- Account balance updates

## ⚠️ Important Notes

- **Live Trading**: This bot trades with real money
- **Test First**: Verify your setup with small amounts
- **Monitor**: Always monitor the bot's performance
- **Backup**: Keep backups of your models and configuration

## 🆘 Troubleshooting

**Bot not starting**: Check your API credentials in `.env`
**No trades**: Verify signal strength threshold and market conditions
**API errors**: Check OKX API status and your account permissions

---

**Status**: ✅ Production Ready  
**Last Updated**: August 2024
