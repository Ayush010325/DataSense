from sqlalchemy.orm import Session
from app.crud.dataset import create_dataset
from app.models.dataset import Dataset

def dataset_service__create_or_update(
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
    return create_dataset(
        db=db,
        name=name,
        filename=filename,
        row_count=row_count,
        col_count=col_count,
        file_path=file_path,
        file_data=file_data,
        file_size=file_size,
        content_type=content_type
    )
