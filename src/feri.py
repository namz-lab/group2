"""
Financial Exclusion Risk Index (FERI) construction.

FERI is a composite 0-100 index that quantifies an individual's risk of
financial exclusion driven by KYC barriers.  Three sub-indices are combined:

  KYC Documentation Gap Score  (weight 0.45)
    Reflects missing documentation weighted by regulatory importance.
    National ID: 40 pts, Proof of Address: 30 pts, TIN: 20 pts,
    Employment Proof: 10 pts.

  Demographic Vulnerability Score  (weight 0.35)
    Rural location: 20 pts, Unemployment: 20 pts, Informal employment: 12 pts,
    Income quintile 1: 15 pts / Q2: 8 pts, Female: 10 pts,
    No formal education: 12 pts / Primary only: 6 pts,
    Age < 25 or > 64: 8 pts.

  Institutional Barrier Score  (weight 0.20)
    Distance > 20 km: 30 pts / 10-20 km: 15 pts / 5-10 km: 5 pts,
    No mobile phone: 30 pts, No internet: 20 pts,
    Remote province bonus: 20 pts.
"""

import numpy as np
import pandas as pd


REMOTE_PROVINCES = {
    'Matabeleland North', 'Matabeleland South',
    'Mashonaland Central', 'Masvingo',
}


def kyc_doc_gap_score(df: pd.DataFrame) -> pd.Series:
    score = (
        (1 - df['has_national_id']) * 40
        + (1 - df['has_proof_of_address']) * 30
        + (1 - df['has_tin']) * 20
        + (1 - df['has_employment_proof']) * 10
    )
    return score.clip(0, 100)


def demographic_vulnerability_score(df: pd.DataFrame) -> pd.Series:
    score = pd.Series(0.0, index=df.index)

    score += (df['location'] == 'Rural').astype(int) * 20
    score += (df['employment_sector'] == 'Unemployed').astype(int) * 20
    score += (df['employment_sector'] == 'Informal').astype(int) * 12
    score += (df['income_quintile'] == 1).astype(int) * 15
    score += (df['income_quintile'] == 2).astype(int) * 8
    score += (df['gender'] == 'Female').astype(int) * 10
    score += (df['education_level'] == 'None').astype(int) * 12
    score += (df['education_level'] == 'Primary').astype(int) * 6
    score += ((df['age'] < 25) | (df['age'] > 64)).astype(int) * 8

    return score.clip(0, 100)


def institutional_barrier_score(df: pd.DataFrame) -> pd.Series:
    score = pd.Series(0.0, index=df.index)

    score += (df['distance_to_branch_km'] > 20).astype(int) * 30
    score += ((df['distance_to_branch_km'] > 10) & (df['distance_to_branch_km'] <= 20)).astype(int) * 15
    score += ((df['distance_to_branch_km'] > 5) & (df['distance_to_branch_km'] <= 10)).astype(int) * 5

    score += (1 - df['has_mobile_phone']) * 30
    score += (1 - df['has_internet']) * 20

    score += df['province'].isin(REMOTE_PROVINCES).astype(int) * 20

    return score.clip(0, 100)


def compute_feri(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add FERI columns to a copy of df.
    Returns df with: kyc_gap_score, demographic_score, institutional_score, feri_score, feri_band.
    """
    out = df.copy()
    out['kyc_gap_score'] = kyc_doc_gap_score(df)
    out['demographic_score'] = demographic_vulnerability_score(df)
    out['institutional_score'] = institutional_barrier_score(df)

    out['feri_score'] = (
        0.45 * out['kyc_gap_score']
        + 0.35 * out['demographic_score']
        + 0.20 * out['institutional_score']
    ).round(2)

    out['feri_band'] = pd.cut(
        out['feri_score'],
        bins=[-1, 25, 45, 65, 101],
        labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
    ).astype(str)
    return out


def feri_summary(df_feri: pd.DataFrame) -> pd.DataFrame:
    """Exclusion rate and mean FERI by demographic group."""
    rows = []

    def add(label, mask):
        sub = df_feri[mask]
        rows.append({
            'Group': label,
            'N': len(sub),
            'Exclusion Rate (%)': round(sub['financially_excluded'].mean() * 100, 1),
            'Mean FERI': round(sub['feri_score'].mean(), 1),
            'Mean KYC Gap Score': round(sub['kyc_gap_score'].mean(), 1),
        })

    add('Overall', pd.Series(True, index=df_feri.index))
    add('Urban', df_feri['location'] == 'Urban')
    add('Rural', df_feri['location'] == 'Rural')
    add('Male', df_feri['gender'] == 'Male')
    add('Female', df_feri['gender'] == 'Female')
    add('Formal Employment', df_feri['employment_sector'] == 'Formal')
    add('Informal Employment', df_feri['employment_sector'] == 'Informal')
    add('Unemployed', df_feri['employment_sector'] == 'Unemployed')
    add('Income Q1 (Lowest)', df_feri['income_quintile'] == 1)
    add('Income Q5 (Highest)', df_feri['income_quintile'] == 5)
    add('No Education', df_feri['education_level'] == 'None')
    add('Tertiary Education', df_feri['education_level'] == 'Tertiary')
    add('Age 18-25', df_feri['age'].between(18, 25))
    add('Age 26-45', df_feri['age'].between(26, 45))
    add('Age 46-64', df_feri['age'].between(46, 64))
    add('Age 65+', df_feri['age'] >= 65)

    return pd.DataFrame(rows).sort_values('Mean FERI', ascending=False).reset_index(drop=True)
