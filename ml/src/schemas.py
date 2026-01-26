from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal


class MarketRow(BaseModel):
    """OHLCV market data schema."""
    symbol: str = Field(..., min_length=1, max_length=10)
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int = Field(..., ge=0)
    ingest_date: Optional[datetime] = None


class CompanyMetadata(BaseModel):
    """Company fundamentals and metadata schema."""
    symbol: str = Field(..., min_length=1, max_length=10)
    
    # GICS Classification
    sector: str
    industry_group: Optional[str] = None
    industry: str
    sub_industry: Optional[str] = None
    
    # Valuation metrics
    market_cap: Optional[Decimal] = None
    pe_ratio: Optional[Decimal] = None
    debt_to_equity: Optional[Decimal] = None
    
    # Company operations
    employees: Optional[int] = None
    hq_country: Optional[str] = None
    founded_year: Optional[int] = None
    
    # Risk/return
    beta: Optional[Decimal] = None
    dividend_yield_pct: Optional[Decimal] = None
    
    # Identifiers
    gics_code: Optional[str] = None
    data_as_of: Optional[datetime] = None
