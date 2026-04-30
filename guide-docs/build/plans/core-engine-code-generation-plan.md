# Code Generation Plan — Unit 1: Core Engine

## Unit Context
- **Unit**: Core Engine (Build 1st)
- **Stories Covered**: US 1.1 (Synthetic Data), US 2.1 (Risk Scoring), US 2.2 (Odd-Hours), US 3.1 (AI Analysis)
- **Dependencies**: SQLite3 (embedded), External Gemini API (outbound HTTPS)
- **Code Location**: `core_engine/` at workspace root
- **Test Framework**: Pytest (TDD)

## Core Engine Modules

| # | Module | Responsibility |
|---|--------|---------------|
| 1 | **Database Manager** | SQLite3 engine, WAL mode, session management, schema creation, seeding |
| 2 | **Rule Engine** | 5 individual fraud detection rules with abstract base class |
| 3 | **Risk Scorer** | Weighted average scoring algorithm, risk classification, tie-breaking |
| 4 | **Analytics Engine** | Fraud rate trends, category breakdown, risk distribution, top flagged merchants |
| 5 | **AI Integration Client** | Gemini HTTPS client, prompt builder, response parser, 5s timeout fallback |
| 6 | **Internal HTTP Server** | Lightweight HTTP interface exposing core engine functions to other units |
| 7 | **Synthetic Data Generator** | 1,000 INR transaction generator with weighted anomaly injection |

## Code Structure
```
core_engine/
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── transaction.py
│   ├── risk_score.py
│   ├── rule_config.py
│   ├── rule_result.py
│   └── ai_analysis.py
├── schemas/
│   ├── __init__.py
│   └── pydantic_schemas.py
├── database_manager/
│   ├── __init__.py
│   ├── engine.py                # SQLite3 engine, WAL mode, connection pooling
│   ├── session.py               # Scoped session factory
│   ├── migrations.py            # CREATE TABLE for all 5 entities
│   └── seed.py                  # Default rule_config seed values
├── rule_engine/
│   ├── __init__.py
│   ├── base_rule.py             # Abstract base class: evaluate(txn) -> RuleResult
│   ├── high_value.py            # Amount threshold rule
│   ├── odd_hours.py             # IST midnight-5AM rule
│   ├── velocity.py              # Rolling 10-min window rule
│   ├── geo_anomaly.py           # Last 3 cities comparison rule
│   ├── merchant_mismatch.py     # Top 5 categories comparison rule
│   └── rule_registry.py         # Load active rules from DB, execute all
├── risk_scorer/
│   ├── __init__.py
│   ├── weighted_scorer.py       # SUM(raw * weight) / SUM(weight) algorithm
│   ├── risk_classifier.py       # LOW/MEDIUM/HIGH classification
│   ├── tie_breaker.py           # Severity-based ranking (velocity > geo > ...)
│   └── batch_processor.py       # 100-record batch processing for 4GB RAM
├── analytics_engine/
│   ├── __init__.py
│   ├── fraud_trends.py          # Fraud rate over time aggregations
│   ├── category_breakdown.py    # Merchant category distribution analysis
│   ├── risk_distribution.py     # Score histogram and percentile analysis
│   └── top_flagged.py           # Top flagged merchants ranking
├── ai_integration/
│   ├── __init__.py
│   ├── prompt_builder.py        # Indian banking context prompt compilation
│   ├── gemini_client.py         # HTTPS client via httpx, 5s timeout
│   └── response_parser.py       # Parse raw Gemini output to structured JSON
├── http_server/
│   ├── __init__.py
│   ├── server.py                # Internal HTTP server entry point
│   └── routes.py                # Route definitions exposing core functions
├── synthetic_generator/
│   ├── __init__.py
│   ├── generator.py             # Main generation orchestrator (1,000 txns)
│   ├── indian_context.py        # Bank names, merchant names, city pools
│   └── anomaly_injector.py      # Weighted anomaly injection logic
├── config/
│   ├── __init__.py
│   └── settings.py              # Env vars, API key loading, default thresholds
└── tests/
    ├── __init__.py
    ├── test_database_manager.py
    ├── test_rule_engine.py
    ├── test_risk_scorer.py
    ├── test_analytics_engine.py
    ├── test_ai_integration.py
    ├── test_http_server.py
    ├── test_synthetic_generator.py
    └── test_models.py
```

---

## Generation Steps

