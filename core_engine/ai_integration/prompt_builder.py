"""
FraudShield - AI Prompt Builder
Compiles Indian banking context prompts for the Gemini API.
"""


def build_analysis_prompt(
    transaction: dict,
    rule_results: list[dict],
    risk_score: float,
    risk_level: str,
) -> str:
    """
    Build a structured prompt for Gemini AI analysis.

    Args:
        transaction: Transaction data dict.
        rule_results: List of rule evaluation results.
        risk_score: Final weighted risk score.
        risk_level: Classified risk level.

    Returns:
        Formatted prompt string.
    """
    triggered_rules = [r for r in rule_results if r.get("triggered")]
    top_3 = sorted(triggered_rules, key=lambda r: r.get("weighted_score", 0), reverse=True)[:3]

    top_3_text = "\n".join([
        f"  - {r['rule_name']}: Score {r['raw_score']}, Weight {r['weighted_score']} — {r.get('details', '')}"
        for r in top_3
    ]) if top_3 else "  No rules triggered."

    prompt = f"""You are an AI fraud detection analyst specializing in Indian banking (BFSI sector).

CONTEXT: Analyze the following Indian banking transaction for potential fraud patterns.

TRANSACTION DETAILS:
- Transaction ID: {transaction.get('id', 'N/A')}
- Account: {transaction.get('account_number', 'N/A')} ({transaction.get('account_holder', 'N/A')})
- Amount: ₹{transaction.get('amount', 0):,.2f}
- Timestamp: {transaction.get('timestamp', 'N/A')} IST
- City: {transaction.get('city', 'N/A')}
- Merchant: {transaction.get('merchant_name', 'N/A')} ({transaction.get('merchant_category', 'N/A')})
- Bank: {transaction.get('bank_name', 'N/A')}
- Type: {transaction.get('transaction_type', 'N/A')}

RISK ASSESSMENT:
- Final Score: {risk_score}/100 ({risk_level})
- Rules Triggered: {len(triggered_rules)} of {len(rule_results)}

TOP 3 CONTRIBUTING FACTORS:
{top_3_text}

REQUIRED OUTPUT FORMAT (respond in JSON):
{{
  "pattern_explanation": "Detailed natural language explanation of the detected fraud pattern in the Indian banking context",
  "top_risk_factors": ["Factor 1 with reasoning", "Factor 2 with reasoning", "Factor 3 with reasoning"],
  "recommendation": "BLOCK / MONITOR / ALLOW — with specific reasoning for Indian banking compliance"
}}"""
    return prompt
