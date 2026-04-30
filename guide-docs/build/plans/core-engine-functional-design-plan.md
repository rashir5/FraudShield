# Functional Design Plan — Unit 1: Core Engine

## Execution Checklist
- [x] Generate `guide-docs/build/core-engine/functional-design/domain-entities.md` defining all data models, entities, and relationships.
- [x] Generate `guide-docs/build/core-engine/functional-design/business-logic-model.md` detailing the weighted scoring algorithm, synthetic data generation logic, and AI prompt compilation.
- [x] Generate `guide-docs/build/core-engine/functional-design/business-rules.md` specifying all fraud detection rules, validation constraints, thresholds, and configuration schema.

## Clarification Questions

Please answer the following questions to ensure the functional design accurately captures your intent.

### Question 1: Weighted Scoring - Tie-Breaking Rules
When multiple rules fire simultaneously and produce identical weighted scores for different transactions, how should the system break ties in the ranking?

A) Chronological order (most recent transaction ranks higher)
B) Rule severity order (velocity and geo-anomaly always rank above odd-hours)
C) No tie-breaking needed — identical scores can share the same rank
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 2: Synthetic Data - Anomaly Distribution
You specified approximately 5% anomalous records. Should these anomalies be evenly spread across all 5 rule types, or should specific rule types have a higher injection rate?

A) Even distribution (each rule type gets roughly equal anomaly count)
B) Weighted distribution (velocity and high-value anomalies appear more frequently than others)
C) Randomized distribution (let the generator randomly assign anomaly types)
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 3: Gemini AI - Failure Fallback
When the Gemini API call fails (timeout, rate limit, network error), what should the Core Engine return to the API Gateway?

A) Return a structured error response with the rule-based analysis only (no AI insight)
B) Return a retry-after header suggesting the dashboard retry in N seconds
C) Return cached previous AI response if one exists for the same merchant/pattern
X) Other (please describe after [Answer]: tag below)

[Answer]: 

### Question 4: SQLite3 - Configuration Storage
Should rule thresholds and weights be stored in a dedicated configuration table in SQLite3, or loaded from a YAML/JSON config file at startup?

A) SQLite3 configuration table (modifiable at runtime via API Gateway endpoints)
B) YAML config file (requires application restart to apply changes)
C) Both — SQLite3 as primary with YAML as default/fallback seed values
X) Other (please describe after [Answer]: tag below)

[Answer]: 
