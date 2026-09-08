import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Prédiction — London Fire Brigade",
    page_icon="⏱️",
    layout="wide",
)

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "firefighter_london.csv")
)

# ============================================================
# VÉRIFICATION DES COLONNES
# ============================================================

st.title("⏱️ Prédiction du temps d'arrivée")

st.write("### Colonnes disponibles dans le dataset")

st.write(df.columns.tolist())
