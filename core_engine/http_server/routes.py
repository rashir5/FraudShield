"""
FraudShield - Internal HTTP Server Routes
FastAPI route definitions exposing all core engine functions.
"""

import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from core_engine.database_manager.session import get_db_session
from core_engine.database_manager.migrations import (
    TransactionModel, RiskScoreModel, RuleConfigModel, RuleResultModel, AIAnalysisModel,
)
from core_engine.schemas.pydantic_schemas import (
    TransactionSchema, TransactionListResponse, RiskScoreSchema,
    RuleConfigSchema, RuleConfigUpdateRequest, RuleResultSchema,
    AIAnalysisSchema, AIAnalysisErrorResponse, AIAnalysisRequest,
    AnalyticsSummary, GenerateRequest, GenerateResponse,
)
from core_engine.synthetic_generator.generator import generate_transactions
from core_engine.risk_scorer.batch_processor import process_all_in_batches
from core_engine.analytics_engine.fraud_trends import get_fraud_trends
from core_engine.analytics_engine.category_breakdown import get_category_breakdown
from core_engine.analytics_engine.risk_distribution import get_risk_distribution
from core_engine.analytics_engine.top_flagged import get_top_flagged_merchants
from core_engine.ai_integration.prompt_builder import build_analysis_prompt
from core_engine.ai_integration.gemini_client import call_gemini
from core_engine.ai_integration.response_parser import parse_gemini_response

router = APIRouter(prefix="/api/v1")


