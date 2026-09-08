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
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

train = pd.read_csv(
    os.path.join(BASE_DIR, "spaceship_train.csv")
)

test = pd.read_csv(
    os.path.join(BASE_DIR, "spaceship_test.csv")
)

st.success("Données chargées avec succès !")

col1, col2 = st.columns(2)

with col1:
    st.metric("Passagers connus", f"{len(train):,}")

with col2:
    st.metric("Passagers à prédire", f"{len(test):,}")

st.markdown("### 👀 Aperçu des données")

st.dataframe(train.head(), use_container_width=True)

st.markdown("### 📊 Exploration des données")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Informations générales")
    st.write(f"**Nombre de lignes :** {train.shape[0]:,}")
    st.write(f"**Nombre de colonnes :** {train.shape[1]}")

with col2:
    st.markdown("#### Variable cible")
    transported_counts = train["Transported"].value_counts()
    transported_pct = train["Transported"].value_counts(normalize=True) * 100

    st.write(
        f"**Transported = True :** "
        f"{transported_counts.get(True, 0):,} "
        f"({transported_pct.get(True, 0):.1f} %)"
    )

    st.write(
        f"**Transported = False :** "
        f"{transported_counts.get(False, 0):,} "
        f"({transported_pct.get(False, 0):.1f} %)"
    )

st.markdown("#### 🔎 Valeurs manquantes")

missing = (
    train.isna()
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

missing.columns = ["Variable", "Valeurs manquantes (%)"]

st.dataframe(
    missing,
    use_container_width=True,
    hide_index=True
)

st.markdown("#### 🧾 Types de variables")

info = pd.DataFrame({
    "Variable": train.columns,
    "Type": train.dtypes.astype(str).values,
    "Valeurs uniques": [
        train[col].nunique(dropna=True)
        for col in train.columns
    ]
})

st.dataframe(
    info,
    use_container_width=True,
    hide_index=True
)

