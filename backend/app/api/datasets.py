from io import BytesIO
import pandas as pd
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.dataset import Dataset
from app.services.dataset_service import dataset_service__create_or_update
from app.ml.analyzer import analyze_dataset
from app.crud.column_metadata import create_column_metadata_bulk

router = APIRouter()


@router.post("/upload", response_model=Dataset)
async def upload_dataset(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Only CSV or XLSX files are allowed")

    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(BytesIO(content))
        else:
            df = pd.read_excel(BytesIO(content))
        row_count, col_count = df.shape
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    dataset_record = dataset_service__create_or_update(
        db=db,
        name=name,
        filename=file.filename,
        row_count=row_count,
        col_count=col_count,
        file_data=content,
        file_size=len(content),
        content_type=file.content_type
    )

    try:
        analysis = analyze_dataset(df)
        create_column_metadata_bulk(db, dataset_record.id, analysis["column_metadata_rows"])
    except Exception:
        pass

    return dataset_record
