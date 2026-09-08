import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Spaceship Titanic — Machine Learning",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Spaceship Titanic")
st.subheader("Prédiction des passagers transportés vers une autre dimension")

st.markdown("""
### 🎯 Objectif

Le Spaceship Titanic a perdu une partie de ses passagers lors d'une
collision avec une anomalie spatio-temporelle.

L'objectif est de construire un modèle de Machine Learning capable de
prédire quels passagers ont été **Transported** vers une autre dimension.
""")

# Chargement des données
train = pd.read_csv("spaceship_train.csv")
test = pd.read_csv("spaceship_test.csv")

st.success("Données chargées avec succès !")

col1, col2 = st.columns(2)

with col1:
    st.metric("Passagers connus", f"{len(train):,}")

with col2:
    st.metric("Passagers à prédire", f"{len(test):,}")

st.markdown("### 👀 Aperçu des données")

st.dataframe(train.head(), use_container_width=True)
