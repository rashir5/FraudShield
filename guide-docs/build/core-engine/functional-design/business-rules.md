# Business Rules — Unit 1: Core Engine

## Rule Definitions

All rules are stored in the `RULE_CONFIG` SQLite3 table and are modifiable at runtime via API Gateway endpoints (Answer: Q4 = A).

### Rule 1: High Value Transaction
| Property | Value |
|----------|-------|
| **Rule Name** | `high_value` |
| **Default Threshold** | ₹50,000 |
| **Default Weight** | 0.20 |
| **Logic** | If `transaction.amount > threshold`, rule fires |
| **Raw Score Calculation** | `min(100, (amount / threshold) × 50)` — scales proportionally, capped at 100 |
| **Severity Rank** | 3 (used for tie-breaking) |

### Rule 2: Odd-Hours Transaction
| Property | Value |
|----------|-------|
| **Rule Name** | `odd_hours` |
| **Default Threshold** | Hour range: 0–5 (Midnight to 5 AM IST) |
| **Default Weight** | 0.10 |
| **Logic** | If `transaction.timestamp.hour >= 0 AND < 5` (IST), rule fires |
| **Raw Score Calculation** | Fixed score of 80 when triggered (binary rule) |
| **Severity Rank** | 5 (lowest priority for tie-breaking) |

### Rule 3: Velocity Check (Rapid Successive Transactions)
| Property | Value |
|----------|-------|
| **Rule Name** | `velocity` |
| **Default Threshold** | 3 transactions within 10 minutes for same account |
| **Default Weight** | 0.30 |
| **Logic** | Count transactions for `account_number` within rolling 10-minute window. If count >= threshold, rule fires |
| **Raw Score Calculation** | `min(100, (count / threshold) × 60)` — scales with number of rapid transactions |
| **Severity Rank** | 1 (highest priority for tie-breaking) |

### Rule 4: Geographic Anomaly
| Property | Value |
|----------|-------|
| **Rule Name** | `geo_anomaly` |
| **Default Threshold** | Transaction city differs from the 3 most recent cities for the account |
| **Default Weight** | 0.25 |
| **Logic** | Compare `transaction.city` against the last 3 known cities for the account. If city is not in that set, rule fires |
| **Raw Score Calculation** | Fixed score of 90 when triggered (high confidence anomaly) |
| **Severity Rank** | 2 (second highest for tie-breaking) |

### Rule 5: Merchant Category Mismatch
| Property | Value |
|----------|-------|
| **Rule Name** | `merchant_mismatch` |
| **Default Threshold** | Transaction merchant category not in account's top 5 historical categories |
| **Default Weight** | 0.15 |
| **Logic** | Compare `transaction.merchant_category` against the account's 5 most frequent categories. If category is absent, rule fires |
| **Raw Score Calculation** | Fixed score of 70 when triggered |
| **Severity Rank** | 4 (used for tie-breaking) |

---

## Validation Constraints

| Constraint | Rule |
|-----------|------|
| Amount range | `amount > 0` (no negative or zero values) |
| Timestamp timezone | Must be IST (UTC+05:30) |
| Risk score bounds | `0 <= final_score <= 100` |
| Weight sum | All active rule weights must sum to a value > 0 |
| Rule uniqueness | Each `rule_name` must be unique in RULE_CONFIG |
| Account number format | 10-16 digit numeric string |

## Configuration Schema (SQLite3 — Runtime Modifiable)

```sql
CREATE TABLE rule_config (
    id TEXT PRIMARY KEY,
    rule_name TEXT UNIQUE NOT NULL,
    weight REAL NOT NULL DEFAULT 0.20,
    threshold REAL NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1,
    updated_at TEXT NOT NULL
);
```

### Default Seed Values

| rule_name | weight | threshold | is_active |
|-----------|--------|-----------|-----------|
| high_value | 0.20 | 50000.0 | 1 |
| odd_hours | 0.10 | 5.0 | 1 |
| velocity | 0.30 | 3.0 | 1 |
| geo_anomaly | 0.25 | 3.0 | 1 |
| merchant_mismatch | 0.15 | 5.0 | 1 |
