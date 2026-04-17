import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import xgboost as xgb
import joblib
from backend.services.ml_service.app.core.config import settings

def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)
    X = np.random.rand(n_samples, 3)  # 3 features: embedding sim, skill overlap, exp match
    # Simulate relevance score with some noise
    y = 0.4 * X[:,0] + 0.3 * X[:,1] + 0.3 * X[:,2] + np.random.normal(0, 0.1, n_samples)
    y = np.clip(y, 0, 1)
    return X, y

def train_and_save():
    X, y = generate_synthetic_data()
    model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=50, max_depth=4)
    model.fit(X, y)
    
    model_path = os.path.join(settings.MODEL_PATH, "xgb_ranker.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_and_save()