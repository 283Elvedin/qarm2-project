# app/pages/Methodology.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from layout import set_page_config, render_header

# --- Config page ---
set_page_config("Vedoinvest – Methodology")
render_header(active_page="Methodology")


# ---------- GLOBAL PAGE STYLE ----------
st.markdown("""
<style>
.method-title {
    font-size: 2.1rem;
    font-weight: 700;
    padding-top: 0.5rem;
    color: #111827;
}

.section-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.7rem;
    box-shadow: 0 8px 22px rgba(0,0,0,0.06);
    margin-bottom: 1.4rem;
}

.section-header {
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 0.3rem;
    color: #0F172A;
}

.highlight {
    background: linear-gradient(90deg, #F97316, #F59E0B);
    color: white;
    padding: 1.5rem;
    border-radius: 14px;
    font-size: 1.45rem;
    font-weight: 600;
    margin-bottom: 1.4rem;
    text-align: center;
}

.info-bullet {
    background: #F8FAFC;
    padding: 0.8rem 1rem;
    border-radius: 10px;
    border-left: 4px solid #2563EB;
    margin-bottom: 0.6rem;
}
</style>
""", unsafe_allow_html=True)

# -------- Banner (bleu) --------
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg, #0d6efd, #1a75ff);
        padding: 28px 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        text-align:center;
        color: white;
        font-weight: 600;
        font-size: 20px;
    ">
        🔷 Methodology – How Vedoinvest Works  
        <div style="font-size:13px; font-weight:300; margin-top:6px;">
            A transparent, quantitative framework for building ETF portfolios.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------- INTRO ----------
st.markdown("""
<div class="section-card">
    <div class="section-header">Overview</div>
    Vedoinvest follows a **fully systematic** and **transparent** investment methodology.
    Everything is calculated directly from data — no discretion, no subjective choices.
    <br><br>
    This page explains *exactly* how portfolios are built so clients understand the underlying logic.
</div>
""", unsafe_allow_html=True)


# ---------- 1. DATA ----------
st.markdown("""
<div class="section-card">
    <div class="section-header">1. Data & Frequency</div>

<div class="info-bullet">• Data source: <strong>Yahoo Finance</strong> via the <code>yfinance</code> Python package</div>
<div class="info-bullet">• Instruments: Global ETF universe (equity, bonds, gold)</div>
<div class="info-bullet">• Frequency: <strong>Daily</strong> adjusted close prices</div>
<div class="info-bullet">• Historical window: Fixed at <strong>2010-01-01</strong> to the most recent data</div>

</div>
""", unsafe_allow_html=True)



# ---------- 2. RISK & RETURN ----------
st.markdown("""
<div class="section-card">
    <div class="section-header">2. Risk & Return Estimates</div>

For the selected set of ETFs, Vedoinvest computes:

<div class="info-bullet">
    • <strong>Mean return vector</strong> — estimated from daily log returns
</div>

<div class="info-bullet">
    • <strong>Covariance matrix</strong> — capturing co-movement and risk
</div>

These are the standard statistical inputs for **modern portfolio theory**.
</div>
""", unsafe_allow_html=True)



# ---------- 3. OPTIMISATION MODELS ----------
st.markdown("""
<div class="section-card">
    <div class="section-header">3. Portfolio Models Optimised</div>

### 🔹 Global Minimum Variance (GMV)
The portfolio with the **lowest total volatility**.
- Objective: minimize  
- Constraints:  
  - Fully invested: 
  - Optionally long-only  

---

### 🔹 Tangency Portfolio (Maximum Sharpe)
Maximizes the ratio of excess returns to risk.
- Objective: maximize  
- Constraints:  
  - Fully invested  
  - Long-only or unconstrained  
  - Solved via convex optimisation (CVXPY)

---

### 🔹 Equal Risk Contribution (ERC)
Ensures **each ETF contributes equally to portfolio risk**.  
- Based on nonlinear optimisation (SLSQP)  
- Balances diversification + stability

</div>
""", unsafe_allow_html=True)



# ---------- 4. LIMITATIONS ----------
st.markdown("""
<div class="section-card">
    <div class="section-header">4. Limitations & Disclaimer</div>

<div class="info-bullet">• Past performance does not guarantee future returns</div>
<div class="info-bullet">• Results depend entirely on historical data quality</div>
<div class="info-bullet">• Transaction costs, taxes and liquidity are not included</div>
<div class="info-bullet">• The platform is for <strong>education</strong> and <strong>illustration</strong> only</div>

</div>
""", unsafe_allow_html=True)

st.caption("© Vedoinvest — Transparent Quantitative Portfolio Construction")
