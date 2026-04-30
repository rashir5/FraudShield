from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import settings
from core.database import create_db_engine, init_session_factory, create_all_tables, seed_rule_configs, get_db_session

from api.routers import transaction, analytics, ai

app = FastAPI(title="FraudShield Gateway", version="1.0.0")

# Enterprise Guardrails: Strictly restrict backend access to the expected frontend/dashboard URL
ALLOWED_ORIGINS = [
    "http://localhost:8501",  # Streamlit default
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

app.include_router(transaction.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")

@app.on_event("startup")
def startup():
    engine = create_db_engine()
    init_session_factory(engine)
    create_all_tables(engine)
    with get_db_session() as session:
        seed_rule_configs(session)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
