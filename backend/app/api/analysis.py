from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.analysis import AnalysisResponse
from app.schemas.insight import Insight
from app.services.analysis_service import get_dataset_analysis, get_dataset_insights
from app.crud.dataset import get_datasets
from app.schemas.dataset import Dataset

router = APIRouter()

@router.get("/datasets/{dataset_id}/analysis", response_model=AnalysisResponse)
def read_dataset_analysis(dataset_id: int, db: Session = Depends(get_db)):
    analysis = get_dataset_analysis(db, dataset_id)
    return analysis

@router.get("/datasets/{dataset_id}/insights", response_model=List[Insight])
def read_dataset_insights(dataset_id: int, db: Session = Depends(get_db)):
    insights = get_dataset_insights(db, dataset_id)
    return insights

@router.get("/datasets", response_model=List[Dataset])
def list_datasets(db: Session = Depends(get_db)):
    return get_datasets(db)
