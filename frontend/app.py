import streamlit as st
from utils.api_client import get_health

st.set_page_config(page_title="DataSense Lab", layout="wide")

st.title("DataSense Lab Dashboard")

# Health Check
is_healthy = get_health()
if is_healthy:
    st.success("Backend Status: OK connected to FastAPI")
else:
    st.error("Backend Status: Disconnected")

st.markdown("""
### Welcome to DataSense Lab!
This is your central hub for data understanding and experimentation.

**How to use:**
1. Go to **1. Upload** in the sidebar to add a new dataset or select an existing one.
2. Visit **2. Overview** to view automated profiling and statistics.
3. Check **3. Insights** for rule-based actionable intelligence on your data.
4. Explore **4. Visual Explorer** to create dynamic charts.
5. Head to **5. ML Sandbox** to run quick ML experiments and analyze results.
6. Visit **6. Experiment History** to view past models.
7. Use the **7. What-If Lab** to make predictions dynamically!
""")

if "dataset_id" in st.session_state:
    st.info(f"Active Dataset ID: {st.session_state['dataset_id']}")
else:
    st.warning("No dataset currently selected.")
