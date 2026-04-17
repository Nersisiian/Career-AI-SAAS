import streamlit as st
from components.api_client import APIClient

def login_form():
    api = APIClient()
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if api.login(email, password):
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    
    with tab2:
        email = st.text_input("Email", key="reg_email")
        full_name = st.text_input("Full Name", key="reg_name")
        password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            if api.register(email, full_name, password):
                st.success("Registration successful! Please login.")
            else:
                st.error("Registration failed. Email may already be in use.")

def logout():
    st.session_state.pop('token', None)
    st.session_state.pop('user_email', None)