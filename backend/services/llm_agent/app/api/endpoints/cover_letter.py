from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from app.core.llm_client import LLMClient
from app.prompts import load_prompt
import json

router = APIRouter()

class CoverLetterRequest(BaseModel):
    resume_id: str
    job_id: str
    job_title: str
    company: str
    job_description: str
    tone: str = "professional"  # professional, enthusiastic, concise

class CoverLetterResponse(BaseModel):
    cover_letter: str
    subject_line: str

@router.post("/generate", response_model=CoverLetterResponse)
async def generate_cover_letter(request: CoverLetterRequest, req: Request):
    llm_client: LLMClient = req.app.state.llm_client
    
    # Fetch resume and job details (simplified - would call other services)
    # For now, use placeholders
    resume_context = "5 years experience in software development, skilled in Python and cloud technologies."
    
    prompt_template = load_prompt("cover_letter.txt")
    prompt = prompt_template.format(
        job_title=request.job_title,
        company=request.company,
        job_description=request.job_description,
        resume_context=resume_context,
        tone=request.tone
    )
    
    response = await llm_client.generate(prompt, temperature=0.7)
    
    # Parse response to extract subject line and body
    # Simple parsing - assume first line is subject
    lines = response.strip().split("\n")
    subject = lines[0].replace("Subject:", "").strip()
    body = "\n".join(lines[1:]).strip()
    
    return CoverLetterResponse(
        cover_letter=body,
        subject_line=subject
    )