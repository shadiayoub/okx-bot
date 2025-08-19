#!/usr/bin/env python3
"""
Core configuration settings
"""

import os
from typing import Optional

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://trading_user:trading_pass@localhost:5432/trading_bot")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OKX API
    OKX_API_KEY: Optional[str] = os.getenv("OKX_API_KEY")
    OKX_API_SECRET: Optional[str] = os.getenv("OKX_API_SECRET")
    OKX_PASSPHRASE: Optional[str] = os.getenv("OKX_PASSPHRASE")
    
    # Trading Parameters
    LEVERAGE: int = int(os.getenv("LEVERAGE", "10"))
    RISK_PER_TRADE: float = float(os.getenv("RISK_PER_TRADE", "0.05"))
    MIN_SIGNAL_STRENGTH: float = float(os.getenv("MIN_SIGNAL_STRENGTH", "0.3"))
    STOP_LOSS_PCT: float = float(os.getenv("STOP_LOSS_PCT", "0.02"))
    TAKE_PROFIT_PCT: float = float(os.getenv("TAKE_PROFIT_PCT", "0.04"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
