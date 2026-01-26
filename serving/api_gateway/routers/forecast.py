from fastapi import APIRouter
from datetime import datetime
from serving.api_gateway.schemas.forecast import ForecastRequest, ForecastResponse


router = APIRouter(tags=["forecast"])

@router.get("/ping")
async def ping_forecast():
    return {"service":"forecast", "status":"ok"}

@router.post("/",response_model=ForecastResponse)
async def create_forecast(request: ForecastRequest) -> ForecastResponse:
    #later orginal model serive for now using the dummy
    dummy_predicted_return =0.012
    dummy_risk = 0.035
    dummy_model_version = "baseline-v0"
    return ForecastResponse(ticker=request.ticker,
                            as_of=request.as_of,
                            horizon=request.horizon,
                            predicted_return=dummy_predicted_return,risk=dummy_risk,
                            model_version=dummy_model_version)
