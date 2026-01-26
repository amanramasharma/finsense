from fastapi import APIRouter

router= APIRouter(tags=["explain"])
@router.get("/ping")
async def ping_explain():
    return {"service":"explain","status":"ok"}


