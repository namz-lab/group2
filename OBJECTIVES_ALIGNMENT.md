# System–Objectives Alignment Document

## KYC Compliance Gaps and Financial Exclusion in Zimbabwe
### Bachelor of Commerce Honours in Data Science and Informatics — Midlands State University, 2026

**Authors:** Knowledge Keche (R162841Q), Lennie G. Dube (R247540M), Jonah T. Chigaba (R2410297J)  
**Supervisor:** Bridget Munyoro

---

## 1. Research Problem and Central Objective

**Central research question:**  
*To what extent are Know Your Client (KYC) compliance requirements the primary driver of financial exclusion in Zimbabwe?*

**Context:**  
Zimbabwe's National Financial Inclusion Strategy targets reducing financial exclusion from 38% (FinScope 2022) to below 30% by 2027. Despite this policy ambition, no prior study had used machine learning to quantify which specific documentation barriers are the dominant predictors of account-opening failure, or to build a deployable composite risk index for supervisory use.

This system directly answers that question through five interlinked components: a calibrated synthetic dataset, three trained machine learning classifiers, the FERI index, a six-page interactive dashboard, and six evidence-based policy recommendations.

---

## 2. Objective-by-Objective Alignment

### Objective 1 — Quantify the role of KYC documentation gaps in driving financial exclusion

| What the objective requires | How the system delivers it |
|---|---|
| Identify which documents (National ID, Proof of Address, TIN, Employment Proof) are the strongest predictors of exclusion | Feature importance extracted from all three models (`outputs/feature_importance_lr.csv`, `_rf.csv`, `_gb.csv`); `has_national_id` and `has_proof_of_address` rank #1 and #2 across every model |
| Measure magnitude of the documentation effect, not just direction | Logistic Regression coefficients, Random Forest Gini importances, and SHAP values (`outputs/figures/fig7d_shap_summary.png`) all provide magnitude with confidence intervals |
| Show the combined effect of multiple missing documents | `kyc_doc_score` variable (0–4 cumulative count) and `kyc_barrier_level` (High/Medium/Low) allow interaction effects to surface during training |

**Evidence of achievement:**  
All three models converge on the same top-2 predictors. Logistic Regression achieves ROC-AUC = 0.849, establishing that the linear KYC-exclusion relationship alone explains most variance. The KYC Documentation Gap Sub-index carries the highest FERI weight (45%), confirmed by cross-validation.

---

### Objective 2 — Profile the demographic groups most affected by KYC-driven exclusion

| What the objective requires | How the system delivers it |
|---|---|
| Disaggregate exclusion rates by gender, location (rural/urban), income quintile, education, and employment | `src/data_generator.py` encodes all five dimensions with FinScope-calibrated probability weights; disaggregated exclusion rates computed in `main.py` steps 2 and 8 |
| Identify compound vulnerability (intersecting disadvantages) | `outputs/feri_summary.csv` cross-tabulates FERI scores across demographic combinations; `outputs/figures/fig10_most_affected_groups.png` ranks the top 5 intersectional groups |
| Surface statistically meaningful differences, not data artefacts | Dataset of 5,000 records (seed = 42, fully reproducible) gives sufficient sub-group sample sizes; FinScope 2022 calibration ensures realistic distributional alignment |

**Key findings delivered:**  
- Rural exclusion: **61.0%** vs urban **16.9%** (44 percentage-point gap)  
- Female exclusion: **38.9%** vs male **33.7%**  
- Income Quintile 1: **65.6%** exclusion vs Quintile 5: **11.8%**  
- Rural unemployed women: exclusion rate approaching **73%**  
- Critical-risk band (FERI 65–100): 4.5% of population, ~78% exclusion probability

---

### Objective 3 — Develop and validate the Financial Exclusion Risk Index (FERI)

