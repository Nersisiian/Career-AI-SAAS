from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict

from app.agents.interview_coach import InterviewCoachAgent

router = APIRouter()

class GenerateQuestionsRequest(BaseModel):
    job_id: str
    resume_id: str
    num_questions: int = 5

class EvaluateAnswerRequest(BaseModel):
    question: str
    answer: str

@router.post("/generate-questions")
async def generate_questions(request: GenerateQuestionsRequest, req: Request):
    agent = InterviewCoachAgent()
    questions = agent.generate_questions(request.job_id, request.resume_id, request.num_questions)
    return {"questions": questions}

@router.post("/evaluate-answer")
async def evaluate_answer(request: EvaluateAnswerRequest, req: Request):
    agent = InterviewCoachAgent()
    evaluation = agent.evaluate_answer(request.question, request.answer)
    return evaluation