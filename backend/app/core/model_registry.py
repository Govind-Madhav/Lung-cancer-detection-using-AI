import os
import sys
import threading
import torch
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import ModelLoadError

# Standardize path to ml_train to allow importing TripleHybrid
# Assuming structure: backend/app/core/../../ml_train
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ML_TRAIN_DIR = os.path.join(BASE_DIR, 'ml_train')
if ML_TRAIN_DIR not in sys.path:
    sys.path.append(ML_TRAIN_DIR)

try:
    from models.cnn_rnn import TripleHybrid
except ImportError:
    logger.warning("Could not import TripleHybrid from ml_train. Ensure backend/ml_train exists.")
    TripleHybrid = None

class ModelRegistry:
    _instance = None
    _cnn_rnn_model = None
    _vit_model = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ModelRegistry, cls).__new__(cls)
        return cls._instance

    def load_models(self):
        """Loads models if they are not already loaded. Thread-safe."""
        if self._cnn_rnn_model is not None:
            return

        with self._lock:
            # Double check inside lock
            if self._cnn_rnn_model is not None:
                return
                
            logger.info("Loading models...")
            try:
                # Load TripleHybrid
                if TripleHybrid:
                    self._cnn_rnn_model = TripleHybrid(
                        in_channels=1,
                        num_classes=1,
                        cnn_feature_dim=512,
                        rnn_hidden_dim=256,
                        vit_hidden_dim=512,
                        max_depth=128
                    )
                    
                    # Try to load weights
                    # Path: backend/models/triple_hybrid/triple_hybrid_v1.pth
                    # Relative to backend root
                    weights_path = os.path.join(BASE_DIR, "models", "triple_hybrid", "triple_hybrid_v1.pth")
                    
                    if os.path.exists(weights_path):
                        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                        self._cnn_rnn_model.load_state_dict(torch.load(weights_path, map_location=device))
                        self._cnn_rnn_model.to(device)
                        self._cnn_rnn_model.eval()
                        logger.info(f"TripleHybrid loaded from {weights_path}")
                    else:
                        logger.warning(f"TripleHybrid weights not found at {weights_path}. Using initialized model.")
                        # Move to device anyway
                        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                        self._cnn_rnn_model.to(device)
                        self._cnn_rnn_model.eval()

                    # ViT is now part of TripleHybrid, so we can expose it if needed or just use the same instance
                    # For legacy compatibility, we can point _vit_model to something or just leave it
                    self._vit_model = self._cnn_rnn_model 
                else:
                    self._cnn_rnn_model = "Mock TripleHybrid (Import Failed)"
                    self._vit_model = "Mock ViT"

            except Exception as e:
                logger.error(f"Failed to load models: {e}")
                raise ModelLoadError(f"Critical failure loading models: {e}")

    def reload_models(self):
        """Forces a reload of models (Zero-downtime strategy)."""
        logger.info("Reloading models...")
        with self._lock:
             self._cnn_rnn_model = None
             self._vit_model = None
             self.load_models()

    @property
    def cnn_rnn_model(self):
        if self._cnn_rnn_model is None:
            self.load_models()
        return self._cnn_rnn_model

    @property
    def vit_model(self):
        if self._vit_model is None:
            self.load_models()
        return self._vit_model

model_registry = ModelRegistry()
