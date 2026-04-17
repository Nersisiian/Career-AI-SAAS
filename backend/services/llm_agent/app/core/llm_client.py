import openai
from langchain.llms import OpenAI
from app.core.config import settings

class LLMClient:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model_name = settings.LLM_MODEL
        self.langchain_llm = OpenAI(
            temperature=0.7,
            model_name=self.model_name,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def generate(self, prompt: str, **kwargs) -> str:
        # Async version for FastAPI
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self.langchain_llm(prompt)
        )
        return response

def get_llm():
    return LLMClient().langchain_llm