import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.core.config import settings
from app.scrapers.indeed import IndeedScraperSimulated
from app.scrapers.linkedin import LinkedInScraperSimulated
from app.core.database import SessionLocal
from app.models.job import Job
from app.core.cleaning import deduplicate_jobs, clean_job_description

scheduler = AsyncIOScheduler()

async def scheduled_scrape():
    print("Running scheduled scrape...")
    scrapers = [IndeedScraperSimulated(), LinkedInScraperSimulated()]
    keywords = ["software engineer", "data scientist", "ml engineer"]
    
    all_jobs = []
    for scraper in scrapers:
        jobs = await scraper.scrape(keywords, location="United States")
        all_jobs.extend(jobs)
    
    unique_jobs = deduplicate_jobs(all_jobs)
    db = SessionLocal()
    saved = 0
    for job_data in unique_jobs:
        job_data["description"] = clean_job_description(job_data["description"])
        existing = db.query(Job).filter(Job.external_id == job_data["external_id"]).first()
        if not existing:
            job = Job(**job_data)
            db.add(job)
            saved += 1
    db.commit()
    db.close()
    print(f"Scheduled scrape completed. Saved {saved} new jobs.")

def start_scheduler():
    scheduler.add_job(scheduled_scrape, 'interval', hours=settings.SCRAPE_INTERVAL_HOURS)
    scheduler.start()