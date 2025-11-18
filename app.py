import streamlit as st
import pandas as pd
import numpy as np
from utils.plotting import plot_histogram, plot_cdf, plot_data_with_fit
from utils.storage import load_saved, save_distribution
from distributions.uniform_dist import uniform_ui, uniform_sample
from distributions.gaussian_dist import gaussian_ui, gaussian_sample
from distributions.lognormal_dist import lognormal_ui, lognormal_sample
from distributions.triangular_dist import triangular_ui, triangular_sample
from scipy.stats import norm, lognorm, uniform, triang, truncnorm

st.title("Probability Distribution Generator")

# --------------------------
# Sidebar page selection
# --------------------------
page = st.sidebar.radio("Select page:", ["Generate Distribution", "Upload & Fit"])

# --------------------------
# PAGE 1: Generate Distribution
# --------------------------
if page == "Generate Distribution":
    # Load saved distributions
    saved_data = load_saved()
    saved_list = saved_data["distributions"]

    # Distribution selector
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

    # Plots
    st.subheader("Histogram")
    st.pyplot(plot_histogram(samples))
    st.subheader("CDF")
    st.pyplot(plot_cdf(samples))

    # Save distribution
    if st.button("Add distribution"):
        save_distribution(dist_type, params)
        st.success(f"{dist_type} distribution saved!")

    # Saved table
    st.subheader("Saved distributions")
    saved_data = load_saved()
    saved_list = saved_data["distributions"]

    if saved_list:
        df = pd.DataFrame(saved_list)
        st.table(df)
    else:
        st.write("No distributions saved yet.")

# --------------------------
# PAGE 2: Upload & Fit
# --------------------------
elif page == "Upload & Fit":
    st.subheader("Upload your CSV or Excel file")
    uploaded_file = st.file_uploader("Choose CSV or Excel", type=["csv", "xlsx"])

    # Distribution selector
    dist_type = st.sidebar.selectbox(
        "Select a distribution",
        ["Uniform", "Gaussian", "Lognormal", "Triangular"]
    )

    if dist_type == "Uniform":
        params = uniform_ui(sidebar=True)
        fitted_samples = uniform_sample(params)

    elif dist_type == "Gaussian":
        params = gaussian_ui(sidebar=True)
        fitted_samples = gaussian_sample(params)

    elif dist_type == "Lognormal":
        params = lognormal_ui(sidebar=True)
        fitted_samples = lognormal_sample(params)

    elif dist_type == "Triangular":
        params = triangular_ui(sidebar=True)
        fitted_samples = triangular_sample(params)

    if uploaded_file:
        # Load data
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.write("Data preview:")
        st.dataframe(df.head())

        # Column selection
        col = st.selectbox("Select column to fit", df.columns)
        values = df[col].dropna().values

        st.subheader("Histogram of selected data")
        st.pyplot(plot_histogram(values))

        # Fit parameters
        if dist_type == "Uniform":
            low, high = values.min(), values.max()
            params = {"low": low, "high": high}

        elif dist_type == "Gaussian":
            mean, std = values.mean(), values.std()
            params = {"mean": mean, "std": std}

        elif dist_type == "Lognormal":
            # Fit lognormal via log-transform
            log_vals = np.log(values[values > 0])
            mu, sigma = log_vals.mean(), log_vals.std()
            params = {"mu": mu, "sigma": sigma}

        elif dist_type == "Triangular":
            left, right = values.min(), values.max()
            mode = values.mean()
            c = (mode - left) / (right - left)
            params = {"left": left, "mode": mode, "right": right}

        # Display fitted parameters
        st.subheader("Fitted parameters")
        for key, value in params.items():
            st.write(f"{key}: {value}")

        # Plot comparison
        st.subheader(f"Histogram with fitted {dist_type}")
        st.pyplot(
            plot_data_with_fit(
                values,
                fitted_samples,
                title=f"{dist_type} fit"
            )
        )