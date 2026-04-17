from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List

class ResumeBase(BaseModel):
    original_filename: str
    file_size: Optional[int]

class ResumeCreate(ResumeBase):
    user_id: UUID
    file_path: str

class ResumeOut(ResumeBase):
    id: UUID
    user_id: UUID
    processed: bool
    extracted_skills: Optional[List[str]]
    experience_years: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    resume_id: UUID
    filename: str
    status: str