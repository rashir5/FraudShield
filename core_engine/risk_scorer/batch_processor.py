"""
FraudShield - Batch Processor
Processes transactions in memory-safe batches for 4GB RAM constraint.
"""

import uuid
from datetime import datetime, timezone
from core_engine.config.settings import settings
from core_engine.rule_engine.rule_registry import evaluate_transaction, load_active_rules
from core_engine.risk_scorer.weighted_scorer import calculate_weighted_score
from core_engine.risk_scorer.risk_classifier import classify_risk
from core_engine.risk_scorer.tie_breaker import get_severity_key
from core_engine.database_manager.migrations import RiskScoreModel, RuleResultModel


def process_batch(
    transactions: list[dict],
    rules,
    history_map: dict,
    session,
) -> list[dict]:
    """
    Process a batch of transactions: evaluate rules, score, classify, and persist.

    Args:
        transactions: List of transaction dicts to process.
        rules: List of active rule instances.
        history_map: Dict mapping account_number -> list of historical transactions.
        session: Active SQLAlchemy session.

    Returns:
        List of scored transaction summaries.
    """
    results = []
    for txn in transactions:
        account = txn.get("account_number", "")
        history = history_map.get(account, [])

        # Evaluate all rules
        evaluations = evaluate_transaction(txn, rules, history)

        # Calculate weighted score
        final_score = calculate_weighted_score(evaluations)
        risk_level = classify_risk(final_score)
        severity_key = get_severity_key(evaluations)
        triggered_count = sum(1 for e in evaluations if e.triggered)

        # Persist RiskScore
        risk_score = RiskScoreModel(
            id=str(uuid.uuid4()),
            transaction_id=txn["id"],
            final_score=final_score,
            risk_level=risk_level,
            rules_triggered=triggered_count,
            calculated_at=datetime.now(timezone.utc),
        )
        session.add(risk_score)

        # Persist RuleResults
        for evaluation in evaluations:
            rule_result = RuleResultModel(
                id=str(uuid.uuid4()),
                transaction_id=txn["id"],
                rule_name=evaluation.rule_name,
                triggered=evaluation.triggered,
                raw_score=evaluation.raw_score,
                weighted_score=evaluation.weighted_score,
                details=evaluation.details,
            )
            session.add(rule_result)

        results.append({
            "transaction_id": txn["id"],
            "final_score": final_score,
            "risk_level": risk_level,
            "severity_key": severity_key,
            "rules_triggered": triggered_count,
        })

    session.flush()
    return results


def process_all_in_batches(
    transactions: list[dict],
    session,
    history_map: dict = None,
) -> list[dict]:
    """
    Process all transactions in memory-safe batches.

    Args:
        transactions: Full list of transactions.
        session: Active SQLAlchemy session.
        history_map: Optional pre-built history map.

    Returns:
        Combined list of all scored results.
    """
    if history_map is None:
        history_map = {}

    rules = load_active_rules(session)
    batch_size = settings.BATCH_SIZE
    all_results = []

    for i in range(0, len(transactions), batch_size):
        batch = transactions[i : i + batch_size]
        batch_results = process_batch(batch, rules, history_map, session)
        all_results.extend(batch_results)

    return all_results
