import logging
import json
from datetime import datetime
from typing import Any, Dict
from app.core.privacy import PrivacyGuard

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit_log")
        self.logger.setLevel(logging.INFO)
        # Ensure separate handler in production, for now using standard
        
    def log_prediction(self, 
                       model_type: str, 
                       model_version: str, 
                       outcome: str, 
                       confidence: float,
                       patient_id: int):
        """
        Logs an audit event for a prediction.
        Crucially, does NOT log the image or PHI.
        """
        event = {
            "event_type": "PREDICTION",
            "timestamp": datetime.utcnow().isoformat(),
            "model_type": model_type,
            "model_version": model_version,
            "outcome": outcome,
            "confidence": confidence,
            "patient_id": patient_id
        }
        
        # Double check privacy
        sanitized_event = PrivacyGuard.sanitize_log_data(event)
        
        self.logger.info(json.dumps(sanitized_event))

audit_logger = AuditLogger()