# --- Transaction Endpoints ---
@router.get("/transactions", response_model=TransactionListResponse)
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    risk_level: str = Query(None, pattern="^(LOW|MEDIUM|HIGH)$"),
    is_flagged: bool = Query(None),
):
    """List transactions with pagination and optional filters."""
    with get_db_session() as session:
        query = session.query(TransactionModel)

        if is_flagged is not None:
            query = query.filter(TransactionModel.is_flagged == is_flagged)

        if risk_level:
            query = (
                query.join(RiskScoreModel, RiskScoreModel.transaction_id == TransactionModel.id)
                .filter(RiskScoreModel.risk_level == risk_level)
            )

        total = query.count()
        transactions = (
            query.order_by(TransactionModel.timestamp.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return TransactionListResponse(
            transactions=[TransactionSchema.model_validate(t) for t in transactions],
            total=total,
            page=page,
            page_size=page_size,
        )


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    """Get a single transaction with its risk score and rule results."""
    with get_db_session() as session:
        txn = session.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if not txn:
            raise HTTPException(status_code=404, detail="Transaction not found")

        risk = session.query(RiskScoreModel).filter(RiskScoreModel.transaction_id == transaction_id).first()
        rules = session.query(RuleResultModel).filter(RuleResultModel.transaction_id == transaction_id).all()

        return {
            "transaction": TransactionSchema.model_validate(txn),
            "risk_score": RiskScoreSchema.model_validate(risk) if risk else None,
            "rule_results": [RuleResultSchema.model_validate(r) for r in rules],
        }


# --- Synthetic Data Generation ---
@router.post("/transactions/generate", response_model=GenerateResponse)
def generate_data(request: GenerateRequest = GenerateRequest()):
    """Generate synthetic transactions, score them, and persist to database."""
    with get_db_session() as session:
        transactions = generate_transactions(request.count)

        # Persist transactions
        for txn_data in transactions:
            txn = TransactionModel(**txn_data)
            session.add(txn)
        session.flush()

        # Score all transactions in batches
        txn_dicts = [
            {k: v for k, v in t.items() if not k.startswith("_")}
            for t in transactions
        ]
        results = process_all_in_batches(txn_dicts, session)

        # Update is_flagged based on risk level
        flagged = 0
        for result in results:
            if result["risk_level"] in ("MEDIUM", "HIGH"):
                session.query(TransactionModel).filter(
                    TransactionModel.id == result["transaction_id"]
                ).update({"is_flagged": True})
                flagged += 1

        return GenerateResponse(
            message=f"Successfully generated {len(transactions)} transactions",
            transactions_created=len(transactions),
            flagged_count=flagged,
        )


# --- Rule Configuration ---
@router.get("/rules", response_model=list[RuleConfigSchema])
def list_rules():
    """List all rule configurations."""
    with get_db_session() as session:
        rules = session.query(RuleConfigModel).all()
        return [RuleConfigSchema.model_validate(r) for r in rules]


@router.put("/rules/{rule_name}", response_model=RuleConfigSchema)
def update_rule(rule_name: str, update: RuleConfigUpdateRequest):
    """Update a rule's weight, threshold, or active status."""
    with get_db_session() as session:
        rule = session.query(RuleConfigModel).filter(RuleConfigModel.rule_name == rule_name).first()
        if not rule:
            raise HTTPException(status_code=404, detail=f"Rule '{rule_name}' not found")

        if update.weight is not None:
            rule.weight = update.weight
        if update.threshold is not None:
            rule.threshold = update.threshold
        if update.is_active is not None:
            rule.is_active = update.is_active
        rule.updated_at = datetime.now(timezone.utc)

        session.flush()
        return RuleConfigSchema.model_validate(rule)


# --- Analytics ---
@router.get("/analytics", response_model=AnalyticsSummary)
def get_analytics():
    """Get complete analytics summary."""
    with get_db_session() as session:
        return AnalyticsSummary(
            fraud_trends=get_fraud_trends(session),
            category_breakdown=get_category_breakdown(session),
            risk_distribution=get_risk_distribution(session),
            top_flagged_merchants=get_top_flagged_merchants(session),
        )


# --- AI Analysis ---
@router.post("/analyze")
async def analyze_transaction(request: AIAnalysisRequest):
    """Trigger AI analysis for a specific transaction."""
    with get_db_session() as session:
        txn = session.query(TransactionModel).filter(TransactionModel.id == request.transaction_id).first()
        if not txn:
            raise HTTPException(status_code=404, detail="Transaction not found")

        risk = session.query(RiskScoreModel).filter(RiskScoreModel.transaction_id == request.transaction_id).first()
        rule_results = session.query(RuleResultModel).filter(
            RuleResultModel.transaction_id == request.transaction_id
        ).all()

        txn_dict = {c.name: getattr(txn, c.name) for c in TransactionModel.__table__.columns}
        rule_dicts = [
            {"rule_name": r.rule_name, "triggered": r.triggered, "raw_score": r.raw_score,
             "weighted_score": r.weighted_score, "details": r.details}
            for r in rule_results
        ]

        prompt = build_analysis_prompt(
            txn_dict, rule_dicts,
            risk.final_score if risk else 0,
            risk.risk_level if risk else "LOW",
        )

        # Call Gemini API
        gemini_result = await call_gemini(prompt)

        if not gemini_result["success"]:
            # Fallback: return rule-based analysis only (Answer: Q3 = A)
            return AIAnalysisErrorResponse(
                transaction_id=request.transaction_id,
                ai_status="unavailable",
                error_message=gemini_result["error"],
                rule_results=[RuleResultSchema.model_validate(r) for r in rule_results],
                risk_score=RiskScoreSchema.model_validate(risk) if risk else None,
            )

        # Parse and persist AI analysis
        parsed = parse_gemini_response(gemini_result["response_text"])
        ai_record = AIAnalysisModel(
            id=str(uuid.uuid4()),
            transaction_id=request.transaction_id,
            prompt_sent=prompt,
            response_raw=gemini_result["response_text"],
            pattern_explanation=parsed["pattern_explanation"],
            top_risk_factors=parsed["top_risk_factors"],
            recommendation=parsed["recommendation"],
            response_time_ms=gemini_result["response_time_ms"],
            analyzed_at=datetime.now(timezone.utc),
        )
        session.add(ai_record)
        session.flush()

        return AIAnalysisSchema.model_validate(ai_record)
