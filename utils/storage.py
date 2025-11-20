import json
import os

import pandas as pd
import streamlit as st

DATA_PATH = "data/saved_distributions.json"

def load_saved():
    """Load saved distributions from JSON as a dict."""
    if not os.path.exists(DATA_PATH):
        return {"distributions": []}
    try:
        with open(DATA_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return {"distributions": []}
            data = json.loads(content)
            if "distributions" not in data or not isinstance(data["distributions"], list):
                data["distributions"] = []
            return data
    except json.JSONDecodeError:
        return {"distributions": []}

def save_distribution(name, params):
    """Save a new distribution into the JSON dict."""
    data = load_saved()
    data["distributions"].append({
        "Distribution": name,
        "Parameters": params
    })
    os.makedirs("data", exist_ok=True)
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def get_uploaded_data():
    uploaded_file = st.file_uploader("Choose CSV or Excel", type=["csv", "xlsx"])
    if uploaded_file:
        st.session_state["uploaded_file"] = uploaded_file
    elif "uploaded_file" in st.session_state:
        uploaded_file = st.session_state["uploaded_file"]
    else:
        return None, None

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.session_state["uploaded_df"] = df
    return df, uploaded_file