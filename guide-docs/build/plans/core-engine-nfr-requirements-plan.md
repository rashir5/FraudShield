# NFR Requirements Plan — Unit 1: Core Engine

## Execution Checklist
- [ ] Generate `guide-docs/build/core-engine/nfr-requirements/nfr-requirements.md` covering performance, security, reliability, and maintainability.
- [ ] Generate `guide-docs/build/core-engine/nfr-requirements/tech-stack-decisions.md` documenting technology choices and rationale.

## Clarification Questions

The following questions refine the non-functional boundaries for the Core Engine running on a 4GB RAM Windows machine.

### Question 1: Performance — Scoring Throughput
What is the maximum acceptable time for the full risk scoring pipeline to process all 1,000 generated transactions (including SQLite3 writes)?

A) Under 5 seconds (fast — aggressive batching and indexing required)
B) Under 15 seconds (moderate — standard batch processing)
C) Under 30 seconds (relaxed — simple sequential processing acceptable)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 2: Security — API Key Management
How should the Gemini API key be stored and accessed by the Core Engine?

A) Environment variable only (loaded at startup via `os.environ`)
B) `.env` file with python-dotenv (never committed to version control)
C) SQLite3 encrypted secrets table
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 3: Reliability — SQLite3 Concurrency
Since both the generation pipeline and the dashboard queries may hit the database simultaneously, how should write conflicts be handled?

A) WAL mode (Write-Ahead Logging) — allows concurrent reads during writes
B) Exclusive locking with retry — simple but may cause short UI delays
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 4: Maintainability — Logging Strategy
What logging level and framework should be used across the Core Engine?

A) Python standard `logging` module with DEBUG level during development and INFO in production
B) Structured JSON logging via `structlog` for machine-parseable output
C) Minimal print-based logging (lightweight, no dependencies)
X) Other (please describe after [Answer]: tag below)

[Answer]: 
