from typing import Dict, Callable
import numpy as np


def _fit_uniform(values: np.ndarray) -> Dict[str, float]:
    return {
        "low": float(values.min()),
        "high": float(values.max())
    }


def _fit_gaussian(values: np.ndarray) -> Dict[str, float]:
    return {
        "mean": float(values.mean()),
        "std": float(values.std())
    }


def _fit_lognormal(values: np.ndarray) -> Dict[str, float]:
    # Remove non-positive values (log undefined)
    positive = values[values > 0]
    if len(positive) == 0:
        raise ValueError("Lognormal fit failed: no positive values in dataset.")

    log_vals = np.log(positive)
    return {
        "mu": float(log_vals.mean()),
        "sigma": float(log_vals.std())
    }


def _fit_triangular(values: np.ndarray) -> Dict[str, float]:
    left, right = float(values.min()), float(values.max())
    mode = float(values.mean())   # crude but common
    return {"left": left, "mode": mode, "right": right}


_FIT_FUNCTIONS: Dict[str, Callable[[np.ndarray], Dict[str, float]]] = {
    "Uniform": _fit_uniform,
    "Gaussian": _fit_gaussian,
    "Lognormal": _fit_lognormal,
    "Triangular": _fit_triangular,
}

def moment_fit(values: np.ndarray, dist_type: str) -> Dict[str, float]:
    """
    Fit distribution parameters using simple moment estimates.

    Parameters
    ----------
    values : np.ndarray
        Input data array.
    dist_type : str
        Distribution type: "Uniform", "Gaussian", "Lognormal",
        "Triangular".

    Returns
    -------
    Dict[str, float]
        Dictionary of fitted parameters.

    Raises
    ------
    ValueError
        If the distribution type is not supported or data is invalid.
    """

    if not isinstance(values, np.ndarray):
        values = np.asarray(values)

    if len(values) == 0:
        raise ValueError("moment_fit() received an empty dataset.")

    if dist_type not in _FIT_FUNCTIONS:
        raise ValueError(f"Unsupported distribution type: '{dist_type}'.")

    fit_func = _FIT_FUNCTIONS[dist_type]
    return fit_func(values)