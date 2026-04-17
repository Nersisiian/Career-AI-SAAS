from .base import BaseAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.tools import fetch_job_details, fetch_resume_context
import json

class InterviewCoachAgent(BaseAgent):
    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="JobDetails",
                func=fetch_job_details,
                description="Get job requirements and typical interview topics"
            ),
            Tool(
                name="ResumeContext",
                func=fetch_resume_context,
                description="Get candidate background for personalized questions"
            )
        ]
    
    def _get_prompt_template(self):
        template = """You are an interview coach who has helped thousands of candidates land jobs at top tech companies.
You generate realistic interview questions and provide constructive feedback on answers.

Tools: {tools}
Format: standard

{chat_history}
Question: {input}
{agent_scratchpad}"""
        return PromptTemplate.from_template(template)
    
    def generate_questions(self, job_id: str, resume_id: str, num_questions: int = 5) -> List[str]:
        prompt = f"""Generate {num_questions} interview questions for job {job_id} tailored to candidate {resume_id}.
Include mix of behavioral, technical, and situational questions.
Format as numbered list."""
        response = self.run(prompt)
        # Parse numbered list
        questions = [q.strip() for q in response.split('\n') if q.strip() and q[0].isdigit()]
        return questions
    
    def evaluate_answer(self, question: str, answer: str) -> Dict:
        prompt = f"""Evaluate this interview answer:
Question: {question}
Candidate's Answer: {answer}

Provide:
1. Score (1-10)
2. Strengths
3. Areas for improvement
4. Suggested better response (brief)
"""
        response = self.run(prompt)
        return self._parse_evaluation(response)
    
    def _parse_evaluation(self, text: str) -> Dict:
        # Attempt to extract score using regex
        import re
        score_match = re.search(r'Score:\s*(\d+)', text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 7
        return {
            "score": score,
            "feedback": text,
            "strengths": [],
            "improvements": []
        }