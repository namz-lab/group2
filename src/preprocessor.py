"""
Data preprocessing pipeline for KYC Financial Exclusion study.
Handles encoding, scaling, class imbalance, and train/test splitting.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE


CATEGORICAL_FEATURES = [
    'gender', 'location', 'province', 'education_level',
    'employment_sector', 'kyc_barrier_level',
]

NUMERIC_FEATURES = [
    'age', 'income_quintile', 'kyc_doc_score',
    'distance_to_branch_km',
]

BINARY_FEATURES = [
    'has_national_id', 'has_proof_of_address', 'has_tin',
    'has_employment_proof', 'has_mobile_phone', 'has_internet',
]

TARGET = 'financially_excluded'


def encode_and_scale(df: pd.DataFrame, fit_encoders: dict = None, fit_scaler=None):
    """
    One-hot encode categoricals, keep binaries, scale numerics.
    Returns (X_processed, feature_names, encoders_dict, scaler).
    Pass fit_encoders/fit_scaler when transforming test data.
    """
    df = df.copy()

    # One-hot encode categoricals
    if fit_encoders is None:
        df_encoded = pd.get_dummies(df[CATEGORICAL_FEATURES], drop_first=True)
        encoders = {'columns': list(df_encoded.columns)}
    else:
        df_encoded = pd.get_dummies(df[CATEGORICAL_FEATURES], drop_first=True)
        # Align to training columns
        for col in fit_encoders['columns']:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[fit_encoders['columns']]
        encoders = fit_encoders

    # Numeric features
    num_data = df[NUMERIC_FEATURES].copy()
    if fit_scaler is None:
        scaler = StandardScaler()
        num_scaled = pd.DataFrame(
            scaler.fit_transform(num_data),
            columns=NUMERIC_FEATURES,
            index=df.index,
        )
    else:
        scaler = fit_scaler
        num_scaled = pd.DataFrame(
            scaler.transform(num_data),
            columns=NUMERIC_FEATURES,
            index=df.index,
        )

    # Binary features (no scaling needed)
    bin_data = df[BINARY_FEATURES].copy().reset_index(drop=True)
    num_scaled = num_scaled.reset_index(drop=True)
    df_encoded = df_encoded.reset_index(drop=True)

    X = pd.concat([num_scaled, bin_data, df_encoded], axis=1)
    return X, list(X.columns), encoders, scaler


def prepare_data(df: pd.DataFrame, test_size: float = 0.2, balance: bool = True,
                 random_state: int = 42):
    """
    Full preprocessing pipeline: encode -> split -> optionally SMOTE-balance.
    Returns (X_train, X_test, y_train, y_test, feature_names, encoders, scaler).
    """
    y = df[TARGET].values

    X_full, feature_names, encoders, scaler = encode_and_scale(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X_full, y, test_size=test_size, random_state=random_state, stratify=y
    )

    if balance:
        smote = SMOTE(random_state=random_state)
        X_train_arr, y_train_arr = smote.fit_resample(X_train.values, y_train)
        X_train = pd.DataFrame(X_train_arr, columns=feature_names)
        y_train = y_train_arr

    return X_train, X_test, y_train, y_test, feature_names, encoders, scaler
