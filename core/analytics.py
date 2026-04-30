"""FraudShield - Analytics Engine"""
from sqlalchemy import func, case, Integer
from core.models import TransactionModel, RiskScoreModel

def get_fraud_trends(session, days: int = 30) -> list[dict]:
    results = session.query(
        func.date(TransactionModel.timestamp).label("period"),
        func.count(TransactionModel.id).label("total"),
        func.sum(case((TransactionModel.is_flagged == True, 1), else_=0)).label("flagged")
    ).group_by(func.date(TransactionModel.timestamp)).order_by(func.date(TransactionModel.timestamp).desc()).limit(days).all()
    
    return [{
        "period": str(row.period), "total_transactions": row.total or 0,
        "flagged_count": int(row.flagged or 0),
        "fraud_rate": round(((row.flagged or 0) / (row.total or 1) * 100), 2)
    } for row in results]

def get_category_breakdown(session) -> list[dict]:
    results = session.query(
        TransactionModel.merchant_category,
        func.count(TransactionModel.id).label("total"),
        func.sum(case((TransactionModel.is_flagged == True, 1), else_=0)).label("flagged")
    ).group_by(TransactionModel.merchant_category).order_by(func.count(TransactionModel.id).desc()).all()
    
    out = []
    for row in results:
        avg = session.query(func.avg(RiskScoreModel.final_score)).join(TransactionModel).filter(TransactionModel.merchant_category == row.merchant_category).scalar()
        out.append({"category": row.merchant_category, "transaction_count": row.total, "flagged_count": int(row.flagged or 0), "average_risk_score": round(float(avg or 0), 2)})
    return out

def get_risk_distribution(session) -> list[dict]:
    total = session.query(func.count(RiskScoreModel.id)).scalar() or 0
    if total == 0: return [{"risk_level": l, "count": 0, "percentage": 0.0} for l in ["LOW", "MEDIUM", "HIGH"]]
    results = session.query(RiskScoreModel.risk_level, func.count(RiskScoreModel.id).label("count")).group_by(RiskScoreModel.risk_level).all()
    
    dist = {row.risk_level: {"risk_level": row.risk_level, "count": row.count, "percentage": round((row.count / total * 100), 2)} for row in results}
    for l in ["LOW", "MEDIUM", "HIGH"]:
        if l not in dist: dist[l] = {"risk_level": l, "count": 0, "percentage": 0.0}
    return [dist[l] for l in ["LOW", "MEDIUM", "HIGH"]]

def get_top_flagged_merchants(session, limit: int = 10) -> list[dict]:
    results = session.query(TransactionModel.merchant_name, func.count(TransactionModel.id).label("c")).filter(TransactionModel.is_flagged == True).group_by(TransactionModel.merchant_name).order_by(func.count(TransactionModel.id).desc()).limit(limit).all()
    out = []
    for row in results:
        avg = session.query(func.avg(RiskScoreModel.final_score)).join(TransactionModel).filter(TransactionModel.merchant_name == row.merchant_name, TransactionModel.is_flagged == True).scalar()
        out.append({"merchant_name": row.merchant_name, "flagged_count": row.c, "average_risk_score": round(float(avg or 0), 2)})
    return out

def get_geographic_distribution(session) -> list[dict]:
    """Calculate fraud density per city for heatmap visualizations."""
    results = session.query(
        TransactionModel.city,
        func.count(TransactionModel.id).label("total"),
        func.sum(case((TransactionModel.is_flagged == True, 1), else_=0)).label("flagged")
    ).group_by(TransactionModel.city).all()
    
    return [{
        "city": row.city,
        "total_count": row.total,
        "flagged_count": int(row.flagged or 0),
        "fraud_intensity": round((int(row.flagged or 0) / (row.total or 1) * 10), 2)  # Scale for heatmap weighting
    } for row in results]

