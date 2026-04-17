import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.user_service.app.core.database import engine, Base
from backend.services.user_service.app.models.user import User
from backend.services.user_service.app.models.resume import Resume
from backend.services.scraper_service.app.models.job import Job

def init_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
    