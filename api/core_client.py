"""FraudShield API - Internal Client to Core Logic"""
from core.database import get_db_session
from core.models import TransactionModel, RiskScoreModel, RuleResultModel, RuleConfigModel
from core.generator import generate_transactions
from core.scorer import process_all_in_batches
from core.analytics import get_fraud_trends, get_category_breakdown, get_risk_distribution, get_top_flagged_merchants, get_geographic_distribution
from core.ai_client import build_analysis_prompt, call_gemini, parse_gemini_response
from core.models import AIAnalysisModel
import uuid
from datetime import datetime, timezone

class CoreClient:
    """Wrapper to interact with the underlying core logic cleanly."""

    def list_transactions(self, page: int, page_size: int, risk_level: str = None, is_flagged: bool = None):
        with get_db_session() as session:
            query = session.query(TransactionModel)
            if is_flagged is not None: query = query.filter(TransactionModel.is_flagged == is_flagged)
            if risk_level: query = query.join(RiskScoreModel).filter(RiskScoreModel.risk_level == risk_level)
            total = query.count()
            txns = query.order_by(TransactionModel.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
            # Eagerly convert ORM instances to dicts inside the session scope
            # to avoid DetachedInstanceError when FastAPI serializes outside this block
            cols = [c.name for c in TransactionModel.__table__.columns]
            txn_dicts = [{col: getattr(t, col) for col in cols} for t in txns]
            return txn_dicts, total

    def generate_and_score(self, count: int):
        with get_db_session() as session:
            txns = generate_transactions(count)
            for t in txns:
                # Filter out internal generator keys (e.g. _velocity_flag) before constructing ORM
                clean = {k: v for k, v in t.items() if not k.startswith("_")}
                session.add(TransactionModel(**clean))
            session.flush()
            dicts = [{k: v for k, v in t.items() if not k.startswith("_")} for t in txns]
            res = process_all_in_batches(dicts, session)
            flagged = sum(1 for r in res if r["risk_level"] in ("MEDIUM", "HIGH"))
            for r in res:
                if r["risk_level"] in ("MEDIUM", "HIGH"):
                    session.query(TransactionModel).filter(TransactionModel.id == r["transaction_id"]).update({"is_flagged": True})
            return len(txns), flagged

    def get_analytics_summary(self):
        with get_db_session() as session:
            return {
                "fraud_trends": get_fraud_trends(session),
                "category_breakdown": get_category_breakdown(session),
                "risk_distribution": get_risk_distribution(session),
                "top_flagged_merchants": get_top_flagged_merchants(session),
                "geo_distribution": get_geographic_distribution(session)
            }

    async def analyze_transaction(self, transaction_id: str):
        with get_db_session() as session:
            txn = session.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
            if not txn: return None
            risk = session.query(RiskScoreModel).filter(RiskScoreModel.transaction_id == transaction_id).first()
            rules = session.query(RuleResultModel).filter(RuleResultModel.transaction_id == transaction_id).all()
            
            tdict = {c.name: getattr(txn, c.name) for c in TransactionModel.__table__.columns}
            rdicts = [{"rule_name": r.rule_name, "triggered": r.triggered, "raw_score": r.raw_score, "weighted_score": r.weighted_score, "details": r.details} for r in rules]
            prompt = build_analysis_prompt(tdict, rdicts, risk.final_score if risk else 0, risk.risk_level if risk else "LOW")
            
            g_res = await call_gemini(prompt)
            if not g_res["success"]: return {"error": g_res["error"]}
            
            parsed = parse_gemini_response(g_res["response_text"])
            ai_record = AIAnalysisModel(
                id=str(uuid.uuid4()), transaction_id=transaction_id,
                prompt_sent=prompt, response_raw=g_res["response_text"],
                pattern_explanation=parsed["pattern_explanation"],
                top_risk_factors=parsed["top_risk_factors"],
                recommendation=parsed["recommendation"],
                response_time_ms=g_res["response_time_ms"],
                analyzed_at=datetime.now(timezone.utc)
            )
            session.add(ai_record)
            session.flush()
            return ai_record

core_client = CoreClient()
