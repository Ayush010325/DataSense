import uuid
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.dataset import DatasetResponse, DatasetCreate
from app.crud import crud_dataset
from app.utils.file_handler import save_upload_file

router = APIRouter()

@router.post("/upload", response_model=DatasetResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files are allowed.")
        
    # Generate unique filename to avoid overwrites
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    
    try:
        # Save file to disk
        file_path = save_upload_file(file, unique_filename)
        
        # Read a small chunk to get row/col counts
        # This is a basic preview; deep analysis happens in Phase 3
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
            
        row_count, col_count = df.shape
        
        # Save metadata to database
        dataset_in = DatasetCreate(
            name=name,
            filename=file.filename,
            file_path=file_path,
            row_count=row_count,
            col_count=col_count
        )
        
        dataset = crud_dataset.create_dataset(db=db, dataset=dataset_in)
        return dataset
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/", response_model=List[DatasetResponse])
def list_datasets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    datasets = crud_dataset.get_datasets(db, skip=skip, limit=limit)
    return datasets
