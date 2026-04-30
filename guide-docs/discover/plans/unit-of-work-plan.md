# Unit of Work Plan

## Part 1: Unit Decomposition Execution Plan
- [x] Generate `guide-docs/discover/application-design/unit-of-work.md` with unit definitions, responsibilities, and the underlying code organization strategy (Greenfield).
- [x] Generate `guide-docs/discover/application-design/unit-of-work-dependency.md` with the dependency matrix mapping between units.
- [x] Generate `guide-docs/discover/application-design/unit-of-work-story-map.md` mapping our 4 Epics (Synthetic Data, Rule Engine, Gemini AI, Dashboard) directly to the technical units.
- [x] Validate unit boundaries and dependencies against the 4GB RAM architectural limit.
- [x] Ensure all stories are completely assigned to actionable units.

## Part 2: Clarification Questions

To accurately define the architectural boundaries and directories representing our Units of Work for FraudShield, please provide your preference on the following points:

### Question 1: System Architecture & Deployment Boundary
How should we group our codebase for deployment/execution within the 4GB RAM constraints?

A) **Modular Monolith (Single Unit)**: Everything runs together. The Streamlit dashboard and FastAPI backend are instantiated via a single runner script, simplifying startup on a single constrained Windows machine.
B) **Decoupled Architecture (Two Units)**: Strict separation between the Frontend Unit (Streamlit) and Backend Unit (FastAPI + SQLite + Core Engine), requiring two separate terminal processes to run the application.
X) Other (please describe after [Answer]: tag below)

[Answer]: B (Decoupled Architecture using FastAPI over HTTP)
### Question 2: Code Organization Strategy (Greenfield)
Since this is a new project, how would you prefer the code directory structure to reflect our units?

A) **Feature-Based**: Group files vertically by feature (e.g., `src/synthetic_data/`, `src/ai_analysis/`, `src/dashboard/`).
B) **Layer-Based**: Group files horizontally by technical layer (e.g., `src/api/`, `src/core/`, `src/db/`, `ui/`).
X) Other (please describe after [Answer]: tag below)

[Answer]: B (Layer-Based organization - Auto-confirmed via final approval)
