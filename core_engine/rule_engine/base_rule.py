"""
FraudShield - Base Rule (Abstract)
All fraud detection rules must inherit from this class.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RuleEvaluation:
    """Result of evaluating a single rule against a transaction."""
    rule_name: str
    triggered: bool
    raw_score: float  # 0-100
    weighted_score: float  # raw_score * weight
    details: str


class BaseRule(ABC):
    """Abstract base class for all fraud detection rules."""

    def __init__(self, rule_name: str, weight: float, threshold: float):
        self.rule_name = rule_name
        self.weight = weight
        self.threshold = threshold

    @abstractmethod
    def evaluate(self, transaction: dict, history: list[dict] = None) -> RuleEvaluation:
        """
        Evaluate a transaction against this rule.

        Args:
            transaction: Transaction data dictionary.
            history: Optional list of historical transactions for the same account.

        Returns:
            RuleEvaluation with triggered status, scores, and details.
        """
        pass

    def _build_result(self, triggered: bool, raw_score: float, details: str) -> RuleEvaluation:
        """Helper to construct a RuleEvaluation with weighted score."""
        weighted = raw_score * self.weight if triggered else 0.0
        return RuleEvaluation(
            rule_name=self.rule_name,
            triggered=triggered,
            raw_score=raw_score if triggered else 0.0,
            weighted_score=round(weighted, 2),
            details=details,
        )
