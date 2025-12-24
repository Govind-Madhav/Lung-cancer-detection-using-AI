from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_metrics():
    response = client.get("/api/v1/model-metrics")
    assert response.status_code == 200
    assert "total_predictions" in response.json()
