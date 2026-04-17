import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies import get_current_user
from app.core.config import settings
from app.core.database import get_db
from app.crud.resume import create_resume, get_resumes_by_user, get_resume
from app.schemas.resume import ResumeOut, ResumeUploadResponse
from app.models.user import User
import redis
import json

router = APIRouter()
redis_client = redis.from_url(settings.REDIS_URL)

@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF, DOC, and DOCX files are allowed"
        )
    
    # Save file
    file_id = uuid.uuid4()
    filename = f"{file_id}_{file.filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    content = await file.read()
    
    with open(file_path, "wb") as f:
        f.write(content)
    
    # Save resume record
    resume = create_resume(
        db=db,
        user_id=current_user.id,
        file_path=file_path,
        original_filename=file.filename,
        file_size=len(content)
    )
    
    # Trigger async processing via Redis pub/sub or Celery
    task_data = {
        "resume_id": str(resume.id),
        "file_path": file_path,
        "user_id": str(current_user.id)
    }
    redis_client.publish("resume_uploads", json.dumps(task_data))
    
    return ResumeUploadResponse(
        resume_id=resume.id,
        filename=file.filename,
        status="processing"
    )

@router.get("/", response_model=List[ResumeOut])
async def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resumes = get_resumes_by_user(db, current_user.id)
    return resumes

@router.get("/{resume_id}", response_model=ResumeOut)
async def get_resume_details(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    resume = get_resume(db, resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    return resume