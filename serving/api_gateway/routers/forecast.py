from fastapi import APIRouter

from serving.api_gateway.schemas.forecast import ForecastRequest, ForecastResponse
from serving.api_gateway.model_service import ModelService

router = APIRouter(tags=["forecast"])

# Global instance (later can be injected / replaced in tests)
model_service = ModelService()


@router.get("/ping")
async def ping_forecast():
    return {"service": "forecast", "status": "ok"}


@router.post("/", response_model=ForecastResponse)
async def create_forecast(request: ForecastRequest) -> ForecastResponse:
    """
    Delegate to the model service adapter.
    """
    return model_service.predict(request)
