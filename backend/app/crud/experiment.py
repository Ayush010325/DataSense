from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.experiment import Experiment

def create_experiment(db: Session, exp_data: dict) -> Experiment:
    db_exp = Experiment(**exp_data)
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp

def get_experiment(db: Session, experiment_id: int):
    stmt = select(Experiment).where(Experiment.id == experiment_id)
    return db.scalars(stmt).first()

def get_experiments_for_dataset(db: Session, dataset_id: int):
    stmt = select(Experiment).where(Experiment.dataset_id == dataset_id).order_by(Experiment.created_at.desc())
    return list(db.scalars(stmt).all())

def get_recent_experiments(db: Session, limit: int = 20):
    stmt = select(Experiment).order_by(Experiment.created_at.desc()).limit(limit)
    return list(db.scalars(stmt).all())
