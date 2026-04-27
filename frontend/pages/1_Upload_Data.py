import streamlit as st
import pandas as pd
from utils.api_client import upload_dataset, get_datasets

st.set_page_config(page_title="Upload Data", page_icon="📤", layout="wide")

st.title("📤 Data Ingestion")
st.markdown("Upload your dataset to begin analysis. Max size: 20MB.")

# Initialize session state for dataset
if 'dataset_id' not in st.session_state:
    st.session_state.dataset_id = None

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Upload New Dataset")
    with st.form("upload_form", clear_on_submit=True):
        dataset_name = st.text_input("Dataset Name (e.g., Sales Data 2023)")
        uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=["csv", "xlsx"])
        submit_button = st.form_submit_button("Upload and Process")

        if submit_button:
            if not dataset_name:
                st.warning("Please provide a name for the dataset.")
            elif uploaded_file is None:
                st.warning("Please select a file to upload.")
            elif uploaded_file.size > 20 * 1024 * 1024:
                st.error("File exceeds the 20MB limit.")
            else:
                with st.spinner("Uploading and extracting metadata..."):
                    result = upload_dataset(uploaded_file, dataset_name)
                    if result:
                        st.success(f"Successfully uploaded: {result['name']}!")
                        st.session_state.dataset_id = result['id']
                        st.info(f"Shape: {result['row_count']} rows, {result['col_count']} columns")

with col2:
    st.subheader("Previously Uploaded")
    datasets = get_datasets()
    if datasets:
        for ds in datasets[:5]: # Show top 5 recent
            with st.container():
                st.markdown(f"**{ds['name']}**")
                st.caption(f"{ds['filename']} | {ds['row_count']} rows")
                if st.button("Select", key=f"select_{ds['id']}"):
                    st.session_state.dataset_id = ds['id']
                    st.experimental_rerun()
    else:
        st.info("No datasets uploaded yet.")

# Show current active dataset
if st.session_state.dataset_id:
    st.divider()
    st.write(f"**Active Dataset ID:** `{st.session_state.dataset_id}`")
    st.success("Head over to the Data Overview page to analyze this dataset.")
