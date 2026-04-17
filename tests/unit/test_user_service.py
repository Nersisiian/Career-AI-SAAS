import pytest
from uuid import uuid4
from backend.services.user_service.app.crud.user import create_user, get_user_by_email
from backend.services.user_service.app.core.security import get_password_hash, verify_password

def test_create_user(db_session):
    email = f"test_{uuid4().hex[:8]}@example.com"
    hashed = get_password_hash("password123")
    user = create_user(db_session, email, "Test User", hashed)
    assert user.id is not None
    assert user.email == email

def test_get_user_by_email(db_session):
    email = f"test_{uuid4().hex[:8]}@example.com"
    hashed = get_password_hash("password123")
    create_user(db_session, email, "Test User", hashed)
    retrieved = get_user_by_email(db_session, email)
    assert retrieved is not None
    assert retrieved.email == email

def test_password_hashing():
    password = "securepassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)