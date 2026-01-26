from datetime import datetime
from pydantic import BaseModel

class ForecastRequest(BaseModel):
    ticker: str
    as_of: datetime
    horizon: str = "1d"

class ForecastResponse(BaseModel):
    ticker: str
    as_of: datetime
    horizon: str
    predicted_return: float
    risk: float
    model_version: str

