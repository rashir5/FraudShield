"""
FraudShield - Risk Level Classifier
Classifies a numeric score into LOW / MEDIUM / HIGH.
"""

from core_engine.config.settings import settings


def classify_risk(score: float) -> str:
    """
    Classify a risk score into a risk level.

    Args:
        score: Numeric risk score (0-100).

    Returns:
        "LOW", "MEDIUM", or "HIGH".
    """
    if score <= settings.RISK_LOW_MAX:
        return "LOW"
    elif score <= settings.RISK_MEDIUM_MAX:
        return "MEDIUM"
    else:
        return "HIGH"
