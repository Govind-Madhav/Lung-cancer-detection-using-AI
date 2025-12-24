import os
import threading
from app.core.config import settings
from app.core.logger import logger
from app.core.exceptions import ModelLoadError

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
        if self._cnn_rnn_model is not None and self._vit_model is not None:
            return

        with self._lock:
            # Double check inside lock
            if self._cnn_rnn_model is not None and self._vit_model is not None:
                return
                
            logger.info("Loading models...")
            try:
                # Placeholder for actual model loading logic
                # In a real app, you would use:
                # self._cnn_rnn_model = tf.keras.models.load_model(settings.CNN_RNN_MODEL_PATH)
                self._cnn_rnn_model = "Mock CNN_RNN Model"
                self._vit_model = "Mock ViT Model"
                logger.info(f"Models loaded from {settings.CNN_RNN_MODEL_PATH} and {settings.VIT_MODEL_PATH}")
            except Exception as e:
                logger.error(f"Failed to load models: {e}")
                raise ModelLoadError(f"Critical failure loading models: {e}")

    def reload_models(self):
        """Forces a reload of models (Zero-downtime strategy)."""
        logger.info("Reloading models...")
        with self._lock:
             # In real impl, load to temp first, then swap advice
             # Here we just clear and reload
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
