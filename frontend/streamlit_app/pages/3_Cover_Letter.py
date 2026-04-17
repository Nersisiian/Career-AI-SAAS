import streamlit as st
from components.api_client import APIClient

st.title("✍️ AI Cover Letter Generator")

api = APIClient()

# Check if job was passed from recommendations page
if 'selected_job_for_cover' in st.session_state:
    job = st.session_state['selected_job_for_cover']
    st.success(f"Generating cover letter for: **{job['title']}** at **{job['company']}**")
else:
    # Manual job entry
    st.subheader("Enter Job Details")
    job_title = st.text_input("Job Title")
    company = st.text_input("Company")
    job_description = st.text_area("Job Description", height=200)
    job = {
        "job_id": "manual",
        "title": job_title,
        "company": company,
        "description": job_description
    }

# Select resume
resumes = api.get_resumes()
if not resumes:
    st.warning("Please upload a resume first.")
    st.stop()

resume_id = st.selectbox("Select Resume", [r['id'] for r in resumes], format_func=lambda x: next(r['original_filename'] for r in resumes if r['id'] == x))

tone = st.selectbox("Tone", ["professional", "enthusiastic", "concise"])

if st.button("Generate Cover Letter"):
    if not job.get('description'):
        st.error("Job description is required.")
    else:
        with st.spinner("Crafting your cover letter..."):
            request = {
                "resume_id": resume_id,
                "job_id": job.get('job_id', 'manual'),
                "job_title": job['title'],
                "company": job['company'],
                "job_description": job['description'],
                "tone": tone
            }
            response = api.generate_cover_letter(request)
            if response:
                st.subheader("Subject Line")
                st.code(response.get('subject_line', ''))
                st.subheader("Cover Letter")
                st.text_area("", response.get('cover_letter', ''), height=400)
                if st.button("Copy to Clipboard"):
                    st.write("Copied! (Use browser copy)")
            else:
                st.error("Failed to generate cover letter.")