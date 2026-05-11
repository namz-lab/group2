"""
KYC Financial Exclusion Study — Main Pipeline Runner
Midlands State University, Bachelor of Commerce Honours (Data Science and Informatics)
Group 2: Knowledge Keche (R162841Q), Lennie G. Dube (R247540M),
         Jonah T. Chigaba (R2410297J)
Supervisor: Bridget Munyoro

Run this script to reproduce the full analysis end-to-end.
Outputs are saved to outputs/ and data/.
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Ensure src/ is importable when running from project root
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # headless rendering for saved figures
import matplotlib.pyplot as plt

from src.data_generator import generate_kyc_financial_data, verify_statistics
from src.preprocessor import prepare_data
from src.models import (
    train_all_models, compare_models, evaluate_model, get_feature_importance,
)
from src.feri import compute_feri, feri_summary
from src.visualizations import (
    plot_exclusion_overview, plot_kyc_documentation, plot_roc_curves,
    plot_confusion_matrices, plot_feature_importance, plot_feri_distribution,
    plot_feri_by_demographics, plot_model_comparison_bar, plot_income_exclusion_gradient,
)

# ── Directories ──────────────────────────────────────────────────────────────
os.makedirs('data', exist_ok=True)
os.makedirs('outputs/figures', exist_ok=True)


def banner(text: str):
    print('\n' + '=' * 65)
    print(f'  {text}')
    print('=' * 65)


# ─────────────────────────────────────────────────────────────────────────────
# 1. DATA GENERATION
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 1 — Generating Synthetic Data (n=5 000)')

df = generate_kyc_financial_data(n=5000, seed=42)
df.to_csv('data/kyc_financial_exclusion_zimbabwe.csv', index=False)
print(f'Dataset saved: data/kyc_financial_exclusion_zimbabwe.csv')
print(f'Shape: {df.shape}')

print('\n--- Key Statistics vs FinScope Zimbabwe 2022 Targets ---')
stats_df = verify_statistics(df)
print(stats_df.to_string())


# ─────────────────────────────────────────────────────────────────────────────
# 2. EXPLORATORY DATA ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 2 — Exploratory Data Analysis')

print(f'\nClass distribution:')
vc = df['financially_excluded'].value_counts(normalize=True) * 100
print(f'  Included  (0): {vc[0]:.1f}%')
print(f'  Excluded  (1): {vc[1]:.1f}%')

print('\nMissing values:', df.isnull().sum().sum())
print('\nNumerical summary:')
print(df[['age', 'income_quintile', 'kyc_doc_score',
          'distance_to_branch_km', 'feri_score' if 'feri_score' in df.columns
          else 'kyc_doc_score']].describe().round(2))

plot_exclusion_overview(df, save_path='outputs/figures/fig1_exclusion_overview.png')
plot_kyc_documentation(df, save_path='outputs/figures/fig2_kyc_documentation.png')
plot_income_exclusion_gradient(df, save_path='outputs/figures/fig3_income_gradient.png')
print('EDA figures saved to outputs/figures/')


# ─────────────────────────────────────────────────────────────────────────────
# 3. DATA PREPROCESSING
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 3 — Data Preprocessing')

X_train, X_test, y_train, y_test, feature_names, encoders, scaler = prepare_data(
    df, test_size=0.20, balance=True, random_state=42
)
print(f'Training set: {X_train.shape[0]:,} samples (after SMOTE balancing)')
print(f'Test set    : {X_test.shape[0]:,} samples')
print(f'Features    : {len(feature_names)}')
print(f'Train class balance: {np.bincount(y_train)}')


# ─────────────────────────────────────────────────────────────────────────────
# 4. MODEL TRAINING
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 4 — Training Models')

models = train_all_models(X_train, y_train, random_state=42)
for name in models:
    print(f'  [OK] {name} trained')


# ─────────────────────────────────────────────────────────────────────────────
# 5. MODEL EVALUATION
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 5 — Model Evaluation')

comparison = compare_models(models, X_test, y_test)
print('\nPerformance Summary:')
print(comparison.to_string())

comparison.to_csv('outputs/model_comparison.csv')
print('\nComparison saved: outputs/model_comparison.csv')

# Detailed metrics per model
print('\nDetailed Metrics:')
for name, model in models.items():
    m = evaluate_model(model, X_test, y_test, name)
    print(f'\n  {name}:')
    print(f'    Accuracy : {m["accuracy"]:.4f}')
    print(f'    ROC-AUC  : {m["roc_auc"]:.4f}')
    print(f'    F1-Score : {m["f1_score"]:.4f}')
    print(f'    Precision: {m["precision"]:.4f}')
    print(f'    Recall   : {m["recall"]:.4f}')


# ─────────────────────────────────────────────────────────────────────────────
# 6. VISUALISE MODEL PERFORMANCE
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 6 — Visualising Model Performance')

plot_roc_curves(models, X_test, y_test,
                save_path='outputs/figures/fig4_roc_curves.png')
plot_confusion_matrices(models, X_test, y_test,
                        save_path='outputs/figures/fig5_confusion_matrices.png')
plot_model_comparison_bar(comparison,
                          save_path='outputs/figures/fig6_model_comparison.png')

# Feature importances
for short, name in [('lr', 'Logistic Regression'),
                    ('rf', 'Random Forest'),
                    ('gb', 'Gradient Boosting')]:
    model_type = {'lr': 'logistic_regression',
                  'rf': 'random_forest',
                  'gb': 'gradient_boosting'}[short]
    fi = get_feature_importance(models[name], feature_names, model_type)
    fi.to_csv(f'outputs/feature_importance_{short}.csv', index=False)
    plot_feature_importance(
        fi, model_name=name, top_n=15,
        save_path=f'outputs/figures/fig7_feature_importance_{short}.png'
    )

print('Model performance figures saved.')


# ─────────────────────────────────────────────────────────────────────────────
# 7. FINANCIAL EXCLUSION RISK INDEX (FERI)
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 7 — Computing Financial Exclusion Risk Index (FERI)')

df_feri = compute_feri(df)
df_feri.to_csv('data/kyc_with_feri.csv', index=False)

summary = feri_summary(df_feri)
print('\nFERI Summary by Demographic Group:')
print(summary.to_string(index=False))
summary.to_csv('outputs/feri_summary.csv', index=False)

print(f'\nFERI Statistics:')
print(f'  Mean  : {df_feri["feri_score"].mean():.2f}')
print(f'  Median: {df_feri["feri_score"].median():.2f}')
print(f'  Std   : {df_feri["feri_score"].std():.2f}')
print('\nFERI Risk Band Distribution:')
print(df_feri['feri_band'].value_counts().to_string())

plot_feri_distribution(df_feri,
                       save_path='outputs/figures/fig8_feri_distribution.png')
plot_feri_by_demographics(df_feri,
                          save_path='outputs/figures/fig9_feri_demographics.png')
print('FERI figures saved.')


# ─────────────────────────────────────────────────────────────────────────────
# 8. MOST AFFECTED GROUPS
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 8 — Most Affected Demographic Groups')

top5 = summary.head(5)
print('\nTop 5 Highest-Risk Groups (by Mean FERI):')
print(top5[['Group', 'Exclusion Rate (%)', 'Mean FERI', 'Mean KYC Gap Score']].to_string(
    index=False))


# ─────────────────────────────────────────────────────────────────────────────
# 9. POLICY RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
banner('STEP 9 — Evidence-Based Policy Recommendations')

recommendations = """
POLICY RECOMMENDATIONS — KYC-Driven Financial Exclusion in Zimbabwe
====================================================================

