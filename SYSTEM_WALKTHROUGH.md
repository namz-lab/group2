# KYC Financial Exclusion AI Platform — System Walkthrough

**Midlands State University — Group 2 Research Project**
**FinScope Zimbabwe 2022 | Version 2.0 | June 2026**

---

## 1. System Overview

The KYC Financial Exclusion AI Platform is a web-based analytics dashboard built with Python and Streamlit. It analyses financial exclusion in Zimbabwe using a synthetic dataset of 5,000 individuals calibrated to the FinScope Zimbabwe 2022 national survey.

The platform combines three technologies:

- **FERI (Financial Exclusion Risk Index)** — a composite 0–100 scoring model that quantifies each individual's risk of financial exclusion driven by KYC barriers
- **Machine Learning** — three classifiers (Logistic Regression, Random Forest, Gradient Boosting) that predict whether an individual is financially excluded
- **Interactive Analytics** — Plotly charts and a Streamlit dashboard that allow policymakers to explore patterns across demographic, geographic, and institutional dimensions

---

## 2. Getting Started — System Requirements

### 2.1 Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or later |
| Streamlit | 1.35 or later |
| pandas | 2.0 or later |
| scikit-learn | 1.4 or later |
| plotly | 5.17 or later |
| imbalanced-learn | 0.12 or later |
| scipy | 1.12 or later |
| python-docx | 1.1 or later |

### 2.2 Installation

1. Clone or download the project folder
2. Open a terminal in the project root
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Launch the dashboard:

```
streamlit run app.py
```

5. Open your browser at `http://localhost:8501`

---

## 3. Security — Login System

Before accessing any dashboard feature, users must authenticate. The login gate prevents unauthorised access to sensitive exclusion data.

### 3.1 Login Page

When the application starts, a branded login screen is displayed:

- **Username field** — enter your assigned username
- **Password field** — enter your password (hidden)
- **LOGIN button** — submits credentials

### 3.2 Default Credentials

| Username | Password | Role |
|---|---|---|
| admin | kyc@msu2024 | System Administrator |
| group2 | msu@group2 | Research Team |
| analyst | feri@2024 | Data Analyst |

> **Note:** Change default passwords before any public deployment. Credentials are stored in `app.py` in the `_USERS` dictionary.

### 3.3 Logout

After logging in, the sidebar displays your username and a **Logout** button. Click it to end your session and return to the login screen.

---

## 4. Navigation

The left sidebar provides navigation to six modules:

| Module | Purpose |
|---|---|
| Overview Dashboard | Key metrics, provincial exclusion map, demographic charts |
| Individual Risk Scanner | Real-time FERI scoring for a single profile |
| Model Performance | ROC curves, confusion matrices, feature importance |
| Data Explorer | Filtered browsing of the full 5,000-record dataset |
| FERI Analytics | Distribution, sub-index statistics, demographic FERI comparison |
| Policy Intelligence | Six evidence-based regulatory recommendations |

---

## 5. Overview Dashboard

### 5.1 KPI Metrics Row

Five headline metrics are displayed at the top:

- **Overall Exclusion Rate (%)** — share of the 5,000 individuals classified as financially excluded
- **Rural Exclusion Rate (%)** — exclusion rate for individuals in rural areas
- **Female Exclusion Rate (%)** — exclusion rate for female individuals
- **Mean FERI Score** — average Financial Exclusion Risk Index across all individuals (0 = fully included, 100 = critically excluded)
- **Critical Risk Individuals** — count of individuals with FERI score above 65

### 5.2 Exclusion Landscape Charts

**Financial Exclusion by Province** — horizontal bar chart showing exclusion rate per province, colour-coded from blue (low) to red (high).

**Risk Band Distribution** — donut chart showing the proportion of individuals in each FERI band:

- Low Risk (FERI 0–25)
- Moderate Risk (FERI 25–45)
- High Risk (FERI 45–65)
- Critical Risk (FERI 65–100)

### 5.3 Demographic Breakdown

Three charts in a row:

