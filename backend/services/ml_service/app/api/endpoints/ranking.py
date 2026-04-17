from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.api.deps import get_db
from app.models.ranker import JobRanker
from app.models.training import train_model_from_feedback

router = APIRouter()

class FeedbackItem(BaseModel):
    resume_id: str
    job_id: str
    relevance_score: float  # 0 to 1

class TrainingRequest(BaseModel):
    feedback_items: List[FeedbackItem]

@router.post("/train")
async def trigger_training(
    request: TrainingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Train model asynchronously
    background_tasks.add_task(train_model_from_feedback, db, request.feedback_items)
    return {"status": "training_started"}

@router.get("/model/info")
async def get_model_info():
    ranker = JobRanker()
    return {
        "model_loaded": ranker.model is not None,
        "model_path": ranker.model_path
    }