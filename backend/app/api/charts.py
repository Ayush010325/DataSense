from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.charts import (
    PlottableColumns, ChartRequestSingle, ChartRequestDouble, ChartRequestMulti,
    DistributionChartData, BoxplotChartData, BarplotChartData, HeatmapChartData, ScatterChartData, PieChartData, LineChartData
)
from app.services.visual_service import (
    get_plottable_columns_service, get_histogram_data, get_boxplot_data,
    get_barplot_data, get_heatmap_data, get_scatter_data, get_pie_data, get_line_data
)

router = APIRouter()

@router.get("/plottable_columns/{dataset_id}", response_model=PlottableColumns)
def api_plottable_columns(dataset_id: int, db: Session = Depends(get_db)):
    return get_plottable_columns_service(db, dataset_id)

@router.post("/histogram", response_model=DistributionChartData)
def api_histogram(req: ChartRequestSingle, db: Session = Depends(get_db)):
    return get_histogram_data(db, req.dataset_id, req.column)

@router.post("/boxplot", response_model=BoxplotChartData)
def api_boxplot(req: ChartRequestSingle, db: Session = Depends(get_db)):
    return get_boxplot_data(db, req.dataset_id, req.column)

@router.post("/barplot", response_model=BarplotChartData)
def api_barplot(req: ChartRequestDouble, db: Session = Depends(get_db)):
    return get_barplot_data(db, req.dataset_id, req.column_x, req.column_y)

@router.post("/heatmap", response_model=HeatmapChartData)
def api_heatmap(req: ChartRequestMulti, db: Session = Depends(get_db)):
    return get_heatmap_data(db, req.dataset_id, req.columns)

@router.post("/scatter", response_model=ScatterChartData)
def api_scatter(req: ChartRequestDouble, db: Session = Depends(get_db)):
    return get_scatter_data(db, req.dataset_id, req.column_x, req.column_y)

@router.post("/pie", response_model=PieChartData)
def api_pie(req: ChartRequestSingle, db: Session = Depends(get_db)):
    return get_pie_data(db, req.dataset_id, req.column)

@router.post("/line", response_model=LineChartData)
def api_line(req: ChartRequestDouble, db: Session = Depends(get_db)):
    return get_line_data(db, req.dataset_id, req.column_x, req.column_y)
