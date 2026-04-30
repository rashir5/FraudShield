"""FraudShield - Rule Engine"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import Counter
from datetime import timedelta
from core.models import RuleConfigModel

@dataclass
class RuleEvaluation:
    rule_name: str
    triggered: bool
    raw_score: float
    weighted_score: float
    details: str

class BaseRule(ABC):
    def __init__(self, rule_name: str, weight: float, threshold: float):
        self.rule_name = rule_name
        self.weight = weight
        self.threshold = threshold
    
    @abstractmethod
    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        pass

    def _build_result(self, triggered: bool, raw_score: float, details: str) -> RuleEvaluation:
        weighted = raw_score * self.weight if triggered else 0.0
        return RuleEvaluation(self.rule_name, triggered, raw_score if triggered else 0.0, round(weighted, 2), details)

class HighValueRule(BaseRule):
    def __init__(self, weight=0.20, threshold=50000.0):
        super().__init__("high_value", weight, threshold)
    def evaluate(self, transaction, history=None):
        amount = transaction.get("amount", 0)
        if amount > self.threshold:
            return self._build_result(True, min(100, (amount / self.threshold) * 50), f"Amount ₹{amount:,.2f} exceeds ₹{self.threshold:,.2f}")
        return self._build_result(False, 0.0, "Amount within normal range")

class OddHoursRule(BaseRule):
    def __init__(self, weight=0.10, threshold=5.0):
        super().__init__("odd_hours", weight, threshold)
    def evaluate(self, transaction, history=None):
        timestamp = transaction.get("timestamp")
        if not timestamp: return self._build_result(False, 0.0, "No timestamp")
        hour = timestamp.hour if hasattr(timestamp, "hour") else 12
        if 0 <= hour < int(self.threshold):
            return self._build_result(True, 80.0, f"Transaction at {hour}:00 IST falls within odd hours")
        return self._build_result(False, 0.0, "Normal business hours")

class VelocityRule(BaseRule):
    WINDOW_MINUTES = 10
    def __init__(self, weight=0.30, threshold=3.0):
        super().__init__("velocity", weight, threshold)
    def evaluate(self, transaction, history=None):
        if not history: return self._build_result(False, 0.0, "No history")
        timestamp = transaction.get("timestamp")
        if not timestamp: return self._build_result(False, 0.0, "No timestamp")
        start = timestamp - timedelta(minutes=self.WINDOW_MINUTES)
        count = sum(1 for h in history if h.get("timestamp") and start <= h["timestamp"] <= timestamp)
        if count >= self.threshold:
            return self._build_result(True, min(100, (count / self.threshold) * 60), f"{count} txns in {self.WINDOW_MINUTES}m window")
        return self._build_result(False, 0.0, f"Only {count} txns in window")

class GeoAnomalyRule(BaseRule):
    def __init__(self, weight=0.25, threshold=3.0):
        super().__init__("geo_anomaly", weight, threshold)
    def evaluate(self, transaction, history=None):
        if not history: return self._build_result(False, 0.0, "No history")
        city = transaction.get("city", "")
        recent = []
        for h in sorted(history, key=lambda x: x.get("timestamp", ""), reverse=True):
            if h.get("city") and h.get("city") not in recent: recent.append(h["city"])
            if len(recent) >= int(self.threshold): break
        if city and city not in recent:
            return self._build_result(True, 90.0, f"City '{city}' not in recent: {recent}")
        return self._build_result(False, 0.0, f"City '{city}' is known")

class MerchantMismatchRule(BaseRule):
    def __init__(self, weight=0.15, threshold=5.0):
        super().__init__("merchant_mismatch", weight, threshold)
    def evaluate(self, transaction, history=None):
        if not history: return self._build_result(False, 0.0, "No history")
        cat = transaction.get("merchant_category", "")
        counts = Counter(h.get("merchant_category", "") for h in history if h.get("merchant_category"))
        tops = [c for c, _ in counts.most_common(int(self.threshold))]
        if cat and cat not in tops:
            return self._build_result(True, 70.0, f"Category '{cat}' not in top: {tops}")
        return self._build_result(False, 0.0, f"Category '{cat}' matches pattern")

RULE_CLASS_MAP = {
    "high_value": HighValueRule, "odd_hours": OddHoursRule, "velocity": VelocityRule,
    "geo_anomaly": GeoAnomalyRule, "merchant_mismatch": MerchantMismatchRule
}

def load_active_rules(session) -> list[BaseRule]:
    configs = session.query(RuleConfigModel).filter(RuleConfigModel.is_active == True).all()
    rules = []
    for config in configs:
        cls = RULE_CLASS_MAP.get(config.rule_name)
        if cls: rules.append(cls(weight=config.weight, threshold=config.threshold))
    return rules

def evaluate_transaction(transaction, rules, history=None):
    return [r.evaluate(transaction, history) for r in rules]