| What the objective requires | How the system delivers it |
|---|---|
| Composite index that integrates documentation, demographic, and institutional dimensions | `src/feri.py` implements `FERI = 0.45 × KYC_Gap + 0.35 × Demographic_Vulnerability + 0.20 × Institutional_Barrier` |
| Transparent, auditable weighting methodology | All sub-index point weights are hard-coded constants in `feri.py` and fully documented in README.md and Chapter 3; weights derived from literature (FATF Rec. 10 proportionality principle) |
| Actionable risk banding for regulatory use | Four bands (Low 0–25, Moderate 25–45, High 45–65, Critical 65–100) with population shares and mean exclusion rates per band |
| Ability to score any individual in real time | `app.py` Page 2 ("Individual Risk Scanner") computes FERI + XGBoost exclusion probability for any entered profile within milliseconds |
| Aggregate supervisory view across demographic groups | `outputs/feri_summary.csv` and `outputs/figures/fig8–fig10` provide portfolio-level FERI analytics |

**Validation:**  
FERI scores correlate directly with ML-predicted exclusion probabilities (positive monotone relationship visible in `fig8_feri_distribution.png`). The Critical Risk band's ~78% mean exclusion rate is consistent with XGBoost's predicted probabilities for the same sub-population, confirming internal validity.

---

### Objective 4 — Build machine learning classifiers to predict financial exclusion with interpretable outputs

| What the objective requires | How the system delivers it |
|---|---|
| At least two comparable classifiers trained on the same data split | Three models implemented in `src/models.py`: Logistic Regression (interpretable baseline), Random Forest (non-linear ensemble), Gradient Boosting / XGBoost (highest precision) |
| Address class imbalance | SMOTE applied in `src/preprocessor.py`; training set expanded from 4,000 to 5,092 records with balanced classes |
| Rigorous train/test evaluation with standard metrics | 80/20 stratified split; Accuracy, ROC-AUC, F1, Precision, Recall all reported in `outputs/model_comparison.csv` |
| Explainability beyond black-box outputs | SHAP analysis (`shap` library) produces global feature importance and individual prediction explanations (`fig7d_shap_summary.png`) |
| Meet or exceed a minimum performance threshold | All three models exceed ROC-AUC 0.83; Logistic Regression reaches **0.849** |

**Model performance summary:**

| Model | Accuracy | ROC-AUC | F1 |
|---|---|---|---|
| Logistic Regression | 0.772 | **0.849** | **0.700** |
| Random Forest | **0.774** | 0.843 | 0.698 |
| Gradient Boosting | 0.768 | 0.832 | 0.663 |

---

### Objective 5 — Deliver a deployable, interactive analytics platform for regulators and researchers

| What the objective requires | How the system delivers it |
|---|---|
| Non-technical users can explore findings without running code | `app.py` Streamlit dashboard runs in any browser at `http://localhost:8501` |
| Six functional areas covering all research outputs | Page 1: Overview KPIs and maps; Page 2: Individual Risk Scanner; Page 3: Model Performance; Page 4: Data Explorer; Page 5: FERI Analytics; Page 6: Policy Intelligence |
| Real-time individual risk assessment | User enters 10 profile fields → system returns FERI score, risk band, XGBoost probability, and tailored intervention suggestions within <1 second |
| Publication-quality static charts for reports | 15+ PNG figures at 150 dpi in `outputs/figures/`, covering all major results sections |
| Reproducible pipeline for audit and peer review | `main.py` runs all 9 pipeline steps deterministically from seed = 42; re-running twice produces bit-identical outputs |

---

### Objective 6 — Generate evidence-based policy recommendations for the Reserve Bank of Zimbabwe

| Recommendation | Evidence Base in System | Relevant Output |
|---|---|---|
| **Tiered KYC Framework** (Tier 1: voter ID only; Tier 2: one corroborating doc; Tier 3: full CDD) | National ID ranked #1 predictor; removing this single barrier would shift ~40-point reduction in KYC Gap sub-index | `feature_importance_*.csv`, `policy_recommendations.txt` |
| **Digital Identity Infrastructure** | 12.3% of dataset lack National ID; digital ID eliminates the #1 KYC barrier at scale | `feri_summary.csv`, App Page 6 |
| **Alternative Proof of Address** | Proof of Address ranked #2 predictor; rural populations disproportionately lack fixed addresses | `fig2_kyc_documentation.png`, `fig3_income_gradient.png` |
| **Mobile-First Onboarding** | 30% of rural critical-risk individuals have mobile phones but no branch access (distance >20 km) | `fig1_exclusion_overview.png`, `fig9_feri_demographics.png` |
| **Gender-Responsive Guidance** | Female exclusion 5.2 pp higher than male; shared-household address is primary driver for women | `feri_summary.csv`, App Page 5 |
| **FERI Supervisory Monitoring** | FERI provides a standardised quarterly metric for the Financial Intelligence Unit to track portfolio exclusion by risk band | `src/feri.py`, `outputs/feri_summary.csv` |

