from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    REDIS_URL: str = "redis://localhost:6379/1"
    MODEL_PATH: str = "/app/models"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    FAISS_INDEX_PATH: str = "/app/data/job_index.faiss"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()