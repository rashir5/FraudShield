"""
FraudShield - AI Integration Tests
Tests for prompt building, response parsing, and error fallback.
"""

import pytest
from core_engine.ai_integration.prompt_builder import build_analysis_prompt
from core_engine.ai_integration.response_parser import parse_gemini_response


class TestPromptBuilder:
    def test_prompt_contains_transaction_data(self):
        txn = {
            "id": "test-123", "account_number": "123456789012",
            "account_holder": "Test User", "amount": 75000,
            "timestamp": "2026-01-01T10:00:00", "city": "Mumbai",
            "merchant_name": "Test Shop", "merchant_category": "Electronics",
            "bank_name": "HDFC Bank", "transaction_type": "Debit",
        }
        rules = [{"rule_name": "high_value", "triggered": True, "raw_score": 75, "weighted_score": 15, "details": "High amount"}]
        prompt = build_analysis_prompt(txn, rules, 75.0, "HIGH")

        assert "₹75,000.00" in prompt
        assert "Mumbai" in prompt
        assert "HIGH" in prompt
        assert "Indian banking" in prompt.lower() or "BFSI" in prompt

    def test_prompt_includes_top_3_factors(self):
        rules = [
            {"rule_name": "velocity", "triggered": True, "raw_score": 90, "weighted_score": 27, "details": "Rapid txns"},
            {"rule_name": "geo_anomaly", "triggered": True, "raw_score": 90, "weighted_score": 22.5, "details": "Unknown city"},
            {"rule_name": "high_value", "triggered": True, "raw_score": 80, "weighted_score": 16, "details": "High amt"},
            {"rule_name": "odd_hours", "triggered": False, "raw_score": 0, "weighted_score": 0, "details": ""},
        ]
        txn = {"id": "x", "amount": 100000}
        prompt = build_analysis_prompt(txn, rules, 85.0, "HIGH")
        assert "velocity" in prompt
        assert "geo_anomaly" in prompt


class TestResponseParser:
    def test_parse_valid_json(self):
        raw = '{"pattern_explanation": "Test pattern", "top_risk_factors": ["Factor 1", "Factor 2"], "recommendation": "BLOCK"}'
        result = parse_gemini_response(raw)
        assert result["pattern_explanation"] == "Test pattern"
        assert "Factor 1" in result["top_risk_factors"]
        assert result["recommendation"] == "BLOCK"

    def test_parse_json_in_code_block(self):
        raw = '```json\n{"pattern_explanation": "Test", "top_risk_factors": [], "recommendation": "ALLOW"}\n```'
        result = parse_gemini_response(raw)
        assert result["recommendation"] == "ALLOW"

    def test_fallback_on_invalid_json(self):
        raw = "This is not valid JSON"
        result = parse_gemini_response(raw)
        assert "This is not valid JSON" in result["pattern_explanation"]
        assert result["recommendation"] != ""

    def test_empty_input(self):
        result = parse_gemini_response("")
        assert result["pattern_explanation"] == ""
