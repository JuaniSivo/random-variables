import streamlit as st

from pages_logic.upload_fit_page import upload_fit_page
from pages_logic.generate_dist_page import generate_dist_page
from pages_logic.saved_distributions import manage_page

st.title("Probability Distribution Generator")
page = st.sidebar.radio(
    "Select page",
    ["Generate Distribution", "Upload & Fit", "Manage Saved"]
)

if page == "Generate Distribution":
    generate_dist_page()
elif page == "Upload & Fit":
    upload_fit_page()
elif page == "Manage Saved":
    manage_page()