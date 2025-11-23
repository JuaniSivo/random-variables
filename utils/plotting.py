import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import streamlit as st


def _auto_bins(x: np.ndarray) -> int:
    """
    Automatic bin size using Freedman–Diaconis rule.
    """
    x = np.asarray(x)
    n = len(x)
    if n < 2:
        return 1

    q25, q75 = np.percentile(x, [25, 75])
    iqr = q75 - q25
    bin_width = 2 * iqr / (n ** (1/3))

    if bin_width <= 0:
        return int(np.sqrt(n))

    bins = int((x.max() - x.min()) / bin_width)
    return max(bins, 1)


def _plot_kde(ax, x, label):
    kde = gaussian_kde(x)
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, kde(xs), linewidth=1.4, label=f"{label} KDE")


def draw_histogram_panel(ax, data=None, distribution=None):
    """Draw histogram + KDE curves."""
    # Real data histogram
    if data is not None:
        bins_data = _auto_bins(data)
        ax.hist(
            data,
            bins=bins_data,
            density=True,
            alpha=0.45,
            label="Real data"
        )
        # _plot_kde(ax, data, "Real")

    # Synthetic distribution histogram
    if distribution is not None:
        bins_dist = _auto_bins(distribution)
        ax.hist(
            distribution,
            bins=bins_dist,
            density=True,
            histtype="step",
            linewidth=1.4,
            label="Synthetic data"
        )
        # _plot_kde(ax, distribution, "Synthetic")

    ax.set_title("Histogram + KDE")
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.2)
    ax.legend()


def draw_cdf_panel(ax, data=None, distribution=None):
    """Draw empirical CDF for data and synthetic distribution."""
    # Real data CDF
    if data is not None:
        xs = np.sort(data)
        ys = np.linspace(0, 1, len(xs))
        ax.plot(xs, ys, linewidth=1.4, label="Real data")

    # Synthetic distribution CDF
    if distribution is not None:
        xs = np.sort(distribution)
        ys = np.linspace(0, 1, len(xs))
        ax.plot(xs, ys, linewidth=1.4, label="Synthetic data")

    ax.set_title("CDF")
    ax.set_xlabel("Value")
    ax.set_ylabel("CDF")
    ax.grid(alpha=0.2)
    ax.legend()
    

def plot_distribution(data=None, distribution=None, figsize=(12, 8), title="Distribution"):
    """
    Plot histogram + KDE on the left and CDF on the right.
    Delegates drawing to smaller, testable functions.
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    ax_hist, ax_cdf = axes

    draw_histogram_panel(ax_hist, data=data, distribution=distribution)
    draw_cdf_panel(ax_cdf, data=data, distribution=distribution)

    fig.suptitle(title, fontsize=14)
    fig.tight_layout()

    return fig


def show_distribution(data=None, distribution=None, title="Distribution"):
    st.pyplot(
        plot_distribution(
            data=data, 
            distribution=distribution, 
            title=title
        )
    )