import streamlit as st
import pandas as pd
from components.api_client import APIClient

st.title("🎯 Job Recommendations")

api = APIClient()

# Select resume
resumes = api.get_resumes()
if not resumes:
    st.warning("Please upload a resume first.")
    st.stop()

resume_options = {r['original_filename']: r['id'] for r in resumes if r.get('processed')}
if not resume_options:
    st.warning("No processed resumes available. Please wait for processing to complete.")
    st.stop()

selected_filename = st.selectbox("Select Resume", list(resume_options.keys()))
resume_id = resume_options[selected_filename]

top_k = st.slider("Number of jobs to show", 5, 50, 20)

if st.button("Find Matching Jobs"):
    with st.spinner("Searching for matching jobs..."):
        result = api.match_jobs(resume_id, top_k)
    
    if result and result.get('matches'):
        matches = result['matches']
        df = pd.DataFrame(matches)
        df['score'] = df['score'].apply(lambda x: f"{x:.0%}")
        st.dataframe(
            df[['title', 'company', 'location', 'score']],
            column_config={
                "title": "Job Title",
                "company": "Company",
                "location": "Location",
                "score": "Match Score"
            },
            use_container_width=True
        )
        
        # Show details for selected job
        selected_job = st.selectbox("Select a job to see details", df['title'].tolist())
        if selected_job:
            job = next(m for m in matches if m['title'] == selected_job)
            with st.expander("Job Details", expanded=True):
                st.markdown(f"**{job['title']}** at **{job['company']}**")
                st.write(f"📍 {job['location']}")
                st.metric("Match Score", f"{job['score']}")
                if st.button("Generate Cover Letter", key=f"cover_{job['job_id']}"):
                    st.session_state['selected_job_for_cover'] = job
                    st.switch_page("pages/3_Cover_Letter.py")
    else:
        st.info("No matching jobs found. Try again later.")