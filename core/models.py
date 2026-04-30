"""FraudShield - ORM Models and Schemas"""
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class TransactionModel(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True)
    account_number = Column(String(16), nullable=False, index=True)
    account_holder = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False, index=True)
    city = Column(String(50), nullable=False)
    merchant_name = Column(String(100), nullable=False)
    merchant_category = Column(String(50), nullable=False, index=True)
    bank_name = Column(String(100), nullable=False)
    transaction_type = Column(String(10), nullable=False)
    is_flagged = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    risk_score = relationship("RiskScoreModel", back_populates="transaction", uselist=False)
    rule_results = relationship("RuleResultModel", back_populates="transaction")
    ai_analysis = relationship("AIAnalysisModel", back_populates="transaction", uselist=False)

class RiskScoreModel(Base):
    __tablename__ = "risk_scores"
    id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False, unique=True, index=True)
    final_score = Column(Float, nullable=False)
    risk_level = Column(String(10), nullable=False)
    rules_triggered = Column(Integer, default=0)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    transaction = relationship("TransactionModel", back_populates="risk_score")

class RuleConfigModel(Base):
    __tablename__ = "rule_config"
    id = Column(String, primary_key=True)
    rule_name = Column(String(50), unique=True, nullable=False, index=True)
    weight = Column(Float, nullable=False, default=0.20)
    threshold = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RuleResultModel(Base):
    __tablename__ = "rule_results"
    id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False, index=True)
    rule_name = Column(String(50), nullable=False, index=True)
    triggered = Column(Boolean, default=False)
    raw_score = Column(Float, default=0.0)
    weighted_score = Column(Float, default=0.0)
    details = Column(Text, default="")
    transaction = relationship("TransactionModel", back_populates="rule_results")

class AIAnalysisModel(Base):
    __tablename__ = "ai_analyses"
    id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False, unique=True, index=True)
    prompt_sent = Column(Text, nullable=False)
    response_raw = Column(Text, default="")
    pattern_explanation = Column(Text, default="")
    top_risk_factors = Column(Text, default="")
    recommendation = Column(Text, default="")
    response_time_ms = Column(Float, default=0.0)
    analyzed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    transaction = relationship("TransactionModel", back_populates="ai_analysis")

class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String, primary_key=True)
    actor_id = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    component = Column(String(50), nullable=False)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TransactionSchema(BaseModel):
    id: str
    account_number: str
    account_holder: str
    amount: float = Field(gt=0)
    timestamp: datetime
    city: str
    merchant_name: str
    merchant_category: str
    bank_name: str
    transaction_type: str
    is_flagged: bool = False
    created_at: Optional[datetime] = None
    class Config: from_attributes = True

class TransactionListResponse(BaseModel):
    transactions: list[TransactionSchema]
    total: int
    page: int
    page_size: int

class RiskScoreSchema(BaseModel):
    id: str
    transaction_id: str
    final_score: float = Field(ge=0, le=100)
    risk_level: str
    rules_triggered: int
    calculated_at: Optional[datetime] = None
    class Config: from_attributes = True

class RuleConfigSchema(BaseModel):
    id: str
    rule_name: str
    weight: float = Field(gt=0, le=1.0)
    threshold: float = Field(gt=0)
    is_active: bool = True
    updated_at: Optional[datetime] = None
    class Config: from_attributes = True

class RuleConfigUpdateRequest(BaseModel):
    weight: Optional[float] = Field(default=None, gt=0, le=1.0)
    threshold: Optional[float] = Field(default=None, gt=0)
    is_active: Optional[bool] = None

class RuleResultSchema(BaseModel):
    id: str
    transaction_id: str
    rule_name: str
    triggered: bool
    raw_score: float
    weighted_score: float
    details: str = ""
    class Config: from_attributes = True

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
    class Config: from_attributes = True

class AIAnalysisErrorResponse(BaseModel):
    transaction_id: str
    ai_status: str = "unavailable"
    error_message: str
    rule_results: list[RuleResultSchema] = []
    risk_score: Optional[RiskScoreSchema] = None

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

class GenerateRequest(BaseModel):
    count: int = Field(default=1000, ge=1, le=5000)

class GenerateResponse(BaseModel):
    message: str
    transactions_created: int
    flagged_count: int

# --- Security Schemas ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AuditLogSchema(BaseModel):
    id: str
    actor_id: str
    action: str
    component: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    timestamp: datetime
    class Config: from_attributes = True
