from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelCapabilities:
    """
    Declares the capabilities of a specific model version.
    Used to prevent the system from requesting unsupported features.
    """
    supports_binary: bool = False
    supports_stage: bool = False
    supports_explainability: bool = False
    explainability_type: Optional[str] = None # "gradcam", "attention", etc.
