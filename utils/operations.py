import numpy as np

def combine_dists(a, b, operation):
    """
    a, b: numpy arrays or scalar floats
    """

    # Convert scalars to arrays matching length of a
    if np.isscalar(a) and not np.isscalar(b):
        a = np.full_like(b, a, dtype=float)
    elif np.isscalar(b) and not np.isscalar(a):
        b = np.full_like(a, b, dtype=float)

    # Match sizes (truncate)
    n = min(len(a), len(b))
    a = a[:n]
    b = b[:n]

    if operation == "Sum":
        return a + b
    elif operation == "Subtract":
        return a - b
    elif operation == "Multiply":
        return a * b
    elif operation == "Divide":
        b = np.where(b == 0, 1e-9, b)
        return a / b
    elif operation == "Power":
        return a ** b

    raise ValueError("Unknown operation")