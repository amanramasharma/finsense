from fastapi import APIRouter

router = APIRouter(tags=["monitoring"])

@router.get("/health")
async def health():
    return {"status": "healthy"}