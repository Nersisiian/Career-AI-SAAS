from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class MatchRequest(BaseModel):
    resume_id: UUID
    top_k: int = 20
    filters: Optional[dict] = None

class JobMatch(BaseModel):
    job_id: UUID
    title: str
    company: str
    location: str
    score: float
    skills_match: float
    experience_match: float

class MatchResponse(BaseModel):
    matches: List[JobMatch]