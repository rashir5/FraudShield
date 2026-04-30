"""
FraudShield - Synthetic Data Generator
Generates 1,000 localized INR transactions with weighted anomaly injection.
"""

import uuid
import random
from core_engine.config.settings import settings
from core_engine.synthetic_generator.indian_context import (
    INDIAN_BANKS, INDIAN_CITIES, ACCOUNT_HOLDERS,
    random_ist_timestamp, random_merchant, random_account_number,
)
from core_engine.synthetic_generator.anomaly_injector import inject_anomalies


def generate_transactions(count: int = None) -> list[dict]:
    """
    Generate synthetic banking transactions in the Indian BFSI context.

    Args:
        count: Number of transactions to generate. Defaults to settings value (1000).

    Returns:
        List of transaction dictionaries ready for database insertion.
    """
    count = count or settings.SYNTHETIC_TRANSACTION_COUNT
    anomaly_count = int(count * settings.ANOMALY_PERCENTAGE)

    # Create a pool of accounts for realistic history patterns
    num_accounts = max(20, count // 50)
    accounts = [
        {
            "account_number": random_account_number(),
            "account_holder": random.choice(ACCOUNT_HOLDERS),
            "bank_name": random.choice(INDIAN_BANKS),
            "home_city": random.choice(INDIAN_CITIES[:10]),  # Primary cities
            "preferred_categories": random.sample(
                ["Groceries", "Electronics", "Fuel", "Restaurants", "Utilities"],
                k=random.randint(2, 4)
            ),
        }
        for _ in range(num_accounts)
    ]

    # Generate normal transactions
    transactions = []
    for i in range(count):
        account = random.choice(accounts)
        merchant_name, merchant_category = random_merchant(
            random.choice(account["preferred_categories"])
        )
        txn = {
            "id": str(uuid.uuid4()),
            "account_number": account["account_number"],
            "account_holder": account["account_holder"],
            "amount": round(random.uniform(100, 45000), 2),  # Normal range in INR
            "timestamp": random_ist_timestamp(),
            "city": account["home_city"],
            "merchant_name": merchant_name,
            "merchant_category": merchant_category,
            "bank_name": account["bank_name"],
            "transaction_type": random.choice(["Credit", "Debit"]),
            "is_flagged": False,
        }
        transactions.append(txn)

    # Inject anomalies with weighted distribution
    transactions = inject_anomalies(transactions, anomaly_count)

    return transactions
