from sqlalchemy.orm import Session
from app.models.dataset import Dataset
from app.schemas.dataset import DatasetCreate

def get_dataset(db: Session, dataset_id: int):
    return db.query(Dataset).filter(Dataset.id == dataset_id).first()

def get_datasets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Dataset).order_by(Dataset.created_at.desc()).offset(skip).limit(limit).all()

def create_dataset(db: Session, dataset: DatasetCreate):
    db_dataset = Dataset(
        name=dataset.name,
        filename=dataset.filename,
        file_path=dataset.file_path,
        row_count=dataset.row_count,
        col_count=dataset.col_count
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset
