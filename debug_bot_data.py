#!/usr/bin/env python3
"""
Debug script to test the exact data format the bot uses
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

def create_bot_like_data():
    """Create data in the exact format the bot uses"""
    # Create sample OHLCV data like the bot would get from OKX
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='1h')
    np.random.seed(42)
    
    # Generate realistic price data
    base_price = 50000
    returns = np.random.normal(0, 0.02, len(dates))
    prices = [base_price]
    
    for ret in returns[1:]:
        new_price = prices[-1] * (1 + ret)
        prices.append(new_price)
    
    # Create OHLCV data in the format the bot uses
    data = []
    for i, (date, price) in enumerate(zip(dates, prices)):
        # Create realistic OHLC from close price
        volatility = 0.01
        high = price * (1 + abs(np.random.normal(0, volatility)))
        low = price * (1 - abs(np.random.normal(0, volatility)))
        open_price = price * (1 + np.random.normal(0, volatility/2))
        volume = np.random.randint(1000, 10000)
        
        # Format like the bot's data structure
        data.append({
            'timestamp': date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': price,
            'volume': volume
        })
    
    df = pd.DataFrame(data)
    # Set timestamp as index like the bot does
    df.set_index('timestamp', inplace=True)
    return df

def test_with_bot_data():
    """Test with data in the exact format the bot uses"""
    print("🧪 Testing with bot-like data format")
    
    # Create data like the bot uses
    test_df = create_bot_like_data()
    print(f"📊 Bot-like data shape: {test_df.shape}")
    print(f"📊 Columns: {list(test_df.columns)}")
    print(f"📊 Index type: {type(test_df.index)}")
    print(f"📊 First few rows:")
    print(test_df.head())
    
    # Test with BTC model
    model_file = 'models/BTCUSDT_gradient_boosting.joblib'
    if not os.path.exists(model_file):
        print(f"❌ Model file not found: {model_file}")
        return
    
    try:
        # Create predictor and load model
        predictor = PricePredictor("gradient_boosting")
        predictor.load_model(model_file)
        
        print(f"\n✅ Model loaded successfully")
        print(f"🤖 Model trained: {predictor.is_trained}")
        print(f"📋 Feature columns: {len(predictor.feature_columns) if predictor.feature_columns else 'None'}")
        
        # Test feature creation with bot data
        print(f"\n🔧 Testing feature creation with bot data...")
        features_df = predictor.create_features(test_df)
        print(f"📊 Features shape: {features_df.shape}")
        print(f"📊 Features columns: {list(features_df.columns)[:10]}...")
        
        # Check if we have the required features
        required_features = predictor.feature_columns
        if required_features:
            missing_features = [f for f in required_features if f not in features_df.columns]
            available_features = [f for f in required_features if f in features_df.columns]
            print(f"📋 Required features: {len(required_features)}")
            print(f"📋 Available features: {len(available_features)}")
            print(f"📋 Missing features: {len(missing_features)}")
            if missing_features:
                print(f"❌ Missing: {missing_features[:5]}...")
        
        # Test prediction with bot data
        print(f"\n🎯 Testing prediction with bot data...")
        prediction, confidence = predictor.predict(test_df)
        print(f"📈 Prediction: {prediction}")
        print(f"🎯 Confidence: {confidence}")
        
        # Test with different data sizes
        print(f"\n📏 Testing with different data sizes...")
        for size in [100, 200, 500]:
            subset_df = test_df.tail(size)
            pred, conf = predictor.predict(subset_df)
            print(f"📊 Size {size}: Prediction={pred:.6f}, Confidence={conf:.3f}")
        
    except Exception as e:
        print(f"❌ Error in prediction pipeline: {e}")
        import traceback
        traceback.print_exc()

def test_model_structure():
    """Test the actual model structure"""
    print("\n🔍 Testing model structure")
    
    model_file = 'models/BTCUSDT_gradient_boosting.joblib'
    if not os.path.exists(model_file):
        print(f"❌ Model file not found: {model_file}")
        return
    
    try:
        # Load the model data
        model_data = joblib.load(model_file)
        print(f"✅ Model data loaded successfully")
        
        if isinstance(model_data, dict):
            print(f"📊 Model data keys: {list(model_data.keys())}")
            
            if 'model' in model_data:
                model = model_data['model']
                print(f"🤖 Model type: {type(model)}")
                
                # Test if the model can predict with dummy data
                print(f"\n🧪 Testing model with dummy data...")
                dummy_data = np.random.random((1, 34))  # 34 features
                try:
                    dummy_pred = model.predict(dummy_data)
                    print(f"✅ Model can predict: {dummy_pred}")
                except Exception as e:
                    print(f"❌ Model prediction failed: {e}")
                
                if hasattr(model, 'estimators_'):
                    print(f"🌳 Number of estimators: {len(model.estimators_)}")
                    # Test individual estimator
                    if len(model.estimators_) > 0:
                        estimator = model.estimators_[0]
                        try:
                            est_pred = estimator.predict(dummy_data)
                            print(f"✅ Individual estimator can predict: {est_pred}")
                        except Exception as e:
                            print(f"❌ Individual estimator failed: {e}")
                
            if 'feature_columns' in model_data:
                feature_cols = model_data['feature_columns']
                print(f"📋 Feature columns: {len(feature_cols)} columns")
                print(f"📋 First 5 features: {feature_cols[:5]}")
                
    except Exception as e:
        print(f"❌ Error loading model: {e}")

if __name__ == "__main__":
    print("🔍 Bot Data Debug Script")
    print("=" * 50)
    
    test_model_structure()
    test_with_bot_data()
    
    print("\n✅ Debug script completed")
