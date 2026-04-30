"""
FraudShield - Synthetic Generator Tests
Tests for transaction generation, Indian context data, and anomaly distribution.
"""

import pytest
from core_engine.synthetic_generator.generator import generate_transactions
from core_engine.synthetic_generator.indian_context import (
    INDIAN_BANKS, INDIAN_CITIES, MERCHANT_CATEGORIES, ACCOUNT_HOLDERS,
    random_ist_timestamp, random_account_number,
)


class TestSyntheticGenerator:
    def test_generates_correct_count(self):
        txns = generate_transactions(100)
        assert len(txns) == 100

    def test_default_generates_1000(self):
        txns = generate_transactions()
        assert len(txns) == 1000

    def test_all_have_required_fields(self):
        txns = generate_transactions(10)
        required = {"id", "account_number", "account_holder", "amount", "timestamp",
                     "city", "merchant_name", "merchant_category", "bank_name",
                     "transaction_type", "is_flagged"}
        for txn in txns:
            assert required.issubset(txn.keys())

    def test_amounts_are_positive(self):
        txns = generate_transactions(100)
        for txn in txns:
            assert txn["amount"] > 0

    def test_transaction_types_valid(self):
        txns = generate_transactions(100)
        for txn in txns:
            assert txn["transaction_type"] in ("Credit", "Debit")

    def test_anomaly_injection(self):
        txns = generate_transactions(1000)
        flagged = [t for t in txns if t["is_flagged"]]
        # ~5% anomaly rate = ~50, allow some variance
        assert 20 <= len(flagged) <= 80


class TestIndianContext:
    def test_bank_pool_populated(self):
        assert len(INDIAN_BANKS) >= 10

    def test_city_pool_populated(self):
        assert len(INDIAN_CITIES) >= 15

    def test_account_number_format(self):
        acc = random_account_number()
        assert len(acc) == 12
        assert acc.isdigit()

    def test_timestamp_has_timezone(self):
        ts = random_ist_timestamp()
        assert ts.tzinfo is not None
