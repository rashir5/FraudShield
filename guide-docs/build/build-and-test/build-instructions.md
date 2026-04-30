# Build Instructions - FraudShield API Gateway

## Prerequisites
- **Build Tool**: Python 3.11+
- **Dependencies**: fastapi, uvicorn, pydantic, sqlalchemy, httpx
- **Environment Variables**: `DATABASE_URL`, `GEMINI_API_KEY`
- **System Requirements**: Windows OS Minimum 4GB RAM

## Build Steps

### 1. Install Dependencies
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
```powershell
$env:DATABASE_URL="sqlite:///fraudshield.db"
$env:GEMINI_API_KEY="your_api_key_here"
```

### 3. Build/Run Unit 2 Gateway
```powershell
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Verify Build Success
- **Expected Output**: "Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"
- **Build Artifacts**: SQLite database files injected locally if running natively.
