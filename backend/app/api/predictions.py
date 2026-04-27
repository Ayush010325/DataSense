from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.prediction import PredictRequest, PredictResponse
from app.services.prediction_service import make_prediction

router = APIRouter()

@router.post("/{experiment_id}/predict", response_model=PredictResponse)
def api_predict(experiment_id: int, req: PredictRequest, db: Session = Depends(get_db)):
    return make_prediction(db, experiment_id, req)
