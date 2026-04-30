"""
FraudShield - Top Flagged Merchants Analytics
Rankings of merchants with highest fraud frequency.
"""

from sqlalchemy import func
from core_engine.database_manager.migrations import TransactionModel, RiskScoreModel


def get_top_flagged_merchants(session, limit: int = 10) -> list[dict]:
    """
    Get the top N merchants by flagged transaction count.

    Args:
        session: Active SQLAlchemy session.
        limit: Number of top merchants to return.

    Returns:
        List of dicts with merchant_name, flagged_count, average_risk_score.
    """
    results = (
        session.query(
            TransactionModel.merchant_name,
            func.count(TransactionModel.id).label("flagged_count"),
        )
        .filter(TransactionModel.is_flagged == True)
        .group_by(TransactionModel.merchant_name)
        .order_by(func.count(TransactionModel.id).desc())
        .limit(limit)
        .all()
    )

    merchants = []
    for row in results:
        avg_score = (
            session.query(func.avg(RiskScoreModel.final_score))
            .join(TransactionModel, TransactionModel.id == RiskScoreModel.transaction_id)
            .filter(TransactionModel.merchant_name == row.merchant_name)
            .filter(TransactionModel.is_flagged == True)
            .scalar()
        )
        merchants.append({
            "merchant_name": row.merchant_name,
            "flagged_count": row.flagged_count,
            "average_risk_score": round(float(avg_score or 0), 2),
        })
    return merchants