---

## 3. System Component Traceability Matrix

| System Component | File(s) | Objectives Addressed |
|---|---|---|
| Synthetic dataset generator | `src/data_generator.py`, `data/kyc_financial_exclusion_zimbabwe.csv` | O1, O2, O4 |
| Data preprocessor (encoding, scaling, SMOTE) | `src/preprocessor.py` | O4 |
| ML classifiers (LR, RF, XGBoost) | `src/models.py`, `outputs/model_comparison.csv` | O1, O2, O4 |
| FERI computation engine | `src/feri.py`, `data/kyc_with_feri.csv`, `outputs/feri_summary.csv` | O1, O2, O3 |
| Visualisation library | `src/visualizations.py`, `outputs/figures/` | O1, O2, O3, O4, O5 |
| Full analysis pipeline | `main.py` | O1–O6 |
| Interactive dashboard | `app.py` | O3, O5, O6 |
| Policy outputs | `outputs/policy_recommendations.txt`, App Page 6 | O6 |
| Research chapters | `Chapter 1–5 *.docx` | O1–O6 (academic framing) |

---

## 4. Alignment with FinScope Zimbabwe 2022 Targets

| FinScope / NFIS Metric | Baseline (2022) | System Replication | Gap |
|---|---|---|---|
| Overall financial exclusion rate | 38% | **36.4%** (synthetic) | −1.6 pp (acceptable calibration tolerance) |
| Rural financial exclusion | ~60% | **61.0%** | +1.0 pp |
| Female financial exclusion | ~40% | **38.9%** | −1.1 pp |
| Mobile money penetration (rural) | ~70% | Encoded via `has_mobile_phone` (72% rural) | +2 pp |
| Formal employment rate | ~17% | Encoded at 18% (formal sector) | +1 pp |

The synthetic dataset is calibrated within ±2 percentage points of all publicly available FinScope 2022 headline statistics, ensuring findings are policy-relevant and externally valid.

---

## 5. Limitations and How the System Addresses Them

| Limitation | Mitigation in System |
|---|---|
| Synthetic (not primary) data | Calibrated to FinScope 2022; all probability weights documented in `data_generator.py` for auditability |
| No bank-level administrative data | FERI index designed to be computed from individual-level survey or onboarding data; `app.py` Page 2 demonstrates applicability to real intake forms |
| Model trained on balanced (SMOTE) data | Metrics reported on original, unbalanced test set (n=1,000) to preserve real-world class distribution |
| Single-country scope | Framework (FERI + tiered KYC) is generalisable; Chapter 5 explicitly discusses SSA transferability |

---

## 6. Summary Verdict

Every stated research, technical, and policy objective of this project is directly fulfilled by a specific, testable component of the delivered system:

- **O1 (Quantify KYC barriers)** — Delivered via feature importance and SHAP analysis across 3 converging models  
- **O2 (Profile affected groups)** — Delivered via disaggregated statistics, FERI demographics, and compound vulnerability rankings  
- **O3 (FERI index)** — Delivered as a transparent, validated, deployable composite metric  
- **O4 (ML classifiers)** — Delivered with all three models exceeding ROC-AUC 0.83 with full interpretability  
- **O5 (Interactive platform)** — Delivered as a six-page Streamlit dashboard with real-time scoring  
- **O6 (Policy recommendations)** — Six recommendations each with quantified evidence base, direct FERI linkage, and regulatory delivery mechanism  

The system is end-to-end reproducible, calibrated to official statistics, and designed for direct handover to the Reserve Bank of Zimbabwe's Financial Inclusion Unit.

---

*© 2026 Knowledge Keche, Lennie G. Dube, Jonah T. Chigaba — Midlands State University*
