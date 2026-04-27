import streamlit as st
import plotly.express as px
import pandas as pd
from utils.api_client import get_plottable_columns, train_experiment

st.set_page_config(page_title="ML Sandbox", layout="wide")

st.title("ML Sandbox")

if "dataset_id" not in st.session_state:
    st.warning("Please select or upload a dataset first on the Upload page.")
    st.stop()

dataset_id = st.session_state["dataset_id"]

plottable = get_plottable_columns(dataset_id)
if not plottable:
    st.error("Could not load dataset columns.")
    st.stop()

num_cols = plottable.get("numeric", [])
cat_cols = plottable.get("categorical", [])
dt_cols = plottable.get("datetime", [])
all_cols = num_cols + cat_cols

with st.form("ml_config_form"):
    st.subheader("Experiment Configuration")
    exp_name = st.text_input("Experiment Name", value="My First Experiment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        task_type = st.selectbox("Task Type", ["classification", "regression", "clustering"])
        model_type_options = {
            "classification": ["logistic_regression", "decision_tree", "random_forest"],
            "regression": ["linear_regression", "decision_tree", "random_forest"],
            "clustering": ["kmeans"]
        }
        
    with col2:
        target_col = st.selectbox("Target Column (Ignored for clustering)", [""] + all_cols)
        
    with col3:
        model_type = st.selectbox("Model Type", model_type_options.get(task_type, []))
        
    features = st.multiselect("Feature Columns (Leave empty to use all except target)", all_cols)
    
    st.subheader("Preprocessing & Hyperparameters")
    col4, col5, col6 = st.columns(3)
    with col4:
        missing_strat = st.selectbox("Missing Value Strategy (Numeric)", ["mean", "median"])
    with col5:
        scale_strat = st.selectbox("Scaling Strategy (Numeric)", ["standard", "minmax", "none"])
    with col6:
        test_size = st.slider("Test Size (Supervised)", 0.1, 0.5, 0.2)
        
    n_clusters = 3
    if task_type == "clustering":
        n_clusters = st.number_input("Number of Clusters (KMeans)", min_value=2, max_value=20, value=3)
        
    submit = st.form_submit_button("Run Experiment")
    
if submit:
    if task_type in ["classification", "regression"] and not target_col:
        st.error("Target column is required for supervised tasks.")
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
        
        with st.spinner("Training model..."):
            result = train_experiment(payload)
            if result and "id" in result:
                st.success(f"Experiment '{result['name']}' saved successfully!")
                
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
                    c4.metric("R2 Score", f"{metrics.get('r2', 0):.4f}")
                    
                elif task_type == "clustering":
                    c1, c2 = st.columns(2)
                    c1.metric("Inertia", f"{metrics.get('inertia', 0):.4f}")
                    if "silhouette_score" in metrics:
                        c2.metric("Silhouette Score", f"{metrics['silhouette_score']:.4f}")
                        
                if "feature_importance" in metrics and metrics["feature_importance"]:
                    st.subheader("Top Features")
                    fi = metrics["feature_importance"]
                    df_fi = pd.DataFrame(fi)
                    fig = px.bar(df_fi, x="importance", y="feature", orientation="h", title="Feature Importance / Coefficients")
                    fig.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Training failed. Please check your configuration.")
