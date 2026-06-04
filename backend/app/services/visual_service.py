from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.dataset import get_dataset
from app.ml.plotter import (
    get_plottable_columns,
    get_chart_data_for_distribution,
    get_chart_data_for_boxplot,
    get_chart_data_for_barplot,
    get_chart_data_for_heatmap,
    get_chart_data_for_scatter,
    get_chart_data_for_pie,
    get_chart_data_for_line
)

from app.services.analysis_service import get_dataset_analysis
from app.crud.column_metadata import get_columns_for_dataset

def _validate_dataset(db: Session, dataset_id: int):
    if not get_dataset(db, dataset_id):
        raise HTTPException(status_code=404, detail="Dataset not found")

def get_plottable_columns_service(db: Session, dataset_id: int) -> dict:
    _validate_dataset(db, dataset_id)
    cols = get_columns_for_dataset(db, dataset_id)
    if not cols:
        # Trigger analysis to populate column metadata
        get_dataset_analysis(db, dataset_id)
    return get_plottable_columns(db, dataset_id)

def get_histogram_data(db: Session, dataset_id: int, column: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_distribution(dataset_id, db, column)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_boxplot_data(db: Session, dataset_id: int, column: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_boxplot(dataset_id, db, column)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_barplot_data(db: Session, dataset_id: int, column_x: str, column_y: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_barplot(dataset_id, db, column_x, column_y)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_heatmap_data(db: Session, dataset_id: int, columns: list) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_heatmap(dataset_id, db, columns)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_scatter_data(db: Session, dataset_id: int, column_x: str, column_y: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_scatter(dataset_id, db, column_x, column_y)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_pie_data(db: Session, dataset_id: int, column: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_pie(dataset_id, db, column)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

def get_line_data(db: Session, dataset_id: int, column_x: str, column_y: str) -> dict:
    _validate_dataset(db, dataset_id)
    try:
        return get_chart_data_for_line(dataset_id, db, column_x, column_y)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
