from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

class FeedbackLog(Base):
    __tablename__ = "feedback_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    match_id = Column(UUID(as_uuid=True), nullable=True)
    rating = Column(Integer)
    feedback_text = Column(Text)
    interaction_type = Column(String(50))  # view, apply, save, dismiss
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MatchFeedback(Base):
    __tablename__ = "match_feedback"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id = Column(UUID(as_uuid=True), nullable=False)
    relevance_score = Column(Integer)  # 0-100
    user_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())