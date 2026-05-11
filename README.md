# KYC Compliance Gaps and Financial Exclusion in Zimbabwe
### A Machine Learning Analysis with FERI Analytics Platform

**Bachelor of Commerce Honours Degree in Data Science and Informatics**  
Department of Information and Marketing Sciences, Faculty of Business Sciences  
**Midlands State University** — Gweru / Harare, 2026

| Student | Registration Number |
|---|---|
| Knowledge Keche | R162841Q |
| Lennie G. Dube | R247540M |
| Jonah T. Chigaba | R2410297J |

**Supervisor:** Bridget Munyoro

---

## Overview

This project investigates how KYC (Know Your Client) compliance requirements drive financial exclusion in Zimbabwe. Using a synthetic dataset of 5,000 individuals calibrated to **FinScope Zimbabwe 2022** statistics, it trains machine learning classifiers, constructs the **Financial Exclusion Risk Index (FERI)**, and delivers an interactive analytics dashboard with evidence-based policy recommendations.

---

## Project Structure

```
group 2 project/
│
├── src/
│   ├── data_generator.py       # Synthetic dataset generator (FinScope-calibrated)
│   ├── preprocessor.py         # Encoding, scaling, SMOTE balancing
│   ├── models.py               # Logistic Regression, Random Forest, XGBoost
│   ├── feri.py                 # Financial Exclusion Risk Index computation
│   └── visualizations.py       # Matplotlib/Seaborn chart functions
│
├── data/
│   ├── kyc_financial_exclusion_zimbabwe.csv    # Raw synthetic dataset (5,000 rows)
│   └── kyc_with_feri.csv                       # Dataset enriched with FERI scores
│
├── outputs/
│   ├── model_comparison.csv                    # Model metrics table
│   ├── feri_summary.csv                        # FERI stats by demographic group
│   ├── feature_importance_lr.csv               # Logistic Regression importances
│   ├── feature_importance_rf.csv               # Random Forest importances
│   ├── feature_importance_gb.csv               # Gradient Boosting importances
│   ├── policy_recommendations.txt              # Plain-text policy summary
│   └── figures/                                # All PNG charts (150 dpi)
│
├── screenshots/                                # Key system & model visualisations
│
├── main.py                      # Full analysis pipeline (run this first)
├── app.py                       # Streamlit interactive dashboard
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

| Package | Version | Purpose |
|---|---|---|
| numpy | >=1.24 | Numerical computations |
| pandas | >=2.0 | Data manipulation |
| scikit-learn | >=1.3 | LR, RF, preprocessing, metrics |
| xgboost | >=1.7 | Gradient Boosting classifier |
| imbalanced-learn | >=0.11 | SMOTE class balancing |
| shap | >=0.42 | Model explainability |
| matplotlib | >=3.7 | Static charts |
| seaborn | >=0.12 | Statistical visualisations |
| scipy | >=1.10 | Logistic sigmoid (data generation) |
| streamlit | >=1.28 | Interactive dashboard |
| plotly | >=5.17 | Dashboard charts |

---

### 2. Run the Full Analysis Pipeline

```bash
python main.py
```

This runs all 9 steps end-to-end (~60 seconds):

1. Generates synthetic dataset (n=5,000, FinScope-calibrated)
2. Exploratory data analysis and charts
3. Data preprocessing (encoding + scaling + SMOTE)
4. Trains Logistic Regression, Random Forest, XGBoost
5. Evaluates all models on held-out test set
6. Saves ROC curves, confusion matrices, feature importance charts
7. Computes FERI scores for all 5,000 individuals
8. Reports top 5 highest-risk demographic groups
9. Outputs evidence-based policy recommendations

**All outputs are saved to `data/` and `outputs/`.**

---

### 3. Launch the Interactive Dashboard

```bash
python -m streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

| Page | What it Shows |
|---|---|
| **Overview Dashboard** | KPI cards, exclusion by province, FERI band distribution, age/income charts, KYC heatmap |
| **Individual Risk Scanner** | Enter any individual's profile → get real-time FERI score + XGBoost exclusion probability + intervention recommendations |
| **Model Performance** | ROC curves, radar chart, confusion matrices, feature importance for all 3 models |
| **Data Explorer** | Filterable table + scatter/histogram charts with the full 5,000-row dataset |
| **FERI Analytics** | FERI distribution, sub-score breakdown, demographic comparisons, correlation matrix |
| **Policy Intelligence** | 6 evidence-based policy cards with evidence base + priority matrix bubble chart |

---

## The FERI Index

The **Financial Exclusion Risk Index** is a composite 0–100 score developed specifically for this study.

```
FERI = 0.45 × KYC_Gap + 0.35 × Demographic_Vulnerability + 0.20 × Institutional_Barrier
```

