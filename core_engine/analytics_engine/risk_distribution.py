"""
FraudShield - Risk Distribution Analytics
Score histogram and percentile analysis.
"""

from sqlalchemy import func, case
from core_engine.database_manager.migrations import RiskScoreModel


def get_risk_distribution(session) -> list[dict]:
    """
    Calculate the distribution of transactions across risk levels.

    Returns:
        List of dicts with risk_level, count, percentage.
    """
    total = session.query(func.count(RiskScoreModel.id)).scalar() or 0
    if total == 0:
        return [
            {"risk_level": "LOW", "count": 0, "percentage": 0.0},
            {"risk_level": "MEDIUM", "count": 0, "percentage": 0.0},
            {"risk_level": "HIGH", "count": 0, "percentage": 0.0},
        ]

    results = (
        session.query(
            RiskScoreModel.risk_level,
            func.count(RiskScoreModel.id).label("count"),
        )
        .group_by(RiskScoreModel.risk_level)
        .all()
    )

    distribution = []
    for row in results:
        distribution.append({
            "risk_level": row.risk_level,
            "count": row.count,
            "percentage": round((row.count / total * 100), 2),
        })

    # Ensure all levels are present
    existing_levels = {d["risk_level"] for d in distribution}
    for level in ["LOW", "MEDIUM", "HIGH"]:
        if level not in existing_levels:
            distribution.append({"risk_level": level, "count": 0, "percentage": 0.0})

    return sorted(distribution, key=lambda d: ["LOW", "MEDIUM", "HIGH"].index(d["risk_level"]))
