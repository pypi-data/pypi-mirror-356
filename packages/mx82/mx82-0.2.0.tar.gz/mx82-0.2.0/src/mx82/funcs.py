import numpy as np


def sf(x, sig=3):
    """Round a number or NumPy array to the specified number of significant figures."""
    if isinstance(x, np.ndarray):
        return np.array([sf(xi, sig) for xi in x])
    if x == 0:
        return 0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)


def sf3(x):
    """Round a number or NumPy array to 3 significant figures."""
    if isinstance(x, np.ndarray):
        return np.array([sf(xi, 3) for xi in x])
    if x == 0:
        return 0
    return round(x, 3 - int(np.floor(np.log10(abs(x)))) - 1)


def sf4(x):
    """Round a number or NumPy array to 4 significant figures."""
    if isinstance(x, np.ndarray):
        return np.array([sf(xi, 4) for xi in x])
    if x == 0:
        return 0
    return round(x, 4 - int(np.floor(np.log10(abs(x)))) - 1)


def sf5(x):
    """Round a number or NumPy array to 5 significant figures."""
    if isinstance(x, np.ndarray):
        return np.array([sf(xi, 5) for xi in x])
    if x == 0:
        return 0
    return round(x, 5 - int(np.floor(np.log10(abs(x)))) - 1)
