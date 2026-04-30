"""
FraudShield - Gemini API Client
HTTPS client with 5-second timeout and structured error fallback.
"""

import httpx
import time
import logging
from core_engine.config.settings import settings

logger = logging.getLogger(__name__)

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


async def call_gemini(prompt: str) -> dict:
    """
    Send a prompt to the Gemini API and return the raw response.

    Args:
        prompt: Compiled prompt string.

    Returns:
        Dict with 'success', 'response_text', 'response_time_ms', and optionally 'error'.
    """
    if not settings.GEMINI_API_KEY:
        return {
            "success": False,
            "response_text": "",
            "response_time_ms": 0,
            "error": "GEMINI_API_KEY not configured",
        }

    url = GEMINI_API_URL.format(model=settings.GEMINI_MODEL)
    headers = {"Content-Type": "application/json"}
    params = {"key": settings.GEMINI_API_KEY}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024,
        },
    }

    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=settings.GEMINI_TIMEOUT_SECONDS) as client:
            response = await client.post(url, json=payload, headers=headers, params=params)
            elapsed_ms = (time.time() - start_time) * 1000

            if response.status_code == 200:
                data = response.json()
                text = _extract_text(data)
                return {
                    "success": True,
                    "response_text": text,
                    "response_time_ms": round(elapsed_ms, 2),
                    "error": None,
                }
            else:
                return {
                    "success": False,
                    "response_text": "",
                    "response_time_ms": round(elapsed_ms, 2),
                    "error": f"API returned status {response.status_code}: {response.text[:200]}",
                }
    except httpx.TimeoutException:
        elapsed_ms = (time.time() - start_time) * 1000
        logger.warning(f"Gemini API timeout after {elapsed_ms:.0f}ms")
        return {
            "success": False,
            "response_text": "",
            "response_time_ms": round(elapsed_ms, 2),
            "error": f"Timeout after {settings.GEMINI_TIMEOUT_SECONDS}s",
        }
    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        logger.error(f"Gemini API error: {e}")
        return {
            "success": False,
            "response_text": "",
            "response_time_ms": round(elapsed_ms, 2),
            "error": str(e),
        }


def _extract_text(api_response: dict) -> str:
    """Extract text content from Gemini API response structure."""
    try:
        candidates = api_response.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "")
    except (IndexError, KeyError, TypeError):
        pass
    return ""