- **Exclusion by Employment** — bar chart for Formal, Informal, and Unemployed sectors
- **Age vs Exclusion Rate** — dual-axis chart: bar (population count) and line (exclusion rate) by age band
- **Income Quintile vs Exclusion** — line chart showing how exclusion rate falls as income increases from Q1 (lowest) to Q5 (highest)

### 5.4 KYC Documentation Gap Analysis

**KYC Document Possession Rate by Segment** — heatmap showing the percentage of Urban/Rural/Male/Female/Formal/Informal/Unemployed individuals who hold each of the four KYC documents:

- National ID
- Proof of Address
- Tax ID Number (TIN)
- Employment Proof

**KYC Barrier Severity** — donut chart showing how many individuals face High, Medium, or Low KYC barriers based on their document count.

---

## 6. Individual Risk Scanner

The scanner computes a real-time FERI score and machine-learning exclusion probability for any individual profile entered by the user.

### 6.1 Profile Input Form

**Demographics (left column)**

- Age (slider: 18–80)
- Location (Urban / Rural)
- Income Quintile (Q1 Lowest to Q5 Highest)
- Distance to nearest bank branch (km)

**Demographics (right column)**

- Gender (Male / Female)
- Province (10 Zimbabwe provinces)
- Employment Sector (Formal / Informal / Unemployed)
- Education Level (None / Primary / Secondary / Tertiary)

### 6.2 KYC Documents

Four checkboxes indicate which documents the individual holds:

- National ID Card
- Proof of Address
- Tax ID Number (TIN)
- Employment Proof (auto-disabled for unemployed individuals)

### 6.3 Connectivity — Including Chimbudzi Phones

The connectivity section captures mobile access using a three-way phone type selector:

| Option | Mobile Score | Internet Score | Notes |
|---|---|---|---|
| Smartphone | Has mobile = Yes | Configurable | Full app and internet KYC |
| Basic Phone (Chimbudzi) | Has mobile = Yes | No | USSD only — EcoCash *151#, ZIPIT *120*1# |
| No Phone | Has mobile = No | No | Highest institutional barrier — physical branch required |

**What is a Chimbudzi phone?** In Zimbabwean slang, a *Chimbudzi* (literally "little toilet") refers to a basic feature phone — the small, cheap handsets that can make calls and send USSD codes but have no mobile data or app capability. Millions of rural Zimbabweans use these phones for EcoCash mobile money. The scanner now correctly models their connectivity level without penalising them for lacking a smartphone.

When "Basic Phone (Chimbudzi)" is selected, the system automatically marks internet access as No and shows a yellow info box confirming USSD-only access.

### 6.4 Running the Assessment

Click **RUN RISK ASSESSMENT** to generate results.

### 6.5 Assessment Output

**FERI Score Card** — displays the composite score (0–100) with a colour-coded risk badge and a horizontal bar.

**ML Exclusion Probability** — the Gradient Boosting model's predicted probability that this individual is financially excluded.

**Sub-Score Breakdown** — three bar indicators showing:

- KYC Gap Score (45% weight in FERI)
- Demographic Vulnerability Score (35% weight)
- Institutional Barrier Score (20% weight)

**Priority Interventions** — personalised recommendations based on the individual's profile gaps, e.g.:

- Missing National ID → urgent document acquisition
- Chimbudzi phone → USSD banking activation
- Rural location > 20 km from branch → agent banking referral
- No phone at all → subsidised feature phone provision

---

## 7. Model Performance

### 7.1 Performance Comparison Matrix

A table comparing all three models across six metrics:

| Metric | Description |
|---|---|
| Accuracy | Overall correct prediction rate |
| ROC-AUC | Area under receiver operating characteristic curve |
| F1-Score | Harmonic mean of precision and recall |
| Precision | Positive predictive value |
| Recall | Sensitivity / true positive rate |
| Avg Precision | Area under precision-recall curve |

Values are colour-coded: green (≥ 0.80), amber (0.70–0.79), red (< 0.70).

### 7.2 ROC Curves

