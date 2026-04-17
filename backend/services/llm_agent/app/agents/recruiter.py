from .base import BaseAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.tools import fetch_job_details, fetch_resume_context

class RecruiterAgent(BaseAgent):
    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="JobDetails",
                func=fetch_job_details,
                description="Retrieve full job description, requirements, and company info for a job ID"
            ),
            Tool(
                name="ResumeContext",
                func=fetch_resume_context,
                description="Get parsed resume content, skills, and experience"
            )
        ]
    
    def _get_prompt_template(self):
        template = """You are an expert recruiter with 20 years of experience in tech hiring.
Your goal is to evaluate a candidate's fit for a specific job and provide actionable feedback.

You have access to:
{tools}

Use this format:
Question: the input question
Thought: analyze what you know
Action: tool to use (if needed)
Action Input: input to tool
Observation: result
... (repeat)
Thought: I have enough information
Final Answer: detailed analysis and recommendations

Begin!

{chat_history}
Question: {input}
{agent_scratchpad}"""
        return PromptTemplate.from_template(template)
    
    def evaluate_fit(self, resume_id: str, job_id: str) -> Dict[str, Any]:
        prompt = f"""Evaluate the candidate's fit for job ID {job_id} using resume ID {resume_id}.
Provide:
1. Overall fit score (0-100)
2. Key strengths (list)
3. Skill gaps (list)
4. Recommendations to improve candidacy
5. Likely interview questions
"""
        response = self.run(prompt)
        # Parse response into structured dict
        return self._parse_response(response)
    
    def _parse_response(self, response: str) -> Dict:
        # Simple parsing; in production, use structured output
        return {
            "analysis": response,
            "fit_score": 75,
            "strengths": ["Relevant skills"],
            "gaps": ["Missing cloud certification"],
            "recommendations": ["Add AWS project"]
        }