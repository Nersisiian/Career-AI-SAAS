import numpy as np
import xgboost as xgb
from sqlalchemy.orm import Session
from typing import List, Dict
import joblib
import os

from app.core.config import settings
from app.models.ranker import JobRanker
from app.utils.feature_engineering import compute_skill_overlap, compute_experience_match

def train_model_from_feedback(db: Session, feedback_items: List):
    """
    Train XGBoost model using feedback data.
    feedback_items: list of objects with resume_id, job_id, relevance_score
    """
    features = []
    labels = []
    
    for item in feedback_items:
        # Fetch resume and job details from DB
        resume = get_resume_from_db(db, item.resume_id)
        job = get_job_from_db(db, item.job_id)
        
        if not resume or not job:
            continue
            
        # Compute features
        skill_overlap = compute_skill_overlap(resume.skills, job.skills)
        exp_match = compute_experience_match(resume.experience_years, job.min_experience)
        
        # Also need embedding similarity; for simplicity, we can fetch from cache or compute
        # Placeholder: assume we have embedding similarity in item or compute
        embedding_sim = 0.5  # In real implementation, compute from vector store
        
        feature_vector = [embedding_sim, skill_overlap, exp_match]
        features.append(feature_vector)
        labels.append(item.relevance_score)
    
    if len(features) < 10:
        return  # Not enough data
    
    X = np.array(features)
    y = np.array(labels)
    
    # Train XGBoost model
    model = xgb.XGBRegressor(
        objective='reg:squarederror',
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1
    )
    model.fit(X, y)
    
    # Save model
    model_path = os.path.join(settings.MODEL_PATH, "xgb_ranker.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    
    # Reload ranker instance
    ranker = JobRanker()
    ranker.model = model

def get_resume_from_db(db: Session, resume_id):
    # Placeholder - would query user_service DB or cache
    class ResumeMock:
        skills = ["Python", "FastAPI"]
        experience_years = 3.0
    return ResumeMock()

def get_job_from_db(db: Session, job_id):
    class JobMock:
        skills = ["Python", "Docker"]
        min_experience = 2
    return JobMock()