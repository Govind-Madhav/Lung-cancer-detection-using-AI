"""
CRUD Operations for Medical-Grade Database Schema

All operations follow medical-grade principles:
- Privacy-safe (no PHI)
- Audit-ready (automatic logging)
- Explicit error handling
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from datetime import datetime, timedelta

from app.db import models
from app.schemas import patient as patient_schema
from app.schemas import prediction as prediction_schema


# ============================================================================
# PATIENT OPERATIONS
# ============================================================================

def get_patient_by_id(db: Session, patient_id: int) -> Optional[models.Patient]:
    """Get patient by internal ID"""
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()


def get_patient_by_external_ref(db: Session, external_ref: str) -> Optional[models.Patient]:
    """Get patient by external reference (dataset ID)"""
    return db.query(models.Patient).filter(models.Patient.external_ref == external_ref).first()


def get_or_create_patient(db: Session, external_ref: str) -> models.Patient:
    """
    Get existing patient or create new one
    
    Uses external_ref for privacy-safe patient tracking
    """
    patient = get_patient_by_external_ref(db, external_ref)
    
    if not patient:
        patient = models.Patient(external_ref=external_ref)
        db.add(patient)
        db.commit()
        db.refresh(patient)
    
    return patient


def list_patients(db: Session, skip: int = 0, limit: int = 100) -> List[models.Patient]:
    """List all patients with pagination"""
    return db.query(models.Patient).offset(skip).limit(limit).all()


# ============================================================================
# MODEL REGISTRY OPERATIONS
# ============================================================================

def get_model_by_id(db: Session, model_id: int) -> Optional[models.Model]:
    """Get model by ID"""
    return db.query(models.Model).filter(models.Model.id == model_id).first()


def get_model_by_name_version(
    db: Session, 
    model_name: str, 
    model_version: str
) -> Optional[models.Model]:
    """Get model by name and version"""
    return db.query(models.Model).filter(
        models.Model.model_name == model_name,
        models.Model.model_version == model_version
    ).first()


def list_models(db: Session) -> List[models.Model]:
    """List all registered models"""
    return db.query(models.Model).all()


def get_active_model(db: Session, model_type: models.ModelType) -> Optional[models.Model]:
    """
    Get the most recently created model of a given type
    (Assumes newest = active)
    """
    return db.query(models.Model).filter(
        models.Model.model_type == model_type
    ).order_by(models.Model.created_at.desc()).first()


# ============================================================================
# PREDICTION OPERATIONS
# ============================================================================

def create_prediction(
    db: Session,
    patient_id: int,
    model_id: int,
    prediction_status: models.PredictionStatus,
    risk_level: models.RiskLevel,
    inference_time_ms: int,
    binary_result: Optional[models.BinaryResult] = None,
    binary_confidence: Optional[float] = None,
    stage_result: Optional[models.StageResult] = None,
    stage_confidence: Optional[float] = None,
) -> models.Prediction:
    """
    Create a new prediction record (append-only)
    
    This is the core medical record creation function.
    ALL predictions must go through this to ensure audit compliance.
    """
    prediction = models.Prediction(
        patient_id=patient_id,
        model_id=model_id,
        prediction_status=prediction_status,
        binary_result=binary_result,
        binary_confidence=binary_confidence,
        stage_result=stage_result,
        stage_confidence=stage_confidence,
        risk_level=risk_level,
        inference_time_ms=inference_time_ms,
    )
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    
    # Create audit log
    create_audit_log(
        db=db,
        event_type=models.AuditEventType.PREDICTION_CREATED,
        reference_id=prediction.id,
        reference_type=models.ReferenceType.PREDICTION,
        message=f"Prediction created: {risk_level.value} risk"
    )
    
    return prediction


def get_prediction_by_id(db: Session, prediction_id: int) -> Optional[models.Prediction]:
    """Get prediction by ID"""
    return db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()


def list_predictions_by_patient(
    db: Session, 
    patient_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[models.Prediction]:
    """List all predictions for a patient"""
    return db.query(models.Prediction).filter(
        models.Prediction.patient_id == patient_id
    ).order_by(models.Prediction.created_at.desc()).offset(skip).limit(limit).all()


def list_all_predictions(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[models.Prediction]:
    """List all predictions with pagination"""
    return db.query(models.Prediction).order_by(
        models.Prediction.created_at.desc()
    ).offset(skip).limit(limit).all()


def get_predictions_count(db: Session) -> int:
    """Get total number of predictions"""
    return db.query(models.Prediction).count()


def get_predictions_by_risk_level(
    db: Session, 
    risk_level: models.RiskLevel
) -> List[models.Prediction]:
    """Get all predictions with specific risk level"""
    return db.query(models.Prediction).filter(
        models.Prediction.risk_level == risk_level
    ).all()


# ============================================================================
# EXPLAINABILITY ARTIFACT OPERATIONS
# ============================================================================

def create_explainability_artifact(
    db: Session,
    prediction_id: int,
    artifact_type: models.ArtifactType,
    artifact_ref: str,
    expires_in_hours: int = 24
) -> models.ExplainabilityArtifact:
    """
    Create explainability artifact with auto-expiry
    
    Default expiry: 24 hours (configurable)
    """
    expires_at = datetime.utcnow() + timedelta(hours=expires_in_hours)
    
    artifact = models.ExplainabilityArtifact(
        prediction_id=prediction_id,
        artifact_type=artifact_type,
        artifact_ref=artifact_ref,
        expires_at=expires_at
    )
    
    db.add(artifact)
    db.commit()
    db.refresh(artifact)
    
    return artifact


def get_explainability_artifacts(
    db: Session,
    prediction_id: int
) -> List[models.ExplainabilityArtifact]:
    """Get all artifacts for a prediction"""
    return db.query(models.ExplainabilityArtifact).filter(
        models.ExplainabilityArtifact.prediction_id == prediction_id
    ).all()


def delete_expired_artifacts(db: Session) -> int:
    """
    Delete expired explainability artifacts
    
    Returns: Number of deleted artifacts
    """
    now = datetime.utcnow()
    expired = db.query(models.ExplainabilityArtifact).filter(
        models.ExplainabilityArtifact.expires_at < now
    ).all()
    
    count = len(expired)
    
    for artifact in expired:
        db.delete(artifact)
    
    db.commit()
    
    return count


# ============================================================================
# AUDIT LOG OPERATIONS
# ============================================================================

def create_audit_log(
    db: Session,
    event_type: models.AuditEventType,
    reference_id: Optional[int] = None,
    reference_type: Optional[models.ReferenceType] = None,
    message: Optional[str] = None
) -> models.AuditLog:
    """Create audit log entry"""
    audit_log = models.AuditLog(
        event_type=event_type,
        reference_id=reference_id,
        reference_type=reference_type,
        message=message
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)
    
    return audit_log


def list_audit_logs(
    db: Session,
    event_type: Optional[models.AuditEventType] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.AuditLog]:
    """List audit logs with optional filtering by event type"""
    query = db.query(models.AuditLog)
    
    if event_type:
        query = query.filter(models.AuditLog.event_type == event_type)
    
    return query.order_by(models.AuditLog.created_at.desc()).offset(skip).limit(limit).all()


# ============================================================================
# STATISTICS OPERATIONS
# ============================================================================

def get_prediction_statistics(db: Session) -> dict:
    """
    Get comprehensive prediction statistics
    
    Returns counts by risk level, status, and model
    """
    total = db.query(models.Prediction).count()
    
    # Risk level breakdown
    risk_stats = {}
    for risk_level in models.RiskLevel:
        count = db.query(models.Prediction).filter(
            models.Prediction.risk_level == risk_level
        ).count()
        risk_stats[risk_level.value] = count
    
    # Status breakdown
    status_stats = {}
    for status in models.PredictionStatus:
        count = db.query(models.Prediction).filter(
            models.Prediction.prediction_status == status
        ).count()
        status_stats[status.value] = count
    
    return {
        "total": total,
        "by_risk_level": risk_stats,
        "by_status": status_stats
    }
