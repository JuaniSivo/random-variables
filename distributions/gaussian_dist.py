import streamlit as st
import numpy as np
from scipy.stats import truncnorm

def gaussian_ui(sidebar=False):
    ui = st.sidebar if sidebar else st
    mean = ui.number_input("Mean", value=0.0)
    std = ui.number_input("Std Dev", value=1.0)
    size = ui.number_input("Sample size", value=1000)

    trunc_opt = ui.selectbox("Truncation", ["None", "Lower", "Upper", "Both"])
    lower, upper = None, None

    if trunc_opt in ["Lower", "Both"]:
        lower = ui.number_input("Lower bound", value=-5.0)
    if trunc_opt in ["Upper", "Both"]:
        upper = ui.number_input("Upper bound", value=5.0)

    return {
        "mean": mean,
        "std": std,
        "size": int(size),
        "lower": lower,
        "upper": upper
    }

def gaussian_sample(p):
    if p["lower"] is None and p["upper"] is None:
        return np.random.normal(p["mean"], p["std"], p["size"])

    a = -np.inf if p["lower"] is None else (p["lower"] - p["mean"]) / p["std"]
    b = np.inf if p["upper"] is None else (p["upper"] - p["mean"]) / p["std"]

    return truncnorm(a, b, loc=p["mean"], scale=p["std"]).rvs(p["size"])