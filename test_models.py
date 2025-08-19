#!/usr/bin/env python3
"""
Test script to verify ML models are working
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from strategies.prediction_models import PricePredictor
import pandas as pd
import numpy as np
import joblib

def test_model(symbol, model_type="gradient_boosting"):
    """Test a specific model"""
    print(f"Testing {symbol} {model_type} model...")
    
    # Load the model
    model_path = os.path.join('models', f'{symbol}_{model_type}.joblib')
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        return False
    
    try:
        # Load the model
        model_data = joblib.load(model_path)
        print(f"Model loaded successfully from {model_path}")
        print(f"Model type: {type(model_data['model'])}")
        print(f"Feature columns: {model_data['feature_columns'][:5] if 'feature_columns' in model_data else 'No feature columns'}")
        
        # Create test data
        print("Creating test data...")
        np.random.seed(42)
        dates = pd.date_range(start='2024-12-01', end='2024-12-31', freq='1H')
        n_samples = len(dates)
        
        # Generate realistic price data
        base_price = 50000 if 'BTC' in symbol else 3000 if 'ETH' in symbol else 100
        price_changes = np.random.normal(0, 0.02, n_samples)
        prices = [base_price]
        
        for change in price_changes[1:]:
            new_price = prices[-1] * (1 + change)
            prices.append(max(new_price, 1))
        
        # Create OHLCV data
        data = []
        for i, (date, price) in enumerate(zip(dates, prices)):
            open_price = price * (1 + np.random.normal(0, 0.005))
            high_price = max(open_price, price) * (1 + abs(np.random.normal(0, 0.01)))
            low_price = min(open_price, price) * (1 - abs(np.random.normal(0, 0.01)))
            close_price = price
            volume = np.random.uniform(1000, 10000)
            
            data.append({
                'timestamp': int(date.timestamp() * 1000),
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume,
                'volCcy': volume * close_price,
                'volCcyQuote': volume,
                'confirm': 1
            })
        
        df = pd.DataFrame(data)
        print(f"Test data created: {df.shape}")
        
        # Test prediction
        predictor = PricePredictor(model_type=model_type)
        predictor.model = model_data['model']
        predictor.scaler = model_data['scaler']
        predictor.feature_columns = model_data.get('feature_columns', [])
        predictor.is_trained = True
        
        prediction, confidence = predictor.predict(df)
        print(f"Prediction: {prediction}")
        print(f"Confidence: {confidence}")
        
        if prediction != 0.0:
            print("✅ Model is working correctly!")
            return True
        else:
            print("❌ Model is returning 0.0 prediction")
            return False
            
    except Exception as e:
        print(f"Error testing model: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Test all models"""
    symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'ADAUSDT', 'SOLUSDT']
    
    print("Testing ML models...")
    print("=" * 50)
    
    working_models = 0
    for symbol in symbols:
        if test_model(symbol):
            working_models += 1
        print("-" * 30)
    
    print(f"Summary: {working_models}/{len(symbols)} models working correctly")
    
    if working_models == 0:
        print("\nAll models are returning 0.0 predictions. This needs to be fixed.")
        print("The models may need to be retrained with proper data.")

if __name__ == "__main__":
    main()
