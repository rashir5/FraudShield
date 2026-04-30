# Epic-Based User Stories

## Epic 1: Synthetic Data Generation & Setup
**Description**: The application must be able to bootstrap itself with mock but highly realistic retail banking data within the Indian financial context.

### US 1.1: Generate Synthetic Transactions
**As a** System Administrator  
**I want** to click a button to generate exactly 1,000 synthetic transactions  
**So that** I have a populated localized dataset for testing rule logic.  
**Acceptance Criteria:**
1. The dashboard must contain a "Generate Test Data" button.
2. Clicking the button emits a non-blocking asynchronous request to the backend.
3. The dataset strictly contains ₹ currency, Indian Merchant strings, and Indian geolocation stubs.
4. Data contains approximately a 5% baseline injection of explicitly anomalous records matching rules (e.g. 3 AM transactions).
5. Must execute cleanly within 4GB constraints.

## Epic 2: Core Rule-Based Detection Engine
**Description**: Evaluation of individual transactions against business rules and compilation of a single weighted numeric score.

### US 2.1: Implement Risk Scoring Algorithm
**As a** Fraud Analyst  
**I want** the system to calculate an aggregated Risk Score (0-100) using a weighted average across all triggers  
**So that** I can universally sort and prioritize the most severe transaction risks.  
**Acceptance Criteria:**
1. The Score strictly adheres to the boundaries `0 <= Score <= 100`.
2. Core rules (Velocity, Odd Hours, Distance, Mismatch, High Value) all have configurable numeric weightings in SQLite.
3. Engine processes 100-batch synchronous blocks to preserve RAM according to NFRs.

### US 2.2: Timezone Aware Odd-Hour Checks
**As a** Fraud Analyst  
**I want** the rule engine to flag transactions that occur between Midnight and 5 AM Indian Standard Time (IST)  
**So that** night-time fraud patterns are surfaced.  
**Acceptance Criteria:**
1. Transaction timestamps must strictly validate as IST.
2. Flag is boolean.

## Epic 3: Generative AI Analysis
**Description**: The connection between the dashboard UI and the external Gemini service for deeper pattern recognition.

### US 3.1: Trigger AI Deep Dive
**As a** Fraud Analyst  
**I want** to click "Analyze with AI" uniquely mapped to a flagged transaction  
**So that** I can get deeper context and pattern explanations for complex fraud vectors.  
**Acceptance Criteria:**
1. The panel expands smoothly on row click.
2. API payload automatically constructs a strict Indian banking context string.
3. API payload explicitly includes the top 3 weighted reasons from the Rules Engine.
4. A strict timeout occurs if the Gemini API exceeds a 5s latency threshold, gracefully returning an error to the UI avoiding a stuck state.
5. AI output is structurally parsed and formatted into markdown within the Alert details panel.

## Epic 4: Dashboard Interface & Analytics
**Description**: The primary visual platform for Fraud Analysts.

### US 4.1: Color-Coded Paginated Table
**As a** Fraud Analyst  
**I want** a paginated, colored transaction grid  
**So that** I can quickly browse through the daily load without system freezing.  
**Acceptance Criteria:**
1. Server-side pagination is enforced with a chunk limit of 50 rows displayed simultaneously.
2. Color Coding enforced strictly as: Green (0-30), Yellow (31-69), Red (70-100).

### US 4.2: Visual Analytics Charts
**As a** Fraud Analyst  
**I want** to see aggregated charts (fraud trends, merchant breakdown, risk distribution)  
**So that** I understand the overall operational health of my bank's network today.  
**Acceptance Criteria:**
1. Render 4 charts using Streamlit natively.
2. Chart data queries SQLite index natively using optimized SQL groupings.
