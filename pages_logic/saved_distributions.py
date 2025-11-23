import streamlit as st

from utils.storage import load_saved, rename_distribution, delete_distribution

def manage_page():
    st.header("Saved Distributions")
    data = load_saved()
    dists = data["distributions"]

    if not dists:
        st.info("No saved distributions.")
        return

    for name, info in dists.items():
        with st.expander(name):
            st.write("Metadata:", info["metadata"])

            new_name = st.text_input(f"Rename {name}", name, key=f"tb_rename_{name}")
            if st.button(f"Click to Rename", key=f"b_rename_{name}") and new_name is not None:
                rename_distribution(name, new_name)
                st.success("Renamed!")
                st.rerun()

            if st.button(f"Click to Delete", key=f"b_delete_{name}"):
                delete_distribution(name)
                st.warning("Deleted!")
                st.rerun()