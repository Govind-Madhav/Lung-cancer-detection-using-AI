"""
Database package - Medical-grade schema for Lung Cancer Detection

This package contains:
- models.py: SQLAlchemy ORM models with privacy-safe design
- session.py: Database session management
- crud.py: CRUD operations
- init_db.py: Database initialization and seeding
"""

from app.db.models import (
    Patient,
    Model,
    Prediction,
    ExplainabilityArtifact,
    AuditLog,
    # Enums
    PredictionStatus,
    BinaryResult,
    StageResult,
    RiskLevel,
    ModelType,
    ExplainabilityType,
    ArtifactType,
    AuditEventType,
    ReferenceType,
)
from app.db.session import Base, engine, SessionLocal, get_db
from app.db.init_db import init_db, create_tables, seed_initial_models

__all__ = [
    # Models
    "Patient",
    "Model",
    "Prediction",
    "ExplainabilityArtifact",
    "AuditLog",
    # Enums
    "PredictionStatus",
    "BinaryResult",
    "StageResult",
    "RiskLevel",
    "ModelType",
    "ExplainabilityType",
    "ArtifactType",
    "AuditEventType",
    "ReferenceType",
    # Session
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    # Init
    "init_db",
    "create_tables",
    "seed_initial_models",
]
