from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TrainExperimentRequest(BaseModel):
    dataset_id: int
    name: str
    task_type: str
    target_column: Optional[str] = None
    feature_columns: Optional[List[str]] = None
    model_type: str
    missing_strategy: str = "mean"
    categorical_encoding: str = "onehot"
    scaling_strategy: str = "standard"
    test_size: float = 0.2
    random_state: int = 42
    n_clusters: Optional[int] = 3

class ExperimentResponse(BaseModel):
    id: int
    dataset_id: int
    name: str
    task_type: str
    target_column: Optional[str]
    model_type: str
    feature_columns: List[str]
    preprocessing_config: Dict[str, Any]
    metrics_json: Dict[str, Any]
    model_filepath: str
    created_at: datetime

    class Config:
        from_attributes = True

class ExperimentListItem(BaseModel):
    id: int
    dataset_id: int
    name: str
    task_type: str
    model_type: str
    created_at: datetime

    class Config:
        from_attributes = True
