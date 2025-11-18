import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(samples, bins=40, alpha=0.6, figsize=(6,4), title="Histogram"):
    """
    Returns a Matplotlib figure with the histogram of the samples.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(samples, bins=int(np.sqrt(len(samples))), density=True, alpha=alpha)
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    return fig

def plot_cdf(samples, figsize=(6,4), title="CDF"):
    """
    Returns a Matplotlib figure with the cumulative distribution
    function.
    """
    fig, ax = plt.subplots(figsize=figsize)
    sorted_s = np.sort(samples)
    cdf = np.linspace(0, 1, len(sorted_s))
    ax.plot(sorted_s, cdf, marker='.', linestyle='none')
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("CDF")
    return fig

def plot_data_with_fit(data, fitted_samples, title="Data vs Fitted", figsize=(6,4)):
    """
    Returns a figure overlaying a histogram of the original data and the
    fitted samples.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.hist(data, bins=int(np.sqrt(len(data))), alpha=0.6, density=True, label="Data")
    ax.hist(fitted_samples, bins=int(np.sqrt(len(fitted_samples))), alpha=0.4, density=True, label="Fitted")
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.legend()
    return fig