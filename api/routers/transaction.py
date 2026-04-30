from fastapi import APIRouter
from api.schemas import PaginatedTransactionResponse, GenerateRequest, GenerateResponse
from api.core_client import core_client

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=PaginatedTransactionResponse)
def list_transactions(page: int = 1, page_size: int = 50, risk_level: str = None, is_flagged: bool = None):
    txns, total = core_client.list_transactions(page, page_size, risk_level, is_flagged)
    return {"transactions": txns, "total": total, "page": page, "page_size": page_size}

@router.post("/generate", response_model=GenerateResponse)
def generate_data(request: GenerateRequest):
    created, flagged = core_client.generate_and_score(request.count)
    return {"message": f"Successfully generated and scored {created} transactions", "transactions_created": created, "flagged_count": flagged}
