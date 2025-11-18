import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(samples):
    fig, ax = plt.subplots()
    ax.hist(samples, bins=40, density=True, alpha=0.6)
    ax.set_title("Histogram")
    return fig

def plot_cdf(samples):
    fig, ax = plt.subplots()
    sorted_s = np.sort(samples)
    cdf = np.linspace(0, 1, len(sorted_s))
    ax.plot(sorted_s, cdf)
    ax.set_title("CDF")
    return fig