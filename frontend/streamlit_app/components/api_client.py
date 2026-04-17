import requests
import streamlit as st
from typing import Optional, Dict, List

class APIClient:
    def __init__(self):
        self.base_url = st.secrets.get("API_BASE_URL", "http://localhost:8000")
    
    def _headers(self) -> Dict:
        headers = {"Content-Type": "application/json"}
        if "token" in st.session_state:
            headers["Authorization"] = f"Bearer {st.session_state.token}"
        return headers
    
    def login(self, email: str, password: str) -> bool:
        try:
            resp = requests.post(
                f"{self.base_url}/auth/login",
                data={"username": email, "password": password}
            )
            if resp.status_code == 200:
                data = resp.json()
                st.session_state.token = data["access_token"]
                st.session_state.user_email = email
                return True
            return False
        except Exception as e:
            st.error(f"Connection error: {e}")
            return False
    
    def register(self, email: str, full_name: str, password: str) -> bool:
        try:
            resp = requests.post(
                f"{self.base_url}/auth/register",
                json={"email": email, "full_name": full_name, "password": password}
            )
            return resp.status_code == 201
        except:
            return False
    
    def upload_resume(self, file) -> Optional[Dict]:
        try:
            files = {"file": (file.name, file, file.type)}
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            resp = requests.post(
                f"{self.base_url}/resumes/upload",
                files=files,
                headers=headers
            )
            return resp.json() if resp.status_code == 200 else None
        except:
            return None
    
    def get_resumes(self) -> List[Dict]:
        try:
            resp = requests.get(
                f"{self.base_url}/resumes/",
                headers=self._headers()
            )
            return resp.json() if resp.status_code == 200 else []
        except:
            return []
    
    def match_jobs(self, resume_id: str, top_k: int = 20) -> Dict:
        try:
            resp = requests.post(
                f"{self.base_url}/matching/jobs",
                json={"resume_id": resume_id, "top_k": top_k},
                headers=self._headers()
            )
            return resp.json() if resp.status_code == 200 else {"matches": []}
        except:
            return {"matches": []}
    
    def generate_cover_letter(self, request: Dict) -> Dict:
        try:
            resp = requests.post(
                f"{self.base_url}/cover-letter/generate",
                json=request,
                headers=self._headers()
            )
            return resp.json() if resp.status_code == 200 else {}
        except:
            return {}