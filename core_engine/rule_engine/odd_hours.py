"""
FraudShield - Odd Hours Transaction Rule
Flags transactions occurring between Midnight and 5 AM IST.
"""

from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation


class OddHoursRule(BaseRule):
    """Flag transactions between 00:00 and 05:00 IST."""

    def __init__(self, weight: float = 0.10, threshold: float = 5.0):
        super().__init__(rule_name="odd_hours", weight=weight, threshold=threshold)

    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        timestamp = transaction.get("timestamp")
        if timestamp is None:
            return self._build_result(False, 0.0, "No timestamp provided")

        hour = timestamp.hour if hasattr(timestamp, "hour") else 12
        if 0 <= hour < int(self.threshold):
            details = f"Transaction at {hour}:00 IST falls within odd hours (00:00-05:00)"
            return self._build_result(True, 80.0, details)
        return self._build_result(False, 0.0, "Transaction within normal business hours")
