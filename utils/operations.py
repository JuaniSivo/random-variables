import numpy as np
from typing import Union, Callable, Any

ArrayLike = Union[int, float, np.ndarray]

def _to_array(x: Any, size: int | None = None) -> np.ndarray:
    """Ensure x is a numeric ndarray. If scalar, expand to given size."""
    # Scalar expansion
    if np.isscalar(x):
        if not isinstance(x, (int, float)):
            raise TypeError(f"Scalar must be int or float, got {type(x)}")
        if size is None:
            raise ValueError("Scalar requires a reference size.")
        return np.full(size, float(x))

    # Array conversion
    x_arr = np.asarray(x, dtype=float)
    if not np.issubdtype(x_arr.dtype, np.floating):
        raise TypeError("Input array must contain numeric values (int or float)")
    return x_arr


def _align_inputs(a: ArrayLike, b: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
    """
    Convert inputs to float arrays and truncate to the same length.
    Scalars are broadcasted to match the length of the other array.
    """
    if np.isscalar(a) and np.isscalar(b):
        raise ValueError("At least one input must be an array.")

    if np.isscalar(a):
        b_arr = _to_array(b)
        a_arr = _to_array(a, size=len(b_arr))
    elif np.isscalar(b):
        a_arr = _to_array(a)
        b_arr = _to_array(b, size=len(a_arr))
    else:
        a_arr = _to_array(a)
        b_arr = _to_array(b)

    # Truncate to smallest length
    n = min(len(a_arr), len(b_arr))
    return a_arr[:n], b_arr[:n]


def _safe_div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a / np.where(b == 0, 1e-9, b)


def combine_dists(a: ArrayLike, b: ArrayLike, operation: str) -> np.ndarray:
    """
    Combine two distributions (or distribution + scalar) using an operation.
    """
    a_arr, b_arr = _align_inputs(a, b)

    OPS: dict[str, Callable[[np.ndarray, np.ndarray], np.ndarray]] = {
        "Sum": lambda x, y: x + y,
        "Subtract": lambda x, y: x - y,
        "Multiply": lambda x, y: x * y,
        "Divide": _safe_div,
        "Power": lambda x, y: x ** y,
    }

    if operation not in OPS:
        raise ValueError(f"Unknown operation '{operation}'.")

    return OPS[operation](a_arr, b_arr)