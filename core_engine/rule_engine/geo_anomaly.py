"""
FraudShield - Geographic Anomaly Rule
Flags transactions from cities not in the account's recent history.
"""

from core_engine.rule_engine.base_rule import BaseRule, RuleEvaluation


class GeoAnomalyRule(BaseRule):
    """Flag transactions from a city not in the account's last N known cities."""

    def __init__(self, weight: float = 0.25, threshold: float = 3.0):
        super().__init__(rule_name="geo_anomaly", weight=weight, threshold=threshold)

    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        if not history:
            return self._build_result(False, 0.0, "No transaction history — first transaction for account")

        current_city = transaction.get("city", "")
        recent_cities = []
        for h in sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True):
            city = h.get("city", "")
            if city and city not in recent_cities:
                recent_cities.append(city)
            if len(recent_cities) >= int(self.threshold):
                break

        if current_city and current_city not in recent_cities:
            details = f"Transaction from '{current_city}' — not in recent cities: {recent_cities}"
            return self._build_result(True, 90.0, details)
        return self._build_result(False, 0.0, f"City '{current_city}' is within known locations")
