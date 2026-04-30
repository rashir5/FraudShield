"""
FraudShield - Fraud Trends Analytics
Aggregates fraud rate over time windows.
"""

from sqlalchemy import func, extract
from core_engine.database_manager.migrations import TransactionModel, RiskScoreModel


def get_fraud_trends(session, days: int = 30) -> list[dict]:
    """
    Calculate daily fraud rate trends.

    Args:
        session: Active SQLAlchemy session.
        days: Number of days to look back.

    Returns:
        List of dicts with period, total_transactions, flagged_count, fraud_rate.
    """
    results = (
        session.query(
            func.date(TransactionModel.timestamp).label("period"),
            func.count(TransactionModel.id).label("total"),
            func.sum(func.cast(TransactionModel.is_flagged, type_=None)).label("flagged"),
        )
        .group_by(func.date(TransactionModel.timestamp))
        .order_by(func.date(TransactionModel.timestamp).desc())
        .limit(days)
        .all()
    )

    trends = []
    for row in results:
        total = row.total or 0
        flagged = int(row.flagged or 0)
        trends.append({
            "period": str(row.period),
            "total_transactions": total,
            "flagged_count": flagged,
            "fraud_rate": round((flagged / total * 100) if total > 0 else 0, 2),
        })
    return trends
