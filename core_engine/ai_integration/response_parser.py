"""
FraudShield - AI Response Parser
Parses raw Gemini API output into structured analysis fields.
"""

import json
import logging

logger = logging.getLogger(__name__)


def parse_gemini_response(raw_text: str) -> dict:
    """
    Parse the raw Gemini response text into structured fields.

    Expected format: JSON with pattern_explanation, top_risk_factors, recommendation.

    Args:
        raw_text: Raw text response from Gemini API.

    Returns:
        Dict with parsed fields. Falls back to raw text on parse failure.
    """
    if not raw_text:
        return _empty_result()

    # Try to extract JSON from response (may be wrapped in markdown code blocks)
    cleaned = _clean_json_text(raw_text)

    try:
        parsed = json.loads(cleaned)
        return {
            "pattern_explanation": parsed.get("pattern_explanation", ""),
            "top_risk_factors": _format_risk_factors(parsed.get("top_risk_factors", [])),
            "recommendation": parsed.get("recommendation", ""),
        }
    except json.JSONDecodeError:
        logger.warning("Failed to parse Gemini response as JSON, using raw text")
        return {
            "pattern_explanation": raw_text[:500],
            "top_risk_factors": "Unable to parse structured factors",
            "recommendation": "Manual review recommended — AI response could not be parsed",
        }


def _clean_json_text(text: str) -> str:
    """Remove markdown code block markers and whitespace from JSON text."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def _format_risk_factors(factors) -> str:
    """Convert risk factors list to a formatted string."""
    if isinstance(factors, list):
        return " | ".join(str(f) for f in factors[:3])
    return str(factors)


def _empty_result() -> dict:
    """Return an empty analysis result."""
    return {
        "pattern_explanation": "",
        "top_risk_factors": "",
        "recommendation": "",
    }
