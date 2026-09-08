import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Exploration — London Fire Brigade",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Exploration des données")

st.subheader("Audit du jeu de données London Fire Brigade")

# Chemin du fichier
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "firefighter_london.csv")
)

st.success("✅ Données chargées avec succès !")

# ============================================================
# INDICATEURS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚒 Mobilisations",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "📊 Variables",
        f"{df.shape[1]}"
    )

with col3:
    st.metric(
        "⏱️ Temps d'arrivée moyen",
        f"{df['AttendanceTimeSeconds'].mean():.1f} s"
    )

# ============================================================
# APERÇU
# ============================================================

st.markdown("### 👀 Aperçu des données")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INFORMATIONS GÉNÉRALES
# ============================================================

st.markdown("### 📋 Informations générales")

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

st.markdown("### 🔎 Valeurs manquantes")

missing = (
    df.isna()
    .sum()
    .to_frame("Nombre de valeurs manquantes")
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
# TYPES
# ============================================================

st.markdown("### 🧾 Types de variables")

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
# STATISTIQUES
# ============================================================

st.markdown("### 📈 Statistiques descriptives")

st.dataframe(
    df.describe().T,
    use_container_width=True
)
