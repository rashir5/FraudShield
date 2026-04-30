"""
FraudShield - Velocity Check Rule
Flags accounts with rapid successive transactions within a rolling time window.
"""

from datetime import timedelta
from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation


class VelocityRule(BaseRule):
    """Flag accounts with >= threshold transactions within a 10-minute window."""

    WINDOW_MINUTES = 10

    def __init__(self, weight: float = 0.30, threshold: float = 3.0):
        super().__init__(rule_name="velocity", weight=weight, threshold=threshold)

    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        if not history:
            return self._build_result(False, 0.0, "No transaction history available")

        timestamp = transaction.get("timestamp")
        if timestamp is None:
            return self._build_result(False, 0.0, "No timestamp provided")

        window_start = timestamp - timedelta(minutes=self.WINDOW_MINUTES)
        rapid_count = sum(
            1 for h in history
            if h.get("timestamp") and window_start <= h["timestamp"] <= timestamp
        )

        if rapid_count >= int(self.threshold):
            raw_score = min(100, (rapid_count / self.threshold) * 60)
            details = f"{rapid_count} transactions within {self.WINDOW_MINUTES} min window (threshold: {int(self.threshold)})"
            return self._build_result(True, raw_score, details)
        return self._build_result(False, 0.0, f"Only {rapid_count} transactions in window")
