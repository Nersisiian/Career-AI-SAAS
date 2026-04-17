from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.scrapers.indeed import IndeedScraperSimulated
from app.scrapers.linkedin import LinkedInScraperSimulated
from app.core.cleaning import clean_job_description, deduplicate_jobs
from app.models.job import Job
from app.schemas.job import JobCreate

router = APIRouter()

@router.post("/trigger")
async def trigger_scrape(
    keywords: List[str],
    location: str = "",
    sources: Optional[List[str]] = None,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    if sources is None:
        sources = ["indeed", "linkedin"]
    
    scrapers = []
    if "indeed" in sources:
        scrapers.append(IndeedScraperSimulated())
    if "linkedin" in sources:
        scrapers.append(LinkedInScraperSimulated())
    
    all_jobs = []
    for scraper in scrapers:
        jobs = await scraper.scrape(keywords, location)
        all_jobs.extend(jobs)
    
    # Deduplicate and clean
    unique_jobs = deduplicate_jobs(all_jobs)
    saved_count = 0
    for job_data in unique_jobs:
        job_data["description"] = clean_job_description(job_data["description"])
        # Save to DB
        job = Job(**job_data)
        db.add(job)
        saved_count += 1
    db.commit()
    
    # In background, trigger embedding generation
    if background_tasks:
        background_tasks.add_task(generate_embeddings_for_new_jobs, [j.id for j in db.new])
    
    return {"status": "completed", "jobs_scraped": len(all_jobs), "jobs_saved": saved_count}

def generate_embeddings_for_new_jobs(job_ids):
    # Call ML service to generate embeddings for these jobs
    pass