Line chart showing the trade-off between true positive rate and false positive rate for each model. Higher AUC = better discrimination.

### 7.3 Performance Radar

Polar/radar chart showing all five metrics simultaneously for a visual multi-dimensional comparison of the three models.

### 7.4 Confusion Matrices

Three heatmaps (one per model) showing counts of true positives, true negatives, false positives, and false negatives against the test set.

### 7.5 Feature Importance

A dropdown selects the model; a horizontal bar chart shows the top 15 most predictive features by importance percentage.

---

## 8. Data Explorer

### 8.1 Interactive Filter Panel

All filters apply in real time — no button required. The filter panel has two rows:

**Row 1 — Core Filters**

- Location (Urban / Rural)
- Gender (Male / Female)
- Employment (Formal / Informal / Unemployed)
- Exclusion Status (Included / Excluded)

**Row 2 — Expanded Filters**

- Province (all 10 Zimbabwe provinces, multiselect)
- FERI Risk Band (Low / Moderate / High / Critical)
- Age Range (slider)

**Advanced Filters (expandable)**

- Income Quintile range (1–5)
- FERI Score range (0–100, half-point steps)

If the filter combination returns no records, a warning is shown prompting the user to widen filters.

### 8.2 Filtered KPI Cards

After filtering, four metric cards update instantly:

- Records Shown (and % of total)
- Exclusion Rate for the filtered group
- Mean FERI Score for the filtered group
- Mean KYC Gap Score for the filtered group

### 8.3 Scatter and Histogram

**FERI Score vs Distance to Branch** — scatter plot (up to 1,500 sampled points) coloured by risk band.

**KYC Score Distribution by Status** — overlaid histogram comparing document score distributions for included vs excluded individuals.

### 8.4 Filtered Records Table

A styled data table showing up to 200 filtered records. The FERI Score column has a red-yellow-green colour gradient. The Exclusion Status column shows red/green indicators.

---

## 9. FERI Analytics

### 9.1 FERI Formula

```
FERI = 0.45 × KYC Gap Score + 0.35 × Demographic Vulnerability + 0.20 × Institutional Barrier
```

| Sub-Index | Weight | Key Drivers |
|---|---|---|
| KYC Gap Score | 45% | Missing National ID (40 pts), no Proof of Address (30 pts), no TIN (20 pts), no Employment Proof (10 pts) |
| Demographic Vulnerability | 35% | Rural (20 pts), unemployed (20 pts), income Q1 (15 pts), female (10 pts), no education (12 pts) |
| Institutional Barrier | 20% | Distance > 20 km (30 pts), no mobile phone (30 pts), no internet (20 pts), remote province (20 pts) |

**Risk Bands**

- **Low Risk**: FERI 0–25 (well-documented, urban, connected)
- **Moderate Risk**: FERI 25–45 (some documentation gaps)
- **High Risk**: FERI 45–65 (multiple barriers)
- **Critical Risk**: FERI 65–100 (severe exclusion, requires active intervention)

### 9.2 FERI Score Distribution

Histogram of all 5,000 FERI scores with vertical dashed lines at band thresholds (25, 45, 65). The colour gradient transitions from green (low risk) to red (critical risk).

### 9.3 Sub-Score Statistics

Cards showing mean, median, and standard deviation for each sub-index.

### 9.4 FERI by Demographic Group

Dual-axis bar + line chart showing mean FERI score (bars) and exclusion rate (line) for each of 12 demographic groups (e.g., Rural, Female, Unemployed, Income Q1, No Education). Groups are sorted from highest to lowest mean FERI.

### 9.5 Sub-Index Correlation Matrix

Pearson correlation heatmap showing how the three sub-indices relate to each other and to the final FERI score and exclusion status.

---

## 10. Policy Intelligence

Six evidence-based policy recommendations, each displayed as an expandable card with:

- **Impact rating** (HIGH / MEDIUM)
- **Summary** of the recommendation
- **Detail** explaining the mechanism and affected population
- **Evidence base** — a live statistic calculated from the dataset

