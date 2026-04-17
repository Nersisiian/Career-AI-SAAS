import asyncio
import random
from typing import List, Dict
from datetime import datetime, timedelta
from .base import BaseScraper

class GlassdoorScraperSimulated(BaseScraper):
    source_name = "glassdoor"
    
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        await self._simulate_delay()
        jobs = []
        for i in range(min(max_results, 15)):
            jobs.append({
                "external_id": f"{self.source_name}_{i}_{random.randint(10000,99999)}",
                "title": "Data Analyst",
                "company": "AnalyticsPro",
                "location": location or "Chicago, IL",
                "description": "Data analysis role with SQL and Python.",
                "skills": ["SQL", "Python", "Tableau"],
                "min_experience": 2,
                "source": self.source_name,
                "url": f"https://www.glassdoor.com/job-listing/{i}",
                "is_remote": False
            })
        return jobs