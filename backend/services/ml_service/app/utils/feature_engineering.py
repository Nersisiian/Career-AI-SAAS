from typing import List

def compute_skill_overlap(resume_skills: List[str], job_skills: List[str]) -> float:
    if not job_skills:
        return 0.0
    set1 = set(s.lower() for s in resume_skills)
    set2 = set(s.lower() for s in job_skills)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0

def compute_experience_match(resume_years: float, job_min_years: float) -> float:
    if job_min_years == 0:
        return 1.0
    ratio = resume_years / job_min_years
    return min(ratio, 1.5) / 1.5