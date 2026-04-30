# Application Components

1. **Dashboard UI (Streamlit)**
   - **Purpose**: Frontend application for Fraud Analysts to review transactions and rule admins to configure rules.
   - **Responsibilities**: Render data from FastAPI backend; present interaction buttons; handle the Rule Settings view.

2. **Backend API (FastAPI)**
   - **Purpose**: Middle tier routing between frontend and logic core.
   - **Responsibilities**: Data validation, routing UI requests to scoring/AI methods, DB connection pooling.

3. **Core Logic Engine**
   - **Purpose**: Central business logic for Risk Scoring and Data Generation.
   - **Responsibilities**: Apply weighted average risk rules; parse synthetic data logic.

4. **AI Gateway (Gemini API Orchestrator)**
   - **Purpose**: Handle on-demand requests to Gemini.
   - **Responsibilities**: Prompt generation, ratelimiting, error-handling.

5. **Data Layer (SQLite)**
   - **Purpose**: Persistence layer decoupled from the presentation.
   - **Responsibilities**: Localized Indian Bank data tracking, merchant tables, storing configuration rule thresholds.
