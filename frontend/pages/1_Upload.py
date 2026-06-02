import streamlit as st
from utils.api_client import upload_dataset, get_datasets

st.set_page_config(page_title="Upload Data", layout="wide")

st.title("Upload Data")
st.markdown("Add a CSV or Excel file. Keep it under 20 MB so the app can profile it quickly.")

if 'dataset_id' not in st.session_state:
    st.session_state.dataset_id = None

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Add a New Dataset")
    with st.form("upload_form", clear_on_submit=True):
        dataset_name = st.text_input("Dataset name", placeholder="Sales data 2023")
        uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
        submit_button = st.form_submit_button("Upload and profile")

        if submit_button:
            if not dataset_name:
                st.warning("Give this dataset a name first.")
            elif uploaded_file is None:
                st.warning("Choose a file to upload.")
            elif uploaded_file.size > 20 * 1024 * 1024:
                st.error("This file is over the 20 MB limit.")
            else:
                with st.spinner("Uploading the file and reading its columns..."):
                    result = upload_dataset(uploaded_file, dataset_name)
                    if result:
                        st.success(f"{result['name']} is ready.")
                        st.session_state.dataset_id = result['id']
                        st.info(f"Shape: {result['row_count']} rows, {result['col_count']} columns")

with col2:
    st.subheader("Recent Datasets")
    datasets = get_datasets()
    if datasets:
        for ds in datasets[:5]:
            with st.container():
                st.markdown(f"**{ds['name']}**")
                st.caption(f"{ds['filename']} | {ds['row_count']} rows")
                if st.button("Select", key=f"select_{ds['id']}"):
                    st.session_state.dataset_id = ds['id']
                    st.experimental_rerun()
    else:
        st.info("No datasets yet.")

if st.session_state.dataset_id:
    st.divider()
    st.write(f"**Active dataset:** `{st.session_state.dataset_id}`")
    st.success("Open Overview next to see what is inside this file.")
