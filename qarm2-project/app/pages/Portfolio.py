# app/pages/Portfolio.py

import sys
import os
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import pandas as pd
import streamlit as st

from layout import set_page_config, render_header
from src.data import load_prices, to_returns, mean_cov
from src.markowitz import gmv_weights, tangency_weights
from src.risk_parity import erc_weights
from src.utils import portfolio_stats

# -------------------------------------------------
# Page config + header
# -------------------------------------------------
set_page_config("Vedoinvest – Portfolio")
render_header(active_page="Portfolio")

# -------- Banner (bleu) --------
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #0d6efd, #1a75ff);
        padding: 28px 20px;
        border-radius: 10px;
        margin: 10px 0 25px 0;
        text-align:center;
        color: white;
        font-weight: 600;
        font-size: 20px;
    ">
        📊 Portfolio Optimisation
        <div style="font-size:13px; font-weight:300; margin-top:6px;">
            Compare three model portfolios (GMV, Tangency and ERC) built on a global ETF universe.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# 1. User parameters (on-page, not in the sidebar)
# -------------------------------------------------
st.subheader("Parameters")

param_col, _ = st.columns([1, 3])
with param_col:
    # Tickers + noms complets des ETF
    universe = ["EEM", "EFA", "GLD", "HYG", "LQD", "QQQ", "SPY", "TLT"]
    etf_names = {
        "EEM": "iShares MSCI Emerging Markets ETF",
        "EFA": "iShares MSCI EAFE (Developed ex-US)",
        "GLD": "SPDR Gold Shares",
        "HYG": "iShares iBoxx High Yield Corporate Bond",
        "LQD": "iShares iBoxx Investment Grade Corporate Bond",
        "QQQ": "Invesco QQQ (Nasdaq-100)",
        "SPY": "SPDR S&P 500 ETF",
        "TLT": "iShares 20+ Year Treasury Bond",
    }
    default_selection = ["EFA", "HYG", "LQD", "SPY"]

    st.markdown("**Select ETFs**")

    # Toggles verticaux : un ETF par ligne, avec nom complet
    tickers: list[str] = []
    for ticker in universe:
        label = f"{ticker} – {etf_names.get(ticker, '')}"
        selected = st.toggle(
            label,
            value=(ticker in default_selection),
            key=f"etf_{ticker}",
        )
        if selected:
            tickers.append(ticker)

    # --- FIXED START DATE IN THE STRATEGY ---
    start_date = date(2010, 1, 1)
    st.caption(
        "Historical window fixed in the strategy: data used from **2010-01-01** "
        "to the latest available date."
    )

    # --- RISK-FREE RATE: DEFAULT CHOSEN BY VEDOINVEST, ADJUSTABLE IN ADVANCED MODE ---
    default_rf = 0.01  # 1% annual risk-free rate
    rf_annual = default_rf

    with st.expander("Advanced – Risk-free rate (optional)"):
        rf_annual = st.slider(
            "Risk-free rate (annual, in decimal)",
            min_value=0.0,
            max_value=0.05,
            value=default_rf,
            step=0.005,
            help=(
                "Annual risk-free rate used in the Tangency portfolio optimisation "
                "(e.g. yield of a high-grade government bond). "
                "Vedoinvest uses 1% by default."
            ),
        )

    st.caption(
        "By default, Vedoinvest uses a **1% annual risk-free rate**. "
        "Advanced users can adjust this assumption in the *Advanced – Risk-free rate* section."
    )

    no_short = st.checkbox("Forbid short-selling (w ≥ 0)", value=True)

    run = st.button("Run optimisation")

st.write("")  # small spacer

# If the user hasn't launched the computation yet
if not tickers:
    st.info("Please select at least one ETF to start the optimisation.")
    st.stop()

if not run:
    st.info("Set your parameters above and click **Run optimisation**.")
    st.stop()

# -------------------------------------------------
# 2. Download data and compute μ, Σ
# -------------------------------------------------
with st.spinner("Downloading data and computing statistics..."):
    prices = load_prices(tickers, start=str(start_date))
    returns = to_returns(prices)
    mu, Sigma, cols = mean_cov(returns)

    mu = mu.loc[tickers]
    Sigma = Sigma.loc[tickers, tickers]

if prices.empty:
    st.error("No price data was returned. Try another ETF set.")
    st.stop()

st.success("Data downloaded and portfolio statistics calculated ✔️")

# -------------------------------------------------
# 3. Data overview
# -------------------------------------------------
st.subheader("Data overview")

# --------- 3.1 : Data preview ----------
st.markdown("### 📊 Data preview")

st.markdown("**Last observations of prices**")
st.dataframe(prices.tail().round(2), use_container_width=True)

