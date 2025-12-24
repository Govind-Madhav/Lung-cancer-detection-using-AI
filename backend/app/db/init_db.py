"""
Database Initialization and Model Seeding

This module:
1. Creates all database tables
2. Seeds initial model records
3. Provides utility functions for database setup
"""

from sqlalchemy.orm import Session
from app.db.session import engine, Base, SessionLocal
from app.db.models import (
    Model, ModelType, ExplainabilityType,
    AuditLog, AuditEventType, ReferenceType
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise


def seed_initial_models(db: Session):
    """
    Seed initial model registry
    
    This ensures that the model registry is populated with
    the current models available in the system.
    """
    models_data = [
        {
            "model_name": "cnn_rnn",
            "model_version": "v1",
            "model_type": ModelType.CNN_RNN,
            "supports_binary": True,
            "supports_stage": True,
            "supports_explainability": True,
            "explainability_type": ExplainabilityType.GRADCAM,
        },
        {
            "model_name": "vit",
            "model_version": "v1",
            "model_type": ModelType.VIT,
            "supports_binary": True,
            "supports_stage": True,
            "supports_explainability": True,
            "explainability_type": ExplainabilityType.ATTENTION,
        },
    ]
    
    try:
        for model_data in models_data:
            # Check if model already exists
            existing_model = db.query(Model).filter(
                Model.model_name == model_data["model_name"],
                Model.model_version == model_data["model_version"]
            ).first()
            
            if not existing_model:
                model = Model(**model_data)
                db.add(model)
                logger.info(f"✅ Seeded model: {model_data['model_name']} {model_data['model_version']}")
                
                # Create audit log for model seeding
                audit_log = AuditLog(
                    event_type=AuditEventType.MODEL_LOADED,
                    reference_type=ReferenceType.MODEL,
                    message=f"Initial model seed: {model_data['model_name']} {model_data['model_version']}"
                )
                db.add(audit_log)
            else:
                logger.info(f"⏭️  Model already exists: {model_data['model_name']} {model_data['model_version']}")
        
        db.commit()
        logger.info("✅ Model seeding completed successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to seed models: {e}")
        raise


def init_db():
    """
    Initialize database:
    1. Create all tables
    2. Seed initial models
    """
    try:
        logger.info("🚀 Starting database initialization...")
        
        # Step 1: Create tables
        create_tables()
        
        # Step 2: Seed models
        db = SessionLocal()
        try:
            seed_initial_models(db)
        finally:
            db.close()
        
        logger.info("✅ Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize database
    init_db()
