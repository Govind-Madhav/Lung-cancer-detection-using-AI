"""
Patient Schemas - Privacy-Safe Design

No PHI (Personal Health Information) stored.
Uses external_ref for dataset ID mapping (e.g., NLST).
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PatientBase(BaseModel):
    """Base patient schema - privacy-safe"""
    external_ref: str  # Dataset ID, not patient name


class PatientCreate(PatientBase):
    """Schema for creating new patient"""
    pass


class Patient(PatientBase):
    """Full patient schema with database fields"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PatientWithPredictions(Patient):
    """Patient with their prediction history"""
    predictions: List['PredictionSummary'] = []
    
    class Config:
        from_attributes = True


# Prevent circular import
from app.schemas.prediction import PredictionSummary
PatientWithPredictions.model_rebuild()

