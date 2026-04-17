from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models.feedback import FeedbackLog, MatchFeedback

router = APIRouter()

class FeedbackCreate(BaseModel):
    user_id: UUID
    match_id: UUID
    rating: int  # 1-5
    feedback_text: Optional[str] = None
    interaction_type: str  # view, apply, save, dismiss

class MetricQuery(BaseModel):
    start_date: datetime
    end_date: datetime
    metric_type: str = "match_quality"

@router.post("/feedback")
async def log_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    fb = FeedbackLog(
        user_id=feedback.user_id,
        match_id=feedback.match_id,
        rating=feedback.rating,
        feedback_text=feedback.feedback_text,
        interaction_type=feedback.interaction_type
    )
    db.add(fb)
    db.commit()
    return {"status": "logged"}

@router.get("/dashboard")
async def get_dashboard_metrics(db: Session = Depends(get_db)):
    # Aggregate metrics
    total_feedback = db.query(FeedbackLog).count()
    avg_rating = db.query(func.avg(FeedbackLog.rating)).scalar() or 0
    
    return {
        "total_feedback": total_feedback,
        "average_rating": float(avg_rating),
        "active_users": 0  # Would join with user service
    }