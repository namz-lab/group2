"""
Model training and evaluation for KYC Financial Exclusion study.
Implements Logistic Regression, Random Forest, and Gradient Boosting classifiers.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, f1_score, precision_score, recall_score,
    confusion_matrix, classification_report, roc_curve, average_precision_score,
)
from sklearn.model_selection import cross_val_score, StratifiedKFold
import xgboost as xgb
import warnings
warnings.filterwarnings('ignore')


def train_logistic_regression(X_train, y_train, random_state=42):
    model = LogisticRegression(
        max_iter=1000, random_state=random_state,
        class_weight='balanced', solver='lbfgs', C=1.0,
    )
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train, random_state=42):
    model = RandomForestClassifier(
        n_estimators=50, max_depth=6, min_samples_leaf=10,
        class_weight='balanced', random_state=random_state, n_jobs=-1,
    )
    model.fit(X_train, y_train)
    return model


def train_gradient_boosting(X_train, y_train, random_state=42):
    model = xgb.XGBClassifier(
        n_estimators=50, max_depth=4, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        scale_pos_weight=1, eval_metric='logloss',
        random_state=random_state,
    )
    model.fit(X_train, y_train, verbose=False)
    return model


def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """Return a metrics dictionary for the given model on test data."""
    y_pred = model.predict(X_test)
    if hasattr(model, 'predict_proba'):
        y_prob = model.predict_proba(X_test)[:, 1]
    else:
        y_prob = model.decision_function(X_test)
        y_prob = (y_prob - y_prob.min()) / (y_prob.max() - y_prob.min())

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    return {
        'model': model_name,
        'accuracy': round(accuracy_score(y_test, y_pred), 4),
        'roc_auc': round(roc_auc_score(y_test, y_prob), 4),
        'f1_score': round(f1_score(y_test, y_pred), 4),
        'precision': round(precision_score(y_test, y_pred), 4),
        'recall': round(recall_score(y_test, y_pred), 4),
        'avg_precision': round(average_precision_score(y_test, y_prob), 4),
        'confusion_matrix': confusion_matrix(y_test, y_pred),
        'fpr': fpr,
        'tpr': tpr,
        'y_prob': y_prob,
        'y_pred': y_pred,
    }


def cross_validate_model(model, X, y, cv=5, scoring='roc_auc') -> dict:
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=skf, scoring=scoring)
    return {
        'mean': round(scores.mean(), 4),
        'std': round(scores.std(), 4),
        'scores': scores,
    }


def get_feature_importance(model, feature_names: list, model_type: str) -> pd.DataFrame:
    if model_type == 'logistic_regression':
        importance = np.abs(model.coef_[0])
    elif model_type in ('random_forest', 'gradient_boosting'):
        importance = model.feature_importances_
    else:
        importance = np.ones(len(feature_names))

    df = pd.DataFrame({'feature': feature_names, 'importance': importance})
    df = df.sort_values('importance', ascending=False).reset_index(drop=True)
    df['importance_pct'] = (df['importance'] / df['importance'].sum() * 100).round(2)
    return df


def train_all_models(X_train, y_train, random_state=42):
    models = {
        'Logistic Regression': train_logistic_regression(X_train, y_train, random_state),
        'Random Forest': train_random_forest(X_train, y_train, random_state),
        'Gradient Boosting': train_gradient_boosting(X_train, y_train, random_state),
    }
    return models


def compare_models(models: dict, X_test, y_test) -> pd.DataFrame:
    rows = []
    for name, model in models.items():
        m = evaluate_model(model, X_test, y_test, name)
        rows.append({
            'Model': name,
            'Accuracy': m['accuracy'],
            'ROC-AUC': m['roc_auc'],
            'F1-Score': m['f1_score'],
            'Precision': m['precision'],
            'Recall': m['recall'],
            'Avg Precision': m['avg_precision'],
        })
    return pd.DataFrame(rows).set_index('Model')
