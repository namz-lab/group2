"""
Synthetic data generator for KYC Financial Exclusion study.
Generates data calibrated to FinScope Zimbabwe Survey 2022 statistics:
  - Overall financial exclusion: ~38%
  - Rural exclusion: ~53%, Urban: ~21%
  - Female exclusion: ~43%, Male: ~33%
  - Informal sector exclusion: ~56%, Formal: ~19%
"""

import numpy as np
import pandas as pd
from scipy.special import expit


def generate_kyc_financial_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    # --- Demographics ---
    location = rng.choice(['Urban', 'Rural'], n, p=[0.55, 0.45])
    is_rural = (location == 'Rural').astype(int)
    is_urban = 1 - is_rural

    gender = rng.choice(['Male', 'Female'], n, p=[0.49, 0.51])
    is_female = (gender == 'Female').astype(int)

    age = np.clip(rng.normal(38, 14, n), 18, 80).astype(int)

    provinces = [
        'Harare', 'Bulawayo', 'Manicaland', 'Mashonaland Central',
        'Mashonaland East', 'Mashonaland West', 'Masvingo',
        'Matabeleland North', 'Matabeleland South', 'Midlands'
    ]
    urban_p = [0.45, 0.25, 0.04, 0.04, 0.04, 0.04, 0.04, 0.03, 0.03, 0.04]
    rural_p = [0.02, 0.01, 0.12, 0.12, 0.12, 0.12, 0.13, 0.10, 0.10, 0.16]
    province = np.array([
        rng.choice(provinces, p=urban_p if location[i] == 'Urban' else rural_p)
        for i in range(n)
    ])

    edu_levels = ['None', 'Primary', 'Secondary', 'Tertiary']
    edu_urban_p = [0.03, 0.12, 0.55, 0.30]
    edu_rural_p = [0.12, 0.28, 0.50, 0.10]
    education = np.array([
        rng.choice(edu_levels, p=edu_urban_p if location[i] == 'Urban' else edu_rural_p)
        for i in range(n)
    ])
    edu_map = {'None': 0, 'Primary': 1, 'Secondary': 2, 'Tertiary': 3}
    edu_score = np.array([edu_map[e] for e in education])

    emp_sectors = ['Formal', 'Informal', 'Unemployed']

    def _emp_p(loc, edu):
        if loc == 'Urban' and edu in ['Secondary', 'Tertiary']:
            return [0.42, 0.42, 0.16]
        elif loc == 'Urban':
            return [0.22, 0.58, 0.20]
        elif edu == 'Tertiary':
            return [0.28, 0.47, 0.25]
        else:
            return [0.10, 0.65, 0.25]

    employment = np.array([
        rng.choice(emp_sectors, p=_emp_p(location[i], education[i]))
        for i in range(n)
    ])
    is_formal = (employment == 'Formal').astype(int)
    is_informal = (employment == 'Informal').astype(int)
    is_unemployed = (employment == 'Unemployed').astype(int)

    income_score = (
        is_urban * 1.2 + is_formal * 2.0 + is_informal * 0.4
        + edu_score * 0.4 + rng.normal(0, 0.8, n)
    )
    income_quintile = (pd.qcut(income_score, 5, labels=False) + 1).astype(int)

    # --- KYC Documentation ---
    p_nid = expit(
        1.2 + 0.7 * is_urban + 0.4 * is_formal + 0.3 * edu_score / 3
        - 0.4 * (age < 22).astype(float) - 0.2 * is_female
        + rng.normal(0, 0.3, n)
    )
    has_national_id = (rng.uniform(0, 1, n) < p_nid).astype(int)

    p_poa = expit(
        0.2 + 1.4 * is_urban + 0.9 * is_formal
        + 0.3 * (income_quintile >= 3).astype(float)
        + 0.2 * edu_score / 3 + rng.normal(0, 0.3, n)
    )
    has_proof_of_address = (rng.uniform(0, 1, n) < p_poa).astype(int)

    p_tin = expit(
        -1.5 + 2.8 * is_formal + 0.3 * is_urban
        + 0.2 * (income_quintile >= 4).astype(float)
        + rng.normal(0, 0.3, n)
    )
    has_tin = (rng.uniform(0, 1, n) < p_tin).astype(int)

    p_ep = expit(
        -0.8 + 3.0 * is_formal + 0.9 * is_informal + 0.4 * is_urban
        + rng.normal(0, 0.3, n)
    )
    has_employment_proof = (rng.uniform(0, 1, n) < p_ep).astype(int)
    has_employment_proof[employment == 'Unemployed'] = 0

    kyc_doc_score = (
        has_national_id + has_proof_of_address + has_tin + has_employment_proof
    )

    # --- Institutional Factors ---
    dist_urban = rng.exponential(3, n).clip(0.1, 20)
    dist_rural = rng.exponential(22, n).clip(1, 150)
    distance_km = np.where(is_rural == 1, dist_rural, dist_urban).round(1)

    p_mobile = expit(
        0.3 + 0.9 * is_urban + 0.5 * is_formal
        + 0.3 * (income_quintile >= 3).astype(float)
        + 0.2 * edu_score / 3 + rng.normal(0, 0.3, n)
    )
    has_mobile_phone = (rng.uniform(0, 1, n) < p_mobile).astype(int)

    p_internet = expit(
        -0.8 + 1.6 * is_urban + 0.8 * is_formal
        + 0.5 * (income_quintile >= 4).astype(float)
        + 0.4 * (edu_score >= 2).astype(float) + rng.normal(0, 0.3, n)
    )
    has_internet = (rng.uniform(0, 1, n) < p_internet).astype(int)

    # --- Financial Exclusion Target (calibrated logistic DGP) ---
    exclusion_logit = (
        -1.3
        + 1.8 * (1 - has_national_id)
        + 1.2 * (1 - has_proof_of_address)
        + 0.7 * is_rural
        + 0.3 * is_female
        + 0.7 * is_unemployed
        + 0.5 * is_informal
        - 0.25 * (income_quintile - 1)
        - 0.35 * edu_score / 3
        + 0.15 * np.log1p(distance_km) * is_rural
        - 0.5 * has_mobile_phone
        + rng.normal(0, 0.5, n)
    )
    p_excluded = expit(exclusion_logit)
    financially_excluded = (rng.uniform(0, 1, n) < p_excluded).astype(int)

    kyc_barrier_level = pd.cut(
        kyc_doc_score, bins=[-1, 1, 2, 4], labels=['High', 'Medium', 'Low']
    ).astype(str)

    df = pd.DataFrame({
        'age': age,
        'gender': gender,
        'location': location,
        'province': province,
        'education_level': education,
        'employment_sector': employment,
        'income_quintile': income_quintile,
        'has_national_id': has_national_id,
        'has_proof_of_address': has_proof_of_address,
        'has_tin': has_tin,
        'has_employment_proof': has_employment_proof,
        'kyc_doc_score': kyc_doc_score,
        'kyc_barrier_level': kyc_barrier_level,
        'distance_to_branch_km': distance_km,
        'has_mobile_phone': has_mobile_phone,
        'has_internet': has_internet,
        'financially_excluded': financially_excluded,
    })
    return df


