import streamlit as st

from utils.plotting import show_distribution
from utils.storage import get_uploaded_data
from utils.fitting import moment_fit
from utils.distributions import DIST_UI_SAMPLE

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
    values = df[col].dropna().to_numpy()

    # Custom data visualization
    show_distribution(data=values)
    params = moment_fit(values, dist_type)

    # Display fitted parameters
    st.subheader("Fitted parameters")
    for key, value in params.items():
        st.write(f"{key}: {value}")

    # Plot comparison
    show_distribution(data=values, distribution=samples)