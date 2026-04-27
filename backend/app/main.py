from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.datasets import router as datasets_router
from app.api.analysis import router as analysis_router
from app.api.charts import router as charts_router
from app.api.experiments import router as experiments_router
from app.api.predictions import router as predictions_router

app = FastAPI(title="DataSense Lab")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(datasets_router, prefix="/api/v1/datasets", tags=["datasets"])
app.include_router(analysis_router, prefix="/api/v1", tags=["analysis"])
app.include_router(charts_router, prefix="/api/v1/charts", tags=["charts"])
app.include_router(experiments_router, prefix="/api/v1/experiments", tags=["experiments"])
app.include_router(predictions_router, prefix="/api/v1/experiments", tags=["predictions"])
