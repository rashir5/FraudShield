"""
FraudShield - Internal HTTP Server
FastAPI application entry point with startup initialization.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core_engine.config.settings import settings
from core_engine.database_manager.engine import create_db_engine
from core_engine.database_manager.session import init_session_factory, get_db_session
from core_engine.database_manager.migrations import create_all_tables
from core_engine.database_manager.seed import seed_rule_configs
from core_engine.http_server.routes import router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("fraudshield")

# Create FastAPI app
app = FastAPI(
    title="FraudShield Core Engine",
    description="AI-powered fraud detection engine for Indian BFSI sector",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
def startup():
    """Initialize database engine, create tables, and seed default data."""
    logger.info("Starting FraudShield Core Engine...")
    engine = create_db_engine()
    init_session_factory(engine)
    create_all_tables(engine)

    # Seed default rule configurations
    with get_db_session() as session:
        count = seed_rule_configs(session)
        if count > 0:
            logger.info(f"Seeded {count} default rule configurations")

    logger.info(f"FraudShield Core Engine ready on {settings.HOST}:{settings.PORT}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "FraudShield Core Engine"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "core_engine.http_server.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
