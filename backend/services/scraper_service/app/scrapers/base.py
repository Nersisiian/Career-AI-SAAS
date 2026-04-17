import asyncio
import random
from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime, timedelta

class BaseScraper(ABC):
    source_name: str = "base"
    
    @abstractmethod
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        pass
    
    async def _simulate_delay(self):
        await asyncio.sleep(random.uniform(0.5, 2.0))

class IndeedScraperSimulated(BaseScraper):
    source_name = "indeed"
    
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        await self._simulate_delay()
        jobs = []
        companies = ["TechCorp", "DataSoft", "WebSolutions", "CloudNine", "AIAnalytics", "DevOpsPro"]
        titles = ["Software Engineer", "Data Scientist", "Full Stack Developer", "ML Engineer", "Backend Developer"]
        
        for i in range(min(max_results, 30)):
            title = random.choice(titles)
            company = random.choice(companies)
            posted_days = random.randint(1, 30)
            jobs.append({
                "external_id": f"{self.source_name}_{i}_{random.randint(10000,99999)}",
                "title": title,
                "company": company,
                "location": location or "Remote",
                "description": f"We are looking for a {title} with experience in Python, cloud services, and agile methodologies.",
                "requirements": "Python, AWS, Docker, Kubernetes",
                "skills": ["Python", "AWS", "Docker", "Kubernetes"],
                "min_experience": random.randint(1, 7),
                "max_experience": random.randint(5, 12),
                "salary_min": random.randint(80000, 120000),
                "salary_max": random.randint(130000, 180000),
                "posted_date": (datetime.now() - timedelta(days=posted_days)).isoformat(),
                "source": self.source_name,
                "url": f"https://www.indeed.com/viewjob?jk={i}",
                "is_remote": "remote" in location.lower()
            })
        return jobs

class LinkedInScraperSimulated(BaseScraper):
    source_name = "linkedin"
    
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        await self._simulate_delay()
        # Similar implementation
        return []