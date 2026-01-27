"""
Build daily OHLCV processed table
Combines all raw market data into single clean table (Parquet + CSV).
"""
import pandas as pd
from pathlib import Path
from loguru import logger
from common.config.paths import RAW_MARKET_DIR, PROCESSED_MARKET_DIR

def process_daily_ohlcv():
    """
    1. Read all data/raw/market/symbol/*.csv files
    2. Concatenate into single DataFrame
    3. Parse timestamps (convert string → datetime)
    4. Sort by symbol, timestamp
    5. Deduplicate (keep latest row if duplicates)
    6. Save as Parquet (ML standard) + CSV (Excel friendly)
    """
    
    logger.info("🔄 Building daily OHLCV processed table...")
    
    # Step 1: Find all CSV files recursively
    csv_files = list(RAW_MARKET_DIR.rglob("*.csv"))
    logger.info(f"📂 Found {len(csv_files)} CSV files: {RAW_MARKET_DIR}")
    
    if not csv_files:
        logger.error("❌ No CSV files found in data/raw/market/")
        return
    
    # Step 2: Read all files and track source
    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            df['source_file'] = csv_file.name  # Track which file it came from
            dfs.append(df)
            logger.info(f"✅ Loaded {len(df)} rows from {csv_file.name}")
        except Exception as e:
            logger.warning(f"⚠️  Failed to load {csv_file.name}: {e}")
    
    if not dfs:
        logger.error("❌ No data successfully loaded")
        return
    
    # Step 3: Concatenate all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    logger.info(f"🔗 Combined: {len(combined_df):,} total rows")
    
    # Step 4: Parse timestamps (string → datetime)
    combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
    logger.info("✅ Timestamps parsed to datetime")
    
    # Step 5: Sort by symbol, timestamp (chronological order)
    combined_df = combined_df.sort_values(['symbol', 'timestamp']).reset_index(drop=True)
    logger.info("✅ Data sorted by symbol, timestamp")
    
    # Step 6: Deduplicate (if same symbol+date exists multiple times, keep latest)
    before_dedup = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['symbol', 'timestamp'], keep='last')
    after_dedup = len(combined_df)
    logger.info(f"🧹 Deduplicated: {before_dedup:,} → {after_dedup:,} rows")
    
    # Step 7: Save as Parquet (ML standard: fast, small, schema-aware)
    output_parquet = PROCESSED_MARKET_DIR / "daily_ohlcv.parquet"
    combined_df.to_parquet(output_parquet, index=False)
    
    # Step 8: Export CSV for Excel/team collaboration
    output_csv = PROCESSED_MARKET_DIR / "daily_ohlcv.csv"
    combined_df.to_csv(output_csv, index=False)
    
    # Step 9: Summary statistics
    symbols_count = combined_df['symbol'].nunique()
    date_range = combined_df['timestamp'].agg(['min', 'max'])
    
    logger.success("FS-9 COMPLETE!")
    logger.success(f" {len(combined_df):,} rows, {symbols_count} symbols")
    logger.success(f" {date_range['min'].date()} → {date_range['max'].date()}")
    logger.success(f" Parquet (ML): {output_parquet}")
    logger.success(f" CSV (Excel): {output_csv}")

if __name__ == "__main__":
    process_daily_ohlcv()
