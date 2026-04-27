import streamlit as st
import pandas as pd
from utils.api_client import get_dataset_analysis

st.set_page_config(page_title="Dataset Overview", layout="wide")

st.title("Dataset Overview")

if "dataset_id" not in st.session_state:
    st.warning("Please select or upload a dataset first on the Upload page.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

with st.spinner("Analyzing dataset..."):
    analysis = get_dataset_analysis(dataset_id)

if not analysis:
    st.error("Failed to load analysis. Check backend logs.")
    st.stop()

shape = analysis.get("dataset_shape", {})
missing = analysis.get("missing_summary", {})
dupes = analysis.get("duplicates_summary", {})

# Top level metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Row Count", shape.get("row_count", 0))
c2.metric("Column Count", shape.get("column_count", 0))
c3.metric("Total Missing Cells", missing.get("total_missing_cells", 0))
c4.metric("Duplicate Rows", dupes.get("duplicate_row_count", 0))

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Column Types")
    types_dict = analysis.get("column_types", {})
    if types_dict:
        types_df = pd.DataFrame(list(types_dict.items()), columns=["Column", "Detected Type"])
        st.dataframe(types_df, use_container_width=True)

with col2:
    st.subheader("Numeric Summary")
    num_summary = analysis.get("numeric_summary", {})
    if num_summary:
        num_df = pd.DataFrame.from_dict(num_summary, orient="index")
        st.dataframe(num_df, use_container_width=True)
    else:
        st.info("No numeric columns detected.")
