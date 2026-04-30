from fastapi import APIRouter, HTTPException
from api.schemas import AIAnalysisRequest, AIAnalysisSchema
from api.core_client import core_client

router = APIRouter(prefix="/analyze", tags=["AI Integration"])

@router.post("/", response_model=AIAnalysisSchema)
async def analyze_transaction(request: AIAnalysisRequest):
    result = await core_client.analyze_transaction(request.transaction_id)
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found or could not be analyzed")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=502, detail=result["error"])
    return result
