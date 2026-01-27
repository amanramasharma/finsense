# FinSense Data Directory

## Structure

### `data/raw/`
**Purpose:** Unmodified data directly from external sources (Yahoo Finance)

**What lives here:**
- `market/{SYMBOL}/YYYYMMDD.csv`: Daily stock prices (OHLCV)
  - Columns: symbol, timestamp, open, high, low, close, volume, ingest_date
  - Source: yfinance API
  - Updated: Daily via `python -m ml.src.ingestion`

- `metadata/companies.csv`: Company information (sector, employees, market cap)
  - Columns: symbol, sector, industry, market_cap, pe_ratio, beta, employees, etc. (16 fields)
  - Source: Manual research from Yahoo Finance / MSCI GICS
  - Updated: Quarterly or when adding new companies

### `data/processed/`
**Purpose:** Cleaned, validated, feature-engineered data ready for machine learning

**What lives here:**
- `market/{SYMBOL}/`: Cleaned prices (outliers removed, missing values handled)
  - Input: data/raw/market/
  - Output: Same schema but quality-assured

- `features/{SYMBOL}/features.csv`: Machine learning features
  - Columns: symbol, timestamp, return_1d, return_5d, volatility_20d, rsi_14, volume_zscore, etc.
  - Input: data/processed/market/
  - Created by: FS-4 feature engineering pipeline

---

## Data Flow (How Data Moves Through the System)

# finsense

# NLP module

This package contains core text ML components for FinSense.

- `preprocessing/`: text cleaning, normalization, tokenization, language detection.
- `models/`: sentiment, topic/event, and entity-linking models.
- `pipelines/`: flows from raw text → enriched documents ready for embeddings and storage.

# RAG module

This package implements retrieval-augmented generation for explanations.

- `retrieval/`: vector + keyword search over OpenSearch with filters (symbol, time, source).
- `orchestration/`: glue code that combines retrieval + LLM prompts and guardrails.
- `postprocessing/`: ranking, deduplication, snippet extraction, and response formatting.
