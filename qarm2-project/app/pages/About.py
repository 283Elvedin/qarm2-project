# app/pages/About.py

import sys
import os
from pathlib import Path

import streamlit as st

# Pour importer layout.py (qui est dans app/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from layout import set_page_config, render_header

# -------- Config de la page --------
set_page_config("Vedoinvest – About")
render_header(active_page="About")

# -------- Layout principal : photo + texte --------
left_col, right_col = st.columns([1, 2])

# --- PHOTO À GAUCHE (taille réduite) ---
with left_col:
    # Fichier situé à la racine du projet : qarm2-project/assets/Elvedin.jpg
    img_path = Path(__file__).parents[2] / "assets" / "Elvedin.jpg"  # ⚠️ extension .jpg

    if img_path.exists():
        st.image(
            str(img_path),
            caption="Elvedin Muminovic",
            width=260,          # taille de la photo (en pixels)
        )
    else:
        st.error(f"Image not found at {img_path}")

# --- TEXTE À DROITE ---
with right_col:
    st.markdown("## About Vedoinvest")

    st.markdown(
        """
Vedoinvest is a boutique, single-manager quantitative investment concept focused on
transparent **ETF portfolio construction**.  
The idea is to take tools used in professional asset management and make them accessible
through a clear, interactive web interface.
"""
    )

    st.markdown("### Who is behind Vedoinvest?")

    st.markdown(
        """
**Elvedin Muminovic**  
*Portfolio manager & developer of the platform*

- Focus on **quantitative investing** and **systematic asset allocation**  
- Designs the **investment methodology** and implements the  
  **portfolio optimisation engine** (Python + Streamlit)  
- Combines academic rigour with a **client-friendly user experience**
"""
    )

st.markdown("---")

# -------- Détails sur la plateforme --------
st.markdown("### What this platform aims to deliver")

st.markdown(
    """
- Turn classic portfolio theory (GMV, Tangency, Risk Parity) into an **intuitive client experience**  
- Show how different optimisation rules allocate capital across the same ETF universe  
- Promote **transparent methodology**, clean documentation and a **professional interface**
"""
)

st.markdown("### Tools & technologies")

st.markdown(
    """
- **Python** for data handling and optimisation  
- **Pandas / NumPy** for data manipulation  
- **cvxpy / scipy** for optimisation routines  
- **yfinance** for historical ETF data  
- **Streamlit** for the web front-end  
"""
)

st.caption("All results are illustrative only and do not constitute investment advice.")
