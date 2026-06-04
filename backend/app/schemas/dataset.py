from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DatasetCreate(BaseModel):
    name: str
    filename: str
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    content_type: Optional[str] = None
    row_count: Optional[int] = None
    col_count: Optional[int] = None

class Dataset(DatasetCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DatasetResponse(DatasetCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
