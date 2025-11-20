import streamlit as st

from pages_logic.upload_fit_page import upload_fit_page
from pages_logic.generate_dist_page import generate_dist_page

st.title("Probability Distribution Generator")
page = st.sidebar.radio("Select page:", ["Generate Distribution", "Upload & Fit"])

if page == "Generate Distribution":
    generate_dist_page()
elif page == "Upload & Fit":
    upload_fit_page()