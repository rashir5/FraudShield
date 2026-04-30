# [Environment Setup] Analytics-Driven Virtual Environment Configuration

This enhanced plan covers the professional setup of the FraudShield environment and a comprehensive validation of the Data Visualization & Analytics stack.

## User Review Required

> [!IMPORTANT]
> **Python Version**: This project requires Python 3.11+. The system detected Python 3.13.1.
> **Dependency Adjustment**: Due to Python 3.13 compatibility requirements, pinned versions for `pydantic` and `fastapi` will be updated to their latest stable releases to ensure pre-built wheels are available.
> **Memory Constraint**: This setup remains optimized for the 4GB RAM target environment by keeping dependencies lean.
> **Data Readiness**: Verification now includes mandatory synthetic data injection to ensure analytics components (Plotly/Pandas) are tested against realistic national datasets.
> **Graphic Latency**: Mapbox-based visual audits may require consistent internet connectivity for tile rendering.

## Proposed Changes

### Phase 1: Environment & Security Infrastructure

1.  **Pre-Check**: Validate Python 3.11+.
2.  **Creation**: `python -m venv venv`.
3.  **Security Bootstrap**: Upgrade `pip` and `setuptools` to latest.
4.  **Dependency Install**: 
    - [MODIFY] `requirements.txt`: Adjust dependency versions for Python 3.13 compatibility (specifically `pydantic` and `fastapi`). 
    - Install using `pip install -r requirements.txt`.

### Phase 2: Data & State Initialization

To prevent the "Empty Graph" state during first-run validation:

1.  **Database Injection**: Execute `python generate_test_db.py` to seed `fraudshield.db`.
2.  **Data Targets**:
    - 1,000+ transaction records.
    - National distribution across **50 Indian Cities**.
    - Anomaly injection (Velocity, High Value, Geo Drifts).

### Phase 3: Analytics Validation & Flow Verification

This phase ensures the mathematical integrity and visual responsiveness of the dashboard.

#### Graphing Implementation Logic
- **Fraud Trends**: `Pandas` resamples SQL-fetched timestamps to Daily frequency. `Plotly Express` generates a multi-trace line graph comparing *Total Volume* vs *Flagged Rate*.
- **Geospatial Heatmaps**: Dataframe is filtered for top 50 cities. `Plotly Mapbox Density` creates a heatmap of national fraud hotspots based on weighted risk scores.

#### Analytics Data Flow
1.  **Persistence**: Transactions stored in SQLite via SQLAlchemy.
2.  **Aggregation**: `core_engine/analytics_engine/` executes GROUP BY queries for trends/cities.
3.  **Serialization**: FastAPI Gateway transforms aggregation results into structured JSON.
4.  **Ingestion**: `dashboard/services/api_client.py` fetches JSON via async HTTPX.
5.  **Visualization**: Streamlit UI wraps JSON in `pd.DataFrame` and renders as interactive `Plotly` figures.

## Verification Plan

### Automated Verification
- **Endpoint Test**: `curl http://127.0.0.1:8000/api/v1/analytics` to verify JSON schema.
- **Data Integrity**: Confirm `transaction` count > 0 in DB before UI launch.

### Phase 3: Visual Audit (Manual)
| Component | Success Criteria |
| :--- | :--- |
| **Risk Distribution** | Histogram must show 3 distinct buckets (Low, Med, High). |
| **National Heatmap** | Map must render 50 city clusters with intensity-based scaling. |
| **Live Feed Line Graph** | Real-time line shifts as new synthetic batches are generated. |
| **Filter Responsiveness** | Selecting a "City" in the sidebar must trigger a Plotly re-draw in <500ms. |

### Deployment Command Review
- **API Start**: `uvicorn api.main:app`
- **Dashboard Start**: `streamlit run dashboard/app.py`
