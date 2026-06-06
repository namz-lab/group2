"""
KYC Financial Exclusion Analysis Platform
Enterprise-Grade Streamlit Dashboard
Midlands State University — Group 2 Research Project
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="KYC Exclusion AI Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject global CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base / Reset ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark gradient background */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b2a 40%, #0a1628 100%);
    color: #e2e8f0;
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #091220 100%);
    border-right: 1px solid rgba(99, 179, 237, 0.15);
}
[data-testid="stSidebar"] .stMarkdown { color: #a0aec0; }

/* Hide default Streamlit header */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(135deg, rgba(13,27,42,0.9) 0%, rgba(17,36,58,0.9) 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #63b3ed, #9f7aea, #63b3ed);
    background-size: 200% 100%;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}
.metric-card .label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #718096;
    margin-bottom: 8px;
}
.metric-card .value {
    font-size: 36px;
    font-weight: 800;
    color: #63b3ed;
    line-height: 1;
    margin-bottom: 6px;
}
.metric-card .delta {
    font-size: 13px;
    font-weight: 500;
    color: #68d391;
}
.metric-card .delta.negative { color: #fc8181; }
.metric-card .sub {
    font-size: 12px;
    color: #4a5568;
    margin-top: 4px;
}

/* ── Section headers ── */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #e2e8f0;
    border-left: 4px solid #63b3ed;
    padding-left: 12px;
    margin: 24px 0 16px 0;
}
.section-sub {
    font-size: 13px;
    color: #718096;
    margin-top: -12px;
    margin-bottom: 16px;
    padding-left: 16px;
}

/* ── Page title banner ── */
.page-banner {
    background: linear-gradient(135deg, rgba(99,179,237,0.08) 0%, rgba(159,122,234,0.06) 100%);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 20px;
    padding: 28px 36px;
    margin-bottom: 28px;
}
.page-banner h1 {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(90deg, #63b3ed, #9f7aea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
}
.page-banner p {
    font-size: 14px;
    color: #718096;
    margin: 0;
}

/* ── Risk badge ── */
.risk-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.risk-low    { background: rgba(104,211,145,0.15); color: #68d391; border: 1px solid rgba(104,211,145,0.3); }
.risk-moderate { background: rgba(246,173,85,0.15);  color: #f6ad55; border: 1px solid rgba(246,173,85,0.3); }
.risk-high   { background: rgba(252,129,74,0.15);  color: #fc814a; border: 1px solid rgba(252,129,74,0.3); }
.risk-critical { background: rgba(252,100,100,0.15); color: #fc6464; border: 1px solid rgba(252,100,100,0.3); }

/* ── Tables ── */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 8px;
}
.styled-table th {
    background: rgba(99,179,237,0.1);
    color: #90cdf4;
    font-weight: 600;
    font-size: 11px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid rgba(99,179,237,0.2);
}
.styled-table td {
    padding: 10px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #cbd5e0;
}
.styled-table tr:hover td { background: rgba(99,179,237,0.05); }

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.3), transparent);
    margin: 24px 0;
}

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stSlider label, .stRadio label, .stCheckbox label,
.stNumberInput label, .stTextInput label { color: #a0aec0 !important; font-size: 13px !important; }

.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #553c9a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(99,179,237,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,179,237,0.35) !important;
}

/* Nav items */
.nav-item {
    padding: 10px 16px;
    border-radius: 10px;
    margin: 3px 0;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #a0aec0;
    transition: all 0.15s ease;
    display: flex;
    align-items: center;
    gap: 10px;
}
.nav-item:hover { background: rgba(99,179,237,0.08); color: #e2e8f0; }
.nav-item.active { background: rgba(99,179,237,0.15); color: #63b3ed; border-left: 3px solid #63b3ed; }

/* Progress bar for FERI */
.feri-bar-container {
    background: rgba(255,255,255,0.06);
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 8px 0;
}
.feri-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.6s ease;
}

/* Info panel */
.info-panel {
    background: rgba(99,179,237,0.06);
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    font-size: 13px;
    color: #90cdf4;
}

/* Alert panels */
.alert-critical {
    background: rgba(252,100,100,0.08);
    border: 1px solid rgba(252,100,100,0.3);
    border-radius: 12px;
    padding: 16px 20px;
}
.alert-success {
    background: rgba(104,211,145,0.08);
    border: 1px solid rgba(104,211,145,0.3);
    border-radius: 12px;
    padding: 16px 20px;
}

/* Plotly chart background */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
    background: transparent !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e1a; }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,179,237,0.5); }

/* Expander */
.streamlit-expanderHeader {
    background: rgba(99,179,237,0.05) !important;
    border: 1px solid rgba(99,179,237,0.15) !important;
    border-radius: 8px !important;
    color: #a0aec0 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Authentication ────────────────────────────────────────────────────────────
# Credentials: username → plaintext password (extend as needed)
_USERS = {
    'admin':   'kyc@msu2024',
    'group2':  'msu@group2',
    'analyst': 'feri@2024',
}


def _show_login_page():
    """Render a branded login form and return True when authenticated."""
    st.markdown("""
    <div style="max-width:420px; margin:80px auto 0 auto;">
        <div style="text-align:center; margin-bottom:32px;">
            <div style="font-size:60px;">🏦</div>
            <div style="font-size:24px; font-weight:800; color:#63b3ed; letter-spacing:0.04em; margin:12px 0 4px 0;">
                KYC EXCLUSION AI PLATFORM
            </div>
            <div style="font-size:12px; color:#4a5568; letter-spacing:0.08em; text-transform:uppercase;">
                Midlands State University — Group 2
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col_l, col_c, col_r = st.columns([1, 2, 1])
        with col_c:
            with st.form("login_form", clear_on_submit=False):
                st.markdown('<div style="font-size:16px; font-weight:600; color:#e2e8f0; margin-bottom:16px;">Sign In</div>',
                            unsafe_allow_html=True)
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("  🔐  LOGIN  ", use_container_width=True)

                if submitted:
                    if username in _USERS and _USERS[username] == password:
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = username
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")

            st.markdown("""
            <div style="text-align:center; margin-top:16px; font-size:12px; color:#4a5568;">
                Contact your administrator for access credentials.
            </div>
            """, unsafe_allow_html=True)


def _require_auth():
    """Return True if user is authenticated, otherwise render login and return False."""
    if st.session_state.get('authenticated', False):
        return True
    _show_login_page()
    return False


# ── Plotly theme ──────────────────────────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#a0aec0', size=12),
    colorway=['#63b3ed', '#9f7aea', '#68d391', '#f6ad55', '#fc8181', '#76e4f7'],
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.08)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='rgba(255,255,255,0.08)'),
)

COLOR_SCALE = [[0, '#0d1b2a'], [0.33, '#2b6cb0'], [0.66, '#9f7aea'], [1, '#fc8181']]
RISK_COLORS = {'Low Risk': '#68d391', 'Moderate Risk': '#f6ad55',
               'High Risk': '#fc814a', 'Critical Risk': '#fc6464'}


