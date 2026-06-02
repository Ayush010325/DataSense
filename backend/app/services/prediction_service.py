import os
import joblib
import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.experiment import get_experiment
from app.schemas.prediction import PredictRequest

def make_prediction(db: Session, experiment_id: int, request: PredictRequest) -> dict:
    experiment = get_experiment(db, experiment_id)
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    model_path = experiment.model_filepath
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Model artifact missing on disk")

    try:
        pipeline = joblib.load(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")

    expected_features = experiment.feature_columns

    df = pd.DataFrame([request.input_data])

    for col in expected_features:
        if col not in df.columns:
            df[col] = None

    df = df[expected_features]

    try:
        prediction = pipeline.predict(df)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

    probability = None
    if experiment.task_type == "classification" and hasattr(pipeline, "predict_proba"):
        try:
            prob = pipeline.predict_proba(df)[0]
            probability = prob.tolist()
        except:
            pass

    feature_contributions = None
    metrics = experiment.metrics_json or {}
    feature_importance = metrics.get("feature_importance", [])
    if feature_importance:
        feature_contributions = feature_importance

    if pd.isna(prediction):
        pred_val = None
    elif isinstance(prediction, (int, float, str, bool)):
        pred_val = prediction
    else:
        try:
            pred_val = prediction.item()
        except:
            pred_val = str(prediction)

    return {
        "prediction": pred_val,
        "probability": probability,
        "feature_contributions": feature_contributions
    }
