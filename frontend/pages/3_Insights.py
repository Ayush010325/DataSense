import streamlit as st
from utils.api_client import get_dataset_insights

st.set_page_config(page_title="Smart Insights", layout="wide")

st.title("Insights")

if "dataset_id" not in st.session_state:
    st.warning("Upload or select a dataset first.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

with st.spinner("Looking for useful signals..."):
    insights = get_dataset_insights(dataset_id)

if not insights:
    st.info("Nothing urgent stood out in this dataset.")
    st.stop()

for ins in insights:
    severity = ins.get("severity", "info")
    msg = ins.get("message", "")

    if severity == "warning":
        st.warning(msg)
    elif severity == "success":
        st.success(msg)
    else:
        st.info(msg)
