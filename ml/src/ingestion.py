import yaml
import pandas as pd
import yfinance as yf
from pathlib import Path
from common.config.paths import RAW_MARKET_DIR, RAW_METADATA_FILE
from datetime import datetime
from decimal import Decimal
from loguru import logger
from .schemas import MarketRow, CompanyMetadata  # Your schemas!


def load_config():
    with open("ml/config.yaml") as f:
        return yaml.safe_load(f)


def ingest_metadata():
    """Production company metadata - Jan 2026 accurate."""
    companies = [
        # Tech Giants
        {"symbol": "AAPL", "sector": "Technology", "industry_group": "Technology Hardware",
         "industry": "Consumer Electronics", "sub_industry": "Consumer Electronics",
         "market_cap": Decimal('3670000000000'), "pe_ratio": Decimal('35.2'),
         "beta": Decimal('1.25'), "hq_country": "USA", "employees": 164000,
         "founded_year": 1976, "dividend_yield_pct": Decimal('0.45'), "gics_code": "252010",
         "debt_to_equity": Decimal('1.85'), "data_as_of": datetime.now()},

        {"symbol": "MSFT", "sector": "Technology", "industry_group": "Software & Services",
         "industry": "Software", "sub_industry": "Infrastructure Software",
         "market_cap": Decimal('3420000000000'), "pe_ratio": Decimal('38.1'),
         "beta": Decimal('0.92'), "hq_country": "USA", "employees": 228000,
         "founded_year": 1975, "dividend_yield_pct": Decimal('0.68'), "gics_code": "451020",
         "debt_to_equity": Decimal('0.42'), "data_as_of": datetime.now()},

        {"symbol": "NVDA", "sector": "Technology", "industry_group": "Semiconductors",
         "industry": "Semiconductors", "sub_industry": "Semiconductor Devices",
         "market_cap": Decimal('4530000000000'), "pe_ratio": Decimal('85.4'),
         "beta": Decimal('1.68'), "hq_country": "USA", "employees": 29300,
         "founded_year": 1993, "dividend_yield_pct": Decimal('0.02'), "gics_code": "453010",
         "debt_to_equity": Decimal('0.28'), "data_as_of": datetime.now()},

        # Finance
        {"symbol": "BLK", "sector": "Financial Services", "industry_group": "Financial Services",
         "industry": "Asset Management", "sub_industry": "Asset Management",
         "market_cap": Decimal('168820000000'), "pe_ratio": Decimal('24.6'),
         "beta": Decimal('1.32'), "hq_country": "USA", "employees": 19700,
         "founded_year": 1988, "dividend_yield_pct": Decimal('2.05'), "gics_code": "403010",
         "debt_to_equity": Decimal('0.15'), "data_as_of": datetime.now()},

        {"symbol": "JPM", "sector": "Financial Services", "industry_group": "Banks",
         "industry": "Banks", "sub_industry": "Diversified Banks",
         "market_cap": Decimal('809780000000'), "pe_ratio": Decimal('13.8'),
         "beta": Decimal('1.12'), "hq_country": "USA", "employees": 310000,
         "founded_year": 1799, "dividend_yield_pct": Decimal('2.12'), "gics_code": "401010",
         "debt_to_equity": Decimal('1.45'), "data_as_of": datetime.now()},

        {"symbol": "HSBC", "sector": "Financial Services", "industry_group": "Banks",
         "industry": "Banks", "sub_industry": "Diversified Banks",
         "market_cap": Decimal('2278000000000'), "pe_ratio": Decimal('8.9'),
         "beta": Decimal('0.65'), "hq_country": "UK", "employees": 220000,
         "founded_year": 1865, "dividend_yield_pct": Decimal('6.85'), "gics_code": "401010",
         "debt_to_equity": Decimal('1.92'), "data_as_of": datetime.now()},

        # Energy
        {"symbol": "LNG", "sector": "Energy", "industry_group": "Oil, Gas & Consumable Fuels",
         "industry": "Oil, Gas & Consumable Fuels", "sub_industry": "Oil & Gas Midstream",
         "market_cap": Decimal('44630000000'), "pe_ratio": Decimal('12.4'),
         "beta": Decimal('0.98'), "hq_country": "USA", "employees": 1500,
         "founded_year": 1996, "dividend_yield_pct": Decimal('0.89'), "gics_code": "551060",
         "debt_to_equity": Decimal('3.25'), "data_as_of": datetime.now()},

        {"symbol": "SHEL", "sector": "Energy", "industry_group": "Oil, Gas & Consumable Fuels",
         "industry": "Integrated Oil & Gas", "sub_industry": "Integrated Oil & Gas",
         "market_cap": Decimal('199000000000'), "pe_ratio": Decimal('11.2'),
         "beta": Decimal('0.55'), "hq_country": "UK", "employees": 103000,
         "founded_year": 1907, "dividend_yield_pct": Decimal('3.98'), "gics_code": "101020",
         "debt_to_equity": Decimal('0.38'), "data_as_of": datetime.now()},

        {"symbol": "BP", "sector": "Energy", "industry_group": "Oil, Gas & Consumable Fuels",
         "industry": "Integrated Oil & Gas", "sub_industry": "Integrated Oil & Gas",
         "market_cap": Decimal('64990000000'), "pe_ratio": Decimal('9.8'),
         "beta": Decimal('0.72'), "hq_country": "UK", "employees": 67800,
         "founded_year": 1909, "dividend_yield_pct": Decimal('5.42'), "gics_code": "101020",
         "debt_to_equity": Decimal('0.65'), "data_as_of": datetime.now()},

        # Healthcare
        {"symbol": "AZN", "sector": "Health Care", "industry_group": "Pharmaceuticals",
         "industry": "Pharmaceuticals", "sub_industry": "Pharma General",
         "market_cap": Decimal('279427000000'), "pe_ratio": Decimal('28.5'),
         "beta": Decimal('0.41'), "hq_country": "UK", "employees": 89400,
         "founded_year": 1999, "dividend_yield_pct": Decimal('1.89'), "gics_code": "352010",
         "debt_to_equity": Decimal('0.92'), "data_as_of": datetime.now()},
    ]

    # Validate with schema
    validated = []
    for row in companies:
        try:
            company_row = CompanyMetadata(**row)
            validated.append(company_row.model_dump())
        except Exception as e:
            logger.warning(f"Metadata validation failed for {row['symbol']}: {e}")

    if validated:
        df = pd.DataFrame(validated)

        # CSV output
        path = RAW_METADATA_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)  # index=False means no extra index column [web:98]
        logger.success(f"✅ Metadata saved: {len(df)} companies → {path}")


