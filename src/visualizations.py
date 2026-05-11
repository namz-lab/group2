"""
Visualization module for KYC Financial Exclusion study.
All functions return (fig, ax) or fig for multi-panel plots.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from sklearn.metrics import roc_curve, confusion_matrix, ConfusionMatrixDisplay

# Consistent colour palette
PALETTE = {
    'excluded': '#D62728',
    'included': '#2CA02C',
    'urban': '#1F77B4',
    'rural': '#FF7F0E',
    'male': '#17BECF',
    'female': '#E377C2',
    'lr': '#1F77B4',
    'rf': '#FF7F0E',
    'gb': '#2CA02C',
}
FERI_COLORS = ['#2CA02C', '#FFDD57', '#FF7F0E', '#D62728']

sns.set_theme(style='whitegrid', palette='muted', font_scale=1.1)


def plot_exclusion_overview(df: pd.DataFrame, save_path: str = None):
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle('Financial Exclusion by Key Demographics (FinScope-Calibrated Synthetic Data)',
                 fontsize=13, fontweight='bold', y=1.02)

    groups = [
        ('location', 'Location', ['Urban', 'Rural']),
        ('gender', 'Gender', ['Male', 'Female']),
        ('employment_sector', 'Employment', ['Formal', 'Informal', 'Unemployed']),
    ]
    colors = [PALETTE['included'], PALETTE['excluded']]

    for ax, (col, title, cats) in zip(axes, groups):
        rates = df.groupby(col)['financially_excluded'].mean().reindex(cats) * 100
        bars = ax.bar(rates.index, rates.values,
                      color=[PALETTE['excluded'] if r > 40 else PALETTE['urban'] for r in rates.values],
                      edgecolor='white', linewidth=0.8)
        ax.axhline(df['financially_excluded'].mean() * 100, color='grey',
                   linestyle='--', linewidth=1.2, label='Overall avg')
        for bar, val in zip(bars, rates.values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
        ax.set_title(title, fontweight='bold')
        ax.set_ylabel('Exclusion Rate (%)')
        ax.set_ylim(0, 85)
        ax.legend(fontsize=9)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_kyc_documentation(df: pd.DataFrame, save_path: str = None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Doc possession rates by urban/rural
    docs = ['has_national_id', 'has_proof_of_address', 'has_tin', 'has_employment_proof']
    labels = ['National ID', 'Proof of Address', 'TIN', 'Employment Proof']

    urban = df[df['location'] == 'Urban'][docs].mean() * 100
    rural = df[df['location'] == 'Rural'][docs].mean() * 100

    x = np.arange(len(labels))
    w = 0.35
    ax = axes[0]
    ax.bar(x - w / 2, urban.values, w, label='Urban', color=PALETTE['urban'], alpha=0.85)
    ax.bar(x + w / 2, rural.values, w, label='Rural', color=PALETTE['rural'], alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha='right')
    ax.set_ylabel('Population with Document (%)')
    ax.set_title('KYC Document Possession by Location', fontweight='bold')
    ax.legend()
    ax.set_ylim(0, 110)

    # Exclusion rate by KYC doc score
    excl_by_score = df.groupby('kyc_doc_score')['financially_excluded'].mean() * 100
    ax2 = axes[1]
    bars = ax2.bar(excl_by_score.index, excl_by_score.values,
                   color=sns.color_palette('RdYlGn_r', len(excl_by_score)),
                   edgecolor='white')
    for bar, val in zip(bars, excl_by_score.values):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 f'{val:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax2.set_xlabel('KYC Documentation Score (0=none, 4=all docs)')
    ax2.set_ylabel('Financial Exclusion Rate (%)')
    ax2.set_title('Exclusion Rate by KYC Documentation Score', fontweight='bold')
    ax2.set_xticks([0, 1, 2, 3, 4])

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_roc_curves(models: dict, X_test, y_test, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 6))
    model_colors = {'Logistic Regression': PALETTE['lr'],
                    'Random Forest': PALETTE['rf'],
                    'Gradient Boosting': PALETTE['gb']}

    for name, model in models.items():
        if hasattr(model, 'predict_proba'):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = model.decision_function(X_test)
        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(y_test, y_prob)
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        ax.plot(fpr, tpr, label=f'{name} (AUC = {auc:.3f})',
                color=model_colors.get(name, 'steelblue'), linewidth=2)

    ax.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random classifier')
    ax.set_xlabel('False Positive Rate', fontsize=12)
    ax.set_ylabel('True Positive Rate', fontsize=12)
    ax.set_title('ROC Curves — Model Comparison', fontweight='bold', fontsize=13)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_confusion_matrices(models: dict, X_test, y_test, save_path: str = None):
    n = len(models)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4))
    if n == 1:
        axes = [axes]
    for ax, (name, model) in zip(axes, models.items()):
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        disp = ConfusionMatrixDisplay(cm, display_labels=['Included', 'Excluded'])
        disp.plot(ax=ax, colorbar=False, cmap='Blues')
        ax.set_title(name, fontweight='bold', fontsize=11)
    fig.suptitle('Confusion Matrices', fontsize=13, fontweight='bold')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_feature_importance(importance_df: pd.DataFrame, model_name: str,
                            top_n: int = 15, save_path: str = None):
    top = importance_df.head(top_n)
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(top['feature'][::-1], top['importance_pct'][::-1],
                   color=sns.color_palette('Blues_d', top_n))
    ax.set_xlabel('Relative Importance (%)', fontsize=11)
    ax.set_title(f'Top {top_n} Feature Importances — {model_name}',
                 fontweight='bold', fontsize=12)
    ax.grid(axis='x', alpha=0.4)
    for bar, val in zip(bars, top['importance_pct'][::-1]):
        ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}%', va='center', fontsize=9)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_feri_distribution(df_feri: pd.DataFrame, save_path: str = None):
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    ax = axes[0]
    ax.hist(df_feri['feri_score'], bins=40, color='steelblue', edgecolor='white', alpha=0.85)
    ax.axvline(df_feri['feri_score'].mean(), color='red', linestyle='--',
               linewidth=1.5, label=f'Mean = {df_feri["feri_score"].mean():.1f}')
    ax.set_xlabel('FERI Score', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title('Distribution of FERI Scores', fontweight='bold', fontsize=12)
    ax.legend()

    ax2 = axes[1]
    band_counts = df_feri['feri_band'].value_counts().reindex(
        ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'])
    wedges, texts, autotexts = ax2.pie(
        band_counts, labels=band_counts.index,
        colors=FERI_COLORS, autopct='%1.1f%%', startangle=140,
        textprops={'fontsize': 10},
    )
    ax2.set_title('Population by FERI Risk Band', fontweight='bold', fontsize=12)

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_feri_by_demographics(df_feri: pd.DataFrame, save_path: str = None):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    plot_configs = [
        ('location', 'FERI by Location'),
        ('gender', 'FERI by Gender'),
        ('employment_sector', 'FERI by Employment Sector'),
        ('education_level', 'FERI by Education Level'),
    ]

    for ax, (col, title) in zip(axes.flat, plot_configs):
        order = df_feri.groupby(col)['feri_score'].median().sort_values(ascending=False).index
        sns.boxplot(data=df_feri, x=col, y='feri_score', order=order,
                    palette='RdYlGn_r', ax=ax)
        ax.set_title(title, fontweight='bold', fontsize=11)
        ax.set_xlabel('')
        ax.set_ylabel('FERI Score')
        ax.tick_params(axis='x', rotation=15)

    plt.suptitle('FERI Score Distribution by Demographic Groups', fontsize=13,
                 fontweight='bold', y=1.01)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_model_comparison_bar(comparison_df: pd.DataFrame, save_path: str = None):
    metrics = ['Accuracy', 'ROC-AUC', 'F1-Score', 'Precision', 'Recall']
    df_plot = comparison_df[metrics].reset_index()
    df_melt = df_plot.melt(id_vars='Model', var_name='Metric', value_name='Score')

    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(data=df_melt, x='Metric', y='Score', hue='Model',
                palette=[PALETTE['lr'], PALETTE['rf'], PALETTE['gb']], ax=ax)
    ax.set_ylim(0, 1.05)
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=13)
    ax.legend(loc='lower right', fontsize=10)
    ax.axhline(0.5, color='grey', linestyle=':', linewidth=1)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.3f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=8, rotation=45)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig


def plot_income_exclusion_gradient(df: pd.DataFrame, save_path: str = None):
    fig, ax = plt.subplots(figsize=(8, 5))
    data = df.groupby(['income_quintile', 'location'])['financially_excluded'].mean() * 100
    data = data.reset_index()
    data.columns = ['income_quintile', 'location', 'exclusion_rate']

    for loc, grp in data.groupby('location'):
        color = PALETTE['urban'] if loc == 'Urban' else PALETTE['rural']
        ax.plot(grp['income_quintile'], grp['exclusion_rate'], marker='o',
                label=loc, color=color, linewidth=2)

    ax.set_xlabel('Income Quintile (1=Lowest, 5=Highest)', fontsize=11)
    ax.set_ylabel('Financial Exclusion Rate (%)', fontsize=11)
    ax.set_title('Exclusion Rate by Income Quintile and Location', fontweight='bold', fontsize=12)
    ax.legend(fontsize=10)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.grid(True, alpha=0.4)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    return fig
