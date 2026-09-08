import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(
    page_title="Energy Efficiency — Exploration",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Exploration des données")
st.subheader("Audit du jeu de données Energy Efficiency")

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "ENB_data.xlsx"),
    sep=";"
)

st.success("Données chargées avec succès !")

# ============================================================
# INDICATEURS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🏢 Bâtiments", f"{df.shape[0]:,}")

with col2:
    st.metric("📊 Variables", df.shape[1])

with col3:
    st.metric(
        "🔥 Charge chauffage moyenne",
        f"{df['heating_load'].mean():.2f}"
    )

with col4:
    st.metric(
        "❄️ Charge climatisation moyenne",
        f"{df['cooling_load'].mean():.2f}"
    )

# ============================================================
# APERÇU
# ============================================================

st.markdown("## 👀 Aperçu des données")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# INFORMATIONS GÉNÉRALES
# ============================================================

st.markdown("## 📐 Informations générales")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Dimensions")
    st.write(f"**Nombre de lignes :** {df.shape[0]:,}")
    st.write(f"**Nombre de colonnes :** {df.shape[1]}")

with col2:
    st.markdown("### Valeurs manquantes")

    missing = df.isna().sum()

    if missing.sum() == 0:
        st.success("✅ Aucune valeur manquante.")
    else:
        missing_df = (
            missing[missing > 0]
            .sort_values(ascending=False)
            .reset_index()
        )

        missing_df.columns = [
            "Variable",
            "Valeurs manquantes"
        ]

        st.dataframe(
            missing_df,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# TYPES DES VARIABLES
# ============================================================

st.markdown("## 🧾 Types des variables")

info = pd.DataFrame({
    "Variable": df.columns,
    "Type": df.dtypes.astype(str).values,
    "Valeurs uniques": [
        df[col].nunique()
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

st.markdown("## 📊 Statistiques descriptives")

st.dataframe(
    df.describe().T,
    use_container_width=True
)

# ============================================================
# DISTRIBUTIONS
# ============================================================

st.markdown("## 📈 Distribution des variables")

variable = st.selectbox(
    "Sélectionnez une variable",
    df.columns
)

fig = px.histogram(
    df,
    x=variable,
    title=f"Distribution de {variable}",
    marginal="box"
)

fig.update_layout(
    xaxis_title=variable,
    yaxis_title="Nombre de bâtiments"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# VARIABLES CIBLES
# ============================================================

st.markdown("## 🔥❄️ Variables énergétiques")

col1, col2 = st.columns(2)

with col1:
    fig_heating = px.histogram(
        df,
        x="heating_load",
        title="Distribution des charges de chauffage",
        marginal="box"
    )

    st.plotly_chart(
        fig_heating,
        use_container_width=True
    )

with col2:
    fig_cooling = px.histogram(
        df,
        x="cooling_load",
        title="Distribution des charges de climatisation",
        marginal="box"
    )

    st.plotly_chart(
        fig_cooling,
        use_container_width=True
    )

st.markdown("""
### 💡 Première observation

Le jeu de données contient **768 bâtiments** décrits par
**8 caractéristiques architecturales** et **2 variables énergétiques**.

La suite de l'analyse permettra d'étudier les relations entre les
caractéristiques des bâtiments et leurs charges énergétiques.
""")