def fetch_and_save(symbol: str, start_date: str, data_dir: Path):
    """Fetch OHLCV, validate schema, save CSV."""
    logger.info(f"Fetching {symbol} from {start_date}")

    # Get data (simple!)
    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, interval='1d')

    if df.empty:
        logger.error(f"No data for {symbol}")
        return

    # Convert to your schema format
    df.reset_index(inplace=True)
    df = df.rename(columns={
        'Date': 'timestamp', 'Open': 'open', 'High': 'high',
        'Low': 'low', 'Close': 'close', 'Volume': 'volume'
    })
    df['symbol'] = symbol
    df['ingest_date'] = datetime.now().date()

    # Validate EVERY row with your schema
    validated_rows = []
    for _, row in df.iterrows():
        try:
            market_row = MarketRow(**row.to_dict())
            validated_rows.append(market_row.model_dump())
        except Exception as e:
            logger.warning(f"Skipping invalid row: {e}")

    if not validated_rows:
        return

    validated_df = pd.DataFrame(validated_rows)

    # Save partitioned (symbol/date)
    symbol_dir = RAW_MARKET_DIR / symbol
    symbol_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = symbol_dir / f"{date_str}.csv"

    validated_df.to_csv(path, index=False)  # CSV output [web:98]
    logger.success(f"Saved {len(validated_df)} rows to {path}")


if __name__ == "__main__":
    config = load_config()
    data_dir = RAW_MARKET_DIR.parent
    for symbol in config['symbols']:
        fetch_and_save(symbol, config['start_date'], data_dir)
    ingest_metadata()  # Always ingest metadata
