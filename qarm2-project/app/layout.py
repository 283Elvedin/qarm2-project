import streamlit as st
from pathlib import Path

# --- Couleurs globales Vedoinvest ---
PRIMARY_COLOR = "#111827"      # dark grey / blue
ACCENT_COLOR = "#F97316"       # orange accent
BG_LIGHT = "#F9FAFB"           # light background


def set_page_config(page_title: str) -> None:
    """
    À appeler tout en haut de chaque page.
    """
    st.set_page_config(
        page_title=page_title,
        page_icon="📈",
        layout="wide",
    )
    apply_global_style()


def apply_global_style() -> None:
    """
    CSS global : supprime header Streamlit, footer et sidebar par défaut
    + style un peu plus pro.
    """
    st.markdown(
        f"""
        <style>
        /* Cacher le footer "Made with Streamlit" */
        footer {{visibility: hidden;}}

        /* Cacher le header par défaut */
        header {{visibility: hidden;}}

        /* Cacher complètement la sidebar Streamlit (menu vertical) */
        [data-testid="stSidebar"] {{
            display: none;
        }}

        /* Fond général */
        .stApp {{
            background-color: {BG_LIGHT};
        }}

        /* Container principal un peu plus large et centré */
        .block-container {{
            padding-top: 1.5rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }}

        /* Cartes Vedoinvest */
        .vedoinvest-card {{
            background-color: #FFFFFF;
            padding: 1.2rem 1.4rem;
            border-radius: 0.75rem;
            border: 1px solid #E5E7EB;
            box-shadow: 0 4px 10px rgba(15, 23, 42, 0.04);
        }}

        .vedoinvest-title {{
            font-size: 2.0rem;
            font-weight: 800;
            color: {PRIMARY_COLOR};
            margin-bottom: 0.25rem;
        }}

        .vedoinvest-subtitle {{
            font-size: 0.95rem;
            color: #6B7280;
        }}

        /* Boutons Streamlit */
        .stButton>button {{
            border-radius: 999px;
            border: 1px solid {PRIMARY_COLOR};
            background-color: {PRIMARY_COLOR};
            color: white;
            padding: 0.35rem 1.0rem;
            font-size: 0.9rem;
        }}
        .stButton>button:hover {{
            background-color: #030712;
            border-color: #030712;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header(active_page: str) -> None:
    """
    Barre tout en haut : logo à gauche + navigation horizontale.
    On utilise st.page_link -> navigation dans le MÊME onglet.
    `active_page` est juste pour le style léger (gras).
    """
    from textwrap import dedent

    col_left, col_right = st.columns([1.5, 3])

    # --- Logo + titre ---
    with col_left:
        logo_path = Path("assets/logo.png")
        if logo_path.exists():
            st.image(str(logo_path), width=120)
        

    # --- Menu horizontal avec page_link (même onglet) ---
    with col_right:
        nav_cols = st.columns(5)

        def label(txt: str) -> str:
            style = "font-weight:600;" if txt == active_page else "font-weight:400;"
            return f"<span style='{style}'>{txt}</span>"

        with nav_cols[0]:
            st.page_link("Home.py", label="Home", icon="🏠")
        with nav_cols[1]:
            st.page_link("pages/Portfolio.py", label="Portfolio", icon="📊")
        with nav_cols[2]:
            st.page_link("pages/Methodology.py", label="Methodology", icon="📐")
        with nav_cols[3]:
            st.page_link("pages/About.py", label="About", icon="👤")
        with nav_cols[4]:
            st.page_link("pages/Contact.py", label="Contact", icon="✉️")

    st.markdown("---")
