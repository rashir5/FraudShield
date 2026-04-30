# Fraud Analyst Daily Review Journey

This outlines the primary workflow of the System Administrator and Fraud Analyst using the FraudShield platform.

```mermaid
flowchart TD
    START(["🏦 Analyst Opens Dashboard"])

    subgraph PHASE_1 ["1 - Situational Awareness"]
        direction TB
        A1["Review Macro Analytics"]
        A2["Scan Category Breakdown"]
        A1 --> A2
    end

    subgraph PHASE_2 ["2 - Triage & Investigation"]
        direction TB
        B1["Apply Filters (Date, Amount, City)"]
        B2["Sort by Risk Score"]
        B3{"Risk Score Classification"}
        B4["🟢 Low Risk (0-30) - Action Not Required"]
        B5["🟡 Medium Risk (31-69) - Review Watchlist"]
        B6["🔴 High Risk (70-100) - Investigate Immediately"]
        B1 --> B2 --> B3
        B3 -->|"Low"| B4
        B3 -->|"Medium"| B5
        B3 -->|"High"| B6
    end

    subgraph PHASE_3 ["3 - Deep Dive Analysis"]
        direction TB
        C1["Open Alert Detail Panel"]
        C2{"Requires AI Assistance?"}
        C3["Click Analyze with AI button"]
        C4["Receive Structured Gemini Insights"]
        C1 --> C2
        C2 -->|"Yes"| C3 --> C4
        C2 -->|"No"| D1
    end

    subgraph PHASE_4 ["4 - Resolution & Audit"]
        direction TB
        D1["Analyst Submits Decision (Allow or Block)"]
        D2["Record Decision in SQLite Database"]
        D3{"More flagged transactions exist?"}
        D1 --> D2 --> D3
    end

    START --> PHASE_1
    PHASE_1 --> PHASE_2
    B6 --> PHASE_3
    C4 --> D1
    PHASE_3 --> PHASE_4
    D3 -->|"Yes"| B1
    D3 -->|"No"| END_NODE(["✅ Daily Review Complete"])

    subgraph ADMIN_FLOW ["Administrative Setup Path"]
        direction TB
        E1["Rule Settings Page"]
        E2["Adjust Thresholds and Weights"]
        E3["Generate Test Data (1,000 txns)"]
        E4["Validate Logic"]
        E1 --> E2 --> E3 --> E4
    end

    %% Business Theme Styling %%
    style PHASE_1 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    style PHASE_2 fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    style PHASE_3 fill:#fce4ec,stroke:#b71c1c,stroke-width:2px,color:#000
    style PHASE_4 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    style ADMIN_FLOW fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000,stroke-dasharray: 8 4

    style START fill:#1565c0,stroke:#0d47a1,color:#fff,stroke-width:2px
    style END_NODE fill:#2e7d32,stroke:#1b5e20,color:#fff,stroke-width:2px

    style B3 fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style C2 fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    style D3 fill:#fff9c4,stroke:#f57f17,stroke-width:2px,color:#000
    
    style B4 fill:#c8e6c9,stroke:#388e3c,color:#000
    style B5 fill:#fff9c4,stroke:#fbc02d,color:#000
    style B6 fill:#ffcdd2,stroke:#c62828,color:#000
```

## Workflow Summary

| Phase | Actor | Key Activities | Outcome |
|-------|-------|----------------|---------|
| **1 - Situational Awareness** | Fraud Analyst | Review macro analytics, category breakdown | Operational context established |
| **2 - Triage & Investigation** | Fraud Analyst | Filter, sort, classify by Risk Score | Prioritized investigation queue |
| **3 - Deep Dive** | Fraud Analyst + Gemini AI | Inspect rule breakdown, invoke AI analysis | Structured insight and recommendation |
| **4 - Resolution & Audit** | Fraud Analyst | Allow / Block / Escalate, record decision | Auditable decision trail |
| **Admin Setup Pathway** | System Administrator | Adjust thresholds, generate test data | Engine tuned for localized Indian banking |
