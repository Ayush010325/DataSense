from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.dataset import get_dataset
from app.crud.column_metadata import create_column_metadata_bulk
from app.ml.analyzer import load_dataset_record, analyze_dataset
from app.ml.insights import generate_insights
from typing import Dict, Any, List

def get_dataset_analysis(db: Session, dataset_id: int) -> Dict[str, Any]:
    dataset = get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    try:
        df = load_dataset_record(dataset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dataset: {str(e)}")

    analysis = analyze_dataset(df)

    create_column_metadata_bulk(db, dataset_id, analysis["column_metadata_rows"])

    return analysis

def get_dataset_insights(db: Session, dataset_id: int) -> List[Dict[str, str]]:
    analysis = get_dataset_analysis(db, dataset_id)
    insights = generate_insights(analysis)
    return insights
