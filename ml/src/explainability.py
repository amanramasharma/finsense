import pandas as pd
import numpy as np
import shap
import joblib
import lightgbm as lgb  # for type compatibility
from pathlib import Path
from loguru import logger
from common.config.paths import PROCESSED_FEATURES_DIR


FEATURE_COLS = ["ret_1d", "ret_3d", "ret_5d", "vol_20d", "vol_zscore"]


def _load_model(model_path: Path):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = joblib.load(model_path)
    logger.info(f"Loaded model from {model_path}")
    return model


def _load_validation_frame() -> pd.DataFrame:
    data_file = PROCESSED_FEATURES_DIR.parent / "train_market_only.parquet"
    if not data_file.exists():
        raise FileNotFoundError(f"Training dataset not found: {data_file}")

    df = pd.read_parquet(data_file)
    logger.info(f"Loaded dataset: {len(df)} rows from {data_file}")

    df_sorted = df.sort_values("timestamp").reset_index(drop=True)
    split_idx = int(len(df_sorted) * 0.8)
    val_df = df_sorted.iloc[split_idx:].reset_index(drop=True)
    logger.info(f"Validation slice for SHAP: {len(val_df)} rows")

    return val_df


def generate_shap_for_baseline():
    logger.info("FS-Explain: Starting SHAP computation for baseline model")

    # 1. Load model and validation data
    model_path = Path("ml/artifacts/lgbm_market_only.pkl")
    model = _load_model(model_path)

    val_df = _load_validation_frame()
    X_val = val_df[FEATURE_COLS]

    # 2. SHAP explainer and values
    logger.info("Creating SHAP TreeExplainer")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_val)
    base_value = explainer.expected_value
    logger.info("SHAP values computed")

    # 3. Global summary plot
    artifacts_dir = Path("ml/artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    shap_plot_path = artifacts_dir / "shap_market_only_summary.png"

    logger.info(f"Saving SHAP summary plot to {shap_plot_path}")
    import matplotlib.pyplot as plt

    plt.figure()
    shap.summary_plot(shap_values, X_val, show=False)
    plt.tight_layout()
    plt.savefig(shap_plot_path, dpi=200)
    plt.close()

    # 4. Per-row SHAP table
    shap_df = pd.DataFrame(
        shap_values,
        columns=[f"shap_{col}" for col in FEATURE_COLS],
    )

    y_pred = model.predict(X_val)

    shap_full = pd.concat(
        [
            val_df[["symbol", "timestamp"]].reset_index(drop=True),
            X_val.reset_index(drop=True),
            shap_df.reset_index(drop=True),
        ],
        axis=1,
    )
    shap_full["prediction"] = y_pred
    shap_full["base_value"] = base_value

    # 5. Save SHAP values (Parquet + CSV)
    shap_parquet_path = PROCESSED_FEATURES_DIR / "shap_market_only.parquet"
    shap_csv_path = PROCESSED_FEATURES_DIR / "shap_market_only.csv"
    shap_parquet_path.parent.mkdir(parents=True, exist_ok=True)

    shap_full.to_parquet(shap_parquet_path, index=False)
    shap_full.to_csv(shap_csv_path, index=False)

    logger.success(f"Saved per-row SHAP values to {shap_parquet_path}")
    logger.success(f"Saved per-row SHAP CSV to {shap_csv_path}")
    logger.success(f"Saved SHAP summary plot to {shap_plot_path}")
    logger.success("FS-Explain: SHAP explainability generation complete")


if __name__ == "__main__":
    generate_shap_for_baseline()
