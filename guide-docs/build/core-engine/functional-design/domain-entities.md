# Domain Entities — Unit 1: Core Engine

## Entity Relationship Diagram

```mermaid
erDiagram
    TRANSACTION ||--o{ RULE_RESULT : "evaluated by"
    TRANSACTION }o--|| RISK_SCORE : "produces"
    RULE_CONFIG ||--o{ RULE_RESULT : "configures"
    TRANSACTION }o--o| AI_ANALYSIS : "optionally analyzed"

    TRANSACTION {
        string id PK "UUID"
        string account_number "Indian bank account"
        string account_holder "Customer name"
        float amount "INR currency"
        datetime timestamp "IST timezone"
        string city "Transaction location"
        string merchant_name "Indian merchant"
        string merchant_category "Category code"
        string bank_name "Indian bank"
        string transaction_type "Credit or Debit"
        boolean is_flagged "Fraud flag"
        datetime created_at "Record creation"
    }

    RISK_SCORE {
        string id PK "UUID"
        string transaction_id FK "Links to Transaction"
        float final_score "0-100 weighted average"
        string risk_level "LOW, MEDIUM, HIGH"
        int rules_triggered "Count of fired rules"
        datetime calculated_at "Score timestamp"
    }

    RULE_CONFIG {
        string id PK "UUID"
        string rule_name "Unique rule identifier"
        float weight "Scoring weight factor"
        float threshold "Trigger threshold value"
        boolean is_active "Enable or disable rule"
        datetime updated_at "Last modification"
    }

    RULE_RESULT {
        string id PK "UUID"
        string transaction_id FK "Links to Transaction"
        string rule_name FK "Links to Rule Config"
        boolean triggered "Did the rule fire"
        float raw_score "Individual rule score 0-100"
        float weighted_score "raw_score times weight"
        string details "Reason description"
    }

    AI_ANALYSIS {
        string id PK "UUID"
        string transaction_id FK "Links to Transaction"
        string prompt_sent "Full prompt text"
        string response_raw "Raw Gemini response"
        string pattern_explanation "Parsed explanation"
        string top_risk_factors "Top 3 weighted reasons"
        string recommendation "AI recommendation"
        float response_time_ms "Latency tracking"
        datetime analyzed_at "Analysis timestamp"
    }
```

## Entity Descriptions

### Transaction
The central entity representing a single banking transaction. All fields are strictly localized to the Indian BFSI context (INR amounts, Indian bank names, Indian cities, IST timestamps).

### Risk Score
A computed aggregate result linked 1:1 to a Transaction. Contains the final weighted average score (0-100) and the derived risk level classification (LOW: 0-30, MEDIUM: 31-69, HIGH: 70-100).

### Rule Config
Runtime-configurable rule definitions stored in SQLite3. Each rule has a unique name, a numeric weight for the scoring algorithm, a threshold value for triggering, and an active/inactive toggle. Modifiable at runtime via API Gateway endpoints.

### Rule Result
A per-rule evaluation record linked to both a Transaction and a Rule Config. Captures whether the rule triggered, the individual raw score, the weighted contribution, and a human-readable reason string.

### AI Analysis
An optional enrichment entity created only when a Fraud Analyst clicks "Analyze with AI." Stores the full prompt, raw Gemini response, parsed pattern explanation, top 3 risk factors, and the AI recommendation.