### Step 1: Project Structure Setup
- [x] Create `core_engine/` directory structure with all subdirectories and `__init__.py` files
- [x] Create `requirements.txt` (sqlalchemy, pydantic, httpx, pytest, python-dotenv, uvicorn, fastapi)
- [x] Create `.env.example` template at workspace root

### Step 2: Configuration Module
- [x] Implement `config/settings.py` — environment variable loading, Gemini API key, default thresholds

---

### Step 3: Database Manager — Implementation
- [x] Implement `database_manager/engine.py` — SQLite3 engine with WAL mode, connection pooling
- [x] Implement `database_manager/session.py` — Scoped session factory, context manager
- [x] Implement `database_manager/migrations.py` — CREATE TABLE for Transaction, RiskScore, RuleConfig, RuleResult, AIAnalysis
- [x] Implement `database_manager/seed.py` — Insert 5 default rule configurations with weights and thresholds
- **Story**: US 2.1

### Step 4: Database Manager — Tests
- [x] Implement `tests/test_database_manager.py` — Engine creation, table creation, seeding, session lifecycle
- **Story**: US 2.1

---

### Step 5: ORM Models + Schemas
- [x] Implement `models/transaction.py` — Transaction SQLAlchemy model (Indian context fields)
- [x] Implement `models/risk_score.py` — RiskScore linked to Transaction
- [x] Implement `models/rule_config.py` — RuleConfig with weight, threshold, is_active
- [x] Implement `models/rule_result.py` — RuleResult linked to Transaction and RuleConfig
- [x] Implement `models/ai_analysis.py` — AIAnalysis linked to Transaction
- [x] Implement `schemas/pydantic_schemas.py` — Pydantic request/response models
- **Story**: US 2.1, US 3.1

### Step 6: ORM Models — Tests
- [x] Implement `tests/test_models.py` — Model creation, relationships, field validation
- **Story**: US 2.1, US 3.1

---

### Step 7: Rule Engine — Implementation
- [x] Implement `rule_engine/base_rule.py` — Abstract base class with `evaluate(transaction) -> RuleResult`
- [x] Implement `rule_engine/high_value.py` — Amount threshold: `min(100, (amount/threshold) * 50)`
- [x] Implement `rule_engine/odd_hours.py` — IST midnight-5AM: fixed score 80
- [x] Implement `rule_engine/velocity.py` — Rolling 10-min window: `min(100, (count/threshold) * 60)`
- [x] Implement `rule_engine/geo_anomaly.py` — Last 3 cities comparison: fixed score 90
- [x] Implement `rule_engine/merchant_mismatch.py` — Top 5 categories: fixed score 70
- [x] Implement `rule_engine/rule_registry.py` — Load active rules from SQLite3, execute all against a transaction
- **Story**: US 2.1, US 2.2

### Step 8: Rule Engine — Tests
- [x] Implement `tests/test_rule_engine.py` — Each rule individually, edge cases, boundary conditions, registry loading
- **Story**: US 2.1, US 2.2

---

### Step 9: Risk Scorer — Implementation
- [x] Implement `risk_scorer/weighted_scorer.py` — `SUM(raw * weight) / SUM(weight)`, rounded to 2 decimals
- [x] Implement `risk_scorer/risk_classifier.py` — LOW (0-30), MEDIUM (31-69), HIGH (70-100)
- [x] Implement `risk_scorer/tie_breaker.py` — Severity order: velocity > geo > high_value > mismatch > odd_hours
- [x] Implement `risk_scorer/batch_processor.py` — Process 100 transactions per batch within 4GB RAM
- **Story**: US 2.1

### Step 10: Risk Scorer — Tests
- [x] Implement `tests/test_risk_scorer.py` — Weighted math, boundary scores, tie-breaking, batch processing
- **Story**: US 2.1

---

### Step 11: Synthetic Data Generator — Implementation
- [x] Implement `synthetic_generator/indian_context.py` — Indian bank names, merchant names, city name pools, IST timestamp generation
- [x] Implement `synthetic_generator/anomaly_injector.py` — Weighted injection (velocity 30%, high_value 25%, geo 20%, mismatch 15%, odd_hours 10%)
- [x] Implement `synthetic_generator/generator.py` — Orchestrate 1,000 transaction creation, inject anomalies, return batch
- **Story**: US 1.1

### Step 12: Synthetic Data Generator — Tests
- [x] Implement `tests/test_synthetic_generator.py` — Record count, INR currency, anomaly ratios, Indian context data
- **Story**: US 1.1

