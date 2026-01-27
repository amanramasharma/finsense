from fastapi import APIRouter

router = APIRouter(tags=["monitoring"])

@router.get("/health")
async def health():
    return {"status": "healthy"}

@router.get("/metrics")
async def metrics():
    return {"prediction_count_24h":0,"error_rate_24h":0.0,}

@router.get("/drift")
async def drift():
    return {"feature_drift":False,"embedding_drift":False,}