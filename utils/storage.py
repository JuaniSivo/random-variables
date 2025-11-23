import json
import os
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st

DATA_PATH = "data/saved_distributions.json"

def _ensure_storage() -> None:
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump({"distributions": {}}, f)

def _read_storage() -> dict:
    _ensure_storage()
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def _write_storage(data: dict) -> None:
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_saved():
    return _read_storage()

def save_all(data):
    _write_storage(data)

def save_distribution(name: str, samples: np.ndarray, metadata: Optional[dict] = None) -> None:
    data = _read_storage()

    if not isinstance(samples, np.ndarray):
        raise TypeError("samples must be a numpy array")

    data["distributions"][name] = {
        "metadata": metadata or {},
        "samples": samples.astype(float).tolist()
    }

    _write_storage(data)


def rename_distribution(old: str, new: str) -> None:
    if old == new:
        return

    data = _read_storage()

    if old not in data["distributions"]:
        raise KeyError(f"Distribution '{old}' does not exist")
    if new in data["distributions"]:
        raise KeyError(f"Distribution '{new}' already exists")

    data["distributions"][new] = data["distributions"].pop(old)
    _write_storage(data)


def delete_distribution(name: str) -> None:
    data = _read_storage()

    if name not in data["distributions"]:
        raise KeyError(f"Distribution '{name}' does not exist")

    del data["distributions"][name]
    _write_storage(data)


def load_distribution_samples(name: str) -> np.ndarray:
    data = _read_storage()
    try:
        return np.array(data["distributions"][name]["samples"], dtype=float)
    except KeyError:
        raise KeyError(f"Distribution '{name}' not found")

def get_uploaded_data() -> Tuple[Optional[pd.DataFrame], Optional[object]]:
    """Handles persistent upload (CSV/XLSX) across reruns."""
    uploaded = st.file_uploader("Choose CSV or Excel", type=["csv", "xlsx"])

    if uploaded:
        st.session_state["uploaded_file"] = uploaded
    elif "uploaded_file" in st.session_state:
        uploaded = st.session_state["uploaded_file"]
    else:
        return None, None

    ext = uploaded.name.lower()

    if ext.endswith(".csv"):
        df = pd.read_csv(uploaded)
    elif ext.endswith(".xlsx"):
        df = pd.read_excel(uploaded)
    else:
        st.error("Unsupported file type.")
        return None, None

    st.session_state["uploaded_df"] = df
    return df, uploaded