import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Energy Efficiency — Machine Learning",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 Energy Efficiency")
st.subheader("Classification des bâtiments selon leurs charges énergétiques")

st.markdown("""
### 🎯 Objectif

Ce projet analyse l'efficacité énergétique de bâtiments résidentiels
à partir de leurs caractéristiques architecturales.

L'objectif est de construire un modèle de Machine Learning capable de
classer les bâtiments selon leur niveau de **charges énergétiques
totales**, calculées à partir des charges de chauffage et de
climatisation.
""")

st.markdown("### 📊 Le jeu de données")

st.markdown("""
Le dataset contient **768 configurations de bâtiments** et
**8 variables explicatives** décrivant notamment :

- la compacité du bâtiment ;
- la surface ;
- la surface des murs ;
- la surface du toit ;
- la hauteur ;
- l'orientation ;
- la surface vitrée ;
- la distribution de la surface vitrée.

Les deux variables énergétiques sont :

- 🔥 `heating_load` — charge de chauffage ;
- ❄️ `cooling_load` — charge de climatisation.

Les données proviennent du dataset **Energy Efficiency** de l'UCI
Machine Learning Repository.
""")

st.markdown("### 🧠 Approche Machine Learning")

st.markdown("""
Les charges de chauffage et de climatisation sont d'abord additionnées
afin de créer une variable **`total_charges`**.

Les bâtiments sont ensuite répartis en **4 classes** selon les
quartiles de leurs charges énergétiques totales.

Trois algorithmes sont comparés :

- **K-Nearest Neighbors (KNN)**
- **Support Vector Machine (SVM)**
- **Random Forest**

Les hyperparamètres sont sélectionnés avec une **validation croisée
(GridSearchCV)**.
""")

st.markdown("---")

st.markdown("### 🏆 Résultat")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Bâtiments", "768")

with col2:
    st.metric("Classes énergétiques", "4")

with col3:
    st.metric("Meilleur modèle", "Random Forest")

st.info(
    "🏆 Le Random Forest obtient une accuracy de **96,10 %** "
    "sur l'ensemble de test dans l'étude."
)
