"""
FraudShield - Risk Scorer Tests
Tests for weighted scoring, classification, tie-breaking, and batch processing.
"""

import pytest
from core_engine.rule_engine.base_rule import RuleEvaluation
from core_engine.risk_scorer.weighted_scorer import calculate_weighted_score
from core_engine.risk_scorer.risk_classifier import classify_risk
from core_engine.risk_scorer.tie_breaker import get_severity_key, sort_by_risk


class TestWeightedScorer:
    def test_no_triggered_rules(self):
        evaluations = [
            RuleEvaluation("high_value", False, 0, 0, "ok"),
        ]
        assert calculate_weighted_score(evaluations) == 0.0

    def test_single_triggered_rule(self):
        evaluations = [
            RuleEvaluation("high_value", True, 80.0, 16.0, "triggered"),
        ]
        score = calculate_weighted_score(evaluations)
        assert score > 0
        assert score <= 100

    def test_score_bounded(self):
        evaluations = [
            RuleEvaluation("velocity", True, 100.0, 30.0, "max"),
            RuleEvaluation("geo_anomaly", True, 100.0, 25.0, "max"),
        ]
        score = calculate_weighted_score(evaluations)
        assert 0 <= score <= 100


class TestRiskClassifier:
    def test_low_risk(self):
        assert classify_risk(15.0) == "LOW"
        assert classify_risk(30.0) == "LOW"

    def test_medium_risk(self):
        assert classify_risk(31.0) == "MEDIUM"
        assert classify_risk(69.0) == "MEDIUM"

    def test_high_risk(self):
        assert classify_risk(70.0) == "HIGH"
        assert classify_risk(100.0) == "HIGH"

    def test_boundary_zero(self):
        assert classify_risk(0) == "LOW"


class TestTieBreaker:
    def test_velocity_highest_priority(self):
        evaluations = [
            RuleEvaluation("velocity", True, 80, 24, ""),
            RuleEvaluation("odd_hours", True, 80, 8, ""),
        ]
        assert get_severity_key(evaluations) == 1

    def test_no_triggered_returns_99(self):
        evaluations = [RuleEvaluation("high_value", False, 0, 0, "")]
        assert get_severity_key(evaluations) == 99

    def test_sort_by_risk_descending(self):
        data = [
            {"final_score": 50, "severity_key": 3},
            {"final_score": 80, "severity_key": 1},
            {"final_score": 80, "severity_key": 2},
        ]
        sorted_data = sort_by_risk(data)
        assert sorted_data[0]["severity_key"] == 1  # Velocity first at tied score
        assert sorted_data[1]["severity_key"] == 2
        assert sorted_data[2]["final_score"] == 50
