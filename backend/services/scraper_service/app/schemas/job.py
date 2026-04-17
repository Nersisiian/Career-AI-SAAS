from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class JobCreate(BaseModel):
    external_id: str
    title: str
    company: str
    location: str
    description: str
    requirements: Optional[str] = None
    skills: List[str]
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    posted_date: Optional[datetime] = None
    source: str
    url: str
    is_remote: bool = False

class JobOut(JobCreate):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True