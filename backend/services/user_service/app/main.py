from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, resume, user
from app.core.config import settings
from app.core.database import engine
from app.models import user as user_model
from app.models import resume as resume_model

# Create tables
user_model.Base.metadata.create_all(bind=engine)
resume_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Career Agent - User Service",
    version="1.0.0",
    description="Handles user authentication, resume uploads, and profile management",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(resume.router, prefix="/resumes", tags=["Resumes"])
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "user-service"}