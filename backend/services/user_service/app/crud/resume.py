from sqlalchemy.orm import Session
from app.models.resume import Resume
import uuid
from typing import List

def create_resume(db: Session, user_id: uuid.UUID, file_path: str, 
                  original_filename: str, file_size: int) -> Resume:
    db_resume = Resume(
        user_id=user_id,
        file_path=file_path,
        original_filename=original_filename,
        file_size=file_size
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def get_resumes_by_user(db: Session, user_id: uuid.UUID) -> List[Resume]:
    return db.query(Resume).filter(Resume.user_id == user_id).order_by(Resume.created_at.desc()).all()

def get_resume(db: Session, resume_id: uuid.UUID) -> Resume | None:
    return db.query(Resume).filter(Resume.id == resume_id).first()

def update_resume_processed_data(db: Session, resume_id: uuid.UUID, 
                                 parsed_text: str, skills: list, experience_years: float) -> Resume:
    resume = get_resume(db, resume_id)
    if resume:
        resume.parsed_text = parsed_text
        resume.extracted_skills = skills
        resume.experience_years = experience_years
        resume.processed = True
        db.commit()
        db.refresh(resume)
    return resume