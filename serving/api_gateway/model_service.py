from datetime import datetime, timedelta

from serving.api_gateway.schemas.forecast import ForecastRequest,ForecastResponse,PredictionPayload,RiskPayload,ModelMetadata


class ModelService:
    def __init__(self, model_name: str = "dummy_model") -> None:
        self.model_name = model_name
        self.model_version = "v0.1.0"
        self.feature_version = "v0.0.1"
        self.trained_to = datetime(2024, 12, 31)

    def predict(self, req: ForecastRequest) -> ForecastResponse:
        """
        Dummy implementation.

        Later this will:
        - Load/call Shri's trained model.
        - Use real features from his feature store or artifacts.
        """
        now = datetime.utcnow()

        prediction = PredictionPayload(horizon=req.horizon,predicted_return=0.012,predicted_volatility=0.035,predicted_direction="up",)

        risk = RiskPayload(var_95=-0.04,var_99=-0.07,expected_shortfall_95=-0.05,model_confidence=0.82,)

        model = ModelMetadata(model_name=self.model_name,model_version=self.model_version,trained_until=self.trained_to,backtest_start=now - timedelta(days=365),backtest_end=now - timedelta(days=1),)

        return ForecastResponse(symbol=req.symbol,as_of=req.as_of,prediction=prediction,risk=risk,model=model,)
