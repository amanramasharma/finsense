"""
FS-10: Core Market Features (Returns, Volatility, Volume)
Input: data/processed/market/daily_ohlcv.parquet
Output: data/processed/features/market.parquet + market.csv
"""
import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
from common.config.paths import PROCESSED_MARKET_DIR, PROCESSED_FEATURES_DIR

def calculate_market_features():
    """
    Features:
    - ret_1d, ret_3d, ret_5d: Returns over 1/3/5 days
    - vol_20d: 20-day rolling volatility  
    - vol_zscore: Volume vs 20-day rolling mean/std
    """
    
    logger.info("🔄 FS-10: Calculating core market features...")
    
    # Step 1: Load clean OHLCV data
    input_file = PROCESSED_MARKET_DIR / "daily_ohlcv.parquet"
    df = pd.read_parquet(input_file)
    logger.info(f"📊 Loaded {len(df):,} rows from {input_file}")
    
    # Step 2: Calculate returns (1D, 3D, 5D)
    df['ret_1d'] = df.groupby('symbol')['close'].pct_change(1)
    df['ret_3d'] = df.groupby('symbol')['close'].pct_change(3)  
    df['ret_5d'] = df.groupby('symbol')['close'].pct_change(5)
    
    # Step 3: 20D Volatility (std dev of daily returns)
    df['vol_20d'] = (df.groupby('symbol')['ret_1d']
                    .rolling(window=20, min_periods=10)
                    .std()
                    .reset_index(0, drop=True))
    
    # Step 4: Volume stats for Z-Score
    df['vol_mean_20d'] = (df.groupby('symbol')['volume']
                         .rolling(window=20, min_periods=10)
                         .mean()
                         .reset_index(0, drop=True))
    
    df['vol_std_20d'] = (df.groupby('symbol')['volume']
                        .rolling(window=20, min_periods=10)
                        .std()
                        .reset_index(0, drop=True))
    
    # Step 5: Volume Z-Score
    df['vol_zscore'] = (df['volume'] - df['vol_mean_20d']) / df['vol_std_20d']
    
    # Step 6: Select FINAL features + sort
    feature_cols = ['symbol', 'timestamp', 'ret_1d', 'ret_3d', 'ret_5d', 'vol_20d', 'vol_zscore']
    features_df = df[feature_cols].sort_values(['symbol', 'timestamp']).reset_index(drop=True)
    
    # Step 7: Save Parquet (ML fast format)
    output_parquet = PROCESSED_FEATURES_DIR / "market.parquet"
    features_df.to_parquet(output_parquet, index=False)
    
    # Step 8: Save CSV (Excel friendly)
    output_csv = PROCESSED_FEATURES_DIR / "market.csv"
    features_df.to_csv(output_csv, index=False)
    
    # Step 9: Summary
    non_null_features = features_df[['ret_1d', 'ret_3d', 'ret_5d', 'vol_20d', 'vol_zscore']].notna().sum()
    
    logger.success("🎉 FS-10 COMPLETE!")
    logger.success(f"   📊 {len(features_df):,} rows, {features_df['symbol'].nunique()} symbols")
    logger.success(f"   🏷️  Features: {non_null_features.to_dict()}")
    logger.success(f"   💾 Parquet: {output_parquet}")
    logger.success(f"   📊 CSV: {output_csv}")

if __name__ == "__main__":
    calculate_market_features()
