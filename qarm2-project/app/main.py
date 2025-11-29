import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# =============================
# GLOBAL PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Vedoinvest",
    page_icon="📈",
    layout="wide"
)

# =============================
# CUSTOM CSS (Amberquant-like)
# =============================
st.markdown("""
<style>

footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background-color: #F9FAFB;
}

/* Top navigation bar */
.navbar {
    display: flex;
    justify-content: center;
    gap: 40px;
    padding: 20px 0;
    border-bottom: 1px solid #E5E7EB;
    background-color: white;
}

.navitem {
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.95rem;
    color: #374151;
    text-decoration: none;
}

.navitem:hover {
    background-color: #E5E7EB;
}

.navitem-active {
    background-color: #111827;
    color: white !important;
}

/* Card style */
.vedocard {
    background-color: white;
    padding: 1rem 1.3rem;
    border-radius: 0.6rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)


# =============================
# ROUTER (navigation internal)
# =============================

if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate(page):
    st.session_state.page = page

# =============================
# NAVBAR
# =============================
pages = ["Home", "Portfolio", "Methodology", "About", "Contact"]

st.markdown('<div class="navbar">', unsafe_allow_html=True)
for p in pages:
    active = "navitem-active" if st.session_state.page == p else "navitem"
    st.markdown(
        f'<a class="{active}" href="#" onclick="window.location.reload();" >{p}</a>',
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# =============================
# PAGE CONTENT FUNCTIONS
# =============================

def page_home():
    st.title("Welcome to Vedoinvest")
    st.write("""
    Vedoinvest is a quantitative portfolio lab focused on global ETFs.
    This platform demonstrates three portfolio construction models:
    **Global Minimum Variance (GMV)**, **Tangency (max Sharpe)** and
    **Equal Risk Contribution (ERC)**.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="vedocard"><b>Global Minimum Variance</b><br><br>Minimises overall volatility.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="vedocard"><b>Tangency Portfolio</b><br><br>Maximises the Sharpe ratio.</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="vedocard"><b>Equal Risk Contribution</b><br><br>Equalises risk across assets.</div>', unsafe_allow_html=True)


def page_methodology():
    st.title("Methodology")
    st.write("""
    ### 1. Global Minimum Variance (GMV)
    - Minimises portfolio variance.
    - Convex optimisation.

    ### 2. Tangency Portfolio
    - Maximises Sharpe ratio.
    - DCP-friendly formulation.

    ### 3. Equal Risk Contribution (ERC)
    - Each asset contributes equally to total risk.
    """)


def page_about():
    st.title("About Vedoinvest")
    st.write("""
    Vedoinvest is a boutique quantitative investment concept.
    Built by **Elvedin Muminovic**.
    """)


def page_contact():
    st.title("Contact")
    name = st.text_input("Name")
    message = st.text_area("Message")
    if st.button("Send"):
        st.success("Message received (demo only).")


def page_portfolio():
    st.title("Portfolio Optimisation")

    col1, col2 = st.columns([1.2, 3])

    with col1:
        st.subheader("Parameters")
        universe = ["EEM","EFA","GLD","HYG","LQD","QQQ","SPY","TLT"]

        tickers = st.multiselect("Select ETFs", universe, ["EFA", "HYG", "LQD", "SPY"])
        start_date = st.date_input("Start date", value=date(2019,1,1))
        rf = st.slider("Risk-free rate (%)", 0.0, 5.0, 1.0) / 100
        no_short = st.checkbox("Forbid short selling", value=True)
        run = st.button("Run optimisation")

    with col2:
        if not run:
            st.info("Set parameters and click **Run optimisation**.")
            return
        
        st.success("Data downloaded and portfolio statistics calculated ✔️")
        st.write("### (Demo results shown — connect backend here)")


# =============================
# RENDER SELECTED PAGE
# =============================

if st.session_state.page == "Home":
    page_home()

elif st.session_state.page == "Portfolio":
    page_portfolio()

elif st.session_state.page == "Methodology":
    page_methodology()

elif st.session_state.page == "About":
    page_about()

elif st.session_state.page == "Contact":
    page_contact()
