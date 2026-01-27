"""
Centralized data path configuration.
Shared by all modules (ml, nlp, rag, serving).
"""
from pathlib import Path

# Project root (assumes this file is in common/config/)
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Raw data paths (unmodified data from external sources)
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_MARKET_DIR = RAW_DATA_DIR / "market"
RAW_METADATA_DIR = RAW_DATA_DIR / "metadata"
RAW_METADATA_FILE = RAW_METADATA_DIR / "companies.csv"

# Processed data paths (ML-ready data)
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_MARKET_DIR = PROCESSED_DATA_DIR / "market"
PROCESSED_FEATURES_DIR = PROCESSED_DATA_DIR / "features"

# YAML config (for symbols, date ranges)
ML_CONFIG_FILE = PROJECT_ROOT / "ml" / "config.yaml"

# Auto-create directories on import (prevents crashes)
RAW_MARKET_DIR.mkdir(parents=True, exist_ok=True)
RAW_METADATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_MARKET_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_FEATURES_DIR.mkdir(parents=True, exist_ok=True)
