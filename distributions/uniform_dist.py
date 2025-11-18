import streamlit as st
import numpy as np

def uniform_ui(sidebar=False):
    ui = st.sidebar if sidebar else st
    low = ui.number_input("Lower bound", value=0.0)
    high = ui.number_input("Upper bound", value=1.0)
    size = ui.number_input("Sample size", value=1000)
    return {"low": low, "high": high, "size": int(size)}

def uniform_sample(params):
    return np.random.uniform(
        params["low"],
        params["high"],
        params["size"]
    )