# Annualised mean returns in %
mu_annual_pct = ((1 + mu) ** 252 - 1) * 100.0
st.markdown("**Annualised mean returns (approximate, %)**")
st.dataframe(
    mu_annual_pct.to_frame(name="mu_annual_%").round(2),
    use_container_width=True,
)

# -------------------------------------------------
# 4. Optimisation of the three portfolios
# -------------------------------------------------
mu_vec = mu.values.astype(float)
Sigma_mat = Sigma.values.astype(float)

rf_daily = rf_annual / 252.0
mu_ann = mu_vec * 252.0
Sigma_ann = Sigma_mat * 252.0

try:
    short = not no_short

    w_gmv = gmv_weights(Sigma_mat, short=short)
    w_tan = tangency_weights(mu_vec, Sigma_mat, rf=rf_daily, short=short)
    w_erc = erc_weights(Sigma_mat)

except Exception as e:
    st.error(f"An optimisation error occurred: **{e}**")
    st.stop()

w_gmv = np.array(w_gmv, dtype=float).flatten()
w_tan = np.array(w_tan, dtype=float).flatten()
w_erc = np.array(w_erc, dtype=float).flatten()

weights_df = pd.DataFrame(
    {
        "GMV": w_gmv,
        "Tangency": w_tan,
        "ERC (Risk Parity)": w_erc,
    },
    index=tickers,
)

# -------------------------------------------------
# 5. Weights display
# -------------------------------------------------
st.markdown("### 📈 Portfolio weights")

st.dataframe(weights_df.round(4), use_container_width=True)

st.markdown("#### Visual comparison")
chart_df = weights_df.copy()
chart_df.index.name = "Ticker"
st.bar_chart(chart_df, use_container_width=True)

# -------------------------------------------------
# 6. Annualised performance statistics
# -------------------------------------------------
st.markdown("### 📐 Performance summary")

stats_gmv = portfolio_stats(w_gmv, mu_ann, Sigma_ann, rf=rf_annual)
stats_tan = portfolio_stats(w_tan, mu_ann, Sigma_ann, rf=rf_annual)
stats_erc = portfolio_stats(w_erc, mu_ann, Sigma_ann, rf=rf_annual)

# Tableau des 3 portefeuilles – return & vol en %
stats_df = pd.DataFrame.from_dict(
    {
        "GMV": stats_gmv,
        "Tangency": stats_tan,
        "ERC": stats_erc,
    },
    orient="index",
)

stats_table = stats_df.copy()
stats_table["return_%"] = (stats_table["return"] * 100.0).round(2)
stats_table["vol_%"] = (stats_table["vol"] * 100.0).round(2)

# On garde la colonne sharpe telle quelle
stats_table = stats_table[["return_%", "vol_%", "sharpe"]]

st.dataframe(stats_table, use_container_width=True)

# ---- Cards "AmberQuant style" pour le Tangency portfolio ----
# estimation de la durée de l'échantillon en années
n_days = returns.shape[0]
years = n_days / 252.0 if n_days > 0 else 0.0

tan_return_ann = stats_tan["return"]          # déjà annualisé (décimal)
tan_vol_ann = stats_tan["vol"]               # annualisée
tan_sharpe = stats_tan["sharpe"]
# Cumulative return sur la période d'échantillon
tan_cum_return = (1 + tan_return_ann) ** years - 1 if years > 0 else 0.0

# Un peu de CSS pour de jolies cards
st.markdown(
    """
    <style>
    .perf-cards-row {
        display: flex;
        gap: 1rem;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
    .perf-card {
        flex: 1;
        background: white;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        border: 1px solid #E5E7EB;
    }
    .perf-card-label {
        font-size: 0.78rem;
        font-weight: 500;
        color: #6B7280;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .perf-card-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: #111827;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="perf-cards-row">
        <div class="perf-card">
            <div class="perf-card-label">Expected annual return (Tangency)</div>
            <div class="perf-card-value">{tan_return_ann*100:.2f}%</div>
        </div>
        <div class="perf-card">
            <div class="perf-card-label">Annual volatility (Tangency)</div>
            <div class="perf-card-value">{tan_vol_ann*100:.2f}%</div>
        </div>
        <div class="perf-card">
            <div class="perf-card-label">Sharpe ratio (Tangency)</div>
            <div class="perf-card-value">{tan_sharpe:.2f}</div>
        </div>
        <div class="perf-card">
            <div class="perf-card-label">Cumulative return over sample</div>
            <div class="perf-card-value">{tan_cum_return*100:.2f}%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Note: annualisation is approximate (×252). Results are indicative only and do not "
    "constitute investment advice."
)
