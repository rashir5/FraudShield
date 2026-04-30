"""FraudShield - HTTP Server and Routes"""
import uuid, logging
from datetime import datetime, timezone
from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from core import settings
from core.security import create_access_token, get_current_user
from core.database import get_db_session, create_db_engine, init_session_factory, create_all_tables, seed_rule_configs
from core.models import (
    TransactionModel, RiskScoreModel, RuleConfigModel, RuleResultModel, AIAnalysisModel, 
    TransactionSchema, TransactionListResponse, RiskScoreSchema, RuleConfigSchema, 
    RuleConfigUpdateRequest, RuleResultSchema, AIAnalysisSchema, AIAnalysisErrorResponse, 
    AIAnalysisRequest, AnalyticsSummary, GenerateRequest, GenerateResponse, Token
)
from core.generator import generate_transactions
from core.scorer import process_all_in_batches
from core.analytics import get_fraud_trends, get_category_breakdown, get_risk_distribution, get_top_flagged_merchants
from core.ai_client import build_analysis_prompt, call_gemini, parse_gemini_response

logger = logging.getLogger("fraudshield")
router = APIRouter(prefix="/api/v1")

# --- WebSocket Manager for Real-time Alerting ---
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Connection might be dead, silence for now
                pass

manager = ConnectionManager()

@router.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, listen for ping if needed
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.post("/auth/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    import os
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_pass = os.getenv("ADMIN_PASSWORD", "fraudshield2026")
    
    if form_data.username != admin_user or form_data.password != admin_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/transactions", response_model=TransactionListResponse)
def list_transactions(
    page: int = 1, page_size: int = 50, risk_level: str = None, 
    is_flagged: bool = None, current_user: str = Depends(get_current_user)
):
    with get_db_session() as session:
        query = session.query(TransactionModel)
        if is_flagged is not None: query = query.filter(TransactionModel.is_flagged == is_flagged)
        if risk_level: query = query.join(RiskScoreModel).filter(RiskScoreModel.risk_level == risk_level)
        total = query.count()
        txns = query.order_by(TransactionModel.timestamp.desc()).offset((page - 1) * page_size).limit(page_size).all()
        return TransactionListResponse(transactions=[TransactionSchema.model_validate(t) for t in txns], total=total, page=page, page_size=page_size)

@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str, current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        txn = session.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        if not txn: raise HTTPException(status_code=404, detail="Not found")
        risk = session.query(RiskScoreModel).filter(RiskScoreModel.transaction_id == transaction_id).first()
        rules = session.query(RuleResultModel).filter(RuleResultModel.transaction_id == transaction_id).all()
        return {"transaction": TransactionSchema.model_validate(txn), "risk_score": RiskScoreSchema.model_validate(risk) if risk else None, "rule_results": [RuleResultSchema.model_validate(r) for r in rules]}

@router.post("/transactions/generate", response_model=GenerateResponse)
def generate_data(request: GenerateRequest = GenerateRequest(), current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        txns = generate_transactions(request.count)
        for t in txns: session.add(TransactionModel(**t))
        session.flush()
        dicts = [{k: v for k, v in t.items() if not k.startswith("_")} for t in txns]
        res = process_all_in_batches(dicts, session)
        flagged = sum(1 for r in res if r["risk_level"] in ("MEDIUM", "HIGH"))
        # Trigger Real-time Alerts for HIGH/MEDIUM risk
        for r in [r for r in res if r["risk_level"] in ("MEDIUM", "HIGH")]:
            import asyncio
            # We use the background loop to broadcast since generate_data is sync
            # Note: In a production app, we'd use a background task or message queue
            loop = asyncio.get_event_loop()
            loop.create_task(manager.broadcast({
                "event": "FRAUD_ALERT",
                "risk_level": r["risk_level"],
                "transaction_id": r["transaction_id"],
                "score": r["final_score"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }))
        
        return GenerateResponse(message=f"Generated {len(txns)}", transactions_created=len(txns), flagged_count=flagged)

@router.get("/rules", response_model=list[RuleConfigSchema])
def list_rules(current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        return [RuleConfigSchema.model_validate(r) for r in session.query(RuleConfigModel).all()]

@router.put("/rules/{rule_name}", response_model=RuleConfigSchema)
def update_rule(rule_name: str, update: RuleConfigUpdateRequest, current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        rule = session.query(RuleConfigModel).filter(RuleConfigModel.rule_name == rule_name).first()
        if not rule: raise HTTPException(status_code=404)
        if update.weight is not None: rule.weight = update.weight
        if update.threshold is not None: rule.threshold = update.threshold
        if update.is_active is not None: rule.is_active = update.is_active
        rule.updated_at = datetime.now(timezone.utc)
        session.flush()
        return RuleConfigSchema.model_validate(rule)

@router.get("/analytics", response_model=AnalyticsSummary)
def get_analytics(current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        return AnalyticsSummary(fraud_trends=get_fraud_trends(session), category_breakdown=get_category_breakdown(session), risk_distribution=get_risk_distribution(session), top_flagged_merchants=get_top_flagged_merchants(session))

@router.post("/analyze")
async def analyze_transaction(request: AIAnalysisRequest, current_user: str = Depends(get_current_user)):
    with get_db_session() as session:
        txn = session.query(TransactionModel).filter(TransactionModel.id == request.transaction_id).first()
        if not txn: raise HTTPException(status_code=404)
        risk = session.query(RiskScoreModel).filter(RiskScoreModel.transaction_id == request.transaction_id).first()
        rules = session.query(RuleResultModel).filter(RuleResultModel.transaction_id == request.transaction_id).all()
        
        tdict = {c.name: getattr(txn, c.name) for c in TransactionModel.__table__.columns}
        rdicts = [{"rule_name": r.rule_name, "triggered": r.triggered, "raw_score": r.raw_score, "weighted_score": r.weighted_score, "details": r.details} for r in rules]
        prompt = build_analysis_prompt(tdict, rdicts, risk.final_score if risk else 0, risk.risk_level if risk else "LOW")
        
        g_res = await call_gemini(prompt)
        if not g_res["success"]:
            return AIAnalysisErrorResponse(transaction_id=request.transaction_id, error_message=g_res["error"], rule_results=[RuleResultSchema.model_validate(r) for r in rules], risk_score=RiskScoreSchema.model_validate(risk) if risk else None)
        
        parsed = parse_gemini_response(g_res["response_text"])
        ai_record = AIAnalysisModel(id=str(uuid.uuid4()), transaction_id=request.transaction_id, prompt_sent=prompt, response_raw=g_res["response_text"], pattern_explanation=parsed["pattern_explanation"], top_risk_factors=parsed["top_risk_factors"], recommendation=parsed["recommendation"], response_time_ms=g_res["response_time_ms"], analyzed_at=datetime.now(timezone.utc))
        session.add(ai_record)
        session.flush()
        return AIAnalysisSchema.model_validate(ai_record)

app = FastAPI(title="FraudShield Core")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router)

@app.on_event("startup")
def startup():
    engine = create_db_engine()
    init_session_factory(engine)
    create_all_tables(engine)
    with get_db_session() as session: seed_rule_configs(session)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("core.server:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
