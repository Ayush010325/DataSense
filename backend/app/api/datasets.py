import os
import uuid
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import Dataset
from app.services.dataset_service import dataset_service__create_or_update

router = APIRouter()

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data_storage")

@router.post("/upload", response_model=Dataset)
async def upload_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files are allowed")

    os.makedirs(STORAGE_DIR, exist_ok=True)
    
    unique_filename = f"dataset_{uuid.uuid4().hex}_{file.filename}"
    file_path = os.path.join(STORAGE_DIR, unique_filename)
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        row_count = df.shape[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    dataset_record = dataset_service__create_or_update(
        db=db,
        name=name,
        filename=file.filename,
        file_path=file_path,
        row_count=row_count
    )
    
    return dataset_record
