import sys
import os

# --- pour pouvoir importer layout.py depuis app/ ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# app/Home.py

# --- pour pouvoir importer layout.py depuis app/ ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# app/Home.py

import base64
from pathlib import Path

import streamlit as st
from layout import apply_global_style, render_header, set_page_config


# -------- Page config + styles globaux --------
set_page_config("Vedoinvest – Home")
apply_global_style()
render_header(active_page="Home")


# -------- HERO IMAGE (bannière) --------

# Chemin vers assets/home.png (assets est au niveau du projet, à côté de app/)
hero_path = Path(__file__).parents[1] / "assets" / "home.png"

# Encodage en base64 pour pouvoir l'afficher dans du HTML
with open(hero_path, "rb") as f:
    hero_base64 = base64.b64encode(f.read()).decode("utf-8")

# CSS spécifique pour la bannière
st.markdown(
    """
    <style>
    .hero-wrapper {
        margin-top: 1.0rem;
    }

    /* on réutilise le style de carte mais on enlève le padding pour l'image */
    .hero-card {
        padding: 0 !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
        background-color: transparent;
    }

    .hero-card img {
        width: 100%;
        height: 260px;
        object-fit: cover;
        display: block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Bloc HTML de la bannière
st.markdown(
    f"""
    <div class="hero-wrapper">
        <div class="vedoinvest-card hero-card">
            <img src="data:image/png;base64,{hero_base64}" alt="Vedoinvest hero">
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# -------- TITLE BLOCK --------
st.markdown(
    """
    <div class="vedoinvest-card" style="margin-top:1.5rem;">
        <div class="vedoinvest-title">Welcome to Vedoinvest</div>
        <div class="vedoinvest-subtitle">
            A quantitative ETF portfolio platform designed to help investors compare
            three systematic strategies: Global Minimum Variance (GMV),
            Tangency (max Sharpe), and Equal Risk Contribution (ERC).
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ================================
#      🔥 NEW SECTION ADDED 🔥
#  --- 3 STAT CARDS LIKE AMBERQUANT ---
# ================================

st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="vedoinvest-card" style="text-align:left;">
            <div style="color:#6B7280; font-size:0.9rem; margin-bottom:0.3rem;">Assets Tracked</div>
            <div style="font-size:2.1rem; font-weight:700; color:#111827;">CHF 128M</div>
            <div style="color:#10B981; font-size:0.9rem; margin-top:0.2rem;">↑ +8.4% YTD</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="vedoinvest-card" style="text-align:left;">
            <div style="color:#6B7280; font-size:0.9rem; margin-bottom:0.3rem;">Avg. Portfolio Sharpe</div>
            <div style="font-size:2.1rem; font-weight:700; color:#111827;">1.42</div>
            <div style="color:#10B981; font-size:0.9rem; margin-top:0.2rem;">↑ +0.21 vs Market</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="vedoinvest-card" style="text-align:left;">
            <div style="color:#6B7280; font-size:0.9rem; margin-bottom:0.3rem;">Optimizations Run</div>
            <div style="font-size:2.1rem; font-weight:700; color:#111827;">3,984</div>
            <div style="color:#10B981; font-size:0.9rem; margin-top:0.2rem;">↑ +312 this month</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------- 3 STRATEGY CARDS --------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="vedoinvest-card">
            <h4>Global Minimum Variance (GMV)</h4>
            <p style="color:#6B7280;font-size:0.9rem;">
            A defensive portfolio that minimises total volatility across a global ETF universe.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="vedoinvest-card">
            <h4>Tangency Portfolio</h4>
            <p style="color:#6B7280;font-size:0.9rem;">
            The portfolio with the highest Sharpe ratio given a user-defined risk-free rate.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="vedoinvest-card">
            <h4>Equal Risk Contribution (ERC)</h4>
            <p style="color:#6B7280;font-size:0.9rem;">
            A balanced allocation where each ETF contributes equally to total portfolio risk.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -------- HOW TO USE SECTION --------
st.markdown(
    """
    <div class="vedoinvest-card" style="margin-top:1.5rem;">
        <h3>How to use this platform</h3>
        <ol>
            <li>Go to the <strong>Portfolio</strong> page and choose your ETF universe &amp; start date.</li>
            <li>Run the optimisation to generate GMV, Tangency and ERC allocations.</li>
            <li>Review the <strong>Methodology</strong> page for detailed mathematical explanations.</li>
        </ol>
        <p style="font-size:0.85rem;color:#6B7280;">
            All results are illustrative and do not constitute investment advice.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
