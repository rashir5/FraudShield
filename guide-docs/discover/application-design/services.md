# Application Services

This document defines the core orchestrated services acting as the connective tissue between the frontend, backend rules, database, and external APIs.

## 1. Transaction Lifecycle Service
- **Purpose**: Manage the core data pipeline from synthetic generation to risk classification and database storage.
- **Responsibilities**: Orchestrates the creation of synthetic data (from UI button press), passes it through the Core Logic Engine, calculates the weighted Risk Score dynamically, and writes it sequentially to the Data Layer.

## 2. AI Insight Orchestration Service
- **Purpose**: Serve as a secure boundary for all Generative AI interactions.
- **Responsibilities**: Takes a Fraud UI request, fetches that exact user's transaction history from the SQLite database securely, compiles the strict Indian Context AI prompt, pings Gemini via the API Gateway, and formats the response to JSON for the presentation panel.

---

## Service Orchestration Flowcharts

The flowcharts below detail how these services route HTTP requests through the decoupled backend infrastructure.

### Transaction Lifecycle Workflow
```mermaid
flowchart TD
    UI["Streamlit UI"]
    TLS["FastAPI - Lifecycle Service"]
    Engine["Core Rule Engine"]
    DB[("SQLite DB")]

    UI -- "1. HTTP POST (Generate Data)" --> TLS
    TLS -- "2. Trigger Generator" --> Engine
    Engine -- "3. Return 1000 Mock Txns" --> TLS
    TLS -- "4. Process Risk Array" --> Engine
    Engine -- "5. Scored Results" --> TLS
    TLS -- "6. Bulk Insert" --> DB
    DB -- "7. Success Status" --> TLS
    TLS -- "8. HTTP 200 OK" --> UI
    
    style UI fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style TLS fill:#c8e6c9,stroke:#388e3c,stroke-width:2px,color:#000
    style Engine fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
    style DB fill:#ffcc80,stroke:#ef6c00,stroke-width:2px,color:#000
```

### AI Insight Workflow
```mermaid
flowchart TD
    UI["Streamlit UI"]
    AI["FastAPI - AI Service"]
    DB[("SQLite DB")]
    Gemini["External Gemini API"]

    UI -- "1. HTTP GET (Txn ID)" --> AI
    AI -- "2. Fetch Context" --> DB
    DB -- "3. Data Row" --> AI
    AI -- "4. Compile Prompt" --> AI
    AI -- "5. Remote API Call" --> Gemini
    Gemini -- "6. Raw Response" --> AI
    AI -- "7. Parse JSON" --> AI
    AI -- "8. HTTP 200 OK" --> UI
    
    style UI fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style AI fill:#e1bee7,stroke:#8e24aa,stroke-width:2px,color:#000
    style DB fill:#ffcc80,stroke:#ef6c00,stroke-width:2px,color:#000
    style Gemini fill:#f8bbd0,stroke:#c2185b,stroke-width:2px,color:#000
```
