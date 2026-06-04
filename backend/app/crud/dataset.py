from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from app.models.dataset import Dataset

def create_dataset(
    db: Session,
    name: str,
    filename: str,
    row_count: int,
    col_count: int = 0,
    file_path: str | None = None,
    file_data: bytes | None = None,
    file_size: int | None = None,
    content_type: str | None = None
) -> Dataset:
    db_dataset = Dataset(
        name=name,
        filename=filename,
        file_path=file_path,
        file_data=file_data,
        file_size=file_size,
        content_type=content_type,
        row_count=row_count,
        col_count=col_count
    )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_dataset(db: Session, dataset_id: int) -> Optional[Dataset]:
    stmt = select(Dataset).where(Dataset.id == dataset_id)
    return db.scalars(stmt).first()

def get_datasets(db: Session, skip: int = 0, limit: int = 100) -> List[Dataset]:
    stmt = select(Dataset).order_by(Dataset.created_at.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())