1. TIERED KYC FRAMEWORK
   Implement risk-proportionate onboarding aligned with FATF Rec. 10.
   - Tier 1 (Basic): Mobile money / low-value accounts — accept single
     government-issued ID (voter registration card, birth certificate)
     without proof-of-address requirement.
   - Tier 2 (Standard): Savings / credit access — national ID + one
     corroborating document (letter from village chief, employer letter).
   - Tier 3 (Full): Large transactions, foreign exchange — full CDD.

2. DIGITAL IDENTITY INFRASTRUCTURE
   Invest in a national digital ID system interoperable across financial
   institutions to eliminate duplicative paper-based verification and
   reduce compliance costs for low-income segments.

3. ALTERNATIVE PROOF OF ADDRESS
   Formally accept community vouching letters, ward councillor
   attestations, and mobile network location data as valid address proof
   for rural and informal sector customers.

4. MOBILE-FIRST ONBOARDING
   Mandate that all regulated institutions accept Eco-Cash / mobile wallet
   history as supplementary identity verification, reducing institutional
   distance barriers identified in the FERI analysis.

5. GENDER-RESPONSIVE COMPLIANCE GUIDANCE
   Issue RBZ circular acknowledging female-headed households face
   disproportionate address documentation barriers; standardise
   husband/guardian letter waiver for joint accounts.

6. REGULATORY CLARITY
   Publish binding RBZ compliance bulletins specifying the minimum
   acceptable documentation set, reducing institutional over-compliance
   driven by regulatory ambiguity.

7. MONITORING WITH FERI
   Adopt the Financial Exclusion Risk Index as a supervisory tool —
   financial institutions should report quarterly FERI-banded account
   opening rejection rates to the FIU as an inclusion metric.
"""

print(recommendations)

with open('outputs/policy_recommendations.txt', 'w') as f:
    f.write(recommendations)
print('Recommendations saved: outputs/policy_recommendations.txt')


# ─────────────────────────────────────────────────────────────────────────────
banner('PIPELINE COMPLETE')
print('\nAll outputs saved to:')
print('  data/                  — synthetic dataset with FERI scores')
print('  outputs/               — model comparison, FERI summary, policy recs')
print('  outputs/figures/       — all 9 figures (PNG, 150 dpi)')
print('\nNext: open KYC_Financial_Exclusion_Zimbabwe.ipynb for the full')
print('      interactive analysis with narrative and inline figures.')
