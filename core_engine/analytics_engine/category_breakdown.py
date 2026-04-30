"""
FraudShield - Category Breakdown Analytics
Merchant category distribution analysis.
"""

from sqlalchemy import func
from core_engine.database_manager.migrations import TransactionModel, RiskScoreModel


def get_category_breakdown(session) -> list[dict]:
    """
    Calculate fraud statistics per merchant category.

    Returns:
        List of dicts with category, transaction_count, flagged_count, average_risk_score.
    """
    results = (
        session.query(
            TransactionModel.merchant_category,
            func.count(TransactionModel.id).label("total"),
            func.sum(func.cast(TransactionModel.is_flagged, type_=None)).label("flagged"),
        )
        .group_by(TransactionModel.merchant_category)
        .order_by(func.count(TransactionModel.id).desc())
        .all()
    )

    breakdown = []
    for row in results:
        # Get average risk score for this category
        avg_score_result = (
            session.query(func.avg(RiskScoreModel.final_score))
            .join(TransactionModel, TransactionModel.id == RiskScoreModel.transaction_id)
            .filter(TransactionModel.merchant_category == row.merchant_category)
            .scalar()
        )

        breakdown.append({
            "category": row.merchant_category,
            "transaction_count": row.total,
            "flagged_count": int(row.flagged or 0),
            "average_risk_score": round(float(avg_score_result or 0), 2),
        })
    return breakdown
