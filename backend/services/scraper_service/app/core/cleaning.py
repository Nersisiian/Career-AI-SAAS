import re
from typing import List, Dict

def clean_job_description(text: str) -> str:
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove special characters except punctuation
    text = re.sub(r'[^\w\s\.\,\-\:\;\(\)]', '', text)
    return text

def deduplicate_jobs(jobs: List[Dict]) -> List[Dict]:
    seen = set()
    unique = []
    for job in jobs:
        # Create a key based on title, company, location
        key = (
            job.get('title', '').lower().strip(),
            job.get('company', '').lower().strip(),
            job.get('location', '').lower().strip()
        )
        if key not in seen:
            seen.add(key)
            unique.append(job)
    return unique

def extract_skills(text: str, skill_keywords: List[str]) -> List[str]:
    text_lower = text.lower()
    found = set()
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found.add(skill)
    return list(found)