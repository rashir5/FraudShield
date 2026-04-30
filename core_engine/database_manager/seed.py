"""
FraudShield - Database Seed Data
Inserts default rule configurations into SQLite3.
"""

import uuid
from datetime import datetime, timezone
from core_engine.database_manager.migrations import RuleConfigModel
from core_engine.config.settings import settings


def get_default_rule_configs() -> list[dict]:
    """Return the default rule configuration seed data."""
    configs = []
    for rule_name, params in settings.DEFAULT_RULE_WEIGHTS.items():
        configs.append({
            "id": str(uuid.uuid4()),
            "rule_name": rule_name,
            "weight": params["weight"],
            "threshold": params["threshold"],
            "is_active": True,
            "updated_at": datetime.now(timezone.utc),
        })
    return configs


def seed_rule_configs(session):
    """
    Insert default rule configurations if the table is empty.

    Args:
        session: Active SQLAlchemy session.

    Returns:
        Number of records inserted.
    """
    existing_count = session.query(RuleConfigModel).count()
    if existing_count > 0:
        return 0

    configs = get_default_rule_configs()
    for config_data in configs:
        rule_config = RuleConfigModel(**config_data)
        session.add(rule_config)

    session.flush()
    return len(configs)
