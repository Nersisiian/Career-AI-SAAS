from fastapi import FastAPI
from app.api.endpoints import scrape
from app.tasks.scheduler import start_scheduler
from app.core.config import settings

app = FastAPI(title="Scraper Service", version="1.0.0")

@app.on_event("startup")
async def startup():
    if settings.ENABLE_SCHEDULER:
        start_scheduler()

app.include_router(scrape.router, prefix="/scrape", tags=["Scrape"])

@app.get("/health")
async def health():
    return {"status": "ok"}