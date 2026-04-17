from fastapi import FastAPI
from app.api.endpoints import metrics
from app.core.config import settings
from app.core.database import engine
from app.models.feedback import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Analytics Service", version="1.0.0")

app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/health")
async def health():
    return {"status": "ok"}