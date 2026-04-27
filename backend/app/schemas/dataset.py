from pydantic import BaseModel
from datetime import datetime

class DatasetCreate(BaseModel):
    name: str
    filename: str
    row_count: int

class Dataset(DatasetCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
