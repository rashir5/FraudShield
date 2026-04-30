# Requirements Analysis: FraudShield Dashboard

## Intent Analysis Summary
- **User Request**: Build "FraudShield", an AI-powered fraud detection dashboard designed for the Indian BFSI context, enabling the tracking and resolution of synthetic banking transactions using a configurable rule-based engine and Gemini AI. 
- **Request Type**: New Project
- **Scope Estimate**: System-wide (Frontend, Backend APIs, Core Logic, Database)
- **Complexity Estimate**: Moderate

## Functional Requirements
1. **Synthetic Data Generation**: 
   - Feature to dynamically generate 1,000 synthetic transactions simulating normal and suspicious patterns in ₹.
   - The generation process is triggered on-demand via a button in the Streamlit dashboard, which automatically kicks off processing.
2. **Rule-Based Fraud Detection System**:
   - Evaluate transactions against multiple parameters:
     - High value transactions (above specified threshold).
     - Unusual transaction hours (Midnight to 5 AM).
     - Rapid successive transactions (Velocity check).
     - Geographic anomaly (Transaction location diverges from historical/known city).
     - Merchant category mismatch.
   - Calculate a combined Risk Score (0-100) using a weighted scoring average of the triggered rule signals, allowing different rules to have different levels of influence on the final score.
3. **Fully Localized Context**:
   - Apply Indian Bank and Merchant naming conventions.
   - All financial amounts and logic processed strictly in ₹ (INR).
4. **Configurable Rule Engine**:
   - Rule parameters and thresholds must be securely stored in SQLite.
   - Configurable settings should be exposed via FastAPI backend endpoints.
   - Users must be able to modify these configurations via a "Settings" or "Rule Management" page in the Streamlit interface.
5. **AI-Powered Pattern Analysis**:
   - Integration with Gemini API to provide deep technical/contextual explanations and strategic recommendations on flagged items.
   - This analysis is triggered on-demand by the user clicking "Analyze with AI" specifically for a flagged transaction in the Streamlit dashboard.
5. **Interactive Dashboard Features**:
   - Transaction table with color-coded risk levels.
   - Alert detail panels for a deeper dive into specific flagged cases.
   - Various data filters for transaction review.
   - Advanced analytics displaying:
     - Fraud rate trends.
     - Merchant category breakdown.
     - Risk distribution.
     - Top flagged merchants.

## Non-Functional Requirements
1. **Performance**: System must be lightweight, relying on minimal dependencies, and designed to perform smoothly on a Windows machine with exactly 4GB of RAM.
2. **Architecture**: 
   - Python Core (TDD practices strictly implemented with Pytest).
   - Backend logic served through FastAPI REST architecture.
   - Streamlit acting as the sole presentation layer.
