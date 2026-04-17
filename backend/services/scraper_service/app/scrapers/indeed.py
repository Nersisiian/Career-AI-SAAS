import asyncio
import random
from typing import List, Dict
from datetime import datetime, timedelta
from .base import BaseScraper

class IndeedScraperSimulated(BaseScraper):
    source_name = "indeed"
    
    async def scrape(self, keywords: List[str], location: str = "", max_results: int = 50) -> List[Dict]:
        await self._simulate_delay()
        jobs = []
        companies = [
            "Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Salesforce",
            "Adobe", "Uber", "Airbnb", "Stripe", "Shopify", "Spotify", "Slack"
        ]
        titles = [
            "Software Engineer", "Senior Software Engineer", "Full Stack Developer",
            "Backend Engineer", "Frontend Engineer", "DevOps Engineer", "ML Engineer",
            "Data Scientist", "Product Manager", "Technical Lead"
        ]
        
        for i in range(min(max_results, 30)):
            title = random.choice(titles)
            company = random.choice(companies)
            loc = location if location else random.choice(["Remote", "New York, NY", "San Francisco, CA", "Austin, TX"])
            posted_days = random.randint(0, 14)
            salary_min = random.randint(80000, 130000)
            salary_max = salary_min + random.randint(20000, 50000)
            
            description = f"""
            About the job:
            {company} is seeking a {title} to join our growing team.
            
            Responsibilities:
            - Design and develop scalable software solutions
            - Collaborate with cross-functional teams
            - Write clean, maintainable code
            - Participate in code reviews and mentoring
            
            Requirements:
            - {random.randint(2,8)}+ years of experience
            - Proficiency in {', '.join(random.sample(['Python', 'Java', 'JavaScript', 'Go', 'C++'], 2))}
            - Experience with cloud platforms (AWS/Azure/GCP)
            - Strong problem-solving skills
            
            Nice to have:
            - Experience with containerization (Docker, Kubernetes)
            - Knowledge of microservices architecture
            """
            
            jobs.append({
                "external_id": f"{self.source_name}_{i}_{random.randint(10000,99999)}",
                "title": title,
                "company": company,
                "location": loc,
                "description": description,
                "requirements": "Python, AWS, Docker",
                "skills": random.sample(["Python", "Java", "AWS", "Docker", "Kubernetes", "SQL", "React"], 4),
                "min_experience": random.randint(1, 5),
                "max_experience": random.randint(6, 10),
                "salary_min": salary_min,
                "salary_max": salary_max,
                "posted_date": (datetime.now() - timedelta(days=posted_days)).isoformat(),
                "source": self.source_name,
                "url": f"https://www.indeed.com/viewjob?jk={random.randint(1000,9999)}",
                "is_remote": "remote" in loc.lower()
            })
        return jobs