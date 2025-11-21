import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import load_saved, load_distribution_samples, save_distribution
from utils.operations import combine_dists
from utils.plotting import show_distribution
from utils.distributions import DIST_UI_SAMPLE
from distributions.uniform_dist import uniform_sample
from distributions.gaussian_dist import gaussian_sample
from distributions.lognormal_dist import lognormal_sample
from distributions.triangular_dist import triangular_sample

def calc_page():
    st.title("Distribution Calculator")

    data = load_saved()
    dists = data["distributions"]
    if not dists:
        st.warning("No saved distributions found.")
        return

    # ---- Operation mode ----
    mode = st.selectbox(
        "Operation mode",
        ["Distribution with Distribution", "Distribution with Number"]
    )

    st.subheader("Select distribution A")
    dist_name_a = st.selectbox("Distribution A", dists.keys())
    samples_a = load_distribution_samples(dist_name_a)

    # ---- SECOND OPERAND ----
    if mode == "Distribution with Distribution":
        st.subheader("Select distribution B")
        dist_name_b = st.selectbox("Distribution B", dists.keys())
        samples_b = load_distribution_samples(dist_name_b)
    else:
        st.subheader("Enter number")
        number = st.number_input("Value", value=1.0)
        samples_b = number  # scalar

    # ---- OPERATION ----
    op = st.selectbox("Operation", ["Sum", "Subtract", "Multiply", "Divide", "Power"])

    # ---- COMPUTE ----
    result = combine_dists(samples_a, samples_b, op)

    # ---- PLOTS ----
    st.subheader("Result distribution")
    show_distribution(data=result)

    # ---- SAVE DISTRIBUTION ----
    save_name = st.text_input("Distribution name", value=f"Calc dist")
    if st.button("Save distribution"):
        metadata = {"type": "Calculation"}
        save_distribution(save_name, result, metadata)
        st.success(f"Saved as '{save_name}'")

    # ---- DOWNLOAD ----
    st.download_button(
        "Download result samples (CSV)",
        data=pd.DataFrame(result, columns=["result"]).to_csv(index=False),
        file_name="combined_distribution.csv",
        mime="text/csv"
    )