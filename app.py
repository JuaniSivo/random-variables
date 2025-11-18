import streamlit as st
import pandas as pd
from utils.plotting import plot_histogram, plot_cdf
from utils.storage import load_saved, save_distribution

from distributions.uniform_dist import uniform_ui, uniform_sample
from distributions.gaussian_dist import gaussian_ui, gaussian_sample
from distributions.lognormal_dist import lognormal_ui, lognormal_sample
from distributions.triangular_dist import triangular_ui, triangular_sample

st.title("Probability Distribution Generator")

# Load saved distributions
saved_data = load_saved()
saved_list = saved_data["distributions"]

# --------------------------
# Sidebar inputs
# --------------------------
dist_type = st.sidebar.selectbox(
    "Select a distribution",
    ["Uniform", "Gaussian", "Lognormal", "Triangular"]
)

if dist_type == "Uniform":
    params = uniform_ui(sidebar=True)
    samples = uniform_sample(params)

elif dist_type == "Gaussian":
    params = gaussian_ui(sidebar=True)
    samples = gaussian_sample(params)

elif dist_type == "Lognormal":
    params = lognormal_ui(sidebar=True)
    samples = lognormal_sample(params)

elif dist_type == "Triangular":
    params = triangular_ui(sidebar=True)
    samples = triangular_sample(params)

# --------------------------
# Plots
# --------------------------
st.subheader("Histogram")
st.pyplot(plot_histogram(samples))

st.subheader("CDF")
st.pyplot(plot_cdf(samples))

# --------------------------
# Save distribution
# --------------------------
if st.button("Add distribution"):
    save_distribution(dist_type, params)
    st.success(f"{dist_type} distribution saved!")

# --------------------------
# Table of saved distributions
# --------------------------
st.subheader("Saved distributions")
saved_data = load_saved()
saved_list = saved_data["distributions"]

if saved_list:
    df = pd.DataFrame(saved_list)
    st.table(df)
else:
    st.write("No distributions saved yet.")