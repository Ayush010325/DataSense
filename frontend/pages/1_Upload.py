import streamlit as st
from utils.api_client import upload_dataset, get_datasets

st.set_page_config(page_title="Upload Dataset", layout="wide")

st.title("Upload Dataset")

col1, col2 = st.columns(2)

with col1:
    st.subheader("New Upload")
    with st.form("upload_form", clear_on_submit=True):
        dataset_name = st.text_input("Dataset Name")
        uploaded_file = st.file_uploader("Upload CSV/XLSX", type=["csv", "xlsx"])
        submit = st.form_submit_button("Upload")

        if submit:
            if uploaded_file and dataset_name:
                with st.spinner("Uploading and analyzing shape..."):
                    result = upload_dataset(uploaded_file, dataset_name)
                    if result and "id" in result:
                        st.success("Dataset uploaded successfully!")
                        st.session_state["dataset_id"] = result["id"]
                    else:
                        st.error("Upload failed.")
            else:
                st.warning("Please provide a name and file.")

with col2:
    st.subheader("Previously Uploaded")
    datasets = get_datasets()
    if datasets:
        for ds in datasets:
            with st.container():
                st.write(f"**{ds['name']}** (Rows: {ds.get('row_count', 'N/A')})")
                if st.button(f"Select##{ds['id']}"):
                    st.session_state["dataset_id"] = ds["id"]
                    st.success(f"Selected {ds['name']}")
                    st.experimental_rerun()
    else:
        st.info("No datasets found.")

if "dataset_id" in st.session_state:
    st.divider()
    st.info(f"Active Dataset ID: {st.session_state['dataset_id']}")
