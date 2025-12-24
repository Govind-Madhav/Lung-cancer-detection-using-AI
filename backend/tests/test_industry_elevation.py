import pytest
from app.core.risk_engine import risk_engine
from app.core.inference_engine import inference_engine, InferenceEngine
from app.core.exceptions import InferenceError

def test_risk_threshold():
    # Test strict medical threshold
    assert risk_engine.calculate_risk(0.1) == "Inconclusive" # Below 0.4
    assert risk_engine.calculate_risk(0.45) == "Low Risk"

def test_inference_timeout():
    # Mock inference time check to simulate timeout
    # We can't easily slow down time, but we can verify check_timeout raises
    engine = InferenceEngine()
    engine.MAX_INFERENCE_TIME = 0.001
    import time
    start = time.time()
    time.sleep(0.01)
    
    with pytest.raises(InferenceError):
        engine._check_timeout(start)

def test_privacy_guard():
    from app.core.privacy import PrivacyGuard
    log_data = {"event": "test", "patient_name": "John Doe", "binary_result": 0.9}
    sanitized = PrivacyGuard.sanitize_log_data(log_data)
    assert sanitized["patient_name"] == "[REDACTED]"
    assert sanitized["binary_result"] == 0.9
