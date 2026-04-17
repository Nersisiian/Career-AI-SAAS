from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    REDIS_URL: str = "redis://localhost:6379/3"
    ENABLE_SCHEDULER: bool = True
    SCRAPE_INTERVAL_HOURS: int = 24
    
    class Config:
        env_file = ".env"

settings = Settings()