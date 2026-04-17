from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    skills: List[str]
    min_experience: float
    max_experience: Optional[float] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    is_remote: bool = False

class JobCreate(JobBase):
    external_id: str
    source: str
    url: str

class Job(JobBase):
    id: UUID
    external_id: str
    source: str
    url: str
    posted_date: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True