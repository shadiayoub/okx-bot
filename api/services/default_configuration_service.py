#!/usr/bin/env python3
"""
Default configuration service for recommended models and symbols
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DefaultConfigurationService:
    def __init__(self):
        self.default_symbols = [
            {
                "okx_symbol": "BTC-USDT-SWAP",
                "model_symbol": "BTC-USDT-SWAP",
                "display_name": "Bitcoin",
                "enabled": True,
                "risk_multiplier": 1.0,
                "min_balance": 100.0,
                "max_position_size": 0.1,
                "recommended_model": "gradient_boosting"
            },
            {
                "okx_symbol": "ETH-USDT-SWAP",
                "model_symbol": "ETH-USDT-SWAP",
                "display_name": "Ethereum",
                "enabled": True,
                "risk_multiplier": 1.0,
                "min_balance": 100.0,
                "max_position_size": 0.1,
                "recommended_model": "gradient_boosting"
            },
            {
                "okx_symbol": "BNB-USDT-SWAP",
                "model_symbol": "BNB-USDT-SWAP",
                "display_name": "Binance Coin",
                "enabled": False,
                "risk_multiplier": 0.8,
                "min_balance": 50.0,
                "max_position_size": 0.05,
                "recommended_model": "random_forest"
            },
            {
                "okx_symbol": "ADA-USDT-SWAP",
                "model_symbol": "ADA-USDT-SWAP",
                "display_name": "Cardano",
                "enabled": False,
                "risk_multiplier": 0.6,
                "min_balance": 30.0,
                "max_position_size": 0.03,
                "recommended_model": "random_forest"
            },
            {
                "okx_symbol": "SOL-USDT-SWAP",
                "model_symbol": "SOL-USDT-SWAP",
                "display_name": "Solana",
                "enabled": False,
                "risk_multiplier": 0.7,
                "min_balance": 40.0,
                "max_position_size": 0.04,
                "recommended_model": "gradient_boosting"
            },
            {
                "okx_symbol": "DOGE-USDT-SWAP",
                "model_symbol": "DOGE-USDT-SWAP",
                "display_name": "Dogecoin",
                "enabled": False,
                "risk_multiplier": 0.5,
                "min_balance": 20.0,
                "max_position_size": 0.02,
                "recommended_model": "random_forest"
            },
            {
                "okx_symbol": "MATIC-USDT-SWAP",
                "model_symbol": "MATIC-USDT-SWAP",
                "display_name": "Polygon",
                "enabled": False,
                "risk_multiplier": 0.6,
                "min_balance": 25.0,
                "max_position_size": 0.025,
                "recommended_model": "random_forest"
            },
            {
                "okx_symbol": "AVAX-USDT-SWAP",
                "model_symbol": "AVAX-USDT-SWAP",
                "display_name": "Avalanche",
                "enabled": False,
                "risk_multiplier": 0.7,
                "min_balance": 35.0,
                "max_position_size": 0.035,
                "recommended_model": "gradient_boosting"
            }
        ]

        self.default_models = {
            "gradient_boosting": {
                "hyperparameters": {
                    "n_estimators": 100,
                    "learning_rate": 0.1,
                    "max_depth": 6,
                    "subsample": 0.8,
                    "random_state": 42
                },
                "description": "Best for trending markets and most trading scenarios"
            },
            "random_forest": {
                "hyperparameters": {
                    "n_estimators": 100,
                    "max_depth": 10,
                    "min_samples_split": 5,
                    "min_samples_leaf": 2,
                    "random_state": 42
                },
                "description": "Best for volatile markets and risk management"
            },
            "neural_network": {
                "hyperparameters": {
                    "hidden_layer_sizes": (100, 50),
                    "learning_rate_init": 0.001,
                    "max_iter": 500,
                    "early_stopping": True,
                    "random_state": 42
                },
                "description": "Best for complex patterns and large datasets"
            },
            "ensemble": {
                "hyperparameters": {
                    "models": ["gradient_boosting", "random_forest", "neural_network"],
                    "weights": [0.4, 0.3, 0.3]
                },
                "description": "Best for production trading and maximum accuracy"
            }
        }

    def get_default_symbols(self) -> List[Dict[str, Any]]:
        """Get list of default recommended symbols"""
        return self.default_symbols

    def get_default_models(self) -> Dict[str, Dict[str, Any]]:
        """Get default model configurations"""
        return self.default_models

    def get_recommended_symbols_for_trading(self) -> List[Dict[str, Any]]:
        """Get symbols recommended for active trading"""
        return [symbol for symbol in self.default_symbols if symbol["enabled"]]

    def get_symbol_by_name(self, symbol_name: str) -> Dict[str, Any]:
        """Get specific symbol configuration by name"""
        for symbol in self.default_symbols:
            if symbol["okx_symbol"] == symbol_name or symbol["display_name"] == symbol_name:
                return symbol
        return None

    def get_model_config(self, model_type: str) -> Dict[str, Any]:
        """Get configuration for a specific model type"""
        return self.default_models.get(model_type, {})

    def get_bulk_operations(self) -> Dict[str, List[str]]:
        """Get predefined bulk operation groups"""
        return {
            "major_coins": ["BTC-USDT-SWAP", "ETH-USDT-SWAP"],
            "defi_tokens": ["BNB-USDT-SWAP", "ADA-USDT-SWAP", "SOL-USDT-SWAP"],
            "meme_coins": ["DOGE-USDT-SWAP"],
            "layer2_tokens": ["MATIC-USDT-SWAP", "AVAX-USDT-SWAP"],
            "all_trending": ["BTC-USDT-SWAP", "ETH-USDT-SWAP", "SOL-USDT-SWAP", "AVAX-USDT-SWAP"],
            "all_volatile": ["BNB-USDT-SWAP", "ADA-USDT-SWAP", "DOGE-USDT-SWAP", "MATIC-USDT-SWAP"]
        }
