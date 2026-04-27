import streamlit as st
from utils.api_client import get_dataset_insights

st.set_page_config(page_title="Smart Insights", layout="wide")

st.title("Smart Insights")

if "dataset_id" not in st.session_state:
    st.warning("Please select or upload a dataset first on the Upload page.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

with st.spinner("Generating rule-based insights..."):
    insights = get_dataset_insights(dataset_id)

if not insights:
    st.info("No actionable insights found for this dataset.")
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
