from fastapi import APIRouter
from api.core_client import core_client

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
def get_analytics():
    return core_client.get_analytics_summary()
