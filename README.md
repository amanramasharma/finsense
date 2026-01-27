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

