from fastapi import FastAPI
from app.api.endpoints import cover_letter, interview, career_gap
from app.core.config import settings
from app.core.llm_client import LLMClient
from app.core.memory import MemorySystem

app = FastAPI(title="LLM Agent Service", version="1.0.0")

# Initialize on startup
@app.on_event("startup")
async def startup():
    app.state.llm_client = LLMClient()
    app.state.memory = MemorySystem()

app.include_router(cover_letter.router, prefix="/cover-letter", tags=["Cover Letter"])
app.include_router(interview.router, prefix="/interview", tags=["Interview"])
app.include_router(career_gap.router, prefix="/career-gap", tags=["Career Gap"])

@app.get("/health")
async def health():
    return {"status": "ok"}