| # | Policy | Impact |
|---|---|---|
| 1 | Tiered KYC Framework | HIGH |
| 2 | Digital Identity Infrastructure | HIGH |
| 3 | Alternative Proof of Address | HIGH |
| 4 | Mobile-First Onboarding | MEDIUM |
| 5 | Gender-Responsive Compliance | MEDIUM |
| 6 | FERI as Supervisory Metric | MEDIUM |

### 10.1 Policy Priority Matrix

A bubble chart plotting each policy by:

- **X-axis**: Implementation feasibility (%)
- **Y-axis**: Expected impact (%)
- **Bubble size**: Share of population affected (%)

Quadrant guidelines divide the chart into "Quick Wins" (high feasibility, high impact) and "Strategic" (lower feasibility, high impact).

---

## 11. Technical Architecture

### 11.1 Project Structure

```
group 2 project/
├── app.py                  Main Streamlit application
├── src/
│   ├── data_generator.py   Synthetic dataset generation (n=5,000)
│   ├── feri.py             FERI computation (three sub-indices)
│   ├── preprocessor.py     Feature encoding, scaling, train/test split, SMOTE
│   ├── models.py           Model training and evaluation
│   └── visualizations.py   Static chart exports
├── data/
│   └── kyc_with_feri.csv   Pre-computed dataset with FERI columns
├── outputs/
│   ├── figures/            PNG chart exports
│   └── model_comparison.csv
└── requirements.txt
```

### 11.2 Data Pipeline

1. **Data generation** — `data_generator.py` produces 5,000 synthetic individuals with demographics, KYC documents, and institutional factors calibrated to FinScope 2022 statistics
2. **FERI computation** — `feri.py` adds five columns: `kyc_gap_score`, `demographic_score`, `institutional_score`, `feri_score`, `feri_band`
3. **Preprocessing** — `preprocessor.py` one-hot encodes categoricals, scales numeric features, and applies SMOTE to balance the training set
4. **Model training** — `models.py` trains Logistic Regression, Random Forest, and Gradient Boosting classifiers

### 11.3 Caching

The application uses Streamlit's `@st.cache_data` and `@st.cache_resource` decorators to cache the dataset and trained models respectively. This means:

- The dataset is loaded once per session (not on every page navigation)
- Models are trained once per server restart (training is computationally expensive)

---

## 12. Known Limitations and Future Work

| Area | Current Limitation | Recommended Enhancement |
|---|---|---|
| Data | Synthetic dataset (calibrated but not real survey data) | Integrate live FinScope or RBZ data feeds |
| Authentication | Plain-text passwords in source code | Implement hashed passwords (bcrypt) or OAuth2 |
| Models | Trained on balanced synthetic data | Retrain on real administrative data when available |
| Connectivity | Binary internet flag | Add mobile data speed / coverage tier |
| Geography | Province-level only | District / ward-level mapping with choropleth |

---

## 13. Research Context

This platform was developed by Group 2 at Midlands State University as part of a research project investigating KYC-driven financial exclusion in Zimbabwe.

**Research Question:** To what extent do Know-Your-Customer (KYC) documentation requirements contribute to financial exclusion in Zimbabwe, and which demographic groups are most affected?

**Key Findings:**

- Overall exclusion rate of approximately 38% aligns with FinScope Zimbabwe 2022 benchmarks
- Proof-of-address absence is the single largest documentation barrier, particularly for rural women
- The Gradient Boosting model achieves the highest predictive accuracy (ROC-AUC > 0.85)
- Critical Risk individuals (FERI > 65) are concentrated among rural, unemployed, income-Q1 females with no proof of address
- Mobile phone access (including Chimbudzi feature phones) significantly reduces the institutional barrier component of FERI

**Policy Implication:** A tiered KYC framework accepting alternative proof of address (chiefs' letters, ward councillor attestations) combined with USSD-based mobile onboarding could bring 68% of currently excluded individuals into the formal financial system.

---

*Generated by Claude Code for the KYC Financial Exclusion AI Platform — Group 2, Midlands State University*
