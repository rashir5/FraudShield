"""
FraudShield - Pydantic Schemas
Request/response models for API serialization and validation.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Transaction Schemas ---
class TransactionSchema(BaseModel):
    id: str
    account_number: str
    account_holder: str
    amount: float = Field(gt=0, description="Transaction amount in INR")
    timestamp: datetime
    city: str
    merchant_name: str
    merchant_category: str
    bank_name: str
    transaction_type: str = Field(pattern="^(Credit|Debit)$")
    is_flagged: bool = False
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    transactions: list[TransactionSchema]
    total: int
    page: int
    page_size: int


# --- Risk Score Schemas ---
class RiskScoreSchema(BaseModel):
    id: str
    transaction_id: str
    final_score: float = Field(ge=0, le=100)
    risk_level: str = Field(pattern="^(LOW|MEDIUM|HIGH)$")
    rules_triggered: int
    calculated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Rule Config Schemas ---
class RuleConfigSchema(BaseModel):
    id: str
    rule_name: str
    weight: float = Field(gt=0, le=1.0)
    threshold: float = Field(gt=0)
    is_active: bool = True
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RuleConfigUpdateRequest(BaseModel):
    weight: Optional[float] = Field(default=None, gt=0, le=1.0)
    threshold: Optional[float] = Field(default=None, gt=0)
    is_active: Optional[bool] = None


# --- Rule Result Schemas ---
class RuleResultSchema(BaseModel):
    id: str
    transaction_id: str
    rule_name: str
    triggered: bool
    raw_score: float
    weighted_score: float
    details: str = ""

    class Config:
        from_attributes = True


# --- AI Analysis Schemas ---
class AIAnalysisRequest(BaseModel):
    transaction_id: str


class AIAnalysisSchema(BaseModel):
    id: str
    transaction_id: str
    pattern_explanation: str
    top_risk_factors: str
    recommendation: str
    response_time_ms: float
    analyzed_at: Optional[datetime] = None
    ai_status: str = "success"

    class Config:
        from_attributes = True


class AIAnalysisErrorResponse(BaseModel):
    transaction_id: str
    ai_status: str = "unavailable"
    error_message: str
    rule_results: list[RuleResultSchema] = []
    risk_score: Optional[RiskScoreSchema] = None


# --- Analytics Schemas ---
class FraudTrendPoint(BaseModel):
    period: str
    total_transactions: int
    flagged_count: int
    fraud_rate: float


class CategoryBreakdown(BaseModel):
    category: str
    transaction_count: int
    flagged_count: int
    average_risk_score: float


class RiskDistribution(BaseModel):
    risk_level: str
    count: int
    percentage: float


class TopFlaggedMerchant(BaseModel):
    merchant_name: str
    flagged_count: int
    average_risk_score: float


class AnalyticsSummary(BaseModel):
    fraud_trends: list[FraudTrendPoint]
    category_breakdown: list[CategoryBreakdown]
    risk_distribution: list[RiskDistribution]
    top_flagged_merchants: list[TopFlaggedMerchant]


# --- Generation Schemas ---
class GenerateRequest(BaseModel):
    count: int = Field(default=1000, ge=1, le=5000)


class GenerateResponse(BaseModel):
    message: str
    transactions_created: int
    flagged_count: int
