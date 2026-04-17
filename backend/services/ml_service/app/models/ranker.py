import xgboost as xgb
import numpy as np
import joblib
import os

class JobRanker:
    def __init__(self, model_path: str = "/app/models/xgb_ranker.pkl"):
        self.model_path = model_path
        self.model = None
        self._load_model()
    
    def _load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            # Initialize a dummy model for initial runs
            self.model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=50)
            # Train with dummy data if needed
            X = np.array([[0.8, 0.7, 0.9], [0.5, 0.3, 0.4], [0.2, 0.1, 0.0]])
            y = np.array([0.9, 0.5, 0.1])
            self.model.fit(X, y)
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        return self.model.predict(features)
    
    def save(self):
        joblib.dump(self.model, self.model_path)