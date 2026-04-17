from .base import BaseAgent
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from app.core.tools import fetch_job_details, fetch_resume_context

class ResumeOptimizerAgent(BaseAgent):
    def _setup_tools(self) -> List[Tool]:
        return [
            Tool(
                name="JobDetails",
                func=fetch_job_details,
                description="Get job description and required skills"
            ),
            Tool(
                name="ResumeContext",
                func=fetch_resume_context,
                description="Get current resume text and structure"
            )
        ]
    
    def _get_prompt_template(self):
        template = """You are an expert resume writer who helps candidates tailor their resumes to specific job postings.
Your goal is to suggest improvements to make the resume ATS-friendly and highlight relevant experience.

Tools: {tools}

Format:
Question: input
Thought: plan
Action: tool
Action Input: ...
Observation: ...
Final Answer: optimized suggestions

{chat_history}
Question: {input}
{agent_scratchpad}"""
        return PromptTemplate.from_template(template)
    
    def optimize_resume(self, resume_id: str, job_id: str) -> Dict:
        prompt = f"""Analyze resume {resume_id} against job {job_id} and provide:
1. Suggested summary section rewrite
2. Skills to add/highlight
3. Experience bullet improvements
4. Keyword optimization for ATS
"""
        response = self.run(prompt)
        return {"suggestions": response}