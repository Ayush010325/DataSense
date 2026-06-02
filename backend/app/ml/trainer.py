import os
import uuid
import joblib
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score, silhouette_score
)

from app.schemas.experiment import TrainExperimentRequest

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage", "models")

def build_preprocessor(df: pd.DataFrame, feature_columns: list, missing_strategy: str, categorical_encoding: str, scaling_strategy: str):
    numeric_cols = []
    categorical_cols = []

    for col in feature_columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)
        else:
            categorical_cols.append(col)

    numeric_transformer_steps = []
    if missing_strategy in ["mean", "median"]:
        numeric_transformer_steps.append(("imputer", SimpleImputer(strategy=missing_strategy)))
    else:
        numeric_transformer_steps.append(("imputer", SimpleImputer(strategy="mean")))

    if scaling_strategy == "standard":
        numeric_transformer_steps.append(("scaler", StandardScaler()))
    elif scaling_strategy == "minmax":
        numeric_transformer_steps.append(("scaler", MinMaxScaler()))

    numeric_transformer = Pipeline(steps=numeric_transformer_steps)

    categorical_transformer_steps = [
        ("imputer", SimpleImputer(strategy="most_frequent"))
    ]
    if categorical_encoding == "onehot":
        categorical_transformer_steps.append(("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)))

    categorical_transformer = Pipeline(steps=categorical_transformer_steps)

    transformers = []
    if numeric_cols:
        transformers.append(("num", numeric_transformer, numeric_cols))
    if categorical_cols:
        transformers.append(("cat", categorical_transformer, categorical_cols))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")
    return preprocessor, numeric_cols, categorical_cols

def build_model(task_type: str, model_type: str, random_state: int, n_clusters: int):
    if task_type == "classification":
        if model_type == "logistic_regression":
            return LogisticRegression(random_state=random_state, max_iter=1000)
        elif model_type == "decision_tree":
            return DecisionTreeClassifier(random_state=random_state)
        elif model_type == "random_forest":
            return RandomForestClassifier(random_state=random_state)
    elif task_type == "regression":
        if model_type == "linear_regression":
            return LinearRegression()
        elif model_type == "decision_tree":
            return DecisionTreeRegressor(random_state=random_state)
        elif model_type == "random_forest":
            return RandomForestRegressor(random_state=random_state)
    elif task_type == "clustering":
        if model_type == "kmeans":
            return KMeans(n_clusters=n_clusters, random_state=random_state)

    raise ValueError(f"Unsupported model type '{model_type}' for task '{task_type}'")

def extract_feature_importance(estimator, preprocessor, numeric_cols, categorical_cols):
    importances = None
    if hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        importances = np.abs(estimator.coef_[0]) if estimator.coef_.ndim > 1 else np.abs(estimator.coef_)

    if importances is None:
        return []

    feature_names = list(numeric_cols)
    try:
        if categorical_cols and hasattr(preprocessor, "named_transformers_"):
            if "cat" in preprocessor.named_transformers_:
                cat_pipe = preprocessor.named_transformers_["cat"]
                if "encoder" in cat_pipe.named_steps:
                    encoder = cat_pipe.named_steps["encoder"]
                    cat_names = encoder.get_feature_names_out(categorical_cols)
                    feature_names.extend(cat_names)
    except Exception:
        pass

    if len(feature_names) != len(importances):
        feature_names = [f"Feature {i}" for i in range(len(importances))]

    sorted_idx = np.argsort(importances)[::-1][:20]
    result = [{"feature": feature_names[i], "importance": float(importances[i])} for i in sorted_idx]
    return result

def train_experiment_pipeline(request: TrainExperimentRequest, file_path: str) -> dict:
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    features = request.feature_columns
    if not features:
        features = df.columns.tolist()
        if request.target_column in features:
            features.remove(request.target_column)

    if request.target_column and request.target_column in features:
        features.remove(request.target_column)

    if not features:
        raise ValueError("No feature columns available for training.")

    preprocessor, num_cols, cat_cols = build_preprocessor(
        df, features, request.missing_strategy, request.categorical_encoding, request.scaling_strategy
    )

    model = build_model(request.task_type, request.model_type, request.random_state, request.n_clusters)

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    metrics = {}

    if request.task_type in ["classification", "regression"]:
        if not request.target_column:
            raise ValueError("Target column is required for supervised tasks.")
        if request.target_column not in df.columns:
            raise ValueError(f"Target column '{request.target_column}' not found.")

        df_clean = df.dropna(subset=[request.target_column])
        X = df_clean[features]
        y = df_clean[request.target_column]

        if request.task_type == "classification" and pd.api.types.is_numeric_dtype(y) and y.nunique() > 20:
            raise ValueError("Target has too many unique numeric values for classification.")
        if request.task_type == "regression" and not pd.api.types.is_numeric_dtype(y):
            raise ValueError("Regression target must be numeric.")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=request.test_size, random_state=request.random_state)

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        if request.task_type == "classification":
            metrics["accuracy"] = float(accuracy_score(y_test, y_pred))
            metrics["precision"] = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
            metrics["recall"] = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
            metrics["f1"] = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))
            metrics["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()
            try:
                y_proba = pipeline.predict_proba(X_test)
                if len(np.unique(y_test)) == 2:
                    metrics["roc_auc"] = float(roc_auc_score(y_test, y_proba[:, 1]))
            except:
                pass

        elif request.task_type == "regression":
            metrics["mae"] = float(mean_absolute_error(y_test, y_pred))
            metrics["mse"] = float(mean_squared_error(y_test, y_pred))
            metrics["rmse"] = float(np.sqrt(metrics["mse"]))
            metrics["r2"] = float(r2_score(y_test, y_pred))

        metrics["feature_importance"] = extract_feature_importance(model, preprocessor, num_cols, cat_cols)

    elif request.task_type == "clustering":
        X = df[features]
        pipeline.fit(X)
        labels = pipeline.predict(X)
        metrics["inertia"] = float(model.inertia_)
        unique_labels, counts = np.unique(labels, return_counts=True)
        metrics["cluster_counts"] = {str(k): int(v) for k, v in zip(unique_labels, counts)}
        if len(X) <= 10000 and len(unique_labels) > 1:
            try:
                transformed_X = preprocessor.transform(X)
                metrics["silhouette_score"] = float(silhouette_score(transformed_X, labels))
            except:
                pass

    os.makedirs(STORAGE_DIR, exist_ok=True)
    filename = f"model_{uuid.uuid4().hex}.joblib"
    filepath = os.path.join(STORAGE_DIR, filename)
    joblib.dump(pipeline, filepath)

    return {
        "task_type": request.task_type,
        "model_type": request.model_type,
        "target_column": request.target_column,
        "feature_columns": features,
        "preprocessing_config": {
            "missing_strategy": request.missing_strategy,
            "categorical_encoding": request.categorical_encoding,
            "scaling_strategy": request.scaling_strategy
        },
        "metrics_json": metrics,
        "model_filepath": filepath
    }
