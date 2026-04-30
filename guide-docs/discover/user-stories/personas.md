# User Personas

## 1. Rohan Patel (Primary Persona)
**Role**: Fraud Analyst at an Indian Commercial Bank
**Background**: 3 years of experience in retail banking fraud detection. Used to manual review queues.
**Primary Goals**:
- Efficiently review the daily queue of flagged transactions.
- Understand the exact triggering conditions (Risk score components).
- Leverage AI explanations to make rapid, accurate block/allow decisions.
**Pain Points**:
- High volume of false positives from legacy rule engines.
- Missing context regarding new merchant categories or geographic anomalies in India.
- Inability to quickly parse thousands of data points without visual aids.
**System Interaction**: Will use the dashboard daily. Relies heavily on the Data Table, filtering tools, and the AI Analysis popup.

## 2. System Administrator (Secondary Persona)
**Role**: Rule Engine / Backend Admin
**Background**: Technical background, configures the thresholds for Indian RBI compliance.
**Primary Goals**:
- Generate synthetic datasets to test the rule engine before going live.
- Adjust parameters (e.g., High-Value threshold in ₹, Velocity timespan).
**System Interaction**: Uses the application sporadically to tweak settings and run synthesis checks.
