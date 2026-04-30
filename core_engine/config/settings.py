"""
FraudShield Core Engine - Configuration Settings
Loads environment variables and provides default configuration values.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from project root
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings:
    """Central configuration for the FraudShield Core Engine."""

    # --- Database ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///fraudshield.db")

    # --- Gemini AI ---
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_TIMEOUT_SECONDS: int = int(os.getenv("GEMINI_TIMEOUT_SECONDS", "5"))
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    # --- Server ---
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # --- Scoring Defaults ---
    RISK_LOW_MAX: int = 30
    RISK_MEDIUM_MAX: int = 69
    RISK_HIGH_MIN: int = 70

    # --- Batch Processing ---
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))

    # --- Synthetic Data ---
    SYNTHETIC_TRANSACTION_COUNT: int = 1000
    ANOMALY_PERCENTAGE: float = 0.05

    # --- Rule Severity Order (for tie-breaking, 1 = highest) ---
    RULE_SEVERITY_ORDER: dict = {
        "velocity": 1,
        "geo_anomaly": 2,
        "high_value": 3,
        "merchant_mismatch": 4,
        "odd_hours": 5,
    }

    # --- Default Rule Weights ---
    DEFAULT_RULE_WEIGHTS: dict = {
        "high_value": {"weight": 0.20, "threshold": 50000.0},
        "odd_hours": {"weight": 0.10, "threshold": 5.0},
        "velocity": {"weight": 0.30, "threshold": 3.0},
        "geo_anomaly": {"weight": 0.25, "threshold": 3.0},
        "merchant_mismatch": {"weight": 0.15, "threshold": 5.0},
    }

    # --- Anomaly Injection Weights ---
    ANOMALY_INJECTION_WEIGHTS: dict = {
        "velocity": 0.30,
        "high_value": 0.25,
        "geo_anomaly": 0.20,
        "merchant_mismatch": 0.15,
        "odd_hours": 0.10,
    }


settings = Settings()
