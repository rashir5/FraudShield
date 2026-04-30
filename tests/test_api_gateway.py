from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_generation():
    response = client.post("/api/v1/transactions/generate", json={"count": 5})
    assert response.status_code == 200
    data = response.json()
    assert "transactions_created" in data
    assert data["transactions_created"] == 5

def test_api_list_transactions():
    response = client.get("/api/v1/transactions/")
    assert response.status_code == 200
    assert "transactions" in response.json()

def test_api_analytics():
    response = client.get("/api/v1/analytics/")
    assert response.status_code == 200
    data = response.json()
    assert "fraud_trends" in data
    assert "category_breakdown" in data

def test_api_ai_analysis_boundary():
    # Attempting to analyze a non-existent transaction should cleanly return 404 validation
    response = client.post("/api/v1/analyze/", json={"transaction_id": "invalid-id-boundary-check"})
    assert response.status_code == 404
