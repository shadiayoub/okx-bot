#!/usr/bin/env python3
"""
Model recommendation service for choosing optimal model types
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class ModelRecommendationService:
    def __init__(self):
        self.model_characteristics = {
            'gradient_boosting': {
                'min_data_points': 1000,
                'best_for': ['trending', 'medium_volatility'],
                'training_time': 'medium',
                'accuracy': 'high',
                'stability': 'medium'
            },
            'random_forest': {
                'min_data_points': 500,
                'best_for': ['volatile', 'sideways', 'high_volatility'],
                'training_time': 'fast',
                'accuracy': 'medium',
                'stability': 'high'
            },
            'neural_network': {
                'min_data_points': 2000,
                'best_for': ['complex_patterns', 'large_datasets'],
                'training_time': 'slow',
                'accuracy': 'very_high',
                'stability': 'medium'
            },
            'ensemble': {
                'min_data_points': 1500,
                'best_for': ['production', 'maximum_accuracy'],
                'training_time': 'slow',
                'accuracy': 'very_high',
                'stability': 'very_high'
            }
        }

    def analyze_market_characteristics(self, price_data: pd.DataFrame) -> Dict[str, float]:
        """Analyze market data to determine characteristics"""
        if len(price_data) < 100:
            return {'volatility': 'unknown', 'trend': 'unknown', 'complexity': 'unknown'}
        
        # Calculate volatility
        returns = price_data['close'].pct_change().dropna()
        volatility = returns.std()
        
        # Calculate trend strength
        price_change = (price_data['close'].iloc[-1] - price_data['close'].iloc[0]) / price_data['close'].iloc[0]
        trend_strength = abs(price_change)
        
        # Calculate complexity (using autocorrelation)
        autocorr = returns.autocorr()
        complexity = 1 - abs(autocorr) if not np.isnan(autocorr) else 0.5
        
        return {
            'volatility': volatility,
            'trend_strength': trend_strength,
            'complexity': complexity,
            'data_points': len(price_data)
        }

    def recommend_model_type(self, market_data: pd.DataFrame, 
                           trading_style: str = 'balanced',
                           data_availability: str = 'medium') -> Dict[str, any]:
        """Recommend the best model type based on market characteristics"""
        
        characteristics = self.analyze_market_characteristics(market_data)
        
        # Determine market type
        if characteristics['volatility'] > 0.05:  # High volatility
            market_type = 'volatile'
        elif characteristics['trend_strength'] > 0.1:  # Strong trend
            market_type = 'trending'
        else:
            market_type = 'sideways'
        
        # Score each model type
        scores = {}
        for model_type, specs in self.model_characteristics.items():
            score = 0
            
            # Data availability check
            if characteristics['data_points'] >= specs['min_data_points']:
                score += 2
            else:
                score -= 3  # Heavy penalty for insufficient data
            
            # Market type compatibility
            if market_type in specs['best_for']:
                score += 3
            elif any(style in specs['best_for'] for style in ['trending', 'volatile', 'sideways']):
                score += 1
            
            # Trading style preference
            if trading_style == 'conservative' and specs['stability'] == 'high':
                score += 2
            elif trading_style == 'aggressive' and specs['accuracy'] == 'very_high':
                score += 2
            elif trading_style == 'balanced':
                score += 1
            
            # Data availability preference
            if data_availability == 'limited' and specs['training_time'] == 'fast':
                score += 1
            elif data_availability == 'extensive' and specs['accuracy'] == 'very_high':
                score += 1
            
            scores[model_type] = score
        
        # Get top recommendations
        sorted_models = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'recommended_model': sorted_models[0][0],
            'alternative_models': [model for model, score in sorted_models[1:3]],
            'market_characteristics': characteristics,
            'market_type': market_type,
            'reasoning': self._get_reasoning(sorted_models[0][0], market_type, characteristics),
            'model_scores': scores
        }

    def _get_reasoning(self, model_type: str, market_type: str, characteristics: Dict) -> str:
        """Generate reasoning for model recommendation"""
        reasons = []
        
        if model_type == 'gradient_boosting':
            if market_type == 'trending':
                reasons.append("Gradient Boosting excels at capturing trending patterns")
            reasons.append("Good balance of accuracy and training speed")
        elif model_type == 'random_forest':
            if market_type == 'volatile':
                reasons.append("Random Forest is robust against market volatility")
            reasons.append("Provides feature importance for better understanding")
        elif model_type == 'neural_network':
            if characteristics['complexity'] > 0.7:
                reasons.append("Neural Network can capture complex market patterns")
            reasons.append("Best for large datasets with complex relationships")
        elif model_type == 'ensemble':
            reasons.append("Ensemble combines multiple models for maximum accuracy")
            reasons.append("Most stable for production trading")
        
        if characteristics['data_points'] < 1000:
            reasons.append("Consider collecting more data for better model performance")
        
        return "; ".join(reasons)

    def get_model_hyperparameters(self, model_type: str, market_type: str) -> Dict:
        """Get recommended hyperparameters for the model type"""
        base_params = {
            'gradient_boosting': {
                'n_estimators': 100,
                'learning_rate': 0.1,
                'max_depth': 6,
                'subsample': 0.8
            },
            'random_forest': {
                'n_estimators': 100,
                'max_depth': 10,
                'min_samples_split': 5,
                'min_samples_leaf': 2
            },
            'neural_network': {
                'hidden_layer_sizes': (100, 50),
                'learning_rate_init': 0.001,
                'max_iter': 500,
                'early_stopping': True
            },
            'ensemble': {
                'models': ['gradient_boosting', 'random_forest', 'neural_network'],
                'weights': [0.4, 0.3, 0.3]
            }
        }
        
        params = base_params.get(model_type, {})
        
        # Adjust based on market type
        if market_type == 'volatile':
            if model_type == 'random_forest':
                params['n_estimators'] = 150  # More trees for stability
            elif model_type == 'gradient_boosting':
                params['learning_rate'] = 0.05  # Slower learning for stability
        
        return params
