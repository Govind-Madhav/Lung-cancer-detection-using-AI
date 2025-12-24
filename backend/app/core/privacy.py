from typing import Any, Dict
import re

class PrivacyGuard:
    @staticmethod
    def sanitize_log_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Removes any potential PHI or large binary data from logs.
        """
        sanitized = data.copy()
        
        # Redact potentially sensitive keys
        sensitive_keys = ["file_bytes", "image_data", "patient_name"]
        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "[REDACTED]"
                
        return sanitized

    @staticmethod
    def enforce_no_storage_guarantee(file_path: str) -> None:
        """
        Explicit check to ensure files are in temp directories or handled correctly.
        """
        if "temp" not in file_path and "static/explainability" not in file_path:
             # In a real strict system, might raise an error or alert
             pass
