from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router
from app.db.session import engine
from app.db import models

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

from app.api.error_handlers import app_exception_handler
from app.core.exceptions import AppException

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to the Lung Cancer Detection API"}
