import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api_client import get_plottable_columns, train_experiment

st.set_page_config(page_title="ML Sandbox", layout="wide")

st.title("ML Sandbox")

if "dataset_id" not in st.session_state:
    st.warning("Upload or select a dataset first.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

plottable = get_plottable_columns(dataset_id)
if not plottable:
    st.error("I could not load the dataset columns.")
    st.stop()

num_cols = plottable.get("numeric", [])
cat_cols = plottable.get("categorical", [])
all_cols = num_cols + cat_cols

with st.form("ml_config_form"):
    st.subheader("Experiment Setup")
    exp_name = st.text_input("Experiment name", value="First pass")

    col1, col2, col3 = st.columns(3)

    with col1:
        task_type = st.selectbox("Task", ["classification", "regression", "clustering"])
        model_type_options = {
            "classification": ["logistic_regression", "decision_tree", "random_forest"],
            "regression": ["linear_regression", "decision_tree", "random_forest"],
            "clustering": ["kmeans"]
        }

    with col2:
        target_col = st.selectbox("Target column", [""] + all_cols)

    with col3:
        model_type = st.selectbox("Model", model_type_options.get(task_type, []))

    features = st.multiselect("Feature columns", all_cols)

    st.subheader("Preprocessing")
    col4, col5, col6 = st.columns(3)
    with col4:
        missing_strat = st.selectbox("Fill missing numeric values with", ["mean", "median"])
    with col5:
        scale_strat = st.selectbox("Scale numeric values with", ["standard", "minmax", "none"])
    with col6:
        test_size = st.slider("Test split", 0.1, 0.5, 0.2)

    n_clusters = 3
    if task_type == "clustering":
        n_clusters = st.number_input("Number of clusters", min_value=2, max_value=20, value=3)

    submit = st.form_submit_button("Run experiment")

if submit:
    if task_type in ["classification", "regression"] and not target_col:
        st.error("Choose a target column for classification or regression.")
    else:
        payload = {
            "dataset_id": dataset_id,
            "name": exp_name,
            "task_type": task_type,
            "target_column": target_col if target_col else None,
            "feature_columns": features if features else None,
            "model_type": model_type,
            "missing_strategy": missing_strat,
            "scaling_strategy": scale_strat,
            "test_size": test_size,
            "n_clusters": n_clusters
        }

        with st.spinner("Training the model..."):
            result = train_experiment(payload)
            if result and "id" in result:
                st.success(f"{result['name']} has been saved.")

                st.subheader("Metrics")
                metrics = result.get("metrics_json", {})

                if task_type == "classification":
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
                    c2.metric("Precision", f"{metrics.get('precision', 0):.4f}")
                    c3.metric("Recall", f"{metrics.get('recall', 0):.4f}")
                    c4.metric("F1 Score", f"{metrics.get('f1', 0):.4f}")

                    if "roc_auc" in metrics:
                        st.metric("ROC AUC", f"{metrics['roc_auc']:.4f}")

                elif task_type == "regression":
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("MAE", f"{metrics.get('mae', 0):.4f}")
                    c2.metric("MSE", f"{metrics.get('mse', 0):.4f}")
                    c3.metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
                    c4.metric("R2", f"{metrics.get('r2', 0):.4f}")

                elif task_type == "clustering":
                    c1, c2 = st.columns(2)
                    c1.metric("Inertia", f"{metrics.get('inertia', 0):.4f}")
                    if "silhouette_score" in metrics:
                        c2.metric("Silhouette Score", f"{metrics['silhouette_score']:.4f}")

                if "feature_importance" in metrics and metrics["feature_importance"]:
                    st.subheader("Top Features")
                    fi = metrics["feature_importance"]
                    df_fi = pd.DataFrame(fi)
                    fig = px.bar(df_fi, x="importance", y="feature", orientation="h", title="Top feature weights")
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Training did not finish. Review the setup and try again.")
