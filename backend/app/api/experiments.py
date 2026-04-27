from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.experiment import TrainExperimentRequest, ExperimentResponse, ExperimentListItem
from app.services.ml_service import train_and_save_experiment, get_experiment_details, get_dataset_experiments_service
from app.crud.experiment import get_recent_experiments

router = APIRouter()

@router.post("/train", response_model=ExperimentResponse)
def api_train_experiment(req: TrainExperimentRequest, db: Session = Depends(get_db)):
    return train_and_save_experiment(db, req)

@router.get("/{experiment_id}", response_model=ExperimentResponse)
def api_get_experiment(experiment_id: int, db: Session = Depends(get_db)):
    return get_experiment_details(db, experiment_id)

@router.get("/dataset/{dataset_id}", response_model=List[ExperimentListItem])
def api_get_dataset_experiments(dataset_id: int, db: Session = Depends(get_db)):
    return get_dataset_experiments_service(db, dataset_id)

@router.get("/list/recent", response_model=List[ExperimentListItem])
def api_get_recent_experiments(limit: int = 20, db: Session = Depends(get_db)):
    return get_recent_experiments(db, limit)
