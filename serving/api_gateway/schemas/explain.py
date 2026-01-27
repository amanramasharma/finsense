from datetime import datetime
from typing import Literal, List
from pydantic import BaseModel

class ExplainRequest(BaseModel):
    symbol: str
    as_of: datetime
    horizon: Literal["1d","5d"]= "1d"

class EvidenceItem(BaseModel):
    id:str
    source: Literal["news","social","filing","other"]
    title: str
    snippet: str
    published_at: datetime
    url: str

class ExplainMetadata(BaseModel):
    model_verison: str
    prompt_version: str

class ExplainResponse(BaseModel):
    symbol: str
    as_of: datetime
    horizon: str
    summary: str
    top_drivers: List[str]
    evidence: List[EvidenceItem]
    meta: ExplainMetadata