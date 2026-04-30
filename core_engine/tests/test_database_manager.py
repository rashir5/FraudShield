"""
FraudShield - Database Manager Tests
Tests for engine creation, table creation, seeding, and session management.
"""

import pytest
from core_engine.database_manager.engine import create_db_engine
from core_engine.database_manager.session import init_session_factory, get_db_session
from core_engine.database_manager.migrations import create_all_tables, drop_all_tables, RuleConfigModel
from core_engine.database_manager.seed import seed_rule_configs


@pytest.fixture
def test_engine():
    """Create an in-memory SQLite engine for testing."""
    engine = create_db_engine("sqlite:///:memory:")
    create_all_tables(engine)
    init_session_factory(engine)
    yield engine
    drop_all_tables(engine)


class TestDatabaseEngine:
    def test_engine_creation(self, test_engine):
        assert test_engine is not None

    def test_tables_created(self, test_engine):
        table_names = test_engine.table_names() if hasattr(test_engine, 'table_names') else []
        # Verify via inspector
        from sqlalchemy import inspect
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "transactions" in tables
        assert "risk_scores" in tables
        assert "rule_config" in tables
        assert "rule_results" in tables
        assert "ai_analyses" in tables


class TestSessionManagement:
    def test_session_context_manager(self, test_engine):
        with get_db_session() as session:
            assert session is not None

    def test_session_commit(self, test_engine):
        with get_db_session() as session:
            count = seed_rule_configs(session)
            assert count == 5

        with get_db_session() as session:
            rules = session.query(RuleConfigModel).all()
            assert len(rules) == 5


class TestSeedData:
    def test_seed_inserts_five_rules(self, test_engine):
        with get_db_session() as session:
            count = seed_rule_configs(session)
        assert count == 5

    def test_seed_idempotent(self, test_engine):
        with get_db_session() as session:
            seed_rule_configs(session)
        with get_db_session() as session:
            count = seed_rule_configs(session)
        assert count == 0  # Already seeded

    def test_seed_rule_names(self, test_engine):
        with get_db_session() as session:
            seed_rule_configs(session)
        with get_db_session() as session:
            names = {r.rule_name for r in session.query(RuleConfigModel).all()}
        assert names == {"high_value", "odd_hours", "velocity", "geo_anomaly", "merchant_mismatch"}
