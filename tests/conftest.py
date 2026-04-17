import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.user_service.app.core.database import Base
from backend.services.user_service.app.models.user import User
from backend.services.user_service.app.models.resume import Resume

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

@pytest.fixture(scope="session")
def test_db_engine():
    # Очищаем все мапперы, чтобы избежать конфликтов повторного определения
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
