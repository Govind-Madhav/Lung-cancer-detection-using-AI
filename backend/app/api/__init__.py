from fastapi import APIRouter
from app.api import health, predict, patients, metrics

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(predict.router, tags=["predict"])
api_router.include_router(patients.router, tags=["patients"])
api_router.include_router(metrics.router, tags=["metrics"])
