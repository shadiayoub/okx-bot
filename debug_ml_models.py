#!/usr/bin/env python3
"""
Debug script to test ML model loading and prediction
"""

import os
import sys
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

# Add the current directory to the path
sys.path.append('.')

from strategies.prediction_models import PricePredictor

def create_test_data():
    """Create test data for debugging"""
    # Create sample OHLCV data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='1H')
    np.random.seed(42)
    
    # Generate realistic price data
    base_price = 50000
    returns = np.random.normal(0, 0.02, len(dates))
    prices = [base_price]
    
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(new_price)
    
    # Create OHLCV data
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Create realistic OHLC from close price
        volatility = 0.01
        high = price * (1 + abs(np.random.normal(0, volatility)))
        low = price * (1 - abs(np.random.normal(0, volatility)))
        open_price = price * (1 + np.random.normal(0, volatility/2))
        volume = np.random.randint(1000, 10000)
        
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': price,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    return df

def test_model_loading():
    """Test loading each model and check its properties"""
    model_files = [
        'models/BTCUSDT_gradient_boosting.joblib',
        'models/ETHUSDT_gradient_boosting.joblib',
        'models/BNBUSDT_gradient_boosting.joblib',
        'models/ADAUSDT_gradient_boosting.joblib',
        'models/SOLUSDT_gradient_boosting.joblib'
    ]
    
    for model_file in model_files:
        if not os.path.exists(model_file):
            print(f"❌ Model file not found: {model_file}")
            continue
            
        print(f"\n🔍 Testing {model_file}")
        
        try:
            # Load the model data
            model_data = joblib.load(model_file)
            print(f"✅ Model data loaded successfully")
            
            # Check what's in the model data
            if isinstance(model_data, dict):
                print(f"📊 Model data keys: {list(model_data.keys())}")
                
                if 'model' in model_data:
                    model = model_data['model']
                    print(f"🤖 Model type: {type(model)}")
                    
                    if hasattr(model, 'estimators_'):
                        print(f"🌳 Number of estimators: {len(model.estimators_)}")
                    elif hasattr(model, 'estimators'):
                        print(f"🌳 Number of estimators: {len(model.estimators)}")
                    
                    if hasattr(model, 'feature_importances_'):
                        print(f"📈 Feature importances shape: {model.feature_importances_.shape}")
                    
                if 'feature_columns' in model_data:
                    feature_cols = model_data['feature_columns']
                    print(f"📋 Feature columns: {len(feature_cols)} columns")
                    print(f"📋 First 5 features: {feature_cols[:5]}")
                
                if 'scaler' in model_data:
                    scaler = model_data['scaler']
                    print(f"⚖️ Scaler type: {type(scaler)}")
                    
            else:
                print(f"⚠️ Model data is not a dict: {type(model_data)}")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")

def test_prediction_pipeline():
    """Test the complete prediction pipeline"""
    print("\n🧪 Testing prediction pipeline")
    
    # Create test data
    test_df = create_test_data()
    print(f"📊 Test data shape: {test_df.shape}")
    
    # Test with BTC model
    model_file = 'models/BTCUSDT_gradient_boosting.joblib'
    if not os.path.exists(model_file):
        print(f"❌ Model file not found: {model_file}")
        return
    
    try:
        # Create predictor and load model
        predictor = PricePredictor("gradient_boosting")
        predictor.load_model(model_file)
        
        print(f"✅ Model loaded successfully")
        print(f"🤖 Model trained: {predictor.is_trained}")
        print(f"📋 Feature columns: {len(predictor.feature_columns) if predictor.feature_columns else 'None'}")
        
        # Test feature creation
        print(f"\n🔧 Testing feature creation...")
        features_df = predictor.create_features(test_df)
        print(f"📊 Features shape: {features_df.shape}")
        print(f"📊 Features columns: {list(features_df.columns)[:10]}...")
        
        # Test prediction
        print(f"\n🎯 Testing prediction...")
        prediction, confidence = predictor.predict(test_df)
        print(f"📈 Prediction: {prediction}")
        print(f"🎯 Confidence: {confidence}")
        
        # Test with different data sizes
        print(f"\n📏 Testing with different data sizes...")
        for size in [50, 100, 200]:
            subset_df = test_df.tail(size)
            pred, conf = predictor.predict(subset_df)
            print(f"📊 Size {size}: Prediction={pred:.6f}, Confidence={conf:.3f}")
        
    except Exception as e:
        print(f"❌ Error in prediction pipeline: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 ML Model Debug Script")
    print("=" * 50)
    
    test_model_loading()
    test_prediction_pipeline()
    
    print("\n✅ Debug script completed")
