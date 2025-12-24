class AppException(Exception):
    """Base class for application exceptions."""
    pass

class ModelLoadError(AppException):
    """Raised when a model fails to load."""
    pass

class InferenceError(AppException):
    """Raised when inference fails."""
    pass

class InvalidImageError(AppException):
    """Raised when input image is invalid."""
    pass

class ModelNotFoundError(AppException):
    """Raised when a requested model is not found."""
    pass

class PatientNotFoundError(AppException):
    """Raised when a patient is not found."""
    pass
