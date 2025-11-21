import streamlit as st
import numpy as np
from scipy.stats import triang

SAMPLE_SIZE = 10000

def triangular_ui(sidebar=False):
    ui = st.sidebar if sidebar else st
    left = ui.number_input("Left", value=0.0)
    mode = ui.number_input("Mode", value=0.5)
    right = ui.number_input("Right", value=1.0)
    # size = ui.number_input("Sample size", value=1000)

    c = (mode - left) / (right - left)

    return {
        "left": left,
        "mode": mode,
        "right": right,
        # "size": int(size),
        "c": c
    }

def triangular_sample(p):
    return triang(
        p["c"], 
        loc=p["left"], 
        scale=(p["right"] - p["left"])
    ).rvs(SAMPLE_SIZE)