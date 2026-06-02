import streamlit as st
from utils.api_client import get_dataset_experiments

st.set_page_config(page_title="Experiment History", layout="wide")
st.title("Experiment History")

if "dataset_id" not in st.session_state:
    st.warning("Upload or select a dataset first.")
    st.stop()

dataset_id = st.session_state["dataset_id"]
experiments = get_dataset_experiments(dataset_id)

if not experiments:
    st.info("No experiments yet for this dataset. Run one in ML Sandbox when you are ready.")
    st.stop()

st.write(f"**{len(experiments)}** saved experiment(s)")

for exp in experiments:
    date_str = exp['created_at'][:10]
    task_fmt = exp['task_type'].upper()

    with st.expander(f"[{task_fmt}] {exp['name']} - {exp['model_type']} ({date_str})"):
        st.write(f"**Task:** {exp['task_type']}")
        st.write(f"**Model:** {exp['model_type']}")
        st.write(f"**Created:** {exp['created_at']}")

        if st.button(f"Open What-If Lab for '{exp['name']}'", key=f"btn_{exp['id']}"):
            st.session_state["experiment_id"] = exp["id"]
            st.success("Selected. Open What-If Lab from the sidebar.")
