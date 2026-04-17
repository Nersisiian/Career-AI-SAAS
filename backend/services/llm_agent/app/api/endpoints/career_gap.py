from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Dict

from app.agents.recruiter import RecruiterAgent

router = APIRouter()

class CareerGapRequest(BaseModel):
    resume_id: str
    target_job_titles: List[str]

@router.post("/analyze")
async def analyze_career_gap(request: CareerGapRequest, req: Request):
    agent = RecruiterAgent()
    
    analysis_results = []
    for job_title in request.target_job_titles:
        # In production, you'd fetch a representative job ID for that title
        job_id = "sample_job_id"  # Placeholder
        analysis = agent.evaluate_fit(request.resume_id, job_id)
        analysis["target_job"] = job_title
        analysis_results.append(analysis)
    
    # Aggregate skill gaps and recommendations
    all_gaps = set()
    for result in analysis_results:
        all_gaps.update(result.get("gaps", []))
    
    return {
        "target_roles": request.target_job_titles,
        "overall_gaps": list(all_gaps),
        "detailed_analysis": analysis_results
    }