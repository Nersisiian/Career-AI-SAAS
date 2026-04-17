import streamlit as st
from components.api_client import APIClient

st.title("🎤 Interview Simulation")

api = APIClient()

# Initialize session state
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Select resume and job
resumes = api.get_resumes()
if resumes:
    resume_id = st.selectbox("Select your resume", [r['id'] for r in resumes], format_func=lambda x: next(r['original_filename'] for r in resumes if r['id'] == x))
else:
    st.warning("Upload a resume first.")
    st.stop()

# For job, either from recommendations or manual
job_id = st.text_input("Job ID (from recommendations)", help="Copy a job ID from the recommendations page")
num_questions = st.number_input("Number of questions", 1, 10, 5)

if st.button("Generate Questions") and job_id:
    with st.spinner("Generating interview questions..."):
        result = api.post("/interview/generate-questions", {
            "job_id": job_id,
            "resume_id": resume_id,
            "num_questions": num_questions
        })
        if result:
            st.session_state.questions = result.get('questions', [])
            st.session_state.current_q_index = 0
            st.session_state.answers = {}
            st.rerun()

# Display questions and collect answers
if st.session_state.questions:
    q_index = st.session_state.current_q_index
    if q_index < len(st.session_state.questions):
        question = st.session_state.questions[q_index]
        st.subheader(f"Question {q_index+1}/{len(st.session_state.questions)}")
        st.write(question)
        
        answer = st.text_area("Your Answer", key=f"answer_{q_index}", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer") and answer:
                # Evaluate answer
                with st.spinner("Evaluating..."):
                    eval_result = api.post("/interview/evaluate-answer", {
                        "question": question,
                        "answer": answer
                    })
                    if eval_result:
                        st.session_state.answers[q_index] = {
                            "question": question,
                            "answer": answer,
                            "evaluation": eval_result
                        }
                        st.success(f"Score: {eval_result.get('score', 'N/A')}/10")
                        st.write(eval_result.get('feedback', ''))
        with col2:
            if st.button("Next Question"):
                st.session_state.current_q_index += 1
                st.rerun()
    else:
        st.success("Interview complete!")
        # Show summary
        for idx, ans_data in st.session_state.answers.items():
            with st.expander(f"Q{idx+1}: {ans_data['question'][:50]}..."):
                st.write(f"**Score:** {ans_data['evaluation'].get('score', 'N/A')}/10")
                st.write(ans_data['evaluation'].get('feedback', ''))