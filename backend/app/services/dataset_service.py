from sqlalchemy.orm import Session
from app.crud.dataset import create_dataset
from app.models.dataset import Dataset

def dataset_service__create_or_update(db: Session, name: str, filename: str, file_path: str, row_count: int) -> Dataset:
    # Skeleton service function calling CRUD
    return create_dataset(
        db=db,
        name=name,
        filename=filename,
        file_path=file_path,
        row_count=row_count
    )
