import streamlit as st
import pandas as pd
import altair as alt
from utils.api_client import get_experiment, predict_experiment, get_dataset_analysis

st.set_page_config(page_title="What-If Lab", layout="wide")
st.title("What-If Lab")

if "experiment_id" not in st.session_state:
    st.warning("Choose an experiment from Experiment History first.")
    st.stop()

exp_id = st.session_state["experiment_id"]
experiment = get_experiment(exp_id)

if not experiment:
    st.error("I could not load this experiment.")
    st.stop()

st.subheader(f"Experiment: {experiment['name']}")
st.write(f"**Task:** {experiment['task_type']} | **Target:** {experiment.get('target_column', 'N/A')}")
st.write(f"**Model:** {experiment['model_type']}")

dataset_id = experiment['dataset_id']
analysis = get_dataset_analysis(dataset_id)
if not analysis:
    st.warning("I could not load the dataset profile, so the inputs will be basic.")

num_summary = analysis.get("numeric_summary", {}) if analysis else {}
cat_summary = analysis.get("categorical_summary", {}) if analysis else {}
col_types = analysis.get("column_types", {}) if analysis else {}

feature_cols = experiment.get("feature_columns", [])
if not feature_cols:
    st.error("This experiment does not have recorded features.")
    st.stop()

st.divider()
st.subheader("Try New Values")

input_data = {}

with st.form("whatif_form"):
    cols = st.columns(3)

    for idx, feature in enumerate(feature_cols):
        col_type = col_types.get(feature, "unknown")

        with cols[idx % 3]:
            if col_type == "numeric" or feature in num_summary:
                stats = num_summary.get(feature, {})
                mean_val = float(stats.get("mean", 0.0)) if stats.get("mean") is not None else 0.0
                input_data[feature] = st.number_input(f"{feature} (numeric)", value=mean_val, key=f"input_{feature}")

            elif col_type in ["categorical", "boolean", "text"] or feature in cat_summary:
                stats = cat_summary.get(feature, {})
                top_vals = stats.get("top_values", {})
                options = list(top_vals.keys())
                if not options:
                    options = ["Unknown"]
                input_data[feature] = st.selectbox(f"{feature} (category)", options, key=f"input_{feature}")

            else:
                input_data[feature] = st.text_input(f"{feature}", key=f"input_{feature}")

    submit = st.form_submit_button("Run prediction")

if submit:
    with st.spinner("Running the prediction..."):
        result = predict_experiment(exp_id, {"input_data": input_data})
        if result and "prediction" in result:
            st.success("Prediction ready.")

            st.metric("Prediction", str(result["prediction"]))

            if result.get("probability"):
                st.write("**Class probabilities:**")
                st.write(result["probability"])

            if result.get("feature_contributions"):
                st.write("**Model feature importances:**")
                fi = result["feature_contributions"]
                df_fi = pd.DataFrame(fi)
                if not df_fi.empty and 'importance' in df_fi.columns and 'feature' in df_fi.columns:
                    chart = (
                        alt.Chart(df_fi)
                        .mark_bar(color="#4C9BE8")
                        .encode(
                            x=alt.X("importance:Q", title="Importance"),
                            y=alt.Y("feature:N", title="Feature", sort="-x"),
                            tooltip=["feature", "importance"],
                        )
                        .properties(height=300)
                    )
                    st.altair_chart(chart, use_container_width=True)
        else:
            st.error("Prediction failed.")
