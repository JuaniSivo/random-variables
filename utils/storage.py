import json
import os

import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = "data/saved_distributions.json"

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

def init_storage():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump({"distributions": {}}, f)

def load_saved():
    init_storage()
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_all(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def save_distribution(name, samples, metadata):
    new_dist = {
        # "name": name,
        "metadata": metadata or {},
        "samples": samples.tolist()
    }
    data = load_saved()
    data["distributions"][name] = new_dist
    save_all(data)

def rename_distribution(old_name, new_name):
    if new_name == old_name: return None
    data = load_saved()
    data["distributions"][new_name] = data["distributions"][old_name]
    data["distributions"].pop(old_name)
    save_all(data)

def delete_distribution(name):
    data = load_saved()
    data["distributions"].pop(name)
    save_all(data)

def load_distribution_samples(name):
    data = load_saved()
    dist = data["distributions"][name]
    samples = np.array(dist["samples"])

    return samples