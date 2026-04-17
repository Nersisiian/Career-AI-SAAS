import pytest
import requests
import time

BASE_URL = "http://localhost:8001"  # user service direct

def test_full_user_flow():
    # 1. Register
    email = f"e2e_{int(time.time())}@test.com"
    reg_resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "full_name": "E2E Test User",
        "password": "e2epassword"
    })
    assert reg_resp.status_code == 201
    
    # 2. Login
    login_resp = requests.post(f"{BASE_URL}/auth/login", data={
        "username": email,
        "password": "e2epassword"
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Upload resume (dummy file)
    files = {"file": ("resume.pdf", b"%PDF-1.4 test content", "application/pdf")}
    upload_resp = requests.post(f"{BASE_URL}/resumes/upload", files=files, headers=headers)
    assert upload_resp.status_code == 200
    resume_id = upload_resp.json()["resume_id"]
    
    # 4. Get resumes
    list_resp = requests.get(f"{BASE_URL}/resumes/", headers=headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
    
    # Note: Full flow would also call ML service matching, etc.