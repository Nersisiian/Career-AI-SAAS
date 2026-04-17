import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create fresh Base for tests to avoid "table already defined" errors
TestBase = declarative_base()

# Monkeypatch the Base in the database module so models use TestBase
import backend.services.user_service.app.core.database as db_module
db_module.Base = TestBase

# Now import models — they will be registered with the fresh TestBase
from backend.services.user_service.app.models.user import User
from backend.services.user_service.app.models.resume import Resume

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

@pytest.fixture(scope="session")
def test_db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    TestBase.metadata.create_all(bind=engine)
    yield engine
    TestBase.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
