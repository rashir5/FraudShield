# Component Dependency & NFR Architecture

This diagram visualizes how the components interact, explicitly charting the NFR Requirements (4GB RAM bounds) and NFR Design decisions (Batching, Server-side Pagination, Indexed SQLite access) across the workflow as requested.

```mermaid
flowchart TD
    subgraph NFR_REQUIREMENTS ["⚙️ NFR Requirements: Strict 4GB RAM Limit"]
        direction TB
        subgraph NFR_DESIGN ["🛡️ NFR Design: Memory-Safe Execution"]
            direction TB
            UI["Dashboard UI (Streamlit)<br/><i>Uses Server-side Pagination</i>"]
            API["Backend API (FastAPI)<br/><i>Async single-thread loop</i>"]
            CORE["Core Logic Engine<br/><i>Batch processing 100 rows/tick</i>"]
            GEMINI["AI Gateway (Gemini API)<br/><i>Triggered on-demand strictly</i>"]
            DB[("Data Layer (SQLite)<br/><i>Indexed queries, strict locking</i>")]
        end
    end
    
    UI <-->|JSON over HTTP| API
    API -->|Synchronous Batch Invocation| CORE
    CORE -->|DB Reads/Writes| DB
    API <-->|REST payload| GEMINI
    
    %% Styling
    style NFR_REQUIREMENTS fill:#fbe9e7,stroke:#d84315,stroke-width:3px,stroke-dasharray: 10 5,color:#000
    style NFR_DESIGN fill:#e8f5e9,stroke:#2e7d32,stroke-width:3px,color:#000
    style UI fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style API fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style CORE fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000
    style GEMINI fill:#ce93d8,stroke:#6a1b9a,stroke-width:2px,color:#000
    style DB fill:#ffcc80,stroke:#ef6c00,stroke-width:2px,color:#000
```

## Communication Patterns & NFR Overlap
- **Frontend -> Backend**: Standard synchronous REST (HTTP GET/POST) configured within the FastAPI application. Memory is protected by **NFR Design:** avoiding continuous large WebSocket streams.
- **Backend -> SQLite**: SQLAlchemy ORM utilized. **NFR Design:** Yields scoped sessions to prevent memory leaks and respect the 4GB RAM boundary constraint.
- **Backend -> Core Logic**: In-memory direct functional calls. **NFR Design:** Processed in micro-chunks of data to prevent heap overflows when dealing with generating 1000 synthetic items.
