"""FraudShield API - Pydantic Schemas"""
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class TransactionSchema(BaseModel):
    id: str
    account_number: str
    amount: float
    timestamp: datetime
    city: str
    merchant_name: str
    merchant_category: str
    account_holder: str
    bank_name: str
    is_flagged: bool = False
    
    model_config = ConfigDict(from_attributes=True)

class RiskScoreSchema(BaseModel):
    transaction_id: str
    final_score: int
    risk_level: str
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedTransactionResponse(BaseModel):
    page: int
    page_size: int
    total: int
    transactions: List[TransactionSchema]

class GenerateRequest(BaseModel):
    count: int = 1000

class GenerateResponse(BaseModel):
    message: str
    transactions_created: int
    flagged_count: int

class AIAnalysisRequest(BaseModel):
    transaction_id: str

class AIAnalysisSchema(BaseModel):
    transaction_id: str
    pattern_explanation: str
    top_risk_factors: str
    recommendation: str
    response_time_ms: float
    
    model_config = ConfigDict(from_attributes=True)
