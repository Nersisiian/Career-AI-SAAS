from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    LLM_MODEL: str = "gpt-3.5-turbo"
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/db"
    REDIS_URL: str = "redis://localhost:6379/2"
    SECRET_KEY: str = "shared_secret_key"
    ALGORITHM: str = "HS256"
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    
    class Config:
        env_file = ".env"

settings = Settings()