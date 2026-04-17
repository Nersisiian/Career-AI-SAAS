from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "User Service"
    ENVIRONMENT: str = "development"
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]
    
    # Uploads
    UPLOAD_DIR: str = "./uploads"
    
    # Services
    ML_SERVICE_URL: str = "http://ml-service:8000"
    LLM_SERVICE_URL: str = "http://llm-agent:8000"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()