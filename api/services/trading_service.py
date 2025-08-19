#!/usr/bin/env python3
"""
Trading service for managing trading operations
"""

import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
import redis

logger = logging.getLogger(__name__)

class TradingService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(
            os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        )
        self.status_key = "trading:status"
        self.positions_key = "trading:positions"
        self.settings_key = "trading:settings"

    def get_trading_status(self) -> Dict:
        """Get current trading status"""
        try:
            status = self.redis_client.get(self.status_key)
            if status:
                return json.loads(status)
            else:
                # Default status
                default_status = {
                    "status": "stopped",
                    "last_updated": datetime.now().isoformat(),
                    "active_symbols": [],
                    "total_positions": 0,
                    "total_pnl": 0.0
                }
                self.redis_client.set(self.status_key, json.dumps(default_status))
                return default_status
        except Exception as e:
            logger.error(f"Error getting trading status: {e}")
            return {"status": "error", "message": str(e)}

    def set_trading_status(self, status: str, **kwargs) -> bool:
        """Set trading status"""
        try:
            current_status = self.get_trading_status()
            current_status.update({
                "status": status,
                "last_updated": datetime.now().isoformat(),
                **kwargs
            })
            self.redis_client.set(self.status_key, json.dumps(current_status))
            logger.info(f"Trading status updated to: {status}")
            return True
        except Exception as e:
            logger.error(f"Error setting trading status: {e}")
            return False

    def start_trading(self) -> Dict:
        """Start trading"""
        try:
            success = self.set_trading_status("running")
            if success:
                return {"message": "Trading started successfully", "status": "running"}
            else:
                return {"message": "Failed to start trading", "status": "error"}
        except Exception as e:
            logger.error(f"Error starting trading: {e}")
            return {"message": f"Error starting trading: {str(e)}", "status": "error"}

    def stop_trading(self) -> Dict:
        """Stop trading"""
        try:
            success = self.set_trading_status("stopped")
            if success:
                return {"message": "Trading stopped successfully", "status": "stopped"}
            else:
                return {"message": "Failed to stop trading", "status": "error"}
        except Exception as e:
            logger.error(f"Error stopping trading: {e}")
            return {"message": f"Error stopping trading: {str(e)}", "status": "error"}

    def pause_trading(self) -> Dict:
        """Pause trading"""
        try:
            success = self.set_trading_status("paused")
            if success:
                return {"message": "Trading paused successfully", "status": "paused"}
            else:
                return {"message": "Failed to pause trading", "status": "error"}
        except Exception as e:
            logger.error(f"Error pausing trading: {e}")
            return {"message": f"Error pausing trading: {str(e)}", "status": "error"}

    def emergency_stop(self) -> Dict:
        """Emergency stop all trading"""
        try:
            success = self.set_trading_status("emergency_stopped")
            if success:
                return {"message": "Emergency stop executed successfully", "status": "emergency_stopped"}
            else:
                return {"message": "Failed to execute emergency stop", "status": "error"}
        except Exception as e:
            logger.error(f"Error executing emergency stop: {e}")
            return {"message": f"Error executing emergency stop: {str(e)}", "status": "error"}

    def get_positions(self) -> List[Dict]:
        """Get current trading positions"""
        try:
            positions = self.redis_client.get(self.positions_key)
            if positions:
                return json.loads(positions)
            else:
                return []
        except Exception as e:
            logger.error(f"Error getting positions: {e}")
            return []

    def update_positions(self, positions: List[Dict]) -> bool:
        """Update trading positions"""
        try:
            self.redis_client.set(self.positions_key, json.dumps(positions))
            return True
        except Exception as e:
            logger.error(f"Error updating positions: {e}")
            return False

    def get_trading_settings(self) -> Dict:
        """Get trading settings"""
        try:
            settings = self.redis_client.get(self.settings_key)
            if settings:
                return json.loads(settings)
            else:
                # Default settings
                default_settings = {
                    "leverage": 10,
                    "risk_per_trade": 0.10,  # 10% for true 10x leverage
                    "min_signal_strength": 0.3,
                    "stop_loss_pct": 0.02,
                    "take_profit_pct": 0.04,
                    "auto_trading": True,  # Enable auto trading by default
                    "max_positions": 5
                }
                self.redis_client.set(self.settings_key, json.dumps(default_settings))
                return default_settings
        except Exception as e:
            logger.error(f"Error getting trading settings: {e}")
            return {}

    def update_trading_settings(self, settings: Dict) -> bool:
        """Update trading settings"""
        try:
            current_settings = self.get_trading_settings()
            current_settings.update(settings)
            self.redis_client.set(self.settings_key, json.dumps(current_settings))
            return True
        except Exception as e:
            logger.error(f"Error updating trading settings: {e}")
            return False
