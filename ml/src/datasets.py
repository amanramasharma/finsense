import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
from common.config.paths import PROCESSED_MARKET_DIR, PROCESSED_FEATURES_DIR

def build_market_only_dataset():
    """Join features with next-day log returns."""
    
    logger.info(" FS-11: Building market-only ML dataset...")
    
    # 1. Load PRICES → Create targets
    prices_file = PROCESSED_MARKET_DIR / "daily_ohlcv.parquet"
    prices = pd.read_parquet(prices_file)
    
    # Create next-day close and log return
    prices['next_close'] = prices.groupby('symbol')['close'].shift(-1)
    prices['next_1d_log_return'] = np.log(prices['next_close'] / prices['close'])
    
    logger.info(f" Prices loaded: {len(prices):,} rows, targets created")
    
    # 2. Load FEATURES
    features_file = PROCESSED_FEATURES_DIR / "market.parquet"
    features = pd.read_parquet(features_file)
    logger.info(f" Features loaded: {len(features):,} rows")
    
    # 3. JOIN: features + targets (same symbol/timestamp)
    dataset = features.merge(
        prices[['symbol', 'timestamp', 'next_1d_log_return']],
        on=['symbol', 'timestamp'],
        how='inner'
    )
    
    logger.info(f" Joined dataset: {len(dataset):,} rows")
    
    # 4. Filter COMPLETE rows (no NaN features OR target)
    feature_cols = ['ret_1d', 'ret_3d', 'ret_5d', 'vol_20d', 'vol_zscore']
    before = len(dataset)
    dataset = dataset.dropna(subset=feature_cols + ['next_1d_log_return'])
    after = len(dataset)
    
    logger.info(f"Cleaned: {before:,} → {after:,} complete rows")
    
    # 5. Reorder: features first, target last
    cols = ['symbol', 'timestamp'] + feature_cols + ['next_1d_log_return']
    dataset = dataset[cols]
    
    # 6. Create train folder + save
    output_file = Path("data/processed") / "train_market_only.parquet"
    output_file.parent.mkdir(exist_ok=True)
    dataset.to_parquet(output_file, index=False)
    
    # Export CSV too
    output_csv = output_file.with_suffix('.csv')
    dataset.to_csv(output_csv, index=False)
    
    # Stats
    target_stats = dataset['next_1d_log_return'].describe()
    
    logger.success(" FS-11 COMPLETE - ML READY!")
    logger.success(f"   {len(dataset):,} rows for training")
    logger.success(f"   next_1d_log_return: mean={target_stats['mean']:.4f}")
    logger.success(f"   Parquet: {output_file}")
    logger.success(f"   CSV: {output_csv}")

if __name__ == "__main__":
    build_market_only_dataset()
