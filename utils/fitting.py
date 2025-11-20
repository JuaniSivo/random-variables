import numpy as np

def moment_fit(values, dist_type):
    if dist_type == "Uniform":
        return {"low": values.min(), "high": values.max()}
    elif dist_type == "Gaussian":
        return {"mean": values.mean(), "std": values.std()}
    elif dist_type == "Lognormal":
        log_vals = np.log(values[values > 0])
        return {"mu": log_vals.mean(), "sigma": log_vals.std()}
    elif dist_type == "Triangular":
        left, right = values.min(), values.max()
        mode = values.mean()
        return {"left": left, "mode": mode, "right": right}