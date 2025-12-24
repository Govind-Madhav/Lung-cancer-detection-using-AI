from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModel(ABC):
    """
    Abstract base class for all AI models.
    Enforces a strict contract for inference.
    """
    
    @abstractmethod
    def load(self) -> None:
        """Loads the model artifacts."""
        pass

    @abstractmethod
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Runs inference on the input data.
        Returns a dictionary with results.
        """
        pass
