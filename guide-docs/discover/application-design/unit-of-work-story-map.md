# Unit of Work Story Map

This document maps the Epics from User Stories to the 3 deployable Units of Work.

## Unit 1: Core Engine

| Epic | Stories | Responsibility |
|------|---------|---------------|
| **Epic 1: Synthetic Data** | US 1.1 | Generate 1,000 synthetic INR transactions with anomaly injection. Write to SQLite3. |
| **Epic 2: Core Rule Engine** | US 2.1, US 2.2 | Weighted average risk scoring algorithm. Timezone-aware odd-hour checks. All 5 rule modules. |
| **Epic 3: AI Analysis** | US 3.1 | Compile Indian banking context prompt. Make outbound HTTPS call to Gemini API. Parse and structure response. |

## Unit 2: API Gateway

| Epic | Stories | Responsibility |
|------|---------|---------------|
| **Epic 1: Synthetic Data** | US 1.1 | Expose HTTP POST endpoint to trigger data generation via Core Engine. |
| **Epic 2: Core Rule Engine** | US 2.1 | Expose HTTP GET endpoints to retrieve scored transactions. Expose configuration endpoints for rule thresholds. |
| **Epic 3: AI Analysis** | US 3.1 | Expose HTTP GET endpoint accepting transaction ID. Route to Core Engine AI module. Return structured JSON. |

## Unit 3: Dashboard

| Epic | Stories | Responsibility |
|------|---------|---------------|
| **Epic 4: Dashboard UI** | US 4.1, US 4.2 | Render paginated color-coded transaction table. Display 4 analytics charts. |
| **Epic 1: Synthetic Data** | US 1.1 | "Generate Test Data" button making HTTP POST to API Gateway. |
| **Epic 3: AI Analysis** | US 3.1 | "Analyze with AI" button per flagged row. Expanding alert panel displaying structured Gemini response. |

## Coverage Verification

| Story | Unit 1 | Unit 2 | Unit 3 |
|-------|--------|--------|--------|
| US 1.1 | ✅ Logic | ✅ Endpoint | ✅ Button |
| US 2.1 | ✅ Algorithm | ✅ Endpoint | — |
| US 2.2 | ✅ Rule | — | — |
| US 3.1 | ✅ AI Logic | ✅ Endpoint | ✅ UI Panel |
| US 4.1 | — | — | ✅ Table |
| US 4.2 | — | — | ✅ Charts |

All stories are fully assigned across at least one unit. No orphaned stories exist.
