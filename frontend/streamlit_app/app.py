import streamlit as st
from components.auth import login_form, logout
from components.api_client import APIClient

st.set_page_config(
    page_title="AI Career Agent",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API client
if "api_client" not in st.session_state:
    st.session_state.api_client = APIClient()

# Authentication check
if "token" not in st.session_state:
    st.title("Welcome to AI Career Agent")
    st.markdown("### Your intelligent job search companion")
    login_form()
    st.stop()

# Main app layout
st.sidebar.title("AI Career Agent")
st.sidebar.success(f"Logged in as {st.session_state.get('user_email', 'User')}")
if st.sidebar.button("Logout"):
    logout()
    st.experimental_rerun()

# Navigation
pages = {
    "Upload Resume": "pages/1_Upload_Resume.py",
    "Job Recommendations": "pages/2_Job_Recommendations.py",
    "Cover Letter Generator": "pages/3_Cover_Letter.py",
    "Interview Simulation": "pages/4_Interview_Simulation.py"
}

st.sidebar.markdown("## Navigation")
page = st.sidebar.radio("Go to", list(pages.keys()))

# Execute selected page
exec(open(pages[page]).read())