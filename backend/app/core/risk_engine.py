from typing import Dict

class RiskEngine:
    MIN_CONFIDENCE = 0.4

    @staticmethod
    def calculate_risk(probability: float) -> str:
        """
        Maps probability to risk level.
        Medical rules live here.
        """
        if probability < RiskEngine.MIN_CONFIDENCE:
            return "Inconclusive"
            
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.7:
            return "Medium Risk"
        else:
            return "High Risk"

    @staticmethod
    def determine_stage(vit_output: Dict) -> str:
        """
        Determines stage from ViT output.
        """
        # Placeholder logic
        return vit_output.get("stage", "Unknown")

risk_engine = RiskEngine()
