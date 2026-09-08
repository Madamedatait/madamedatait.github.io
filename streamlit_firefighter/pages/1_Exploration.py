import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Exploration — London Fire Brigade",
    page_icon="🔎",
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
# INTRODUCTION
# ============================================================

st.title("🚒 London Fire Brigade")

st.subheader(
    "Pipeline de Machine Learning pour prédire le temps d'arrivée des secours"
)

st.markdown("""
### 🎯 Objectif

Ce projet s'intéresse aux interventions du **London Fire Brigade** et
vise à construire un modèle de Machine Learning capable de prédire le
**temps d'arrivée des secours**.

L'analyse combine des informations relatives aux interventions et aux
mobilisations des véhicules afin d'identifier les caractéristiques
pouvant influencer le temps nécessaire pour atteindre le lieu de
l'intervention.
""")

st.markdown("""
### 📊 Le jeu de données

Le jeu de données utilisé rassemble des informations sur les
interventions des services d'incendie à Londres.

Chaque observation correspond à une **mobilisation d'un véhicule**
associée à une intervention.

Les données contiennent notamment des informations concernant :

- 📅 la date et l'heure de l'intervention ;
- 📍 la localisation de l'intervention ;
- 🏢 le type de propriété concernée ;
- 🚒 le nombre de véhicules mobilisés ;
- 🚉 la station ayant déployé le véhicule ;
- ⏱️ les différents temps associés à la mobilisation.
""")

st.markdown("""
### 🎯 Variable cible

La variable que nous cherchons à prédire est :

**`AttendanceTimeSeconds`**

Elle correspond au **temps d'arrivée sur les lieux**, exprimé en
secondes.
""")

st.markdown("""
### 🧠 Approche Machine Learning

Le projet suit plusieurs étapes :

1. 🔎 Exploration et audit des données
2. 🛠️ Préparation et nettoyage des données
3. ⚙️ Feature engineering
4. 🔄 Construction d'une Pipeline scikit-learn
5. 🤖 Entraînement et comparaison des modèles
6. 📊 Évaluation des performances
7. ⏱️ Prédiction du temps d'arrivée
""")

st.markdown("---")

# ============================================================
# AUDIT DES DONNÉES
# ============================================================

st.header("🔎 Exploration des données")

st.subheader("Audit du jeu de données")

st.success("✅ Données chargées avec succès !")

# ============================================================
# INDICATEURS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚒 Mobilisations",
        f"{df.shape[0]:,}"
    )

with col2:
    st.metric(
        "📊 Variables",
        f"{df.shape[1]}"
    )

with col3:
    st.metric(
        "⏱️ Temps moyen",
        f"{df['AttendanceTimeSeconds'].mean():.1f} s"
    )

# ============================================================
# APERÇU
# ============================================================

st.subheader("👀 Aperçu des données")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INFORMATIONS GÉNÉRALES
# ============================================================

st.subheader("📋 Informations générales")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Nombre de lignes :** {df.shape[0]:,}")
    st.write(f"**Nombre de colonnes :** {df.shape[1]}")

with col2:
    st.write(
        f"**Nombre d'interventions :** "
        f"{df['IncidentNumber'].nunique():,}"
    )

# ============================================================
# VALEURS MANQUANTES
# ============================================================

st.subheader("🔎 Valeurs manquantes")

missing = df.isna().sum().to_frame(
    "Nombre de valeurs manquantes"
)

missing["Pourcentage (%)"] = (
    missing["Nombre de valeurs manquantes"]
    / len(df)
    * 100
)

missing = missing.sort_values(
    "Nombre de valeurs manquantes",
    ascending=False
)

st.dataframe(
    missing,
    use_container_width=True
)

# ============================================================
# TYPES DE VARIABLES
# ============================================================

st.subheader("🧾 Types de variables")

info = pd.DataFrame({
    "Variable": df.columns,
    "Type": df.dtypes.astype(str).values,
    "Valeurs uniques": [
        df[col].nunique(dropna=True)
        for col in df.columns
    ]
})

st.dataframe(
    info,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# STATISTIQUES DESCRIPTIVES
# ============================================================

st.subheader("📈 Statistiques descriptives")

st.dataframe(
    df.describe().T,
    use_container_width=True
)
