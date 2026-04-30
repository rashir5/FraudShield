"""
FraudShield - Database Migrations
Schema creation for all domain entities.
"""

from sqlalchemy import (
    Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone

Base = declarative_base()


class TransactionModel(Base):
    """Banking transaction record — Indian BFSI context."""
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
    transaction_type = Column(String(10), nullable=False)  # Credit / Debit
    is_flagged = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    risk_score = relationship("RiskScoreModel", back_populates="transaction", uselist=False)
    rule_results = relationship("RuleResultModel", back_populates="transaction")
    ai_analysis = relationship("AIAnalysisModel", back_populates="transaction", uselist=False)


class RiskScoreModel(Base):
    """Aggregated weighted risk score for a transaction."""
    __tablename__ = "risk_scores"

    id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False, unique=True, index=True)
    final_score = Column(Float, nullable=False)
    risk_level = Column(String(10), nullable=False)  # LOW / MEDIUM / HIGH
    rules_triggered = Column(Integer, default=0)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    transaction = relationship("TransactionModel", back_populates="risk_score")


class RuleConfigModel(Base):
    """Runtime-configurable fraud detection rule settings."""
    __tablename__ = "rule_config"

    id = Column(String, primary_key=True)
    rule_name = Column(String(50), unique=True, nullable=False, index=True)
    weight = Column(Float, nullable=False, default=0.20)
    threshold = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class RuleResultModel(Base):
    """Per-rule evaluation result for a single transaction."""
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
    """Optional AI-powered deep analysis for flagged transactions."""
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


def create_all_tables(engine):
    """Create all tables defined in the Base metadata."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables(engine):
    """Drop all tables — use only for testing."""
    Base.metadata.drop_all(bind=engine)
