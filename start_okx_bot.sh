#!/bin/bash

# OKX Futures ML Bot Startup Script
# Uses your trained models with OKX Futures API

echo "🚀 Starting OKX Futures ML Trading Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please create one with your API credentials."
    exit 1
fi

# Check if OKX API credentials are set
source .env
if [ -z "$OKX_API_KEY" ] || [ -z "$OKX_API_SECRET" ] || [ -z "$OKX_PASSPHRASE" ]; then
    echo "❌ OKX API credentials not set in .env file"
    echo "Please add:"
    echo "OKX_API_KEY=your_okx_api_key"
    echo "OKX_API_SECRET=your_okx_api_secret"
    echo "OKX_PASSPHRASE=your_okx_passphrase"
    exit 1
fi

# Create logs directory
mkdir -p logs

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please create one first."
    echo "Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Install OKX library if not installed
echo "🔧 Checking OKX library..."
source venv/bin/activate
python -c "import okx" 2>/dev/null || pip install okx

# Activate virtual environment and run bot
echo "🔧 Starting OKX Futures bot..."
source venv/bin/activate && python okx_futures_bot.py

echo "✅ OKX Futures bot stopped."
