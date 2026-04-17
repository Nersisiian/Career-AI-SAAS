from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import numpy as np
from typing import List

from app.core.config import settings
from app.core.vector_store import VectorStore
from app.core.model_loader import get_embedding_model
from app.models.ranker import JobRanker
from app.schemas.match import MatchRequest, MatchResponse, JobMatch
from app.utils.feature_engineering import compute_skill_overlap, compute_experience_match
from app.api.deps import get_db, get_redis

router = APIRouter()
vector_store = VectorStore()
ranker = JobRanker()

@router.post("/jobs", response_model=MatchResponse)
async def match_jobs(
    request: MatchRequest,
    db: Session = Depends(get_db),
    redis_client = Depends(get_redis)
):
    # Get resume data (from cache or DB)
    resume_cache_key = f"resume:{request.resume_id}"
    resume_data = redis_client.get(resume_cache_key)
    if not resume_data:
        # In real implementation, fetch from DB via user service
        raise HTTPException(404, "Resume not found or not processed")
    
    import json
    resume = json.loads(resume_data)
    resume_skills = resume.get("skills", [])
    resume_years = resume.get("experience_years", 0)
    
    # Generate resume embedding if not cached
    emb_key = f"emb:resume:{request.resume_id}"
    resume_emb_bytes = redis_client.get(emb_key)
    if resume_emb_bytes:
        resume_emb = np.frombuffer(resume_emb_bytes, dtype=np.float32)
    else:
        model = get_embedding_model()
        resume_text = resume.get("parsed_text", "")
        resume_emb = model.encode([resume_text])[0]
        redis_client.set(emb_key, resume_emb.tobytes())
    
    # Search similar jobs from vector store
    similar_jobs = vector_store.search(resume_emb, k=request.top_k * 2)
    
    # Get job details and compute features
    matches = []
    for job_id, similarity in similar_jobs:
        job = get_job_details(db, job_id)
        if not job:
            continue
        
        skill_overlap = compute_skill_overlap(resume_skills, job.skills)
        exp_match = compute_experience_match(resume_years, job.min_experience)
        
        features = np.array([similarity, skill_overlap, exp_match])
        score = ranker.predict(features.reshape(1, -1))[0]
        
        matches.append(JobMatch(
            job_id=job.id,
            title=job.title,
            company=job.company,
            location=job.location,
            score=float(score),
            skills_match=skill_overlap,
            experience_match=exp_match
        ))
    
    # Sort by score and return top_k
    matches.sort(key=lambda x: x.score, reverse=True)
    return MatchResponse(matches=matches[:request.top_k])

def get_job_details(db: Session, job_id: str):
    # Placeholder - should query jobs table
    # For now, return mock data
    from app.schemas.job import Job
    return Job(
        id=job_id,
        title="Software Engineer",
        company="Tech Corp",
        location="Remote",
        skills=["Python", "FastAPI", "SQL"],
        min_experience=3
    )