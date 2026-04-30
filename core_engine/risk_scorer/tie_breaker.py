"""
FraudShield - Tie Breaker
Ranks transactions with identical scores by rule severity order.
"""

from core_engine.config.settings import settings
from core_engine.rule_engine.base_rule import RuleEvaluation


def get_severity_key(evaluations: list[RuleEvaluation]) -> int:
    """
    Return a tie-breaking severity key based on the highest-priority triggered rule.
    Lower number = higher severity = ranks first.

    Args:
        evaluations: List of RuleEvaluation results.

    Returns:
        Severity key (1=highest priority, 5=lowest). Returns 99 if no rules triggered.
    """
    triggered = [e for e in evaluations if e.triggered]
    if not triggered:
        return 99

    severities = [
        settings.RULE_SEVERITY_ORDER.get(e.rule_name, 99)
        for e in triggered
    ]
    return min(severities)


def sort_by_risk(scored_transactions: list[dict]) -> list[dict]:
    """
    Sort transactions by final_score descending, then by severity key ascending (tie-breaking).

    Args:
        scored_transactions: List of dicts with 'final_score' and 'severity_key'.

    Returns:
        Sorted list.
    """
    return sorted(
        scored_transactions,
        key=lambda t: (-t.get("final_score", 0), t.get("severity_key", 99)),
    )
