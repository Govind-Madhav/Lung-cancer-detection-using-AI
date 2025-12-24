from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException, ModelLoadError, InferenceError, InvalidImageError, ModelNotFoundError, PatientNotFoundError
from app.core.logger import logger

async def app_exception_handler(request: Request, exc: AppException):
    """
    Catches all internal AppExceptions and maps them to standard HTTP responses.
    """
    logger.error(f"AppException: {str(exc)}")
    
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "An internal error occurred."
    
    if isinstance(exc, ModelLoadError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        message = "AI Model service is unavailable."
    elif isinstance(exc, InferenceError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        message = "Unable to process the image for inference."
    elif isinstance(exc, InvalidImageError):
        status_code = status.HTTP_400_BAD_REQUEST
        message = "Invalid image file provided."
    elif isinstance(exc, ModelNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
        message = "Requested model not found."
    elif isinstance(exc, PatientNotFoundError):
        status_code = status.HTTP_404_NOT_FOUND
        message = "Patient not found."
        
    return JSONResponse(
        status_code=status_code,
        content={"detail": message, "error_code": exc.__class__.__name__},
    )
