from fastapi import APIRouter
from app.core.model_registry import model_registry

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}

@router.get("/health/models")
def model_health_check():
    """
    Checks if models are actually loaded and ready.
    """
    return {
        "cnn_rnn": "loaded" if model_registry.cnn_rnn_model else "not_loaded",
        "vit": "loaded" if model_registry.vit_model else "not_loaded",
        "last_reload": "2025-01-12T10:23:00Z" # Mocked for now, implies registry tracking
    }
