from fastapi import APIRouter
from app.schemas.metrics import Metrics

router = APIRouter()

@router.get("/model-metrics", response_model=Metrics)
def get_metrics():
    # Placeholder for real metrics
    return {"total_predictions": 100, "average_confidence": 0.88}
