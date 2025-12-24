import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lung Cancer Detection API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model Paths
    CNN_RNN_MODEL_PATH: str = os.getenv("CNN_RNN_MODEL_PATH", "models/cnn_rnn/cnn_rnn_v1.keras")
    VIT_MODEL_PATH: str = os.getenv("VIT_MODEL_PATH", "models/vit/vit_v1.pth")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    
    class Config:
        env_file = ".env"

settings = Settings()