def verify_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Print key statistics and compare to FinScope 2022 targets."""
    stats = {}
    exc = df['financially_excluded']
    stats['Overall exclusion'] = exc.mean()
    stats['Urban exclusion'] = exc[df['location'] == 'Urban'].mean()
    stats['Rural exclusion'] = exc[df['location'] == 'Rural'].mean()
    stats['Male exclusion'] = exc[df['gender'] == 'Male'].mean()
    stats['Female exclusion'] = exc[df['gender'] == 'Female'].mean()
    stats['Formal exclusion'] = exc[df['employment_sector'] == 'Formal'].mean()
    stats['Informal exclusion'] = exc[df['employment_sector'] == 'Informal'].mean()
    stats['Unemployed exclusion'] = exc[df['employment_sector'] == 'Unemployed'].mean()

    targets = {
        'Overall exclusion': 0.38,
        'Urban exclusion': 0.21,
        'Rural exclusion': 0.53,
        'Male exclusion': 0.33,
        'Female exclusion': 0.43,
        'Formal exclusion': 0.19,
        'Informal exclusion': 0.56,
        'Unemployed exclusion': 0.70,
    }

    result = pd.DataFrame({
        'Generated': stats,
        'FinScope Target': targets,
    }).round(3)
    result['Difference'] = (result['Generated'] - result['FinScope Target']).round(3)
    return result
