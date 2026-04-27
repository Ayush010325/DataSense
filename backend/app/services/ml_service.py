from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.dataset import get_dataset
from app.crud.experiment import create_experiment, get_experiment, get_experiments_for_dataset
from app.schemas.experiment import TrainExperimentRequest
from app.ml.trainer import train_experiment_pipeline

def train_and_save_experiment(db: Session, request: TrainExperimentRequest) -> dict:
    dataset = get_dataset(db, request.dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    try:
        result = train_experiment_pipeline(request, dataset.file_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")
        
    exp_data = {
        "dataset_id": dataset.id,
        "name": request.name,
        "task_type": result["task_type"],
        "target_column": result["target_column"],
        "model_type": result["model_type"],
        "feature_columns": result["feature_columns"],
        "preprocessing_config": result["preprocessing_config"],
        "metrics_json": result["metrics_json"],
        "model_filepath": result["model_filepath"]
    }
    
    return create_experiment(db, exp_data)

def get_experiment_details(db: Session, experiment_id: int):
    exp = get_experiment(db, experiment_id)
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

def get_dataset_experiments_service(db: Session, dataset_id: int):
    return get_experiments_for_dataset(db, dataset_id)
