from pydantic import BaseModel

class Metrics(BaseModel):
    total_predictions: int
    average_confidence: float
