from pydantic import BaseModel
from typing import Optional, List, Dict

class CoverLetterRequest(BaseModel):
    resume_id: str
    job_id: str
    job_title: str
    company: str
    job_description: str
    tone: str = "professional"

class CoverLetterResponse(BaseModel):
    cover_letter: str
    subject_line: str

class InterviewQuestionRequest(BaseModel):
    job_id: str
    resume_id: str
    num_questions: int = 5

class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str

class EvaluationResponse(BaseModel):
    score: int
    feedback: str
    strengths: List[str]
    improvements: List[str]