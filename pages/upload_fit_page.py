import streamlit as st

from utils.plotting import show_distribution
from utils.storage import get_uploaded_data
from utils.fitting import moment_fit

from distributions.uniform_dist import uniform_ui, uniform_sample
from distributions.gaussian_dist import gaussian_ui, gaussian_sample
from distributions.lognormal_dist import lognormal_ui, lognormal_sample
from distributions.triangular_dist import triangular_ui, triangular_sample

DIST_UI_SAMPLE = {
    "Uniform": (uniform_ui, uniform_sample),
    "Gaussian": (gaussian_ui, gaussian_sample),
    "Lognormal": (lognormal_ui, lognormal_sample),
    "Triangular": (triangular_ui, triangular_sample)
}

def upload_fit_page():
    st.subheader("Upload your CSV or Excel file")

    # Distribution selector
    dist_type = st.sidebar.selectbox(
        "Select a distribution",
        DIST_UI_SAMPLE.keys()
    )
    ui_func, sample_func = DIST_UI_SAMPLE[dist_type]
    params = ui_func(sidebar=True)
    samples = sample_func(params)

    # Upload custom data
    df, _ = get_uploaded_data()
    if df is None:
        return None
    
    st.write("Data preview:")
    st.dataframe(df.head())

    # Column selection
    col = st.selectbox("Select column to fit", df.columns)
    values = df[col].dropna().values

    # Custom data visualization
    show_distribution(data=values)
    params = moment_fit(values, dist_type)

    # Display fitted parameters
    st.subheader("Fitted parameters")
    for key, value in params.items():
        st.write(f"{key}: {value}")

    # Plot comparison
    show_distribution(data=values, distribution=samples)