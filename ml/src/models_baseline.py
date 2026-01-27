import pandas as pd
import numpy as np
import lightgbm as lgb
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib
from loguru import logger
from common.config.paths import PROCESSED_FEATURES_DIR

def train_lightgbm_baseline():
    
    logger.info("Training LightGBM baseline...")
    
    # 1. Load ML dataset
    data_file = PROCESSED_FEATURES_DIR.parent / "train_market_only.parquet"
    df = pd.read_parquet(data_file)
    logger.info(f"Dataset loaded: {len(df):,} rows")
    
    # Define features and target
    feature_cols = ['ret_1d', 'ret_3d', 'ret_5d', 'vol_20d', 'vol_zscore']
    X = df[feature_cols]
    y = df['next_1d_log_return']
    
    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target range: {y.min():.4f} to {y.max():.4f}")
    
    # 2. Time-based train/val split (NO future leakage)
    # Sort by time, take first 80% for train, last 20% for val
    df_sorted = df.sort_values('timestamp')
    split_idx = int(len(df_sorted) * 0.8)
    
    X_train = X.iloc[:split_idx]
    X_val = X.iloc[split_idx:]
    y_train = y.iloc[:split_idx]
    y_val = y.iloc[split_idx:]
    
    train_date = df_sorted['timestamp'].iloc[split_idx-1].date()
    val_date = df_sorted['timestamp'].iloc[split_idx].date()
    logger.info(f"Train/Val split: {train_date} | {val_date}")
    logger.info(f"Train: {len(X_train):,} rows, Val: {len(X_val):,} rows")
    
    # 3. LightGBM datasets (optimized format)
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    # 4. LightGBM parameters (stock prediction optimized)
    params = {
        'objective': 'regression',           # Predict continuous returns
        'metric': 'rmse',                    # Optimize root mean squared error
        'boosting_type': 'gbdt',             # Gradient boosting decision tree
        'num_leaves': 31,                    # Max leaves per tree
        'learning_rate': 0.05,               # Step size (slow = stable)
        'feature_fraction': 0.9,             # Use 90% features per tree
        'bagging_fraction': 0.8,             # Use 80% rows per tree
        'bagging_freq': 5,                   # Re-bag every 5 trees
        'verbose': -1,                       # Suppress LightGBM logs
        'random_state': 42,                  # Reproducible results
        'device': 'cpu'                      # Use CPU (GPU optional)
    }
    
    # 5. Train model with early stopping
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,                # Max 1000 trees
        valid_sets=[val_data],               # Validate on val set
        callbacks=[lgb.early_stopping(50),   # Stop if no improvement 50 rounds
                   lgb.log_evaluation(100)]  # Log every 100 rounds
    )
    
    logger.info(f"Training complete: {model.num_trees()} trees")
    
    # 6. Predictions on validation set
    y_pred = model.predict(X_val, num_iteration=model.best_iteration)
    
    # 7. Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    mae = mean_absolute_error(y_val, y_pred)
    
    # Directional accuracy (did we predict up/down correctly?)
    direction_correct = np.mean(np.sign(y_val) == np.sign(y_pred))
    
    logger.info("Validation Metrics:")
    logger.info(f"  RMSE: {rmse:.6f}")
    logger.info(f"  MAE:  {mae:.6f}")
    logger.info(f"  Dir Acc: {direction_correct:.1%}")
    
    # 8. Feature importance
    importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importance(importance_type='gain')
    }).sort_values('importance', ascending=False)
    
    logger.info("Feature Importance:")
    logger.info(importance.to_string(index=False))
    
    # 9. Create artifacts folder + save model
    artifacts_dir = Path("ml/artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    
    model_file = artifacts_dir / "lgbm_market_only.pkl"
    joblib.dump(model, model_file)
    
    # FIXED OOF predictions
    oof_file = artifacts_dir / "lgbm_market_only_oof.csv"  
    oof_df = pd.DataFrame({
        'timestamp': df_sorted['timestamp'].iloc[split_idx:].values,
        'symbol': df_sorted['symbol'].iloc[split_idx:].values,
        'y_true': y_val.values,
        'y_pred': y_pred
    })
    oof_df.to_csv(oof_file, index=False)

    logger.success(f"Model saved: {model_file}")
    logger.success(f"OOF preds: {oof_file}")
    logger.success("FS-12 COMPLETE - LightGBM baseline ready!")

if __name__ == "__main__":
    train_lightgbm_baseline()
