# Integration Test Instructions - FraudShield API Gateway

## Purpose
Test interactions between Unit 2 (API Gateway) and Unit 1 (Core Engine) to ensure they work together securely and accurately over local module limits.

## Test Scenarios

### Scenario 1: API Boundary → Core Database Scorer Mapping
- **Description**: Verify the generate endpoint persists data correctly to SQLite via the internal HTTP orchestrator.
- **Setup**: Run `test_api_gateway.py` which mocks a POST request to `/api/v1/transactions/generate`.
- **Expected Results**: Response code 200, output mapping to `GenerateResponse` schema displaying `transactions_created`.

### Scenario 2: Frontend Data Emulation
- **Description**: Ensure the `analytics` and `transactions` endpoints correctly serialize raw DB Rows into strictly formatted JSON outputs.
- **Expected Results**: Data output matches strictly to Pydantic definitions in `api/schemas.py`.

## Run Integration Tests

### 1. Execute Integration Test Suite
```powershell
pytest tests/test_api_gateway.py::test_api_analytics -v
pytest tests/test_api_gateway.py::test_api_list_transactions -v
```
