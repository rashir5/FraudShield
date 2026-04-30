"""
FraudShield - Anomaly Injector
Injects weighted anomalous patterns into synthetic transactions.
"""

import random
from datetime import timedelta
from core_engine.config.settings import settings
from core_engine.synthetic_generator.indian_context import (
    random_odd_hour_timestamp, INDIAN_CITIES, MERCHANT_CATEGORIES,
)


def inject_anomalies(transactions: list[dict], anomaly_count: int) -> list[dict]:
    """
    Inject anomalous patterns into a subset of transactions using weighted distribution.

    Distribution (from settings):
        velocity: 30%, high_value: 25%, geo_anomaly: 20%,
        merchant_mismatch: 15%, odd_hours: 10%

    Args:
        transactions: List of normal transaction dicts.
        anomaly_count: Number of transactions to make anomalous.

    Returns:
        Modified transaction list with anomalies injected.
    """
    if anomaly_count <= 0 or not transactions:
        return transactions

    weights = settings.ANOMALY_INJECTION_WEIGHTS
    anomaly_indices = random.sample(range(len(transactions)), min(anomaly_count, len(transactions)))

    # Distribute anomaly types by weight
    anomaly_types = []
    for atype, w in weights.items():
        anomaly_types.extend([atype] * max(1, int(anomaly_count * w)))
    random.shuffle(anomaly_types)

    for i, idx in enumerate(anomaly_indices):
        atype = anomaly_types[i % len(anomaly_types)]
        transactions[idx] = _apply_anomaly(transactions[idx], atype)
        transactions[idx]["is_flagged"] = True

    return transactions


def _apply_anomaly(txn: dict, anomaly_type: str) -> dict:
    """Apply a specific anomaly type to a transaction."""
    if anomaly_type == "high_value":
        txn["amount"] = random.uniform(75000, 500000)

    elif anomaly_type == "odd_hours":
        txn["timestamp"] = random_odd_hour_timestamp()

    elif anomaly_type == "velocity":
        # Mark for velocity — the generator will create rapid successive txns
        txn["_velocity_flag"] = True

    elif anomaly_type == "geo_anomaly":
        # Set city to a random different city
        current_city = txn.get("city", "")
        other_cities = [c for c in INDIAN_CITIES if c != current_city]
        txn["city"] = random.choice(other_cities) if other_cities else "Unknown City"

    elif anomaly_type == "merchant_mismatch":
        # Set category to something unusual
        current_cat = txn.get("merchant_category", "")
        unusual_cats = [c for c in MERCHANT_CATEGORIES if c != current_cat]
        txn["merchant_category"] = random.choice(unusual_cats)
        txn["merchant_name"] = f"Unusual-{txn['merchant_category']}-Store"

    return txn
