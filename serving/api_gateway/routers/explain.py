from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import List
from serving.api_gateway.schemas.explain import ExplainRequest,ExplainMetadata,ExplainResponse,EvidenceItem

router= APIRouter(tags=["explain"])

@router.get("/ping")
async def ping_explain():
    return {"service":"explain","status":"ok"}

@router.post("/",response_model=ExplainResponse)
async def create_explanation(request: ExplainRequest) -> ExplainResponse:
    """
    dummy explanation endpoint 
    later this will call the RAG + LLM pipeline to build a real explanation
    """
    now = datetime.utcnow()
    dummy_evidence: List[EvidenceItem] = [        EvidenceItem(
            id="evt-1",
            source="news",
            title=f"{request.symbol} rallies on positive earnings",
            snippet=f"{request.symbol} reported better-than-expected earnings, "
                    f"driving bullish sentiment in the short term.",
            published_at=now - timedelta(hours=12),
            url="https://example.com/news/a",
        )
    ]

    meta = ExplainMetadata(
        model_version="v0.1.0",
        prompt_version="prompt-explain-v0",
    )

    return ExplainResponse(
        symbol=request.symbol,
        as_of=request.as_of,
        horizon=request.horizon,
        summary="This is a placeholder explanation.",
        top_drivers=[
            "Recent earnings beat",
            "Positive short-term sentiment in news flow",
        ],
        evidence=dummy_evidence,
        meta=meta,
    )
