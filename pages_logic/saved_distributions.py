import streamlit as st

from utils.storage import load_saved, rename_distribution, delete_distribution

def manage_page():
    st.header("Saved Distributions")
    data = load_saved()
    dists = data["distributions"]

    if not dists:
        st.info("No saved distributions.")
        return

    for i, dist in enumerate(dists):
        with st.expander(f"{dist['name']} ({dist['type']})"):
            st.write("Parameters:", dist["params"])

            new_name = st.text_input(f"Rename #{i}", dist["name"], key=f"name_{i}")
            if st.button(f"Apply rename #{i}"):
                rename_distribution(i, new_name)
                st.success("Renamed!")
                st.rerun()

            if st.button(f"Delete #{i}"):
                delete_distribution(i)
                st.warning("Deleted!")
                st.rerun()