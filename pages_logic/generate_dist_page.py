import streamlit as st
import pandas as pd

from utils.plotting import show_distribution
from utils.storage import load_saved, save_distribution
from utils.distributions import DIST_UI_SAMPLE

def generate_dist_page():
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
        metadata = {"type": dist_type, "params": params}
        save_distribution(save_name, samples, metadata)
        st.success(f"Saved as '{save_name}'")