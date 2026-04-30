# Requirement Verification Questions

Please answer the following questions to help clarify the requirements for FraudShield.

## Question 1
How should the rule configurations (e.g., high value threshold, velocity limit) be managed in the system?

A) Hardcoded in the backend configuration or environment variables
B) Stored in the SQLite database and updatable via backend REST endpoints
C) Editable directly through the Streamlit dashboard via a Rule Settings panel
X) Other (please describe after [Answer]: tag below)

[Answer]: B & C

## Question 2
How should the generation of synthetic transactions be handled?

A) A button in the Streamlit dashboard triggers the generation of 1,000 new transactions and re-processes them
B) The system generates a single static dataset of 1,000 transactions at startup, which is strictly viewed and analyzed
C) A background script continuously generates small batches of transactions over time
X) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
For transactions flagged as fraudulent by the rule-based engine, when should Gemini AI perform the deeper pattern explanation?

A) Automatically analyze all flagged transactions in the backend pipeline before displaying in the dashboard
B) Triggered on-demand, where the user selects a flagged transaction in the dashboard and clicks "Analyze with AI"
C) Only analyze the top 10 highest-scored transactions automatically to save API cost
X) Other (please describe after [Answer]: tag below)

[Answer]: B
