# System Units of Work

The FraudShield project is decomposed into **Three Units of Work**, built sequentially in the order listed below.

---

## Unit 1: Core Engine (Build 1st)
**Purpose**: The foundational business logic layer. Contains all fraud detection algorithms, data models, synthetic data generation, weighted risk scoring, and direct database access.
**Owns**:
- Rule-based fraud detection engine (velocity, odd-hours, geo-anomaly, merchant mismatch, high-value)
- Weighted average risk scoring algorithm (0–100)
- Synthetic transaction generator (1,000 INR transactions)
- SQLite3 database — schema definition, connection management, read/write operations
- HTTP client for outbound calls to external Gemini API
- AI prompt compilation and response parsing logic

**Code Organization (Layer-Based)**:
```
core_engine/
├── models/          # SQLAlchemy ORM models, Pydantic schemas
├── rules/           # Individual rule modules + scoring aggregator
├── generator/       # Synthetic data generation logic
├── ai/              # Gemini prompt builder, HTTP client, response parser
├── database/        # SQLite3 engine, session management, migrations
├── config/          # Rule thresholds, weights, environment settings
└── tests/           # Pytest modules for all core logic (TDD)
```

---

## Unit 2: API Gateway (Build 2nd)
**Purpose**: The FastAPI HTTP layer that exposes the Core Engine to the outside world. Contains zero business logic — only routing, request validation, and response formatting.
**Owns**:
- FastAPI application and router definitions
- Request/response payload validation
- Endpoint definitions for transactions, rules configuration, synthetic data triggers, and AI analysis
- Error handling and HTTP status code management

**Depends on**: Unit 1 (Core Engine) — imports and invokes core engine functions directly.

**Code Organization (Layer-Based)**:
```
api_gateway/
├── routers/         # FastAPI route handlers grouped by domain
├── schemas/         # Pydantic request/response models for API layer
├── middleware/       # CORS, error handlers, logging
├── main.py          # FastAPI app entry point (uvicorn, port 8000)
└── tests/           # API endpoint integration tests
```

---

## Unit 3: Dashboard (Build 3rd)
**Purpose**: The Streamlit presentation layer for Fraud Analysts and System Administrators. Contains zero business logic. Communicates exclusively with Unit 2 (API Gateway) over HTTP REST.
**Owns**:
- Interactive transaction table with color-coded risk levels
- Analytics charts (fraud trends, merchant breakdown, risk distribution, top flagged)
- Alert detail panel with rule breakdown display
- "Analyze with AI" button triggering HTTP call to API Gateway
- "Generate Test Data" administrative button
- Rule configuration settings page
- All HTTP client wrappers pointing to FastAPI endpoints

**Depends on**: Unit 2 (API Gateway) — all data flows through HTTP REST calls to port 8000.

**Code Organization (Layer-Based)**:
```
dashboard/
├── app.py           # Streamlit entry point (port 8501)
├── pages/           # Multi-page Streamlit views
├── components/      # Reusable UI widgets (table, charts, panels)
├── services/        # HTTP client wrappers calling API Gateway
└── tests/           # UI integration tests
```

---

## Build Sequence

| Order | Unit | Rationale |
|-------|------|-----------|
| 1st | Core Engine | Foundation — all business logic, database, and AI integration must exist first |
| 2nd | API Gateway | Exposes Core Engine over HTTP — cannot be built without the engine to wrap |
| 3rd | Dashboard | Presentation layer — cannot function without API endpoints to call |
