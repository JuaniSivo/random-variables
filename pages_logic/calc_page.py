import streamlit as st
import pandas as pd
import numpy as np
from utils.storage import load_saved
from utils.operations import combine_dists
from utils.plotting import show_distribution
from utils.distributions import DIST_UI_SAMPLE
from distributions.uniform_dist import uniform_sample
from distributions.gaussian_dist import gaussian_sample
from distributions.lognormal_dist import lognormal_sample
from distributions.triangular_dist import triangular_sample

# SAMPLERS = {
#     "Uniform": uniform_sample,
#     "Gaussian": gaussian_sample,
#     "Lognormal": lognormal_sample,
#     "Triangular": triangular_sample,
# }

def load_samples(dist):
    # sampler = SAMPLERS[dist["type"]]
    _, sample_func = DIST_UI_SAMPLE[dist["type"]]
    # params = {k: v for k, v in dist.items() if k not in {"type", "name"}}
    params = dist["params"]
    # params["size"] = params.get("size", 10000)
    params["size"] = 10000
    return sample_func(params)

def calc_page():
    st.title("Distribution Calculator")

    saved_data = load_saved()
    dists = saved_data.get("distributions", [])

    if not dists:
        st.warning("No saved distributions found.")
        return

    names = [d.get("name", f"{d['type']}") for d in dists]

    # ---- Operation mode ----
    mode = st.selectbox(
        "Operation mode",
        ["Distribution with Distribution", "Distribution with Number"]
    )

    st.subheader("Select distribution A")
    idx_a = st.selectbox("Distribution A", range(len(dists)), format_func=lambda i: names[i])
    dist_a = dists[idx_a]
    samples_a = load_samples(dist_a)

    # ---- SECOND OPERAND ----
    if mode == "Distribution with Distribution":
        st.subheader("Select distribution B")
        idx_b = st.selectbox("Distribution B", range(len(dists)), format_func=lambda i: names[i])
        dist_b = dists[idx_b]
        samples_b = load_samples(dist_b)

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

    # ---- DOWNLOAD ----
    st.download_button(
        "Download result samples (CSV)",
        data=pd.DataFrame(result, columns=["result"]).to_csv(index=False),
        file_name="combined_distribution.csv",
        mime="text/csv"
    )