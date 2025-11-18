import streamlit as st
import numpy as np
from scipy.stats import lognorm, truncnorm

def lognormal_ui(sidebar=False):
    ui = st.sidebar if sidebar else st
    mu = ui.number_input("Log-mean (mu)", value=0.0)
    sigma = ui.number_input("Log-std (sigma)", value=0.5)
    size = ui.number_input("Sample size", value=1000)

    trunc_opt = ui.selectbox("Truncation", ["None", "Lower", "Upper", "Both"])
    lower, upper = None, None

    if trunc_opt in ["Lower", "Both"]:
        lower = ui.number_input("Lower bound", value=0.1)
    if trunc_opt in ["Upper", "Both"]:
        upper = ui.number_input("Upper bound", value=5.0)

    return {
        "mu": mu,
        "sigma": sigma,
        "size": int(size),
        "lower": lower,
        "upper": upper
    }

def lognormal_sample(p):
    if p["lower"] is None and p["upper"] is None:
        return lognorm(s=p["sigma"], scale=np.exp(p["mu"])).rvs(p["size"])

    a = -np.inf if p["lower"] is None else (np.log(p["lower"]) - p["mu"]) / p["sigma"]
    b = np.inf if p["upper"] is None else (np.log(p["upper"]) - p["mu"]) / p["sigma"]

    return np.exp(
        truncnorm(a, b, loc=p["mu"], scale=p["sigma"]).rvs(p["size"])
    )