from sqlalchemy.orm import Session
from app.models.user import User
import uuid

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, full_name: str, hashed_password: str) -> User:
    db_user = User(email=email, full_name=full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user