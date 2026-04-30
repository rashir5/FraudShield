"""FraudShield - Risk Scorer"""
import uuid
from datetime import datetime, timezone
from core import settings
from core.models import RiskScoreModel, RuleResultModel
from core.rules import evaluate_transaction, load_active_rules

def calculate_weighted_score(evaluations) -> float:
    triggered = [e for e in evaluations if e.triggered]
    if not triggered: return 0.0
    total_w = sum(e.raw_score * (e.weighted_score / e.raw_score if e.raw_score > 0 else 0) for e in triggered)
    total_v = sum((e.weighted_score / e.raw_score if e.raw_score > 0 else 0) for e in triggered)
    if total_v == 0: return 0.0
    return round(min(100.0, max(0.0, total_w / total_v)), 2)

def classify_risk(score: float) -> str:
    if score <= settings.RISK_LOW_MAX: return "LOW"
    if score <= settings.RISK_MEDIUM_MAX: return "MEDIUM"
    return "HIGH"

def get_severity_key(evaluations) -> int:
    triggered = [e for e in evaluations if e.triggered]
    if not triggered: return 99
    return min(settings.RULE_SEVERITY_ORDER.get(e.rule_name, 99) for e in triggered)

def process_batch(transactions, rules, history_map, session):
    results = []
    for txn in transactions:
        history = history_map.get(txn.get("account_number", ""), [])
        evaluations = evaluate_transaction(txn, rules, history)
        score = calculate_weighted_score(evaluations)
        level = classify_risk(score)
        severity = get_severity_key(evaluations)
        t_count = sum(1 for e in evaluations if e.triggered)
        
        session.add(RiskScoreModel(
            id=str(uuid.uuid4()), transaction_id=txn["id"], final_score=score,
            risk_level=level, rules_triggered=t_count, calculated_at=datetime.now(timezone.utc)
        ))
        for ev in evaluations:
            session.add(RuleResultModel(
                id=str(uuid.uuid4()), transaction_id=txn["id"], rule_name=ev.rule_name,
                triggered=ev.triggered, raw_score=ev.raw_score, weighted_score=ev.weighted_score, details=ev.details
            ))
        results.append({"transaction_id": txn["id"], "final_score": score, "risk_level": level, "severity_key": severity})
    session.flush()
    return results

def process_all_in_batches(transactions, session, history_map=None):
    history_map = history_map or {}
    rules = load_active_rules(session)
    bs = settings.BATCH_SIZE
    all_res = []
    for i in range(0, len(transactions), bs):
        all_res.extend(process_batch(transactions[i:i+bs], rules, history_map, session))
    return all_res
