#!/usr/bin/env python3
"""
Trading controls router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from api.database import get_db
from api.services.trading_service import TradingService
from api.services.balance_service import BalanceService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/status")
async def get_trading_status():
    """Get current trading status"""
    try:
        trading_service = TradingService()
        status = trading_service.get_trading_status()
        return status
    except Exception as e:
        logger.error(f"Failed to get trading status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trading status")

@router.post("/start")
async def start_trading():
    """Start trading"""
    try:
        trading_service = TradingService()
        result = trading_service.start_trading()
        return result
    except Exception as e:
        logger.error(f"Failed to start trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to start trading")

@router.post("/stop")
async def stop_trading():
    """Stop trading"""
    try:
        trading_service = TradingService()
        result = trading_service.stop_trading()
        return result
    except Exception as e:
        logger.error(f"Failed to stop trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to stop trading")

@router.post("/pause")
async def pause_trading():
    """Pause trading"""
    try:
        trading_service = TradingService()
        result = trading_service.pause_trading()
        return result
    except Exception as e:
        logger.error(f"Failed to pause trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to pause trading")

@router.post("/emergency-stop")
async def emergency_stop():
    """Emergency stop all trading"""
    try:
        trading_service = TradingService()
        result = trading_service.emergency_stop()
        return result
    except Exception as e:
        logger.error(f"Failed to execute emergency stop: {e}")
        raise HTTPException(status_code=500, detail="Failed to execute emergency stop")

@router.get("/positions")
async def get_positions():
    """Get current positions"""
    try:
        trading_service = TradingService()
        positions = trading_service.get_positions()
        return positions
    except Exception as e:
        logger.error(f"Failed to get positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get positions")

@router.get("/settings")
async def get_trading_settings():
    """Get trading settings"""
    try:
        trading_service = TradingService()
        settings = trading_service.get_trading_settings()
        return settings
    except Exception as e:
        logger.error(f"Failed to get trading settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to get trading settings")

@router.post("/settings")
async def update_trading_settings(settings: dict):
    """Update trading settings"""
    try:
        trading_service = TradingService()
        success = trading_service.update_trading_settings(settings)
        if success:
            return {"message": "Trading settings updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update trading settings")
    except Exception as e:
        logger.error(f"Failed to update trading settings: {e}")
        raise HTTPException(status_code=500, detail="Failed to update trading settings")

@router.get("/balance")
async def get_account_balance():
    """Get current account balance"""
    try:
        balance_service = BalanceService()
        balance = balance_service.get_account_balance()
        return balance
    except Exception as e:
        logger.error(f"Failed to get account balance: {e}")
        raise HTTPException(status_code=500, detail="Failed to get account balance")

@router.get("/balance/summary")
async def get_balance_summary():
    """Get balance summary for dashboard"""
    try:
        balance_service = BalanceService()
        summary = balance_service.get_balance_summary()
        return summary
    except Exception as e:
        logger.error(f"Failed to get balance summary: {e}")
        raise HTTPException(status_code=500, detail="Failed to get balance summary")

@router.post("/balance/refresh")
async def refresh_balance():
    """Force refresh account balance"""
    try:
        balance_service = BalanceService()
        balance = balance_service.refresh_balance()
        return {"message": "Balance refreshed successfully", "balance": balance}
    except Exception as e:
        logger.error(f"Failed to refresh balance: {e}")
        raise HTTPException(status_code=500, detail="Failed to refresh balance")

@router.get("/balance/history")
async def get_balance_history(days: int = 7):
    """Get balance history for charts"""
    try:
        balance_service = BalanceService()
        history = balance_service.get_balance_history(days)
        return history
    except Exception as e:
        logger.error(f"Failed to get balance history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get balance history")

@router.post("/auto-trading/enable")
async def enable_auto_trading():
    """Enable auto trading"""
    try:
        trading_service = TradingService()
        success = trading_service.update_trading_settings({"auto_trading": True})
        if success:
            return {"message": "Auto trading enabled successfully", "auto_trading": True}
        else:
            raise HTTPException(status_code=500, detail="Failed to enable auto trading")
    except Exception as e:
        logger.error(f"Failed to enable auto trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to enable auto trading")

@router.post("/auto-trading/disable")
async def disable_auto_trading():
    """Disable auto trading"""
    try:
        trading_service = TradingService()
        success = trading_service.update_trading_settings({"auto_trading": False})
        if success:
            return {"message": "Auto trading disabled successfully", "auto_trading": False}
        else:
            raise HTTPException(status_code=500, detail="Failed to disable auto trading")
    except Exception as e:
        logger.error(f"Failed to disable auto trading: {e}")
        raise HTTPException(status_code=500, detail="Failed to disable auto trading")

@router.get("/auto-trading/status")
async def get_auto_trading_status():
    """Get auto trading status"""
    try:
        trading_service = TradingService()
        settings = trading_service.get_trading_settings()
        return {"auto_trading": settings.get("auto_trading", False)}
    except Exception as e:
        logger.error(f"Failed to get auto trading status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get auto trading status")
