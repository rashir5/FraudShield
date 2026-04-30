"""
FraudShield - Rule Registry
Loads active rules from SQLite3 and executes all against a transaction.
"""

from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation
from core_engine.rule_engine.high_value import HighValueRule
from core_engine.rule_engine.odd_hours import OddHoursRule
from core_engine.rule_engine.velocity import VelocityRule
from core_engine.rule_engine.geo_anomaly import GeoAnomalyRule
from core_engine.rule_engine.merchant_mismatch import MerchantMismatchRule
from core_engine.database_manager.migrations import RuleConfigModel


# Map of rule_name -> Rule class
RULE_CLASS_MAP: dict[str, type[BaseRule]] = {
    "high_value": HighValueRule,
    "odd_hours": OddHoursRule,
    "velocity": VelocityRule,
    "geo_anomaly": GeoAnomalyRule,
    "merchant_mismatch": MerchantMismatchRule,
}


def load_active_rules(session) -> list[BaseRule]:
    """
    Load all active rule configurations from SQLite3 and instantiate rule objects.

    Args:
        session: Active SQLAlchemy session.

    Returns:
        List of instantiated BaseRule subclasses with DB-configured weights/thresholds.
    """
    configs = session.query(RuleConfigModel).filter(RuleConfigModel.is_active == True).all()
    rules = []
    for config in configs:
        rule_class = RULE_CLASS_MAP.get(config.rule_name)
        if rule_class:
            rules.append(rule_class(weight=config.weight, threshold=config.threshold))
    return rules


def evaluate_transaction(
    transaction: dict,
    rules: list[BaseRule],
    history: list[dict] = None,
) -> list[RuleEvaluation]:
    """
    Evaluate a single transaction against all provided rules.

    Args:
        transaction: Transaction data dictionary.
        rules: List of instantiated rule objects.
        history: Optional account transaction history.

    Returns:
        List of RuleEvaluation results.
    """
    results = []
    for rule in rules:
        evaluation = rule.evaluate(transaction, history)
        results.append(evaluation)
    return results
