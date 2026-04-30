"""
FraudShield - High Value Transaction Rule
Flags transactions exceeding a configurable INR threshold.
"""

from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation


class HighValueRule(BaseRule):
    """Flag transactions with amount above threshold (default: ₹50,000)."""

    def __init__(self, weight: float = 0.20, threshold: float = 50000.0):
        super().__init__(rule_name="high_value", weight=weight, threshold=threshold)

    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        amount = transaction.get("amount", 0)
        if amount > self.threshold:
            raw_score = min(100, (amount / self.threshold) * 50)
            details = f"Transaction amount ₹{amount:,.2f} exceeds threshold ₹{self.threshold:,.2f}"
            return self._build_result(True, raw_score, details)
        return self._build_result(False, 0.0, "Amount within normal range")
