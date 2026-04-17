import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.scraper_service.app.core.database import SessionLocal
from backend.services.scraper_service.app.models.job import Job
import random
from datetime import datetime, timedelta

def seed_jobs(count=50):
    db = SessionLocal()
    companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix"]
    titles = ["Software Engineer", "Data Scientist", "ML Engineer", "Backend Developer"]
    skills_options = [["Python", "AWS", "Docker"], ["Java", "Spring", "SQL"], ["JavaScript", "React", "Node"]]
    
    for i in range(count):
        job = Job(
            external_id=f"seed_{i}_{random.randint(1000,9999)}",
            title=random.choice(titles),
            company=random.choice(companies),
            location=random.choice(["Remote", "New York, NY", "San Francisco, CA"]),
            description="Sample job description for testing.",
            skills=random.choice(skills_options),
            min_experience=random.randint(1,5),
            source="seed",
            url="https://example.com",
            posted_date=datetime.now() - timedelta(days=random.randint(0,30))
        )
        db.add(job)
    db.commit()
    db.close()
    print(f"Seeded {count} jobs.")

if __name__ == "__main__":
    seed_jobs()