### Sub-Index Components

**KYC Documentation Gap Score (45%)**

| Missing Document | Points |
|---|---|
| National ID | 40 |
| Proof of Address | 30 |
| TIN | 20 |
| Employment Proof | 10 |

**Demographic Vulnerability Score (35%)**

| Factor | Points |
|---|---|
| Rural location | 20 |
| Unemployed | 20 |
| Income Quintile 1 | 15 |
| No formal education | 12 |
| Informal employment | 12 |
| Female | 10 |
| Income Quintile 2 | 8 |
| Age <25 or >64 | 8 |
| Primary education only | 6 |

**Institutional Barrier Score (20%)**

| Factor | Points |
|---|---|
| Distance to branch >20 km | 30 |
| No mobile phone | 30 |
| No internet access | 20 |
| Remote province | 20 |
| Distance 10–20 km | 15 |
| Distance 5–10 km | 5 |

### Risk Bands

| Band | Score Range | Population Share | Mean Exclusion Rate |
|---|---|---|---|
| Low Risk | 0–25 | 43.1% | ~14% |
| Moderate Risk | 25–45 | 31.9% | ~37% |
| High Risk | 45–65 | 20.5% | ~62% |
| Critical Risk | 65–100 | 4.5% | ~78% |

---

## Model Performance Summary

All models trained on SMOTE-balanced training set (n=5,092), evaluated on held-out test set (n=1,000).

| Model | Accuracy | ROC-AUC | F1-Score | Precision | Recall |
|---|---|---|---|---|---|
| Logistic Regression | 0.772 | **0.849** | **0.700** | 0.672 | 0.731 |
| Random Forest | **0.774** | 0.843 | 0.698 | 0.680 | 0.717 |
| Gradient Boosting | 0.768 | 0.832 | 0.663 | **0.704** | 0.626 |

---

## Dataset Variables

| Variable | Type | Description |
|---|---|---|
| `age` | Numeric | Age in years (18–80) |
| `gender` | Categorical | Male / Female |
| `location` | Categorical | Urban / Rural |
| `province` | Categorical | 10 Zimbabwean provinces |
| `education_level` | Categorical | None / Primary / Secondary / Tertiary |
| `employment_sector` | Categorical | Formal / Informal / Unemployed |
| `income_quintile` | Ordinal | 1 (lowest) to 5 (highest) |
| `has_national_id` | Binary | Holds valid national ID (0/1) |
| `has_proof_of_address` | Binary | Holds proof of address (0/1) |
| `has_tin` | Binary | Holds Tax Identification Number (0/1) |
| `has_employment_proof` | Binary | Holds employment documentation (0/1) |
| `kyc_doc_score` | Numeric | Total KYC docs held (0–4) |
| `kyc_barrier_level` | Categorical | High / Medium / Low |
| `distance_to_branch_km` | Numeric | Distance to nearest bank branch |
| `has_mobile_phone` | Binary | Owns mobile phone (0/1) |
| `has_internet` | Binary | Has internet access (0/1) |
| `financially_excluded` | Binary | **Target** — 1=excluded, 0=included |

Synthetic data calibrated to **FinScope Zimbabwe Consumer Survey 2022** statistics.

---

## Key Findings

- Overall financial exclusion rate: **36.4%** (FinScope target: 38%)
- Rural exclusion rate: **61.0%** vs urban **16.9%** — a 44 pp gap
- Female exclusion: **38.9%** vs male **33.7%**
- Top 2 predictors across all models: `has_national_id` and `has_proof_of_address`
- 4.5% of population (Critical Risk band) face ~78% exclusion probability
- Rural unemployed women face exclusion rates approaching **73%**

---

## Policy Recommendations

1. **Tiered KYC Framework** — Implement Tier 1/2/3 risk-proportionate onboarding per FATF Rec. 10
2. **Digital Identity Infrastructure** — National digital ID registry interoperable across FSPs
3. **Alternative Proof of Address** — Accept chief's letters, ward councillor attestations, mobile location data
4. **Mobile-First Onboarding** — Accept Eco-Cash history as KYC evidence; mandate agent banking in rural areas
5. **Gender-Responsive Guidance** — Issue RBZ circular on shared-household address documentation
6. **FERI Supervisory Monitoring** — Require quarterly FERI-banded rejection rate reporting to FIU

---

## Reproduction

All outputs are deterministic (seed = 42). Running `main.py` twice produces identical results.

```bash
python main.py          # Full pipeline
python -m streamlit run app.py   # Dashboard
```

---

*© 2026 Knowledge Keche, Lennie G. Dube, Jonah T. Chigaba — Midlands State University*
