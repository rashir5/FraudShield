"""
FraudShield - Internal HTTP Server Tests
Endpoint integration tests using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from core_engine.http_server.server import app
from core_engine.database_manager.engine import create_db_engine
from core_engine.database_manager.session import init_session_factory
from core_engine.database_manager.migrations import create_all_tables, drop_all_tables
from core_engine.database_manager.seed import seed_rule_configs
from core_engine.database_manager.session import get_db_session


@pytest.fixture(autouse=True)
def setup_test_db():
    """Set up in-memory database for each test."""
    engine = create_db_engine("sqlite:///:memory:")
    create_all_tables(engine)
    init_session_factory(engine)
    with get_db_session() as session:
        seed_rule_configs(session)
    yield
    drop_all_tables(engine)


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestTransactionEndpoints:
    def test_list_empty_transactions(self, client):
        response = client.get("/api/v1/transactions")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["transactions"] == []

    def test_get_nonexistent_transaction(self, client):
        response = client.get("/api/v1/transactions/nonexistent-id")
        assert response.status_code == 404


class TestRuleEndpoints:
    def test_list_rules(self, client):
        response = client.get("/api/v1/rules")
        assert response.status_code == 200
        rules = response.json()
        assert len(rules) == 5

    def test_update_rule(self, client):
        response = client.put(
            "/api/v1/rules/high_value",
            json={"weight": 0.25, "threshold": 75000.0}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["weight"] == 0.25
        assert data["threshold"] == 75000.0

    def test_update_nonexistent_rule(self, client):
        response = client.put("/api/v1/rules/fake_rule", json={"weight": 0.5})
        assert response.status_code == 404


class TestAnalyticsEndpoint:
    def test_analytics_empty_db(self, client):
        response = client.get("/api/v1/analytics")
        assert response.status_code == 200
        data = response.json()
        assert "fraud_trends" in data
        assert "risk_distribution" in data


class TestGenerateEndpoint:
    def test_generate_transactions(self, client):
        response = client.post("/api/v1/transactions/generate", json={"count": 50})
        assert response.status_code == 200
        data = response.json()
        assert data["transactions_created"] == 50
