"""Tests for FraudShield Dashboard — API Client layer.

All tests mock httpx at the transport level to validate that the
client correctly constructs URLs, parses responses, and handles errors
without requiring a live backend.
"""
import pytest
from unittest.mock import patch, MagicMock
from dashboard.services.api_client import (
    get_transactions,
    generate_transactions,
    get_analytics,
    analyze_transaction,
    _url,
)
import httpx


# ── Helper to build a mock response ─────────────────────────
def _mock_response(json_data: dict, status_code: int = 200):
    resp = MagicMock(spec=httpx.Response)
    resp.status_code = status_code
    resp.json.return_value = json_data
    resp.raise_for_status.return_value = None
    resp.text = ""
    return resp


class TestURLConstruction:
    def test_url_prefix(self):
        assert _url("/transactions/") == "http://127.0.0.1:8000/api/v1/transactions/"

    def test_url_analytics(self):
        assert _url("/analytics/") == "http://127.0.0.1:8000/api/v1/analytics/"


class TestGetTransactions:
    @patch("dashboard.services.api_client.httpx.get")
    def test_success_returns_json(self, mock_get):
        mock_get.return_value = _mock_response(
            {"transactions": [{"id": "t1"}], "total": 1, "page": 1, "page_size": 50}
        )
        result = get_transactions()
        assert "transactions" in result
        assert result["total"] == 1
        mock_get.assert_called_once()

    @patch("dashboard.services.api_client.httpx.get")
    def test_passes_risk_filter(self, mock_get):
        mock_get.return_value = _mock_response({"transactions": [], "total": 0})
        get_transactions(risk_level="HIGH")
        call_kwargs = mock_get.call_args
        assert "HIGH" in str(call_kwargs)

    @patch("dashboard.services.api_client.httpx.get")
    def test_connect_error_returns_friendly_message(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")
        result = get_transactions()
        assert "error" in result
        assert "port 8000" in result["error"]


class TestGenerateTransactions:
    @patch("dashboard.services.api_client.httpx.post")
    def test_success(self, mock_post):
        mock_post.return_value = _mock_response(
            {"message": "ok", "transactions_created": 100, "flagged_count": 12}
        )
        result = generate_transactions(100)
        assert result["transactions_created"] == 100
        assert result["flagged_count"] == 12

    @patch("dashboard.services.api_client.httpx.post")
    def test_connect_error(self, mock_post):
        mock_post.side_effect = httpx.ConnectError("refused")
        result = generate_transactions(50)
        assert "error" in result


class TestGetAnalytics:
    @patch("dashboard.services.api_client.httpx.get")
    def test_success(self, mock_get):
        payload = {
            "fraud_trends": [{"period": "2026-04-10", "total_transactions": 100, "flagged_count": 5, "fraud_rate": 5.0}],
            "risk_distribution": [{"risk_level": "LOW", "count": 80, "percentage": 80.0}],
            "category_breakdown": [],
            "top_flagged_merchants": [],
        }
        mock_get.return_value = _mock_response(payload)
        result = get_analytics()
        assert "fraud_trends" in result
        assert result["risk_distribution"][0]["risk_level"] == "LOW"


class TestAnalyzeTransaction:
    @patch("dashboard.services.api_client.httpx.post")
    def test_success(self, mock_post):
        mock_post.return_value = _mock_response({
            "transaction_id": "txn_1",
            "pattern_explanation": "Suspicious velocity",
            "top_risk_factors": "Rapid transactions",
            "recommendation": "Block card",
            "response_time_ms": 245.3,
        })
        result = analyze_transaction("txn_1")
        assert result["pattern_explanation"] == "Suspicious velocity"
        assert result["response_time_ms"] == 245.3

    @patch("dashboard.services.api_client.httpx.post")
    def test_http_404(self, mock_post):
        resp = MagicMock(spec=httpx.Response)
        resp.status_code = 404
        resp.text = "Not Found"
        mock_post.return_value = resp
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not Found", request=MagicMock(), response=resp
        )
        result = analyze_transaction("bad_id")
        assert "error" in result
        assert "404" in result["error"]
