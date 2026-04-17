import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.services.user_service.app.core.database import Base
from backend.services.user_service.app.models.user import User
from backend.services.user_service.app.models.resume import Resume

@pytest.fixture(scope="session")
def test_db_engine():
    """Create test database engine."""
    test_db_url = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db_engine):
    """Create a new database session for a test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()