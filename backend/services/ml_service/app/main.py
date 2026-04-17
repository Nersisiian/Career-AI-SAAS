from fastapi import FastAPI
from app.api.endpoints import embeddings, matching, ranking
from app.core.config import settings
from app.core.model_loader import load_models

app = FastAPI(title="ML Service - AI Career Agent", version="1.0.0")

# Load models on startup
@app.on_event("startup")
async def startup_event():
    load_models()

app.include_router(embeddings.router, prefix="/embeddings", tags=["Embeddings"])
app.include_router(matching.router, prefix="/matching", tags=["Matching"])
app.include_router(ranking.router, prefix="/ranking", tags=["Ranking"])

@app.get("/health")
async def health():
    return {"status": "ok"}