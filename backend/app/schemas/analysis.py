from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class DatasetShape(BaseModel):
    row_count: int
    column_count: int

class MissingSummary(BaseModel):
    total_missing_cells: int
    missing_by_column: Dict[str, int]

class DuplicatesSummary(BaseModel):
    duplicate_row_count: int

class AnalysisResponse(BaseModel):
    dataset_shape: DatasetShape
    missing_summary: MissingSummary
    duplicates_summary: DuplicatesSummary
    column_types: Dict[str, str]
    numeric_summary: Dict[str, Dict[str, Any]]
    categorical_summary: Dict[str, Dict[str, Any]]
    text_summary: Dict[str, Dict[str, Any]]
    datetime_summary: Dict[str, Dict[str, Any]]
    column_metadata_rows: List[Dict[str, Any]] = []
