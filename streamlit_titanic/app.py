import streamlit as st
from theme import inject_custom_css
from model_utils import load_data

st.set_page_config(
    page_title="Titanic — Exploration",
    page_icon="🚢",
    layout="wide",
)
inject_custom_css()

st.title("🚢 Survie sur le Titanic")
st.caption(
    "Exploration du jeu de données Titanic (891 passagers) et entraînement "
    "de modèles de classification binaire pour prédire la survie."
)

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Le fichier `data/train.csv` est introuvable. "
        "Place le dataset Titanic dans le dossier `data/` du projet."
    )
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Passagers", f"{len(df):,}".replace(",", " "))
col2.metric("Taux de survie", f"{df['Survived'].mean() * 100:.0f} %")
col3.metric("Âge moyen", f"{df['Age'].mean():.0f} ans")
col4.metric("Tarif moyen", f"{df['Fare'].mean():.0f} £")

st.divider()

st.write("### Aperçu des données")
st.dataframe(df.head(10), use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.write("### Dimensions")
    st.write(f"{df.shape[0]} lignes × {df.shape[1]} colonnes")
    st.write("### Statistiques descriptives")
    st.dataframe(df.describe(), use_container_width=True)

with col_b:
    st.write("### Valeurs manquantes")
    na_counts = df.isna().sum()
    na_counts = na_counts[na_counts > 0].sort_values(ascending=False)
    if na_counts.empty:
        st.success("Aucune valeur manquante.")
    else:
        st.dataframe(na_counts.rename("Valeurs manquantes"), use_container_width=True)
        st.caption(
            "La colonne `Cabin` est très incomplète et `Age` l'est partiellement — "
            "ces deux variables sont gérées différemment lors de la modélisation."
        )
