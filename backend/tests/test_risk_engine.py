from app.core.risk_engine import risk_engine

def test_risk_calculation():
    assert risk_engine.calculate_risk(0.1) == "Inconclusive" 
    assert risk_engine.calculate_risk(0.5) == "Medium Risk"
    assert risk_engine.calculate_risk(0.9) == "High Risk"
