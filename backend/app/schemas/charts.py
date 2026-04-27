from pydantic import BaseModel
from typing import List, Any

class PlottableColumns(BaseModel):
    numeric: List[str]
    categorical: List[str]
    datetime: List[str]

class ChartRequestSingle(BaseModel):
    dataset_id: int
    column: str

class ChartRequestDouble(BaseModel):
    dataset_id: int
    column_x: str
    column_y: str

class ChartRequestMulti(BaseModel):
    dataset_id: int
    columns: List[str]

class DistributionChartData(BaseModel):
    column_name: str
    values: List[Any]
    type: str

class BoxplotChartData(BaseModel):
    column_name: str
    values: List[float]

class BarplotChartData(BaseModel):
    x_labels: List[str]
    values: List[float]

class HeatmapChartData(BaseModel):
    column_names: List[str]
    data: List[List[float]]

class ScatterChartData(BaseModel):
    column_x: str
    column_y: str
    x: List[float]
    y: List[float]

class PieChartData(BaseModel):
    labels: List[str]
    values: List[int]

class LineChartData(BaseModel):
    x_labels: List[Any]
    values: List[float]
    column_x: str
    column_y: str
