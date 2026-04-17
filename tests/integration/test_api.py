import pytest
from fastapi.testclient import TestClient
from backend.services.user_service.app.main import app
from backend.services.user_service.app.core.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.services.user_service.app.core.database import Base

# Override dependency for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_register_and_login(client):
    # Register
    register_resp = client.post("/auth/register", json={
        "email": "integration@example.com",
        "full_name": "Integration Test",
        "password": "testpass"
    })
    assert register_resp.status_code == 201
    # Login
    login_resp = client.post("/auth/login", data={
        "username": "integration@example.com",
        "password": "testpass"
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()