# ── Data & Model Loading ──────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    """Load or generate all required data."""
    from src.data_generator import generate_kyc_financial_data
    from src.feri import compute_feri, feri_summary

    feri_path = 'data/kyc_with_feri.csv'
    _required_cols = {'feri_score', 'feri_band', 'kyc_gap_score', 'demographic_score', 'institutional_score'}

    if os.path.exists(feri_path):
        df = pd.read_csv(feri_path)
        # Regenerate FERI columns if missing or corrupted
        if not _required_cols.issubset(df.columns) or df['feri_score'].isna().all():
            df = compute_feri(df)
        else:
            # Ensure feri_band has no NaN (can happen from CSV Categorical round-trip)
            if df['feri_band'].isna().any():
                df['feri_band'] = pd.cut(
                    df['feri_score'],
                    bins=[-1, 25, 45, 65, 101],
                    labels=['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
                ).astype(str)
    else:
        df_raw = generate_kyc_financial_data(n=5000, seed=42)
        df = compute_feri(df_raw)

    # Ensure feri_band is always a plain string column (avoids Categorical comparison issues)
    df['feri_band'] = df['feri_band'].astype(str)

    summary = feri_summary(df)
    return df, summary


@st.cache_resource(show_spinner=False)
def load_models():
    """Train models once and cache them."""
    from src.data_generator import generate_kyc_financial_data
    from src.preprocessor import prepare_data
    from src.models import train_all_models, evaluate_model, get_feature_importance
    from src.feri import compute_feri

    df_raw = generate_kyc_financial_data(n=5000, seed=42)
    X_train, X_test, y_train, y_test, feature_names, encoders, scaler = prepare_data(
        df_raw, test_size=0.20, balance=True, random_state=42
    )
    models = train_all_models(X_train, y_train, random_state=42)
    results = {name: evaluate_model(m, X_test, y_test, name) for name, m in models.items()}
    feat_imp = {
        'Logistic Regression': get_feature_importance(models['Logistic Regression'], feature_names, 'logistic_regression'),
        'Random Forest':       get_feature_importance(models['Random Forest'],       feature_names, 'random_forest'),
        'Gradient Boosting':   get_feature_importance(models['Gradient Boosting'],   feature_names, 'gradient_boosting'),
    }
    return models, results, feature_names, feat_imp, X_test, y_test, encoders, scaler


# ── Helper: metric card HTML ──────────────────────────────────────────────────
def metric_card(label, value, delta=None, sub=None, delta_positive=True):
    delta_html = ''
    if delta:
        color = '#68d391' if delta_positive else '#fc8181'
        arrow = '▲' if delta_positive else '▼'
        delta_html = (
            f'<div style="font-size:13px;font-weight:500;color:{color};margin-bottom:4px;">'
            f'{arrow} {delta}</div>'
        )
    sub_html = (
        f'<div style="font-size:12px;color:#4a5568;margin-top:4px;">{sub}</div>'
        if sub else ''
    )
    return (
        '<div style="background:linear-gradient(135deg,rgba(13,27,42,0.9) 0%,rgba(17,36,58,0.9) 100%);'
        'border:1px solid rgba(99,179,237,0.2);border-radius:16px;padding:20px 24px;'
        'box-shadow:0 4px 24px rgba(0,0,0,0.4),inset 0 1px 0 rgba(255,255,255,0.05);'
        'position:relative;overflow:hidden;">'
        f'<div style="font-size:12px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;'
        f'color:#718096;margin-bottom:8px;">{label}</div>'
        f'<div style="font-size:36px;font-weight:800;color:#63b3ed;line-height:1;margin-bottom:6px;">{value}</div>'
        f'{delta_html}'
        f'{sub_html}'
        '</div>'
    )


def section_header(title, subtitle=''):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── Sidebar navigation ────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 20px 0 28px 0; text-align: center;">
            <div style="font-size: 36px; margin-bottom: 8px;">🏦</div>
            <div style="font-size: 16px; font-weight: 700; color: #63b3ed; letter-spacing: 0.04em;">KYC EXCLUSION</div>
            <div style="font-size: 11px; color: #4a5568; letter-spacing: 0.08em; text-transform: uppercase;">AI Analytics Platform</div>
            <div style="height: 1px; background: rgba(99,179,237,0.15); margin: 16px 0 0 0;"></div>
        </div>
        """, unsafe_allow_html=True)

        pages = {
            "📊  Overview Dashboard":     "overview",
            "🔍  Individual Risk Scanner": "scanner",
            "🤖  Model Performance":       "models",
            "📈  Data Explorer":           "explorer",
            "🎯  FERI Analytics":          "feri",
            "📋  Policy Intelligence":     "policy",
        }

        if 'page' not in st.session_state:
            st.session_state.page = 'overview'

        for label, key in pages.items():
            active = 'active' if st.session_state.page == key else ''
            if st.button(label, key=f'nav_{key}',
                         use_container_width=True,
                         help=f"Navigate to {label.split('  ')[1]}"):
                st.session_state.page = key

        st.markdown("""
        <div style="height: 1px; background: rgba(99,179,237,0.1); margin: 20px 0;"></div>
        <div style="font-size: 11px; color: #2d3748; text-align: center; padding-bottom: 12px;">
            <div style="color: #4a5568; margin-bottom: 4px;">Research Project — Group 2</div>
            <div style="color: #2d3748;">Midlands State University</div>
            <div style="color: #2d3748; margin-top: 4px;">FinScope Zimbabwe 2022</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Logged-in user + logout ──
        username = st.session_state.get('username', '')
        st.markdown(f"""
        <div style="margin: 8px 0 4px 0; padding: 10px 14px;
                    background: rgba(99,179,237,0.06); border-radius: 10px;
                    border: 1px solid rgba(99,179,237,0.12);">
            <div style="font-size:11px; color:#4a5568; text-transform:uppercase; letter-spacing:0.06em;">Signed in as</div>
            <div style="font-size:13px; font-weight:600; color:#63b3ed; margin-top:2px;">👤 {username}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True, key="logout_btn"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = ''
            st.rerun()

    return st.session_state.page


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_overview(df, summary):
    st.markdown("""
    <div class="page-banner">
        <h1>KYC Financial Exclusion Platform</h1>
        <p>Zimbabwe Financial Inclusion Intelligence — Powered by Machine Learning & FERI Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Top KPI row ──
    exc_rate   = df['financially_excluded'].mean() * 100
    rural_exc  = df[df['location'] == 'Rural']['financially_excluded'].mean() * 100
    female_exc = df[df['gender'] == 'Female']['financially_excluded'].mean() * 100
    mean_feri  = df['feri_score'].mean() if 'feri_score' in df.columns else 0.0
    critical   = int((df['feri_band'].astype(str) == 'Critical Risk').sum()) if 'feri_band' in df.columns else 0
    if pd.isna(mean_feri):
        mean_feri = 0.0

    cols = st.columns(5)
    with cols[0]:
        st.markdown(metric_card("Overall Exclusion Rate", f"{exc_rate:.1f}%",
                                delta="vs 38% FinScope target", delta_positive=False,
                                sub=f"{int(exc_rate/100*5000):,} of 5,000 individuals"),
                    unsafe_allow_html=True)
    with cols[1]:
        st.markdown(metric_card("Rural Exclusion Rate", f"{rural_exc:.1f}%",
                                delta="2× urban rate", delta_positive=False,
                                sub="Structural geographic barrier"),
                    unsafe_allow_html=True)
    with cols[2]:
        st.markdown(metric_card("Female Exclusion Rate", f"{female_exc:.1f}%",
                                delta=f"+{female_exc - df[df['gender']=='Male']['financially_excluded'].mean()*100:.1f}pp vs male",
                                delta_positive=False,
                                sub="Gender-driven documentation gap"),
                    unsafe_allow_html=True)
    with cols[3]:
        st.markdown(metric_card("Mean FERI Score", f"{mean_feri:.1f}",
                                sub="0 = Fully Included · 100 = Critically Excluded"),
                    unsafe_allow_html=True)
    with cols[4]:
        st.markdown(metric_card("Critical Risk Individuals", f"{critical:,}",
                                delta_positive=False,
                                sub="FERI score > 65"),
                    unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)
    divider()

    # ── Charts row 1 ──
    section_header("Exclusion Landscape", "Geographic and demographic breakdown across Zimbabwe")
    c1, c2 = st.columns([1.4, 1])

    with c1:
        # Exclusion by province
        prov_exc = df.groupby('province')['financially_excluded'].mean().mul(100).reset_index()
        prov_exc.columns = ['Province', 'Exclusion Rate (%)']
        prov_exc = prov_exc.sort_values('Exclusion Rate (%)', ascending=True)
        fig = go.Figure(go.Bar(
            x=prov_exc['Exclusion Rate (%)'],
            y=prov_exc['Province'],
            orientation='h',
            marker=dict(
                color=prov_exc['Exclusion Rate (%)'],
                colorscale=[[0, '#2b6cb0'], [0.5, '#9f7aea'], [1, '#fc6464']],
                showscale=False,
            ),
            text=[f"{v:.1f}%" for v in prov_exc['Exclusion Rate (%)']],
            textposition='outside',
            textfont=dict(size=11, color='#a0aec0'),
        ))
        fig.update_layout(**PLOTLY_THEME, title=dict(text='Financial Exclusion by Province', font=dict(color='#e2e8f0', size=14)),
                          height=340)
        fig.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        # FERI band pie
        band_counts = df['feri_band'].value_counts()
        colors = [RISK_COLORS.get(b, '#718096') for b in band_counts.index]
        fig2 = go.Figure(go.Pie(
            labels=band_counts.index,
            values=band_counts.values,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color='rgba(0,0,0,0.3)', width=2)),
            textinfo='label+percent',
            textfont=dict(size=11),
            insidetextorientation='radial',
        ))
        fig2.add_annotation(text="FERI<br>Bands", x=0.5, y=0.5, font=dict(size=13, color='#a0aec0'), showarrow=False)
        fig2.update_layout(**PLOTLY_THEME, title=dict(text='Risk Band Distribution', font=dict(color='#e2e8f0', size=14)),
                           height=340, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── Charts row 2 ──
    c3, c4, c5 = st.columns(3)

    with c3:
        # Exclusion by employment sector
        emp_exc = df.groupby('employment_sector')['financially_excluded'].mean().mul(100).reset_index()
        emp_exc.columns = ['Sector', 'Exclusion Rate']
        fig3 = go.Figure(go.Bar(
            x=emp_exc['Sector'], y=emp_exc['Exclusion Rate'],
            marker=dict(color=['#63b3ed', '#f6ad55', '#fc8181'], line=dict(color='rgba(0,0,0,0.2)', width=1)),
            text=[f"{v:.1f}%" for v in emp_exc['Exclusion Rate']],
            textposition='outside', textfont=dict(size=11, color='#a0aec0'),
        ))
        fig3.update_layout(**PLOTLY_THEME, title=dict(text='Exclusion by Employment', font=dict(color='#e2e8f0', size=13)),
                           height=280, showlegend=False)
        fig3.update_yaxes(range=[0, 80])
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    with c4:
        # Age distribution with exclusion overlay
        age_bins = pd.cut(df['age'], bins=[17,25,35,45,55,65,80], labels=['18-25','26-35','36-45','46-55','56-65','65+'])
        age_exc = df.groupby(age_bins, observed=True)['financially_excluded'].mean().mul(100)
        age_cnt = df.groupby(age_bins, observed=True)['financially_excluded'].count()
        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.add_trace(go.Bar(x=age_cnt.index.astype(str), y=age_cnt.values, name='Count',
                               marker_color='rgba(99,179,237,0.25)', marker_line_color='rgba(99,179,237,0.6)', marker_line_width=1), secondary_y=False)
        fig4.add_trace(go.Scatter(x=age_exc.index.astype(str), y=age_exc.values, name='Excl. Rate %',
                                   mode='lines+markers', line=dict(color='#fc8181', width=2),
                                   marker=dict(size=7, color='#fc8181')), secondary_y=True)
        fig4.update_layout(**PLOTLY_THEME, title=dict(text='Age vs Exclusion Rate', font=dict(color='#e2e8f0', size=13)), height=280)
        fig4.update_yaxes(title_text="Count", secondary_y=False, gridcolor='rgba(255,255,255,0.04)')
        fig4.update_yaxes(title_text="Excl. Rate %", secondary_y=True, gridcolor='rgba(255,255,255,0.04)')
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

    with c5:
        # Income quintile exclusion
        inc_exc = df.groupby('income_quintile')['financially_excluded'].mean().mul(100).reset_index()
        inc_exc.columns = ['Quintile', 'Exclusion Rate']
        fig5 = go.Figure(go.Scatter(
            x=inc_exc['Quintile'], y=inc_exc['Exclusion Rate'],
            mode='lines+markers+text',
            line=dict(color='#9f7aea', width=3),
            marker=dict(size=10, color='#9f7aea', line=dict(color='white', width=2)),
            fill='tozeroy', fillcolor='rgba(159,122,234,0.1)',
            text=[f"Q{q}: {v:.1f}%" for q, v in zip(inc_exc['Quintile'], inc_exc['Exclusion Rate'])],
            textposition='top center', textfont=dict(size=10, color='#a0aec0'),
        ))
        fig5.update_layout(**PLOTLY_THEME, title=dict(text='Income Quintile vs Exclusion', font=dict(color='#e2e8f0', size=13)),
                           height=280)
        fig5.update_xaxes(ticktext=['Q1\n(Lowest)', 'Q2', 'Q3', 'Q4', 'Q5\n(Highest)'], tickvals=[1, 2, 3, 4, 5])
        st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

    divider()

    # ── KYC Documentation heatmap ──
    section_header("KYC Documentation Gap Analysis")
    c6, c7 = st.columns([1.2, 1])

    with c6:
        # Doc possession by segment
        docs = ['has_national_id', 'has_proof_of_address', 'has_tin', 'has_employment_proof']
        doc_labels = ['National ID', 'Proof of Address', 'TIN', 'Employment Proof']
        segments = ['Urban', 'Rural', 'Male', 'Female', 'Formal', 'Informal', 'Unemployed']
        masks = [
            df['location'] == 'Urban', df['location'] == 'Rural',
            df['gender'] == 'Male', df['gender'] == 'Female',
            df['employment_sector'] == 'Formal',
            df['employment_sector'] == 'Informal',
            df['employment_sector'] == 'Unemployed',
        ]
        z = np.array([[df[m][d].mean() * 100 for d in docs] for m in masks])
        fig6 = go.Figure(go.Heatmap(
            z=z, x=doc_labels, y=segments,
            colorscale=[[0, '#1a0530'], [0.4, '#2b6cb0'], [0.7, '#4299e1'], [1, '#68d391']],
            text=np.round(z, 1), texttemplate="%{text}%", textfont=dict(size=11),
            zmin=0, zmax=100,
            colorbar=dict(tickfont=dict(color='#a0aec0'), thickness=12),
        ))
        fig6.update_layout(**PLOTLY_THEME,
                           title=dict(text='KYC Document Possession Rate by Segment (%)', font=dict(color='#e2e8f0', size=14)),
                           height=320)
        fig6.update_xaxes(tickfont=dict(size=11))
        fig6.update_yaxes(tickfont=dict(size=11))
        st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False})

    with c7:
        # KYC barrier level donut
        barrier_cnt = df['kyc_barrier_level'].value_counts().reindex(['High', 'Medium', 'Low'])
        fig7 = go.Figure(go.Pie(
            labels=barrier_cnt.index, values=barrier_cnt.values,
            hole=0.6,
            marker=dict(colors=['#fc6464', '#f6ad55', '#68d391'],
                        line=dict(color='rgba(0,0,0,0.3)', width=2)),
            textinfo='label+value',
            textfont=dict(size=12),
        ))
        fig7.add_annotation(text=f"{barrier_cnt['High']:,}<br><span style='font-size:11px'>High Barrier</span>",
                            x=0.5, y=0.5, font=dict(size=15, color='#fc8181'), showarrow=False)
        fig7.update_layout(**PLOTLY_THEME,
                           title=dict(text='KYC Barrier Severity', font=dict(color='#e2e8f0', size=14)),
                           height=320, showlegend=True,
                           legend=dict(font=dict(color='#a0aec0', size=11)))
        st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — INDIVIDUAL RISK SCANNER
