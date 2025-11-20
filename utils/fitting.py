from typing import Dict

import numpy as np

def moment_fit(values, dist_type:str) -> Dict[str, float]:
    if dist_type == "Uniform":
        fit_dict = {"low": values.min(), "high": values.max()}
    elif dist_type == "Gaussian":
        fit_dict = {"mean": values.mean(), "std": values.std()}
    elif dist_type == "Lognormal":
        log_vals = np.log(values[values > 0])
        fit_dict = {"mu": log_vals.mean(), "sigma": log_vals.std()}
    elif dist_type == "Triangular":
        left, right = values.min(), values.max()
        mode = values.mean()
        fit_dict = {"left": left, "mode": mode, "right": right}
    
    return fit_dict