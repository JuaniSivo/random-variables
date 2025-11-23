import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import load_saved, load_distribution_samples, save_distribution
from utils.operations import combine_dists
from utils.plotting import show_distribution
from utils.distributions import DIST_UI_SAMPLE

def calc_page():
    data = load_saved()
    dists = data["distributions"]
    if not dists:
        st.warning("No saved distributions found.")
        return

    mode = st.selectbox(
        "Operation mode",
        ["Distribution with Distribution", "Distribution with Number"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        dist_name_a = st.selectbox("Distribution A", dists.keys())
        samples_a = load_distribution_samples(dist_name_a)

    with col2:
        op = st.selectbox("Operation", ["Sum", "Subtract", "Multiply", "Divide", "Power"])

    if mode == "Distribution with Distribution":
        with col3:
            dist_name_b = st.selectbox("Distribution B", dists.keys())
            samples_b = load_distribution_samples(dist_name_b)
    else:
        with col3:
            number = st.number_input("Value", value=1.0)
            samples_b = number

    result = combine_dists(samples_a, samples_b, op)
    show_distribution(data=result)

    save_name = st.text_input("Distribution name", value=f"Calc dist")
    if st.button("Save distribution"):
        metadata = {"type": "Calculation"}
        save_distribution(save_name, result, metadata)
        st.success(f"Saved as '{save_name}'")

    st.download_button(
        "Download result samples (CSV)",
        data=pd.DataFrame(result, columns=["result"]).to_csv(index=False),
        file_name="combined_distribution.csv",
        mime="text/csv"
    )