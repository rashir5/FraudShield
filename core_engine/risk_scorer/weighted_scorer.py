"""
FraudShield - Weighted Risk Scorer
Calculates aggregated risk score using weighted average of rule evaluations.
"""

from core_engine.rule_engine.base_rule import RuleEvaluation


def calculate_weighted_score(evaluations: list[RuleEvaluation]) -> float:
    """
    Calculate the weighted average risk score.
    Formula: SUM(raw_score * weight) / SUM(weight)

    Args:
        evaluations: List of RuleEvaluation results from all rules.

    Returns:
        Final weighted score rounded to 2 decimal places (0-100).
    """
    triggered = [e for e in evaluations if e.triggered]
    if not triggered:
        return 0.0

    total_weighted = sum(e.raw_score * (e.weighted_score / e.raw_score if e.raw_score > 0 else 0) for e in triggered)
    total_weights = sum((e.weighted_score / e.raw_score if e.raw_score > 0 else 0) for e in triggered)

    if total_weights == 0:
        return 0.0

    score = total_weighted / total_weights
    return round(min(100.0, max(0.0, score)), 2)
