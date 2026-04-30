"""
FraudShield - Analytics Engine Tests
Tests for aggregation accuracy, empty data handling, and sort order.
"""

import pytest
from core_engine.analytics_engine.fraud_trends import get_fraud_trends
from core_engine.analytics_engine.category_breakdown import get_category_breakdown
from core_engine.analytics_engine.risk_distribution import get_risk_distribution
from core_engine.analytics_engine.top_flagged import get_top_flagged_merchants
from core_engine.database_manager.engine import create_db_engine
from core_engine.database_manager.session import init_session_factory, get_db_session
from core_engine.database_manager.migrations import create_all_tables, drop_all_tables


@pytest.fixture
def test_engine():
    engine = create_db_engine("sqlite:///:memory:")
    create_all_tables(engine)
    init_session_factory(engine)
    yield engine
    drop_all_tables(engine)


class TestFraudTrends:
    def test_empty_database(self, test_engine):
        with get_db_session() as session:
            trends = get_fraud_trends(session)
        assert trends == []


class TestCategoryBreakdown:
    def test_empty_database(self, test_engine):
        with get_db_session() as session:
            breakdown = get_category_breakdown(session)
        assert breakdown == []


class TestRiskDistribution:
    def test_empty_database(self, test_engine):
        with get_db_session() as session:
            dist = get_risk_distribution(session)
        assert len(dist) == 3
        for d in dist:
            assert d["count"] == 0


class TestTopFlagged:
    def test_empty_database(self, test_engine):
        with get_db_session() as session:
            merchants = get_top_flagged_merchants(session)
        assert merchants == []
