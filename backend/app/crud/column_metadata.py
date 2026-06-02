from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import List, Dict, Any
from app.models.column_metadata import ColumnMetadata

def create_column_metadata_bulk(db: Session, dataset_id: int, rows: List[Dict[str, Any]]):
    stmt = delete(ColumnMetadata).where(ColumnMetadata.dataset_id == dataset_id)
    db.execute(stmt)

    db_rows = []
    for row in rows:
        metadata = ColumnMetadata(
            dataset_id=dataset_id,
            column_name=row["column_name"],
            data_type=row["data_type"],
            missing_count=row["missing_count"],
            missing_ratio=row["missing_ratio"],
            unique_count=row["unique_count"],
            is_nullable=row["is_nullable"]
        )
        db_rows.append(metadata)
    db.add_all(db_rows)
    db.commit()

def get_columns_for_dataset(db: Session, dataset_id: int) -> List[ColumnMetadata]:
    stmt = select(ColumnMetadata).where(ColumnMetadata.dataset_id == dataset_id)
    return list(db.scalars(stmt).all())
