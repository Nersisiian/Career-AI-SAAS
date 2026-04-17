import streamlit as st
import base64

def display_pdf(file_path: str):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def format_currency(amount: float) -> str:
    return f"${amount:,.0f}"

def get_initials(name: str) -> str:
    return ''.join([n[0].upper() for n in name.split()[:2]])