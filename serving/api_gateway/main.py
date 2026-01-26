from fastapi import FastAPI, Request
import time
import logging
from common.logging.logging_config import setup_logging
from serving.api_gateway.routers import forecast_router, explain_router, monitoring_router

setup_logging()
logger = logging.getLogger("api_gateway")


app = FastAPI(title="FinSense API Gateway")

@app.middleware("http")
async def log_requests(request: Request,call_next):
    start_time = time.time()
    response= await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    logger.info("request",extra={"path": request.url.path,"method":request.method,"status_code":response.status_code,"duration_ms":round(duration_ms,2),})
    return response

@app.get("/")
async def root():
    return {"service":"finsense-api-gateway","status":"ok"}

app.include_router(forecast_router,prefix="/forecast")
app.include_router(explain_router,prefix="/explain")
app.include_router(monitoring_router,prefix="/monitoring")
