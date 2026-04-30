"""FraudShield - AI Client Integration"""
import json, httpx, time, logging
from core import settings

logger = logging.getLogger(__name__)

def build_analysis_prompt(transaction, rule_results, risk_score, risk_level) -> str:
    triggered = [r for r in rule_results if r.get("triggered")]
    top_3 = sorted(triggered, key=lambda r: r.get("weighted_score", 0), reverse=True)[:3]
    t3t = "\n".join([f"  - {r['rule_name']}: Score {r['raw_score']}, Weight {r['weighted_score']} — {r.get('details', '')}" for r in top_3]) if top_3 else "  No rules triggered."
    
    return f"""You are an AI fraud detection analyst specializing in Indian banking (BFSI sector).
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
- Rules Triggered: {len(triggered)} of {len(rule_results)}
TOP 3 CONTRIBUTING FACTORS:
{t3t}
REQUIRED OUTPUT FORMAT (respond in JSON):
{{
  "pattern_explanation": "Detailed natural language explanation",
  "top_risk_factors": ["Factor 1", "Factor 2", "Factor 3"],
  "recommendation": "BLOCK / MONITOR / ALLOW"
}}"""

async def call_gemini(prompt: str) -> dict:
    if not settings.GEMINI_API_KEY:
        return {"success": False, "response_text": "", "response_time_ms": 0, "error": "GEMINI_API_KEY not configured"}
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1024}}
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=settings.GEMINI_TIMEOUT_SECONDS) as client:
            resp = await client.post(url, json=payload, headers={"Content-Type": "application/json"}, params={"key": settings.GEMINI_API_KEY})
            ms = round((time.time() - start) * 1000, 2)
            if resp.status_code == 200:
                data = resp.json()
                text = ""
                try: text = data.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text", "")
                except: pass
                return {"success": True, "response_text": text, "response_time_ms": ms, "error": None}
            return {"success": False, "response_text": "", "response_time_ms": ms, "error": f"API {resp.status_code}: {resp.text[:200]}"}
    except Exception as e:
        return {"success": False, "response_text": "", "response_time_ms": round((time.time() - start)*1000, 2), "error": str(e)}

def parse_gemini_response(raw_text: str) -> dict:
    if not raw_text: return {"pattern_explanation": "", "top_risk_factors": "", "recommendation": ""}
    text = raw_text.strip()
    if text.startswith("```json"): text = text[7:]
    elif text.startswith("```"): text = text[3:]
    if text.endswith("```"): text = text[:-3]
    text = text.strip()
    try:
        parsed = json.loads(text)
        factors = parsed.get("top_risk_factors", [])
        return {
            "pattern_explanation": parsed.get("pattern_explanation", ""),
            "top_risk_factors": " | ".join(str(f) for f in factors[:3]) if isinstance(factors, list) else str(factors),
            "recommendation": parsed.get("recommendation", "")
        }
    except:
        return {"pattern_explanation": raw_text[:500], "top_risk_factors": "Unparseable", "recommendation": "Manual review"}