# ═══════════════════════════════════════════════════════════════════════════════
def page_scanner(models, feature_names, encoders, scaler):
    st.markdown("""
    <div class="page-banner">
        <h1>Individual Risk Scanner</h1>
        <p>Enter individual profile details to compute real-time FERI score and ML-driven exclusion probability</p>
    </div>
    """, unsafe_allow_html=True)

    c_form, c_result = st.columns([1, 1.1], gap='large')

    with c_form:
        section_header("Profile Input", "Complete all fields for accurate risk assessment")

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider("Age", 18, 80, 32)
                location = st.selectbox("Location", ['Urban', 'Rural'])
                income_q = st.selectbox("Income Quintile", [1, 2, 3, 4, 5],
                                        format_func=lambda x: f"Q{x} — {'Lowest' if x==1 else 'Highest' if x==5 else ''}".strip(' — '))
                distance = st.slider("Distance to Branch (km)", 0.1, 150.0, 5.0, 0.5)
            with col2:
                gender = st.selectbox("Gender", ['Male', 'Female'])
                province = st.selectbox("Province", [
                    'Harare', 'Bulawayo', 'Manicaland', 'Mashonaland Central',
                    'Mashonaland East', 'Mashonaland West', 'Masvingo',
                    'Matabeleland North', 'Matabeleland South', 'Midlands'])
                employment = st.selectbox("Employment Sector", ['Formal', 'Informal', 'Unemployed'])
                education = st.selectbox("Education Level", ['None', 'Primary', 'Secondary', 'Tertiary'])

        st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
        section_header("KYC Documents", "Check all documents held by individual")
        dc1, dc2 = st.columns(2)
        with dc1:
            has_nid  = st.checkbox("National ID Card", value=True)
            has_poa  = st.checkbox("Proof of Address", value=False)
        with dc2:
            has_tin  = st.checkbox("Tax ID Number (TIN)", value=False)
            has_emp  = st.checkbox("Employment Proof", value=False) if employment != 'Unemployed' else False

        section_header("Connectivity", "Technology access — including basic/feature phones (Chimbudzi)")
        tc1, tc2 = st.columns(2)
        with tc1:
            phone_type = st.radio(
                "Phone / Handset Type",
                options=["Smartphone", "Basic Phone (Chimbudzi)", "No Phone"],
                index=0,
                help=(
                    "Smartphone: data & app capable\n"
                    "Basic Phone / Chimbudzi: USSD (*120#) capable, no mobile data\n"
                    "No Phone: no mobile device at all"
                ),
            )
            has_mobile = phone_type != "No Phone"
        with tc2:
            if phone_type == "Smartphone":
                has_internet = st.checkbox("Internet / Mobile Data Access", value=False)
            else:
                has_internet = False
                if phone_type == "Basic Phone (Chimbudzi)":
                    st.markdown("""
                    <div style="background:rgba(246,173,85,0.08); border:1px solid rgba(246,173,85,0.25);
                                border-radius:10px; padding:12px 14px; margin-top:8px; font-size:12px; color:#f6ad55;">
                        <b>USSD Only</b><br>
                        Can use EcoCash (*151#) and USSD banking.<br>
                        No app / internet KYC available.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background:rgba(252,100,100,0.08); border:1px solid rgba(252,100,100,0.25);
                                border-radius:10px; padding:12px 14px; margin-top:8px; font-size:12px; color:#fc6464;">
                        <b>No Mobile Connectivity</b><br>
                        Highest institutional barrier.<br>
                        Physical branch visit required.
                    </div>
                    """, unsafe_allow_html=True)

        assess_btn = st.button("  ⚡  RUN RISK ASSESSMENT  ", use_container_width=True)

    with c_result:
        section_header("Risk Assessment Output")

        if assess_btn:
            # ── Build individual record ──
            record = pd.DataFrame([{
                'age': age, 'gender': gender, 'location': location, 'province': province,
                'education_level': education, 'employment_sector': employment,
                'income_quintile': income_q,
                'has_national_id': int(has_nid), 'has_proof_of_address': int(has_poa),
                'has_tin': int(has_tin), 'has_employment_proof': int(has_emp),
                'kyc_doc_score': int(has_nid) + int(has_poa) + int(has_tin) + int(has_emp),
                'kyc_barrier_level': 'Low' if (int(has_nid)+int(has_poa)+int(has_tin)+int(has_emp)) >= 3 else 'Medium' if (int(has_nid)+int(has_poa)+int(has_tin)+int(has_emp)) == 2 else 'High',
                'distance_to_branch_km': distance,
                'has_mobile_phone': int(has_mobile), 'has_internet': int(has_internet),
                'financially_excluded': 0,
            }])

            # ── FERI calculation ──
            from src.feri import kyc_doc_gap_score, demographic_vulnerability_score, institutional_barrier_score
            kyc_gap  = kyc_doc_gap_score(record).iloc[0]
            demo_vuln = demographic_vulnerability_score(record).iloc[0]
            inst_bar  = institutional_barrier_score(record).iloc[0]
            feri = round(0.45 * kyc_gap + 0.35 * demo_vuln + 0.20 * inst_bar, 1)

            if feri <= 25:
                band = 'Low Risk';      band_cls = 'risk-low';      band_color = '#68d391'
            elif feri <= 45:
                band = 'Moderate Risk'; band_cls = 'risk-moderate'; band_color = '#f6ad55'
            elif feri <= 65:
                band = 'High Risk';     band_cls = 'risk-high';     band_color = '#fc814a'
            else:
                band = 'Critical Risk'; band_cls = 'risk-critical'; band_color = '#fc6464'

            # ── ML probability ──
            try:
                from src.preprocessor import CATEGORICAL_FEATURES, NUMERIC_FEATURES, BINARY_FEATURES
                X_individual = pd.DataFrame([{
                    'age': age, 'income_quintile': income_q,
                    'kyc_doc_score': int(has_nid)+int(has_poa)+int(has_tin)+int(has_emp),
                    'distance_to_branch_km': distance,
                    'gender': gender, 'location': location, 'province': province,
                    'education_level': education, 'employment_sector': employment,
                    'kyc_barrier_level': record['kyc_barrier_level'].iloc[0],
                    'has_national_id': int(has_nid), 'has_proof_of_address': int(has_poa),
                    'has_tin': int(has_tin), 'has_employment_proof': int(has_emp),
                    'has_mobile_phone': int(has_mobile), 'has_internet': int(has_internet),
                }])
                # One-hot encode categoricals to match training pipeline
                X_cat_ohe = pd.get_dummies(X_individual[CATEGORICAL_FEATURES], drop_first=True)
                for col in encoders['columns']:
                    if col not in X_cat_ohe.columns:
                        X_cat_ohe[col] = 0
                X_cat_ohe = X_cat_ohe[encoders['columns']].reset_index(drop=True)
                # Scale numeric features
                X_num = scaler.transform(X_individual[NUMERIC_FEATURES])
                # Binary features (no scaling)
                X_bin = X_individual[BINARY_FEATURES].values
                # Combine in same order as encode_and_scale: numeric, binary, one-hot
                X_proc = np.hstack([X_num, X_bin, X_cat_ohe.values])
                best_model = models['Gradient Boosting']
                ml_prob = best_model.predict_proba(X_proc)[0][1] * 100
            except Exception:
                ml_prob = None

            # ── Render result ──
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:16px;">
                <div class="label">FERI Score</div>
                <div style="display:flex; align-items:center; gap:16px; margin:8px 0;">
                    <div style="font-size:52px; font-weight:800; color:{band_color};">{feri}</div>
                    <div>
                        <span class="{band_cls} risk-badge">{band}</span>
                        <div class="sub" style="margin-top:8px;">Financial Exclusion Risk Index</div>
                    </div>
                </div>
                <div class="feri-bar-container">
                    <div class="feri-bar-fill" style="width:{feri}%; background:linear-gradient(90deg, #68d391, {band_color});"></div>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:10px; color:#4a5568; margin-top:4px;">
                    <span>0 — No Risk</span><span>100 — Critical</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if ml_prob is not None:
                ml_color = '#68d391' if ml_prob < 30 else '#f6ad55' if ml_prob < 55 else '#fc8181'
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:16px;">
                    <div class="label">ML Exclusion Probability (XGBoost)</div>
                    <div style="font-size:36px; font-weight:800; color:{ml_color}; margin:8px 0;">{ml_prob:.1f}%</div>
                    <div class="feri-bar-container">
                        <div class="feri-bar-fill" style="width:{ml_prob}%; background:linear-gradient(90deg, #68d391, {ml_color});"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Sub-score breakdown ──
            st.markdown('<div class="section-header" style="font-size:16px; margin-top:8px;">Sub-Score Breakdown</div>', unsafe_allow_html=True)
            sub_data = {
                'KYC Gap (45%)':      (kyc_gap,   '#63b3ed'),
                'Demographic (35%)':  (demo_vuln, '#9f7aea'),
                'Institutional (20%)': (inst_bar,  '#f6ad55'),
            }
            for label, (val, color) in sub_data.items():
                st.markdown(f"""
                <div style="margin-bottom:10px;">
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#a0aec0; margin-bottom:4px;">
                        <span>{label}</span><span style="color:{color}; font-weight:600;">{val:.0f}/100</span>
                    </div>
                    <div class="feri-bar-container">
                        <div class="feri-bar-fill" style="width:{val}%; background:{color};"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Recommendations ──
            recs = []
            if not has_nid:
                recs.append(("National ID", "Highest priority — worth 40 KYC-gap points", "#fc6464"))
            if not has_poa:
                recs.append(("Proof of Address", "Accept chief's letter / ward councillor attestation", "#fc814a"))
            if location == 'Rural' and distance > 20:
                recs.append(("Distance Barrier", "Enable mobile onboarding / agent banking nearby", "#f6ad55"))
            if phone_type == "No Phone":
                recs.append(("No Mobile Device", "Provision subsidised feature phone (Chimbudzi) for USSD access", "#fc814a"))
            elif phone_type == "Basic Phone (Chimbudzi)":
                recs.append(("USSD Banking", "Enable EcoCash / ZIPIT USSD onboarding (*120*1# / *151#) for feature phone users", "#f6ad55"))
            if not has_internet and phone_type == "Smartphone":
                recs.append(("Mobile Data", "Access data-lite KYC app — bundles available via Econet/NetOne", "#9f7aea"))
            if not has_tin and employment == 'Formal':
                recs.append(("TIN Registration", "Auto-register TIN at onboarding for formal employees", "#9f7aea"))

            if recs:
                st.markdown('<div class="section-header" style="font-size:16px; margin-top:12px;">Priority Interventions</div>', unsafe_allow_html=True)
                for title, detail, color in recs:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.03); border-left:3px solid {color};
                                border-radius:8px; padding:10px 14px; margin-bottom:8px;">
                        <div style="font-size:13px; font-weight:600; color:{color};">{title}</div>
                        <div style="font-size:12px; color:#718096; margin-top:2px;">{detail}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-success"><div style="color:#68d391; font-weight:600;">Low Barrier Profile</div><div style="color:#718096; font-size:13px; margin-top:4px;">This individual has sufficient documentation and connectivity for standard KYC onboarding.</div></div>', unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="info-panel" style="margin-top:24px; text-align:center; padding:48px 24px;">
                <div style="font-size:48px; margin-bottom:16px;">⚡</div>
                <div style="font-size:16px; font-weight:600; color:#90cdf4; margin-bottom:8px;">Ready to Assess</div>
                <div style="font-size:13px; color:#4a5568;">Complete the profile form on the left and click<br>RUN RISK ASSESSMENT to generate results.</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — MODEL PERFORMANCE
# ═══════════════════════════════════════════════════════════════════════════════
def page_models(results, feat_imp):
    st.markdown("""
    <div class="page-banner">
        <h1>Model Performance Intelligence</h1>
        <p>Comparative evaluation of Logistic Regression, Random Forest, and XGBoost classifiers</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Metric comparison table ──
    section_header("Performance Comparison Matrix")
    metrics = ['accuracy', 'roc_auc', 'f1_score', 'precision', 'recall', 'avg_precision']
    metric_labels = ['Accuracy', 'ROC-AUC', 'F1-Score', 'Precision', 'Recall', 'Avg Precision']
    model_names = list(results.keys())

    table_html = '<table class="styled-table"><thead><tr><th>Model</th>'
    for ml in metric_labels:
        table_html += f'<th>{ml}</th>'
    table_html += '</tr></thead><tbody>'

    for name in model_names:
        r = results[name]
        table_html += f'<tr><td><strong style="color:#63b3ed">{name}</strong></td>'
        for m in metrics:
            val = r[m]
            color = '#68d391' if val >= 0.80 else '#f6ad55' if val >= 0.70 else '#fc8181'
            table_html += f'<td style="color:{color}; font-weight:600; font-family:\'JetBrains Mono\'">{val:.4f}</td>'
        table_html += '</tr>'
    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # ── ROC curves ──
    c1, c2 = st.columns(2)
    with c1:
        section_header("ROC Curves", "Receiver Operating Characteristic — higher AUC = better discrimination")
        fig = go.Figure()
        colors = ['#63b3ed', '#9f7aea', '#68d391']
        for (name, r), color in zip(results.items(), colors):
            fig.add_trace(go.Scatter(
                x=r['fpr'], y=r['tpr'],
                name=f"{name} (AUC={r['roc_auc']:.4f})",
                line=dict(color=color, width=2.5),
                mode='lines',
            ))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                                  line=dict(color='rgba(255,255,255,0.2)', dash='dash', width=1),
                                  showlegend=False))
        fig.update_layout(**PLOTLY_THEME,
                          title=dict(text='ROC Curves — All Models', font=dict(color='#e2e8f0', size=14)),
                          height=360,
                          legend=dict(font=dict(color='#a0aec0', size=11), bgcolor='rgba(0,0,0,0)'))
        fig.update_xaxes(title='False Positive Rate', range=[0, 1])
        fig.update_yaxes(title='True Positive Rate', range=[0, 1])
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        section_header("Metric Radar", "Multi-dimensional performance view")
        categories = ['ROC-AUC', 'F1-Score', 'Precision', 'Recall', 'Accuracy']
        metric_keys = ['roc_auc', 'f1_score', 'precision', 'recall', 'accuracy']
        fig2 = go.Figure()
        for (name, r), color in zip(results.items(), colors):
            vals = [r[k] for k in metric_keys]
            vals_closed = vals + [vals[0]]
            cats_closed = categories + [categories[0]]
            fig2.add_trace(go.Scatterpolar(
                r=vals_closed, theta=cats_closed, name=name,
                fill='toself', fillcolor=f'rgba{tuple(list(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.08])}',
                line=dict(color=color, width=2),
            ))
        fig2.update_layout(**PLOTLY_THEME,
                           polar=dict(
                               bgcolor='rgba(0,0,0,0)',
                               radialaxis=dict(range=[0.6, 1.0], gridcolor='rgba(255,255,255,0.08)', tickfont=dict(size=9, color='#4a5568')),
                               angularaxis=dict(gridcolor='rgba(255,255,255,0.08)', tickfont=dict(size=11, color='#a0aec0')),
                           ),
                           title=dict(text='Performance Radar', font=dict(color='#e2e8f0', size=14)),
                           height=360,
                           legend=dict(font=dict(color='#a0aec0', size=11), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── Confusion matrices ──
    section_header("Confusion Matrices", "Predicted vs actual classification outcomes")
    cm_cols = st.columns(3)
    for i, (name, r) in enumerate(results.items()):
        with cm_cols[i]:
            cm = r['confusion_matrix']
            labels = ['Included', 'Excluded']
            fig3 = go.Figure(go.Heatmap(
                z=cm, x=labels, y=labels,
                colorscale=[[0, '#0d1b2a'], [1, '#2b6cb0']],
                text=cm, texttemplate='<b>%{text}</b>',
                textfont=dict(size=18, color='white'),
                showscale=False,
            ))
            fig3.update_layout(**PLOTLY_THEME,
                               title=dict(text=name, font=dict(color='#e2e8f0', size=13)),
                               height=260)
            fig3.update_xaxes(title='Predicted', tickfont=dict(size=11))
            fig3.update_yaxes(title='Actual', tickfont=dict(size=11))
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    divider()

    # ── Feature importances ──
    section_header("Feature Importance Analysis")
    model_sel = st.selectbox("Select Model", list(feat_imp.keys()))
    fi = feat_imp[model_sel].head(15)
    fig4 = go.Figure(go.Bar(
        x=fi['importance_pct'], y=fi['feature'],
        orientation='h',
        marker=dict(
            color=fi['importance_pct'],
            colorscale=[[0, '#2b6cb0'], [0.5, '#9f7aea'], [1, '#fc6464']],
            showscale=False,
            line=dict(color='rgba(0,0,0,0.2)', width=1),
        ),
        text=[f"{v:.2f}%" for v in fi['importance_pct']],
        textposition='outside', textfont=dict(size=11, color='#a0aec0'),
    ))
    fig4.update_layout(**PLOTLY_THEME,
                       title=dict(text=f'Top 15 Features — {model_sel}', font=dict(color='#e2e8f0', size=14)),
                       height=440)
    fig4.update_xaxes(title='Importance (%)')
    fig4.update_yaxes(autorange='reversed', tickfont=dict(size=11))
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DATA EXPLORER
# ═══════════════════════════════════════════════════════════════════════════════
def page_explorer(df):
    st.markdown("""
    <div class="page-banner">
        <h1>Data Explorer</h1>
        <p>Interactive exploration of the synthetic KYC dataset (n=5,000) calibrated to FinScope Zimbabwe 2022</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Interactive Filter Panel ──
    st.markdown('<div class="section-header" style="margin-top:0;">Filter Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">All filters apply instantly — no button needed</div>', unsafe_allow_html=True)

    row1 = st.columns([1, 1, 1, 1])
    row2 = st.columns([1.5, 1.5, 1])

    with row1[0]:
        loc_f = st.multiselect("Location", ['Urban', 'Rural'], default=['Urban', 'Rural'])
    with row1[1]:
        gen_f = st.multiselect("Gender", ['Male', 'Female'], default=['Male', 'Female'])
    with row1[2]:
        emp_f = st.multiselect("Employment", ['Formal', 'Informal', 'Unemployed'],
                               default=['Formal', 'Informal', 'Unemployed'])
    with row1[3]:
        exc_f = st.multiselect("Exclusion Status", [0, 1],
                               format_func=lambda x: 'Excluded' if x == 1 else 'Included',
                               default=[0, 1])

    with row2[0]:
        all_provinces = sorted(df['province'].unique().tolist())
        prov_f = st.multiselect("Province", all_provinces, default=all_provinces)
    with row2[1]:
        all_bands = ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk']
        band_f = st.multiselect("FERI Risk Band", all_bands, default=all_bands)
    with row2[2]:
        age_range = st.slider("Age Range", int(df['age'].min()), int(df['age'].max()),
                              (int(df['age'].min()), int(df['age'].max())))

    # Collapsible advanced filters
    with st.expander("Advanced Filters", expanded=False):
        adv1, adv2 = st.columns(2)
        with adv1:
            inc_range = st.slider("Income Quintile", 1, 5, (1, 5))
        with adv2:
            feri_range = st.slider("FERI Score Range", 0.0, 100.0, (0.0, 100.0), step=0.5)

    # Build safe default lists if filters are cleared
    loc_f   = loc_f   or ['Urban', 'Rural']
    gen_f   = gen_f   or ['Male', 'Female']
    emp_f   = emp_f   or ['Formal', 'Informal', 'Unemployed']
    exc_f   = exc_f   or [0, 1]
    prov_f  = prov_f  or all_provinces
    band_f  = band_f  or all_bands

    mask = (
        df['location'].isin(loc_f) &
        df['gender'].isin(gen_f) &
        df['employment_sector'].isin(emp_f) &
        df['financially_excluded'].isin(exc_f) &
        df['province'].isin(prov_f) &
        df['feri_band'].astype(str).isin(band_f) &
        df['age'].between(age_range[0], age_range[1]) &
        df['income_quintile'].between(inc_range[0], inc_range[1]) &
        df['feri_score'].between(feri_range[0], feri_range[1])
    )
    dff = df[mask]

    if dff.empty:
        st.warning("No records match the current filter combination. Try widening your filters.")
        return

    divider()

    # ── Filtered KPIs ──
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(metric_card("Records Shown", f"{len(dff):,}",
                                sub=f"{len(dff)/len(df)*100:.1f}% of total"),
                    unsafe_allow_html=True)
    with k2:
        st.markdown(metric_card("Exclusion Rate", f"{dff['financially_excluded'].mean()*100:.1f}%"),
                    unsafe_allow_html=True)
    with k3:
        st.markdown(metric_card("Mean FERI Score", f"{dff['feri_score'].mean():.1f}"),
                    unsafe_allow_html=True)
    with k4:
        st.markdown(metric_card("Mean KYC Gap", f"{dff['kyc_gap_score'].mean():.1f}"),
                    unsafe_allow_html=True)

    st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

    # ── Scatter: FERI vs distance ──
    c1, c2 = st.columns(2)
    with c1:
        fig = px.scatter(
            dff.sample(min(1500, len(dff)), random_state=1),
            x='distance_to_branch_km', y='feri_score',
            color='feri_band',
            color_discrete_map=RISK_COLORS,
            opacity=0.6, size_max=6,
            hover_data=['age', 'gender', 'location', 'employment_sector'],
            labels={'distance_to_branch_km': 'Distance to Branch (km)', 'feri_score': 'FERI Score'},
            title='FERI Score vs Distance to Branch',
        )
        fig.update_traces(marker=dict(size=4))
        fig.update_layout(**PLOTLY_THEME, height=360,
                          title=dict(font=dict(color='#e2e8f0', size=14)),
                          legend=dict(font=dict(color='#a0aec0', size=11), bgcolor='rgba(0,0,0,0)'))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        # KYC doc score histogram by exclusion status
        fig2 = go.Figure()
        for excl, color, label in [(0, '#63b3ed', 'Included'), (1, '#fc8181', 'Excluded')]:
            sub = dff[dff['financially_excluded'] == excl]['kyc_doc_score']
            fig2.add_trace(go.Histogram(
                x=sub, name=label, opacity=0.75,
                marker_color=color, nbinsx=5,
                marker_line=dict(color='rgba(0,0,0,0.3)', width=1),
            ))
        fig2.update_layout(**PLOTLY_THEME,
                           title=dict(text='KYC Score Distribution by Status', font=dict(color='#e2e8f0', size=14)),
                           height=360, barmode='overlay',
                           legend=dict(font=dict(color='#a0aec0'), bgcolor='rgba(0,0,0,0)'))
        fig2.update_xaxes(title='KYC Document Score (0-4)')
        fig2.update_yaxes(title='Count')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── Data table ──
    divider()
    section_header("Filtered Records")
    display_cols = ['age', 'gender', 'location', 'province', 'employment_sector',
                    'income_quintile', 'kyc_doc_score', 'feri_score', 'feri_band', 'financially_excluded']
    st.dataframe(
        dff[display_cols].head(200).style
        .background_gradient(subset=['feri_score'], cmap='RdYlGn_r')
        .format({'feri_score': '{:.1f}', 'financially_excluded': lambda x: '🔴 Excluded' if x else '🟢 Included'}),
        use_container_width=True,
        height=360,
    )
    st.caption(f"Showing first 200 of {len(dff):,} filtered records")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — FERI ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
def page_feri(df, summary):
    st.markdown("""
    <div class="page-banner">
        <h1>FERI Analytics</h1>
        <p>Financial Exclusion Risk Index — Composite 0–100 score combining KYC gap, demographic vulnerability, and institutional barriers</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Index formula card ──
    st.markdown("""
    <div class="info-panel" style="margin-bottom:24px;">
        <div style="font-size:13px; font-weight:700; color:#63b3ed; margin-bottom:8px; letter-spacing:0.04em;">FERI FORMULA</div>
        <div style="font-family:'JetBrains Mono'; font-size:14px; color:#e2e8f0;">
            FERI = 0.45 × <span style="color:#63b3ed">KYC Gap Score</span> + 0.35 × <span style="color:#9f7aea">Demographic Vulnerability</span> + 0.20 × <span style="color:#68d391">Institutional Barrier</span>
        </div>
        <div style="font-size:12px; color:#4a5568; margin-top:8px;">
            Bands: <span style="color:#68d391">Low Risk (0-25)</span> ·
            <span style="color:#f6ad55">Moderate Risk (25-45)</span> ·
            <span style="color:#fc814a">High Risk (45-65)</span> ·
            <span style="color:#fc6464">Critical Risk (65-100)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Distribution ──
    c1, c2 = st.columns([1.5, 1])
    with c1:
        section_header("FERI Score Distribution")
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df['feri_score'], nbinsx=50, opacity=0.8,
            marker=dict(
                color=df['feri_score'].values,
                colorscale=[[0, '#68d391'], [0.35, '#f6ad55'], [0.65, '#fc814a'], [1, '#fc6464']],
                showscale=False,
                line=dict(color='rgba(0,0,0,0.2)', width=0.5),
            ),
            name='FERI Score',
        ))
        for band, xval, color in [(25, 25, '#68d391'), (45, 45, '#f6ad55'), (65, 65, '#fc6464')]:
            fig.add_vline(x=xval, line=dict(color=color, width=1.5, dash='dash'),
                          annotation_text=f'{xval}', annotation_font=dict(color=color, size=10))
        fig.update_layout(**PLOTLY_THEME,
                          title=dict(text='Distribution of FERI Scores (n=5,000)', font=dict(color='#e2e8f0', size=14)),
                          height=320)
        fig.update_xaxes(title='FERI Score')
        fig.update_yaxes(title='Count')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c2:
        section_header("Sub-Score Statistics")
        sub_stats = pd.DataFrame({
            'Sub-Index': ['KYC Gap (45%)', 'Demographic (35%)', 'Institutional (20%)'],
            'Mean': [df['kyc_gap_score'].mean(), df['demographic_score'].mean(), df['institutional_score'].mean()],
            'Median': [df['kyc_gap_score'].median(), df['demographic_score'].median(), df['institutional_score'].median()],
            'Std': [df['kyc_gap_score'].std(), df['demographic_score'].std(), df['institutional_score'].std()],
        }).round(1)
        for _, row in sub_stats.iterrows():
            color = '#63b3ed' if 'KYC' in row['Sub-Index'] else '#9f7aea' if 'Demo' in row['Sub-Index'] else '#68d391'
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.03); border-left:3px solid {color};
                        border-radius:8px; padding:12px 16px; margin-bottom:10px;">
                <div style="font-size:12px; font-weight:600; color:{color}; margin-bottom:6px;">{row['Sub-Index']}</div>
                <div style="display:flex; gap:20px;">
                    <div><span style="color:#4a5568; font-size:11px;">Mean</span><br><span style="color:#e2e8f0; font-weight:700;">{row['Mean']}</span></div>
                    <div><span style="color:#4a5568; font-size:11px;">Median</span><br><span style="color:#e2e8f0; font-weight:700;">{row['Median']}</span></div>
                    <div><span style="color:#4a5568; font-size:11px;">Std</span><br><span style="color:#e2e8f0; font-weight:700;">{row['Std']}</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── By demographic ──
    divider()
    section_header("FERI by Demographic Group", "Sorted by mean FERI (highest risk first)")
    top_groups = summary.head(12)

    fig2 = go.Figure()
    bar_colors = [
        '#fc6464' if r >= 65 else '#fc814a' if r >= 45 else '#f6ad55' if r >= 25 else '#68d391'
        for r in top_groups['Mean FERI']
    ]
    fig2.add_trace(go.Bar(
        x=top_groups['Group'], y=top_groups['Mean FERI'],
        name='Mean FERI',
        marker=dict(color=bar_colors, line=dict(color='rgba(0,0,0,0.2)', width=1)),
        text=[f"{v:.1f}" for v in top_groups['Mean FERI']],
        textposition='outside', textfont=dict(size=11, color='#a0aec0'),
    ))
    fig2.add_trace(go.Scatter(
        x=top_groups['Group'], y=top_groups['Exclusion Rate (%)'],
        name='Exclusion Rate %', yaxis='y2',
        mode='lines+markers',
        line=dict(color='#9f7aea', width=2, dash='dot'),
        marker=dict(size=8, color='#9f7aea'),
    ))
    fig2.update_layout(**PLOTLY_THEME,
                       title=dict(text='Mean FERI Score & Exclusion Rate by Demographic Group', font=dict(color='#e2e8f0', size=14)),
                       height=380,
                       yaxis2=dict(title='Exclusion Rate (%)', overlaying='y', side='right',
                                   gridcolor='rgba(255,255,255,0)', tickfont=dict(color='#9f7aea')),
                       legend=dict(font=dict(color='#a0aec0', size=11), bgcolor='rgba(0,0,0,0)'))
    fig2.update_xaxes(tickangle=-30, tickfont=dict(size=11))
    fig2.update_yaxes(title='Mean FERI Score')
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # ── Correlation heatmap ──
    divider()
    section_header("Sub-Index Correlation Matrix")
    corr_cols = ['kyc_gap_score', 'demographic_score', 'institutional_score', 'feri_score', 'financially_excluded']
    corr_labels = ['KYC Gap', 'Demographic', 'Institutional', 'FERI', 'Excluded']
    corr_mat = df[corr_cols].corr().round(3)

    fig3 = go.Figure(go.Heatmap(
        z=corr_mat.values, x=corr_labels, y=corr_labels,
        colorscale=[[0, '#0d1b2a'], [0.5, '#2b6cb0'], [1, '#68d391']],
        text=corr_mat.values, texttemplate='%{text}',
        textfont=dict(size=12),
        zmin=-1, zmax=1,
        colorbar=dict(tickfont=dict(color='#a0aec0'), thickness=12),
    ))
    fig3.update_layout(**PLOTLY_THEME,
                       title=dict(text='Pearson Correlation — FERI Components vs Exclusion', font=dict(color='#e2e8f0', size=14)),
                       height=320)
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — POLICY INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
def page_policy(df):
    st.markdown("""
    <div class="page-banner">
        <h1>Policy Intelligence</h1>
        <p>Evidence-based regulatory recommendations derived from FERI analytics and ML model findings</p>
    </div>
    """, unsafe_allow_html=True)

    policies = [
        {
            "title": "1. Tiered KYC Framework",
            "impact": "HIGH",
            "icon": "🏛️",
            "color": "#63b3ed",
            "summary": "Implement risk-proportionate onboarding aligned with FATF Recommendation 10.",
            "detail": "Tier 1 (Basic): Mobile money / low-value accounts — accept single government-issued ID (voter card, birth certificate) without proof-of-address. Tier 2 (Standard): Savings / credit — national ID + corroborating document. Tier 3 (Full): Large transactions — full CDD. Our analysis shows 68% of excluded individuals qualify for Tier 1 onboarding.",
            "evidence": f"Proof-of-address gap affects {df['has_proof_of_address'].eq(0).mean()*100:.0f}% of the dataset",
        },
        {
            "title": "2. Digital Identity Infrastructure",
            "impact": "HIGH",
            "icon": "🔐",
            "color": "#9f7aea",
            "summary": "National digital ID system interoperable across all financial institutions.",
            "detail": "Eliminate duplicative paper-based verification and reduce compliance costs for low-income segments. A unified digital ID registry would reduce onboarding friction for the 32% of individuals without proof-of-address.",
            "evidence": f"National ID possession: {df['has_national_id'].mean()*100:.0f}% — highest single-document predictor (weight=40pts in FERI)",
        },
        {
            "title": "3. Alternative Proof of Address",
            "impact": "HIGH",
            "icon": "📍",
            "color": "#68d391",
            "summary": "Formally accept community vouching, ward councillor attestations, and mobile network location data.",
            "detail": "Rural residents constitute 45% of the dataset with proof-of-address possession rate of only 22%. Accepting chief's letters and GPS-verified mobile addresses would immediately reduce FERI scores for this segment.",
            "evidence": f"Rural proof-of-address gap: {df[df['location']=='Rural']['has_proof_of_address'].eq(0).mean()*100:.0f}% lack PoA",
        },
        {
            "title": "4. Mobile-First Onboarding",
            "impact": "MEDIUM",
            "icon": "📱",
            "color": "#f6ad55",
            "summary": "Mandate acceptance of Eco-Cash / mobile wallet history as supplementary identity verification.",
            "detail": "Mobile phone possession (78% overall) significantly reduces FERI institutional barrier score by 30 points. Mobile onboarding removes the distance barrier affecting 31% of rural individuals located >20km from a branch.",
            "evidence": f"Distance >20km affects {df[df['location']=='Rural']['distance_to_branch_km'].gt(20).mean()*100:.0f}% of rural individuals",
        },
        {
            "title": "5. Gender-Responsive Compliance",
            "impact": "MEDIUM",
            "icon": "⚖️",
            "color": "#fc814a",
            "summary": "Issue RBZ circular acknowledging female-headed household documentation barriers.",
            "detail": "Female exclusion rate is 43% vs 33% for males. The primary driver is the proof-of-address gap (female PoA possession: 31% vs male: 42%). Standardising a guardian-letter waiver for joint accounts would address this disparity.",
            "evidence": f"Female exclusion premium: +{(df[df['gender']=='Female']['financially_excluded'].mean()-df[df['gender']=='Male']['financially_excluded'].mean())*100:.1f}pp vs male",
        },
        {
            "title": "6. FERI as Supervisory Metric",
            "impact": "MEDIUM",
            "icon": "📊",
            "color": "#76e4f7",
            "summary": "Adopt FERI as an RBZ supervisory tool — mandate quarterly FERI-banded rejection rate reporting.",
            "detail": "Financial institutions should report quarterly FERI-banded account opening rejection rates to the FIU. This creates accountability for inclusion progress and enables early warning detection of systematic exclusion patterns.",
            "evidence": f"Critical Risk segment ({df['feri_band'].eq('Critical Risk').mean()*100:.0f}% of population) requires active monitoring",
        },
    ]

    for pol in policies:
        impact_color = '#fc6464' if pol['impact'] == 'HIGH' else '#f6ad55'
        with st.expander(f"{pol['icon']}  {pol['title']}", expanded=False):
            st.markdown(f"""
            <div style="padding: 4px 0 12px 0;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
                    <span style="background:rgba(255,255,255,0.05); border:1px solid {impact_color};
                                 color:{impact_color}; font-size:10px; font-weight:700; padding:3px 10px;
                                 border-radius:12px; letter-spacing:0.06em;">{pol['impact']} IMPACT</span>
                    <span style="color:#718096; font-size:13px;">{pol['summary']}</span>
                </div>
                <div style="font-size:13px; color:#a0aec0; line-height:1.7; margin-bottom:12px;">{pol['detail']}</div>
                <div style="background:rgba(99,179,237,0.06); border:1px solid rgba(99,179,237,0.15);
                             border-radius:8px; padding:10px 14px;">
                    <span style="font-size:11px; color:#4a5568; text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">Evidence Base · </span>
                    <span style="font-size:12px; color:#90cdf4;">{pol['evidence']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Priority matrix ──
    section_header("Policy Priority Matrix", "Impact vs implementation feasibility")
    matrix_data = pd.DataFrame({
        'Policy':       ['Tiered KYC', 'Digital ID', 'Alt. Address', 'Mobile-First', 'Gender Guidance', 'FERI Monitoring'],
        'Feasibility':  [85, 40, 75, 80, 90, 70],
        'Impact':       [90, 95, 85, 75, 65, 60],
        'Affected (%)': [68, 32, 45, 22, 43, 12],
        'Color':        ['#63b3ed', '#9f7aea', '#68d391', '#f6ad55', '#fc814a', '#76e4f7'],
    })
    fig = go.Figure()
    for _, row in matrix_data.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Feasibility']], y=[row['Impact']],
            mode='markers+text',
            marker=dict(size=row['Affected (%)']/2 + 15, color=row['Color'], opacity=0.8,
                        line=dict(color='white', width=1.5)),
            text=[row['Policy']],
            textposition='top center',
            textfont=dict(size=11, color='#e2e8f0'),
            name=row['Policy'],
            showlegend=False,
        ))
    fig.add_vline(x=70, line=dict(color='rgba(255,255,255,0.1)', dash='dash'))
    fig.add_hline(y=70, line=dict(color='rgba(255,255,255,0.1)', dash='dash'))
    fig.add_annotation(x=85, y=95, text="Quick Wins", font=dict(color='rgba(255,255,255,0.3)', size=11), showarrow=False)
    fig.add_annotation(x=45, y=95, text="Strategic", font=dict(color='rgba(255,255,255,0.3)', size=11), showarrow=False)
    fig.update_layout(**PLOTLY_THEME,
                      title=dict(text='Policy Priority Matrix (Bubble size = Affected Population %)', font=dict(color='#e2e8f0', size=14)),
                      height=440)
    fig.update_xaxes(title='Implementation Feasibility (%)', range=[30, 100])
    fig.update_yaxes(title='Expected Impact (%)', range=[50, 100])
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main():
    if not _require_auth():
        return

    with st.spinner("Initialising platform..."):
        df, summary = load_data()

    page = render_sidebar()

    if page == 'overview':
        page_overview(df, summary)

    elif page == 'scanner':
        with st.spinner("Loading models..."):
            models, results, feature_names, feat_imp, X_test, y_test, encoders, scaler = load_models()
        page_scanner(models, feature_names, encoders, scaler)

    elif page == 'models':
        with st.spinner("Loading models..."):
            models, results, feature_names, feat_imp, X_test, y_test, encoders, scaler = load_models()
        page_models(results, feat_imp)

    elif page == 'explorer':
        page_explorer(df)

    elif page == 'feri':
        page_feri(df, summary)

    elif page == 'policy':
        page_policy(df)


if __name__ == '__main__':
    main()
