"""
Prediction Schemas - Medical-Grade Design

Uses ENUMs from database models for type safety and consistency.
Explicit uncertainty states and confidence tracking.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


# Import ENUMs from database models for consistency
from app.db.models import (
    PredictionStatus,
    BinaryResult,
    StageResult,
    RiskLevel,
    ArtifactType
)


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class PredictionCreate(BaseModel):
    """
    Schema for creating a prediction
    
    This is used by the API endpoint to receive prediction data
    """
    patient_id: int
    model_id: int
    
    prediction_status: PredictionStatus
    risk_level: RiskLevel
    inference_time_ms: int
    
    # Binary classification (optional)
    binary_result: Optional[BinaryResult] = None
    binary_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    # Stage/risk classification (optional)
    stage_result: Optional[StageResult] = None
    stage_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    
    class Config:
        use_enum_values = True


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class PredictionSummary(BaseModel):
    """
    Summary view of a prediction (for lists)
    """
    id: int
    prediction_status: PredictionStatus
    risk_level: RiskLevel
    binary_result: Optional[BinaryResult] = None
    binary_confidence: Optional[Decimal] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class Prediction(BaseModel):
    """
    Full prediction response schema
    """
    id: int
    patient_id: int
    model_id: int
    
    # Status and results
    prediction_status: PredictionStatus
    binary_result: Optional[BinaryResult] = None
    binary_confidence: Optional[Decimal] = None
    stage_result: Optional[StageResult] = None
    stage_confidence: Optional[Decimal] = None
    risk_level: RiskLevel
    
    # Performance metrics
    inference_time_ms: int
    
    # Metadata
    created_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


class PredictionWithExplainability(Prediction):
    """
    Prediction with explainability artifacts
    """
    explainability_artifacts: list['ExplainabilityArtifactResponse'] = []
    
    class Config:
        from_attributes = True
        use_enum_values = True


# ============================================================================
# EXPLAINABILITY SCHEMAS
# ============================================================================

class ExplainabilityArtifactCreate(BaseModel):
    """Schema for creating explainability artifact"""
    prediction_id: int
    artifact_type: ArtifactType
    artifact_ref: str
    expires_in_hours: int = 24


class ExplainabilityArtifactResponse(BaseModel):
    """Response schema for explainability artifact"""
    id: int
    prediction_id: int
    artifact_type: ArtifactType
    artifact_ref: str
    expires_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
        use_enum_values = True


# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class PredictionStatistics(BaseModel):
    """Statistics about predictions"""
    total: int
    by_risk_level: dict[str, int]
    by_status: dict[str, int]


# Rebuild model to handle forward references
PredictionWithExplainability.model_rebuild()

