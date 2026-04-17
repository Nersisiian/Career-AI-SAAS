import asyncio
import random
from typing import List, Dict
from datetime import datetime, timedelta
from .base import BaseScraper

class LinkedInScraperSimulated(BaseScraper):
    source_name = "linkedin"
    
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        await self._simulate_delay()
        jobs = []
        companies = ["StartupX", "TechGiants", "InnovateCo", "FutureCorp", "DataDynamics"]
        titles = ["Senior Developer", "Tech Lead", "Principal Engineer", "Software Architect"]
        
        for i in range(min(max_results, 20)):
            title = random.choice(titles)
            company = random.choice(companies)
            posted_days = random.randint(1, 7)
            
            jobs.append({
                "external_id": f"{self.source_name}_{i}_{random.randint(10000,99999)}",
                "title": title,
                "company": company,
                "location": location or "United States",
                "description": f"Exciting opportunity for a {title} at {company}.",
                "requirements": "5+ years experience, leadership skills",
                "skills": ["Leadership", "System Design", "Python", "Mentoring"],
                "min_experience": 5,
                "max_experience": 10,
                "salary_min": 120000,
                "salary_max": 180000,
                "posted_date": (datetime.now() - timedelta(days=posted_days)).isoformat(),
                "source": self.source_name,
                "url": f"https://www.linkedin.com/jobs/view/{i}",
                "is_remote": random.choice([True, False])
            })
        return jobs