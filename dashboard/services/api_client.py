"""FraudShield Dashboard — HTTP Client for API Gateway (Unit 2)

All data flows through REST calls to FastAPI on port 8000.
Endpoints: /api/v1/transactions, /api/v1/analytics, /api/v1/analyze
"""
import httpx
import os
from typing import Dict, Any, Optional

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
_API_PREFIX = "/api/v1"


def _url(path: str) -> str:
    return f"{API_BASE_URL}{_API_PREFIX}{path}"


# ── Transactions ─────────────────────────────────────────────
def get_transactions(
    page: int = 1,
    page_size: int = 50,
    risk_level: Optional[str] = None,
    is_flagged: Optional[bool] = None,
) -> Dict[str, Any]:
    """Fetch paginated transactions with optional filters."""
    params: dict = {"page": page, "page_size": page_size}
    if risk_level and risk_level != "All":
        params["risk_level"] = risk_level
    if is_flagged is not None:
        params["is_flagged"] = str(is_flagged).lower()

    try:
        resp = httpx.get(_url("/transactions/"), params=params, timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.ConnectError:
        return {"error": "Cannot reach API Gateway — is the backend running on port 8000?"}
    except httpx.RequestError as exc:
        return {"error": f"Request failed: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}


def generate_transactions(count: int = 100) -> Dict[str, Any]:
    """Trigger synthetic data generation via API Gateway."""
    try:
        resp = httpx.post(
            _url("/transactions/generate"),
            json={"count": count},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.ConnectError:
        return {"error": "Cannot reach API Gateway — is the backend running on port 8000?"}
    except httpx.RequestError as exc:
        return {"error": f"Request failed: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}


# ── Analytics ────────────────────────────────────────────────
def get_analytics() -> Dict[str, Any]:
    """Fetch aggregated analytics summary."""
    try:
        resp = httpx.get(_url("/analytics/"), timeout=10.0)
        resp.raise_for_status()
        return resp.json()
    except httpx.ConnectError:
        return {"error": "Cannot reach API Gateway — is the backend running on port 8000?"}
    except httpx.RequestError as exc:
        return {"error": f"Request failed: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}


# ── AI Analysis ──────────────────────────────────────────────
def analyze_transaction(transaction_id: str) -> Dict[str, Any]:
    """Request Gemini AI analysis for a specific transaction."""
    try:
        resp = httpx.post(
            _url("/analyze/"),
            json={"transaction_id": transaction_id},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()
    except httpx.ConnectError:
        return {"error": "Cannot reach API Gateway — is the backend running on port 8000?"}
    except httpx.RequestError as exc:
        return {"error": f"Request failed: {exc}"}
    except httpx.HTTPStatusError as exc:
        return {"error": f"HTTP {exc.response.status_code}: {exc.response.text}"}
