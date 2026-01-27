from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel


class ForecastRequest(BaseModel):
    symbol: str
    as_of: datetime
    horizon: Literal["1d", "5d", "1w"] = "1d"


class PredictionPayload(BaseModel):
    horizon: str
    predicted_return: float
    predicted_volatility: float
    predicted_direction: Literal["up", "down", "flat"]


class RiskPayload(BaseModel):
    var_95: Optional[float] = None
    var_99: Optional[float] = None
    expected_shortfall_95: Optional[float] = None
    model_confidence: Optional[float] = None


class ModelMetadata(BaseModel):
    model_name: str
    model_version: str
    trained_until: datetime
    backtest_start: datetime
    backtest_end: datetime


class ForecastResponse(BaseModel):
    symbol: str
    as_of: datetime
    prediction: PredictionPayload
    risk: RiskPayload
    model: ModelMetadata
