import streamlit as st
from utils.api_client import get_health

st.set_page_config(page_title="DataSense Lab", layout="wide")

st.title("DataSense Lab")

is_healthy = get_health()
if is_healthy:
    st.success("Backend connected")
else:
    st.error("Backend is not responding")

st.markdown("""
### Start with a dataset, then follow the trail.
Use DataSense Lab to profile a file, spot issues, build charts, and run quick modeling experiments without leaving the workspace.

**A good path through the app:**
1. Upload a dataset or pick one you already added.
2. Open Overview to check shape, missing values, and column types.
3. Read Insights for the first things worth investigating.
4. Use Visual Explorer to build charts.
5. Try an experiment in ML Sandbox and review it later in Experiment History.
6. Open What-If Lab when you want to test saved models with new values.
""")

if "dataset_id" in st.session_state:
    st.info(f"Active dataset: {st.session_state['dataset_id']}")
else:
    st.warning("No dataset selected yet.")
