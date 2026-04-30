# Unit Test Execution - FraudShield API Gateway

## Run Unit Tests

### 1. Execute All API Unit Tests
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\activate

# Run Pytest against the API tests
pytest tests/test_api_gateway.py -v
```

### 2. Review Test Results
- **Expected**: 3 tests pass, 0 failures (specifically testing the API endpoints via `TestClient` mimicking `httpx`).
- **Test Coverage**: ~85% for API routing schema validation.
- **Test Report Location**: Standard console output.

### 3. Fix Failing Tests
If tests fail:
1. Review console output for 4xx/5xx HTTP errors.
2. Cross-reference payload mismatch with `api/schemas.py`.
3. Check `test_detailed.log` for root causes on missing dependencies.
