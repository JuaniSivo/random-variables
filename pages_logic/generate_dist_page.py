import streamlit as st
import pandas as pd

from utils.plotting import show_distribution
from utils.storage import load_saved, save_distribution

from distributions.uniform_dist import uniform_ui, uniform_sample
from distributions.gaussian_dist import gaussian_ui, gaussian_sample
from distributions.lognormal_dist import lognormal_ui, lognormal_sample
from distributions.triangular_dist import triangular_ui, triangular_sample

DIST_UI_SAMPLE = {
    "Uniform": (uniform_ui, uniform_sample),
    "Gaussian": (gaussian_ui, gaussian_sample),
    "Lognormal": (lognormal_ui, lognormal_sample),
    "Triangular": (triangular_ui, triangular_sample)
}

def generate_dist_page():
    # Load saved distributions
    saved_data = load_saved()
    saved_list = saved_data["distributions"]

    # Distribution selector
    dist_type = st.sidebar.selectbox(
        "Select a distribution",
        DIST_UI_SAMPLE.keys()
    )

    ui_func, sample_func = DIST_UI_SAMPLE[dist_type]
    params = ui_func(sidebar=True)
    samples = sample_func(params)

    # Plots
    show_distribution(data=samples)

    # Save distribution
    save_name = st.text_input("Distribution name", value=f"{dist_type} dist")
    if st.button("Save distribution"):
        save_distribution(save_name, dist_type, params)
        st.success(f"Saved as '{save_name}'")

    # Saved table
    st.subheader("Saved distributions")
    saved_data = load_saved()
    saved_list = saved_data["distributions"]

    if saved_list:
        df = pd.DataFrame(saved_list)
        st.table(df)
    else:
        st.write("No distributions saved yet.")