---

### Step 13: Analytics Engine — Implementation
- [x] Implement `analytics_engine/fraud_trends.py` — Fraud rate aggregation over time windows
- [x] Implement `analytics_engine/category_breakdown.py` — Merchant category distribution queries
- [x] Implement `analytics_engine/risk_distribution.py` — Score histogram and percentile calculations
- [x] Implement `analytics_engine/top_flagged.py` — Top N flagged merchants ranking query
- **Story**: US 4.2 (Data support)

### Step 14: Analytics Engine — Tests
- [x] Implement `tests/test_analytics_engine.py` — Aggregation accuracy, empty dataset handling, sort order
- **Story**: US 4.2

---

### Step 15: AI Integration Client — Implementation
- [x] Implement `ai_integration/prompt_builder.py` — Indian banking context prompt with transaction data + top 3 rule reasons
- [x] Implement `ai_integration/gemini_client.py` — HTTPS client via httpx, 5s timeout, structured error fallback
- [x] Implement `ai_integration/response_parser.py` — Parse Gemini response into pattern_explanation, top_risk_factors, recommendation
- **Story**: US 3.1

### Step 16: AI Integration Client — Tests
- [x] Implement `tests/test_ai_integration.py` — Prompt structure, timeout fallback, response parsing, error handling
- **Story**: US 3.1

---

### Step 17: Internal HTTP Server — Implementation
- [x] Implement `http_server/routes.py` — Route definitions: generate data, score transactions, get analytics, analyze with AI, manage rules
- [x] Implement `http_server/server.py` — Lightweight FastAPI app entry point (uvicorn, port 8000)
- **Story**: All (exposes core engine to Unit 2 API Gateway)

### Step 18: Internal HTTP Server — Tests
- [x] Implement `tests/test_http_server.py` — Endpoint integration tests, request/response validation
- **Story**: All

---

### Step 19: Code Summary Documentation
- [x] Generate `guide-docs/build/core-engine/code/code-summary.md` containing:

#### 19.1 — Module Overview Table
- [x] Table listing every module (Database Manager, Rule Engine, Risk Scorer, Analytics Engine, AI Integration, HTTP Server, Synthetic Generator) with purpose, file count, and primary story mapping

#### 19.2 — File Inventory
- [x] Complete file-by-file inventory of `core_engine/` with absolute paths, line counts, and one-line descriptions for every `.py` file created

#### 19.3 — API Reference (Internal HTTP Server)
- [x] Table documenting every HTTP endpoint exposed by the Internal HTTP Server:
  - Method (GET/POST/PUT/DELETE)
  - Path (e.g., `/api/v1/transactions/generate`)
  - Request payload schema
  - Response payload schema
  - Linked module and story

#### 19.4 — Database Schema Reference
- [x] Full SQLite3 schema documentation with CREATE TABLE statements for all 5 entities
- [x] Index definitions and foreign key relationships
- [x] Default seed data values for `rule_config`

#### 19.5 — Module Dependency Map
- [x] Mermaid flowchart showing internal dependencies between all 7 modules (which module imports which)

#### 19.6 — Configuration Reference
- [x] Complete list of all environment variables, `.env` keys, and their default values
- [x] Rule threshold and weight configuration defaults

#### 19.7 — Test Coverage Summary
- [x] Table mapping each test file to its target module, number of test cases, and story coverage

#### 19.8 — README.md Generation
- [x] Generate `core_engine/README.md` at workspace root with:
  - Project overview
  - Quick start instructions (install, configure, run)
  - Module architecture description
  - Environment setup guide

---

## Story Traceability Matrix

| Step | Module | Files | Story |
|------|--------|-------|-------|
| 1-2 | Config | Structure, settings | Infrastructure |
| 3-4 | Database Manager | database_manager/* | US 2.1 |
| 5-6 | Models | models/*, schemas/* | US 2.1, US 3.1 |
| 7-8 | Rule Engine | rule_engine/* | US 2.1, US 2.2 |
| 9-10 | Risk Scorer | risk_scorer/* | US 2.1 |
| 11-12 | Synthetic Generator | synthetic_generator/* | US 1.1 |
| 13-14 | Analytics Engine | analytics_engine/* | US 4.2 |
| 15-16 | AI Integration | ai_integration/* | US 3.1 |
| 17-18 | HTTP Server | http_server/* | All |
| 19 | Documentation | code-summary.md | All |
