from pydantic import BaseModel
from typing import Any, Dict, List, Optional

class PredictRequest(BaseModel):
    input_data: Dict[str, Any]

class PredictResponse(BaseModel):
    prediction: Any
    probability: Optional[List[float]] = None
    feature_contributions: Optional[List[Dict[str, Any]]] = None
