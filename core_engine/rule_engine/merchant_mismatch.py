"""
FraudShield - Merchant Category Mismatch Rule
Flags transactions with merchant categories outside the account's typical pattern.
"""

from collections import Counter
from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation


class MerchantMismatchRule(BaseRule):
    """Flag transactions with a merchant category not in the account's top N categories."""

    def __init__(self, weight: float = 0.15, threshold: float = 5.0):
        super().__init__(rule_name="merchant_mismatch", weight=weight, threshold=threshold)

    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        if not history:
            return self._build_result(False, 0.0, "No transaction history — first transaction for account")

        current_category = transaction.get("merchant_category", "")
        category_counts = Counter(h.get("merchant_category", "") for h in history if h.get("merchant_category"))
        top_categories = [cat for cat, _ in category_counts.most_common(int(self.threshold))]

        if current_category and current_category not in top_categories:
            details = f"Category '{current_category}' not in top {int(self.threshold)} categories: {top_categories}"
            return self._build_result(True, 70.0, details)
        return self._build_result(False, 0.0, f"Category '{current_category}' matches historical pattern")
