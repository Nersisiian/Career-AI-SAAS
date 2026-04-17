import streamlit as st
import pandas as pd
from components.api_client import APIClient

st.title("📄 Upload Resume")

api = APIClient()

# Upload section
uploaded_file = st.file_uploader(
    "Choose your resume file",
    type=["pdf", "doc", "docx"],
    help="Max file size: 10MB"
)

if uploaded_file is not None:
    if st.button("Process Resume"):
        with st.spinner("Uploading and processing..."):
            result = api.upload_resume(uploaded_file)
            if result:
                st.success(f"Resume '{result['filename']}' uploaded successfully!")
                st.info("Processing may take a few minutes. We'll extract skills and experience.")
            else:
                st.error("Upload failed. Please try again.")

# Display existing resumes
st.subheader("Your Resumes")
resumes = api.get_resumes()
if resumes:
    df = pd.DataFrame(resumes)
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
    df_display = df[['original_filename', 'processed', 'created_at']]
    df_display.columns = ['Filename', 'Processed', 'Uploaded']
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("No resumes uploaded yet.")