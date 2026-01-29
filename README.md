


# 📈 FinSense  
**Multi-Signal, Explainable Stock Forecasting Platform**

FinSense is a **production-style machine learning system** for **stock price direction forecasting** that goes beyond traditional technical-indicator models.

Instead of relying solely on historical price data, FinSense combines **market signals, technical indicators, and NLP-based sentiment analysis** to generate **explainable, auditable forecasts** suitable for real-world financial decision support.

The project is designed to demonstrate **how ML forecasting systems are actually built in practice** — with baselines, evaluation discipline, drift monitoring, explainability, and API-based serving.

---

## 🎯 Problem Statement

Most retail and academic stock-forecasting projects suffer from:
- Overfitting on historical prices
- No comparison against realistic baselines
- Black-box predictions with no explanations
- No monitoring once deployed

In real financial environments, **directional accuracy, robustness, and interpretability** matter more than raw returns.

**FinSense addresses these gaps.**

---

## 🧠 Solution Overview

FinSense predicts **next-day price direction** (up / down) using a **multi-signal approach**:

### Signals Used
1. **Technical indicators**
   - Moving averages
   - Momentum & volatility features
2. **Market context**
   - Volume dynamics
   - Trend consistency
3. **NLP sentiment signals**
   - News & text sentiment using FinBERT-style embeddings

All signals are fused into a **single forecasting model**, with results compared against clear baselines.

---

## 🧱 System Architecture

Market Data
│
├── Price & Volume
│       └── Technical Features
│
├── News / Text
│       └── NLP Sentiment (FinBERT)
│
└── Feature Fusion
└── Forecasting Model
│
├── Direction Prediction
├── Confidence Score
└── SHAP Explanations
│
FastAPI Prediction Service

---

## 📊 Model Performance

### 🎯 Directional Accuracy (Out-of-Sample)

| Model | Directional Accuracy |
|-----|----------------------|
| Random Baseline | 50% |
| Technical-Only Model | 52% |
| **FinSense (Multi-Signal)** | **58%** |

Key points:
- Evaluated on a **held-out time-based test set**
- No data leakage
- Accuracy improvement driven by **signal fusion**, not model complexity

---

## 🧠 Explainability

FinSense prioritizes **transparent predictions**:

- SHAP-based feature attribution
- Clear separation of:
  - Technical influence
  - Sentiment influence
- Enables analysts to understand **why** a prediction was made

Example explanation:
> “Positive sentiment offset weak momentum, resulting in a bullish forecast.”

---

## ⚙️ Production-Grade Design

### Key Engineering Decisions
- Time-aware train/validation splits
- Baseline comparison mandatory
- Feature drift monitoring hooks
- Stateless prediction API
- Modular pipeline (ingestion → features → model → explainability → serving)

This is **not a notebook-only project**.

---

## 🛠️ Tech Stack

### Core
- Python
- FastAPI

### Machine Learning
- LightGBM
- Scikit-learn
- Time-series feature engineering

### NLP
- FinBERT / Transformer-based sentiment models
- Text embeddings for sentiment aggregation

### Explainability
- SHAP

### MLOps Concepts
- Feature drift detection
- Reproducible pipelines
- API-based inference

---

## 📁 Project Structure

finsense/
├── api/                 # FastAPI inference service
├── data/                # Market & sentiment datasets
├── features/            # Feature engineering logic
├── models/              # Forecasting models
├── evaluation/          # Metrics & baselines
├── explainability/      # SHAP analysis
├── notebooks/           # Experiments & validation
└── README.md

---

## 🚀 Getting Started


git clone https://github.com/amanramasharma/finsense.git

cd finsense

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn api.main:app --reload

API available at:

http://127.0.0.1:8000


⸻

🔐 Data Disclaimer
	- Data used is public or synthetic
	- No proprietary trading data
	-	Project is for educational and portfolio purposes only
	-	Not financial advice

⸻

📈 Why FinSense Matters

This project demonstrates:
	•	Realistic evaluation discipline (baselines first)
	•	Practical use of NLP in financial forecasting
	•	Explainability as a first-class concern
	•	ML system design beyond model training

It reflects how forecasting systems are built in professional environments, not hype-driven trading bots.

⸻

👨‍💻 Author

- Aman Sharma
- Machine Learning Engineer
- MSc Data Science — University of Surrey
	- 	GitHub: https://github.com/amanramasharma
	- 	LinkedIn: https://www.linkedin.com/in/amanramasharma/

⸻

📌 Disclaimer

This project is not intended for live trading and should not be used as financial advice.

