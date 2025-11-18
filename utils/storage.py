import json
import os

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