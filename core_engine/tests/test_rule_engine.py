"""
FraudShield - Rule Engine Tests
Tests for each fraud detection rule individually.
"""

import pytest
from datetime import datetime, timezone, timedelta
from core_engine.rule_engine.high_value import HighValueRule
from core_engine.rule_engine.odd_hours import OddHoursRule
from core_engine.rule_engine.velocity import VelocityRule
from core_engine.rule_engine.geo_anomaly import GeoAnomalyRule
from core_engine.rule_engine.merchant_mismatch import MerchantMismatchRule


class TestHighValueRule:
    def setup_method(self):
        self.rule = HighValueRule()

    def test_triggers_above_threshold(self):
        txn = {"amount": 75000}
        result = self.rule.evaluate(txn)
        assert result.triggered is True
        assert result.raw_score > 0

    def test_does_not_trigger_below_threshold(self):
        txn = {"amount": 10000}
        result = self.rule.evaluate(txn)
        assert result.triggered is False

    def test_score_capped_at_100(self):
        txn = {"amount": 5000000}
        result = self.rule.evaluate(txn)
        assert result.raw_score <= 100


class TestOddHoursRule:
    def setup_method(self):
        self.rule = OddHoursRule()

    def test_triggers_at_2am(self):
        txn = {"timestamp": datetime(2026, 1, 1, 2, 0, tzinfo=timezone.utc)}
        result = self.rule.evaluate(txn)
        assert result.triggered is True
        assert result.raw_score == 80.0

    def test_does_not_trigger_at_10am(self):
        txn = {"timestamp": datetime(2026, 1, 1, 10, 0, tzinfo=timezone.utc)}
        result = self.rule.evaluate(txn)
        assert result.triggered is False


class TestVelocityRule:
    def setup_method(self):
        self.rule = VelocityRule()

    def test_triggers_with_rapid_transactions(self):
        now = datetime.now(timezone.utc)
        history = [
            {"timestamp": now - timedelta(minutes=2)},
            {"timestamp": now - timedelta(minutes=4)},
            {"timestamp": now - timedelta(minutes=6)},
        ]
        txn = {"timestamp": now}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is True

    def test_does_not_trigger_with_sparse_transactions(self):
        now = datetime.now(timezone.utc)
        history = [{"timestamp": now - timedelta(hours=2)}]
        txn = {"timestamp": now}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is False


class TestGeoAnomalyRule:
    def setup_method(self):
        self.rule = GeoAnomalyRule()

    def test_triggers_unknown_city(self):
        now = datetime.now(timezone.utc)
        history = [
            {"city": "Mumbai", "timestamp": now - timedelta(days=1)},
            {"city": "Delhi", "timestamp": now - timedelta(days=2)},
            {"city": "Pune", "timestamp": now - timedelta(days=3)},
        ]
        txn = {"city": "Guwahati"}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is True
        assert result.raw_score == 90.0

    def test_does_not_trigger_known_city(self):
        now = datetime.now(timezone.utc)
        history = [
            {"city": "Mumbai", "timestamp": now - timedelta(days=1)},
        ]
        txn = {"city": "Mumbai"}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is False


class TestMerchantMismatchRule:
    def setup_method(self):
        self.rule = MerchantMismatchRule()

    def test_triggers_unusual_category(self):
        history = [
            {"merchant_category": "Groceries"},
            {"merchant_category": "Fuel"},
            {"merchant_category": "Groceries"},
        ]
        txn = {"merchant_category": "Jewellery"}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is True
        assert result.raw_score == 70.0

    def test_does_not_trigger_known_category(self):
        history = [
            {"merchant_category": "Groceries"},
            {"merchant_category": "Fuel"},
        ]
        txn = {"merchant_category": "Groceries"}
        result = self.rule.evaluate(txn, history)
        assert result.triggered is False
