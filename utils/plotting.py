import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_histogram(data=None, distribution=None, alpha=0.6, figsize=(6,4), title="Histogram"):
    """
    Returns a Matplotlib figure with the histogram of the samples.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot data
    if data is not None:
        bins_data = int(np.sqrt(len(data)))
        ax.hist(
            data,
            bins=bins_data,
            density=True,
            histtype="bar",
            alpha=alpha,
            label="Real data"
        )
    
    # Plot distribution
    if distribution is not None:
        bins_distribution = int(np.sqrt(len(distribution)))
        ax.hist(
            distribution,
            bins=bins_distribution,
            density=True,
            histtype="step",
            alpha=alpha,
            label="Sintetic data"
        )
    
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("Density")

    return fig

def plot_cdf(data=None, distribution=None, figsize=(6,4), title="CDF"):
    """
    Returns a Matplotlib figure with the cumulative distribution
    function.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot data
    if data is not None:
        bins_data = int(np.sqrt(len(data)))
        ax.hist(
            data,
            bins=bins_data,
            density=True,
            cumulative=True,
            histtype="step",
            label="Real data"
        )
    
    # Plot distribution
    if distribution is not None:
        bins_distribution = int(np.sqrt(len(distribution)))
        ax.hist(
            distribution,
            bins=bins_distribution,
            density=True,
            cumulative=True,
            histtype="step",
            label="Sintetic data"
        )
    
    ax.set_title(title)
    ax.set_xlabel("Value")
    ax.set_ylabel("CDF")

    return fig

def show_distribution(data=None, distribution=None):
    st.subheader("Histogram")
    st.pyplot(plot_histogram(data=data, distribution=distribution))
    st.subheader("CDF")
    st.pyplot(plot_cdf(data=data, distribution=distribution))