"""
Medical-Grade Prediction Service

Integrates with:
- Inference Engine (CNN-RNN, ViT models)
- Risk Engine (deriving risk from predictions)
- Explainability (Grad-CAM, Attention maps)
- Database (medical-grade schema with audit logging)

This service is the orchestration layer that ensures:
1. Privacy-safe patient handling
2. Model registry compliance
3. Automatic audit logging
4. Explainability artifact management with expiry
5. Proper error handling and uncertainty states
"""

from sqlalchemy.orm import Session
from typing import Optional, Tuple
import time
from datetime import datetime

from app.core.inference_engine import inference_engine
from app.core.risk_engine import risk_engine
from app.core.explainability import gradcam, vit_attention
from app.core.audit_logger import audit_logger
from app.core.exceptions import InferenceError, InvalidImageError
from app.core.logger import logger

from app.db import crud, models
from app.utils import image


class PredictionService:
    """
    Medical-grade prediction orchestration service
    
    Handles the complete prediction lifecycle:
    - Patient lookup/creation
    - Model registry lookup
    - Inference execution with timing
    - Risk assessment
    - Explainability generation
    - Database persistence with audit logging
    """
    
    def run_prediction(
        self,
        db: Session,
        external_ref: str,
        file: bytes,
        model_type: str = "cnn_rnn"
    ) -> Tuple[models.Prediction, Optional[str]]:
        """
        Execute complete prediction pipeline
        
        Args:
            db: Database session
            external_ref: Patient external reference (dataset ID)
            file: Image file bytes
            model_type: Model type to use (cnn_rnn, vit)
            
        Returns:
            Tuple of (Prediction record, explainability artifact path)
        """
        start_time = time.time()
        
        # Initialize result variables
        prediction_status = models.PredictionStatus.SUCCESS
        binary_result = None
        binary_confidence = None
        stage_result = None
        stage_confidence = None
        risk_level = models.RiskLevel.INCONCLUSIVE
        explainability_ref = None
        
        try:
            # ================================================================
            # STEP 1: Patient Lookup/Creation (Privacy-Safe)
            # ================================================================
            patient = crud.get_or_create_patient(db, external_ref)
            logger.info(f"Patient lookup/creation complete: ID {patient.id}")
            
            # ================================================================
            # STEP 2: Model Registry Lookup
            # ================================================================
            model_type_enum = models.ModelType.CNN_RNN if model_type == "cnn_rnn" else models.ModelType.VIT
            model = crud.get_active_model(db, model_type_enum)
            
            if not model:
                logger.error(f"No active model found for type: {model_type}")
                raise InferenceError(f"Model {model_type} not found in registry")
            
            logger.info(f"Using model: {model.model_name} {model.model_version} (ID: {model.id})")
            
            # ================================================================
            # STEP 3: Input Validation
            # ================================================================
            if not image.validate_image_file(file):
                prediction_status = models.PredictionStatus.INPUT_INVALID
                raise InvalidImageError("Invalid image file format")
            
            processed_image = image.preprocess_image(file)
            
            # ================================================================
            # STEP 4: Binary Classification Inference
            # ================================================================
            try:
                binary_prob = inference_engine.predict_binary(processed_image)
                
                # Determine binary result from probability
                if binary_prob >= 0.5:
                    binary_result = models.BinaryResult.MALIGNANT
                else:
                    binary_result = models.BinaryResult.BENIGN
                
                binary_confidence = binary_prob
                logger.info(f"Binary classification: {binary_result.value} (confidence: {binary_confidence:.4f})")
                
            except InferenceError as e:
                logger.error(f"Binary inference failed: {e}")
                prediction_status = models.PredictionStatus.MODEL_ERROR
                
                # Create audit log for failure
                crud.create_audit_log(
                    db=db,
                    event_type=models.AuditEventType.INFERENCE_FAILED,
                    reference_type=models.ReferenceType.MODEL,
                    reference_id=model.id,
                    message=f"Binary inference failed: {str(e)}"
                )
                raise e
            
            # ================================================================
            # STEP 5: Stage/Risk Classification (if model supports it)
            # ================================================================
            if model.supports_stage:
                try:
                    stage_info = risk_engine.calculate_risk(binary_prob)
                    
                    # Map risk_engine output to StageResult
                    if stage_info == "High":
                        stage_result = models.StageResult.HIGH
                        stage_confidence = binary_prob
                    elif stage_info == "Medium":
                        stage_result = models.StageResult.MEDIUM
                        stage_confidence = binary_prob * 0.8  # Adjusted confidence
                    elif stage_info == "Low":
                        stage_result = models.StageResult.LOW
                        stage_confidence = 1.0 - binary_prob
                    
                    logger.info(f"Stage classification: {stage_result.value if stage_result else 'None'}")
                    
                except Exception as e:
                    logger.warning(f"Stage classification failed: {e}")
                    # Continue - partial failure acceptable
            
            # ================================================================
            # STEP 6: Derive Final Risk Level
            # ================================================================
            risk_level = self._derive_risk_level(
                binary_result=binary_result,
                binary_confidence=binary_confidence,
                stage_result=stage_result
            )
            
            # Check for inconclusive results
            if risk_level == models.RiskLevel.INCONCLUSIVE:
                prediction_status = models.PredictionStatus.INCONCLUSIVE
            
            logger.info(f"Final risk level: {risk_level.value}")
            
            # ================================================================
            # STEP 7: Explainability Generation (Best Effort)
            # ================================================================
            if model.supports_explainability:
                try:
                    if model.explainability_type == models.ExplainabilityType.GRADCAM:
                        explainability_ref = gradcam.generate_gradcam(None, processed_image, "target_layer")
                    elif model.explainability_type == models.ExplainabilityType.ATTENTION:
                        explainability_ref = vit_attention.generate_attention_map(None, processed_image)
                    
                    logger.info(f"Explainability artifact generated: {explainability_ref}")
                    
                except Exception as e:
                    logger.warning(f"Explainability generation failed (non-critical): {e}")
                    # Do NOT fail the request if explainability fails
        
        except InvalidImageError:
            # Input validation failure - do not save to database
            logger.error("Invalid input - not saving to database")
            raise
            
        except Exception as e:
            # Unexpected error
            if prediction_status == models.PredictionStatus.SUCCESS:
                prediction_status = models.PredictionStatus.MODEL_ERROR
            logger.error(f"Prediction pipeline failed: {e}")
            raise
        
        finally:
            # ================================================================
            # STEP 8: Calculate Inference Time
            # ================================================================
            inference_time_ms = int((time.time() - start_time) * 1000)
            
            # ================================================================
            # STEP 9: Save to Database (if not invalid input)
            # ================================================================
            if prediction_status != models.PredictionStatus.INPUT_INVALID:
                try:
                    prediction = crud.create_prediction(
                        db=db,
                        patient_id=patient.id,
                        model_id=model.id,
                        prediction_status=prediction_status,
                        risk_level=risk_level,
                        inference_time_ms=inference_time_ms,
                        binary_result=binary_result,
                        binary_confidence=binary_confidence,
                        stage_result=stage_result,
                        stage_confidence=stage_confidence,
                    )
                    
                    logger.info(f"Prediction record created: ID {prediction.id}")
                    
                    # ================================================================
                    # STEP 10: Save Explainability Artifact (if generated)
                    # ================================================================
                    if explainability_ref and model.supports_explainability:
                        artifact_type = (
                            models.ArtifactType.GRADCAM 
                            if model.explainability_type == models.ExplainabilityType.GRADCAM 
                            else models.ArtifactType.ATTENTION
                        )
                        
                        crud.create_explainability_artifact(
                            db=db,
                            prediction_id=prediction.id,
                            artifact_type=artifact_type,
                            artifact_ref=explainability_ref,
                            expires_in_hours=24
                        )
                        
                        logger.info(f"Explainability artifact saved with 24h expiry")
                    
                    return prediction, explainability_ref
                    
                except Exception as db_err:
                    logger.critical(f"Failed to save prediction record: {db_err}")
                    db.rollback()
                    raise
    
    def _derive_risk_level(
        self,
        binary_result: Optional[models.BinaryResult],
        binary_confidence: Optional[float],
        stage_result: Optional[models.StageResult]
    ) -> models.RiskLevel:
        """
        Derive final risk level from classification results
        
        Business logic:
        - If confidence < 0.7, mark as INCONCLUSIVE
        - Otherwise use stage_result if available
        - Fall back to binary result mapping
        """
        # Confidence threshold guard
        CONFIDENCE_THRESHOLD = 0.7
        
        if binary_confidence is None or binary_confidence < CONFIDENCE_THRESHOLD:
            return models.RiskLevel.INCONCLUSIVE
        
        # Use stage result if available
        if stage_result:
            if stage_result == models.StageResult.HIGH:
                return models.RiskLevel.HIGH
            elif stage_result == models.StageResult.MEDIUM:
                return models.RiskLevel.MEDIUM
            elif stage_result == models.StageResult.LOW:
                return models.RiskLevel.LOW
        
        # Fall back to binary result
        if binary_result == models.BinaryResult.MALIGNANT:
            # High confidence malignant → HIGH risk
            if binary_confidence >= 0.85:
                return models.RiskLevel.HIGH
            else:
                return models.RiskLevel.MEDIUM
        elif binary_result == models.BinaryResult.BENIGN:
            return models.RiskLevel.LOW
        
        # Default to inconclusive if we can't determine
        return models.RiskLevel.INCONCLUSIVE
    
    def get_patient_predictions(
        self,
        db: Session,
        external_ref: str,
        limit: int = 100
    ) -> list[models.Prediction]:
        """Get all predictions for a patient by external_ref"""
        patient = crud.get_patient_by_external_ref(db, external_ref)
        if not patient:
            return []
        
        return crud.list_predictions_by_patient(db, patient.id, limit=limit)
    
    def get_prediction_statistics(self, db: Session) -> dict:
        """Get comprehensive prediction statistics"""
        return crud.get_prediction_statistics(db)


# Singleton instance
prediction_service = PredictionService()
