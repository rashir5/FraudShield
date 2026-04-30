# Execution Plan

## Detailed Analysis Summary

### Change Impact Assessment
- **User-facing changes**: Yes - A completely new Streamlit interactive dashboard will be built.
- **Structural changes**: Yes - Creating a new system composed of core logic, FastAPI backend, and frontend.
- **Data model changes**: Yes - SQLite schema for transactions and rule thresholds.
- **API changes**: Yes - FastAPI endpoints connecting Streamlit to the backend core engine.
- **NFR impact**: Yes - Must be optimized to run strictly on a 4GB RAM local Windows machine with minimal latency.

### Risk Assessment
- **Risk Level**: Medium
- **Rollback Complexity**: Easy (New Project)
- **Testing Complexity**: Moderate (Mocking LLM API and synthetic dataset generation via TDD)

## Workflow Visualization

```mermaid
flowchart TD
    Start(["User Request"])
    
    subgraph DISCOVER["🔵 DISCOVER PHASE"]
        WD["Workspace Detection<br/><b>COMPLETED</b>"]
        RE["Reverse Engineering<br/><b>SKIP</b>"]
        RA["Requirements Analysis<br/><b>COMPLETED</b>"]
        US["User Stories<br/><b>SKIP</b>"]
        WP["Workflow Planning<br/><b>COMPLETED</b>"]
        AD["Application Design<br/><b>EXECUTE</b>"]
        UG["Units Generation<br/><b>EXECUTE</b>"]
    end
    
    subgraph BUILD["🟢 BUILD PHASE"]
        FD["Functional Design<br/><b>EXECUTE</b>"]
        NFRA["NFR Requirements<br/><b>EXECUTE</b>"]
        NFRD["NFR Design<br/><b>EXECUTE</b>"]
        ID["Infrastructure Design<br/><b>SKIP</b>"]
        CG["Code Generation<br/><b>EXECUTE</b>"]
        BT["Build and Test<br/><b>EXECUTE</b>"]
    end
    
    subgraph DEPLOY["🟡 DEPLOY PHASE"]
        OPS["Deploy<br/><b>PLACEHOLDER</b>"]
    end
    
    Start --> WD
    WD --> RA
    RA --> WP
    WP --> AD
    AD --> UG
    UG --> FD
    FD --> NFRA
    NFRA --> NFRD
    NFRD --> CG
    CG --> BT
    BT --> End(["Complete"])
    
    style WD fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style RA fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style WP fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style CG fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    style BT fill:#4CAF50,stroke:#1B5E20,stroke-width:3px,color:#fff
    
    style AD fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    style UG fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    style FD fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    style NFRA fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    style NFRD fill:#FFA726,stroke:#E65100,stroke-width:3px,stroke-dasharray: 5 5,color:#000
    
    style RE fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray: 5 5,color:#000
    style US fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray: 5 5,color:#000
    style ID fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray: 5 5,color:#000
    style OPS fill:#BDBDBD,stroke:#424242,stroke-width:2px,stroke-dasharray: 5 5,color:#000
    
    style Start fill:#CE93D8,stroke:#6A1B9A,stroke-width:3px,color:#000
    style End fill:#CE93D8,stroke:#6A1B9A,stroke-width:3px,color:#000
    
    style DISCOVER fill:#BBDEFB,stroke:#1565C0,stroke-width:3px, color:#000
    style BUILD fill:#C8E6C9,stroke:#2E7D32,stroke-width:3px, color:#000
    style DEPLOY fill:#FFF59D,stroke:#F57F17,stroke-width:3px, color:#000
```

## Phases to Execute

### 🔵 DISCOVER PHASE
- [x] Workspace Detection (COMPLETED)
- [x] Reverse Engineering (SKIPPED)
- [x] Requirements Elaboration (COMPLETED)
- [x] User Stories (SKIPPED)
- [x] Execution Plan (IN PROGRESS)
- [ ] Application Design - [EXECUTE]
  - **Rationale**: We need to define identical interfaces and internal methods of the Logic Core, FastAPI, and UI components.
- [ ] Units Generation - [EXECUTE]
  - **Rationale**: The project clearly separates into decoupled logic steps forming unique software units of work.

### 🟢 BUILD PHASE
- [ ] Functional Design - [EXECUTE]
  - **Rationale**: Imperative constraint to strictly design the Weighted Scheme algorithm before starting generating classes.
- [ ] NFR Requirements - [EXECUTE]
  - **Rationale**: Windows specific execution bounds dictating 4GB RAM limit must constrain how the Gemini API logic and DB are loaded in python.
- [ ] NFR Design - [EXECUTE]
  - **Rationale**: Formalize the minimal patterns structure.
- [ ] Infrastructure Design - [SKIP]
  - **Rationale**: Local machine execution implies no Cloud infrastructure topology.
- [ ] Code Generation - [EXECUTE]
  - **Rationale**: Logic creation.
- [ ] Build and Test - [EXECUTE]
  - **Rationale**: TDD rule conformance through validation scripts.

### 🟡 DEPLOY PHASE
- [ ] Deploy - PLACEHOLDER
  - **Rationale**: Future deployment workflows.

## Estimated Timeline
- **Total Phases**: 8 actionable items logic.
- **Estimated Duration**: ~1 hour execution block mapping.

## Success Criteria
- **Primary Goal**: Fully functioning and isolated dashboard without errors.
- **Key Deliverables**: TDD Python modules, pytest scripts, UI rendering locally.
