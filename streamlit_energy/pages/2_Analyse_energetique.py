import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px

st.set_page_config(
    page_title="Energy Efficiency — Analyse énergétique",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Analyse énergétique")
st.subheader("Caractéristiques des bâtiments et charges énergétiques")

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "ENB_data.csv"),
    sep=";"
)

# ============================================================
# CRÉATION DES CHARGES TOTALES
# ============================================================

df["total_charges"] = (
    df["heating_load"] +
    df["cooling_load"]
)

# ============================================================
# CRÉATION DES 4 CLASSES
# ============================================================

q1 = df["total_charges"].quantile(0.25)
q2 = df["total_charges"].quantile(0.50)
q3 = df["total_charges"].quantile(0.75)

df["charges_classes"] = pd.cut(
    df["total_charges"],
    bins=[-np.inf, q1, q2, q3, np.inf],
    labels=[0, 1, 2, 3]
)

# ============================================================
# INDICATEURS
# ============================================================

st.markdown("## ⚡ Charges énergétiques")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🔥 Chauffage moyen",
        f"{df['heating_load'].mean():.2f}"
    )

with col2:
    st.metric(
        "❄️ Climatisation moyenne",
        f"{df['cooling_load'].mean():.2f}"
    )

with col3:
    st.metric(
        "⚡ Charge totale moyenne",
        f"{df['total_charges'].mean():.2f}"
    )

with col4:
    st.metric(
        "🏢 Bâtiments",
        f"{len(df):,}"
    )

# ============================================================
# CHAUFFAGE VS CLIMATISATION
# ============================================================

st.markdown("## 🔥 Chauffage vs ❄️ Climatisation")

fig = px.scatter(
    df,
    x="heating_load",
    y="cooling_load",
    hover_data=[
        "relative_compactness",
        "surface_area",
        "overall_height"
    ],
    labels={
        "heating_load": "Charge de chauffage",
        "cooling_load": "Charge de climatisation"
    },
    title="Relation entre les charges de chauffage et de climatisation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    f"Les charges de chauffage et de climatisation présentent une "
    f"forte corrélation positive ({df['heating_load'].corr(df['cooling_load']):.2f})."
)

# ============================================================
# CHARGES TOTALES
# ============================================================

st.markdown("## ⚡ Distribution des charges énergétiques totales")

fig_total = px.histogram(
    df,
    x="total_charges",
    nbins=30,
    marginal="box",
    labels={
        "total_charges": "Charges énergétiques totales"
    },
    title="Distribution des charges totales"
)

st.plotly_chart(
    fig_total,
    use_container_width=True
)

# ============================================================
# QUARTILES
# ============================================================

st.markdown("## 📐 Définition des classes énergétiques")

st.markdown("""
Afin de transformer le problème en classification, les bâtiments sont
répartis en **4 classes** selon les quartiles des charges énergétiques
totales.

- **Classe 0** : charges les plus faibles
- **Classe 1** : charges faibles à intermédiaires
- **Classe 2** : charges intermédiaires à élevées
- **Classe 3** : charges les plus élevées
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("1er quartile", f"{q1:.2f}")

with col2:
    st.metric("Médiane", f"{q2:.2f}")

with col3:
    st.metric("3e quartile", f"{q3:.2f}")

# ============================================================
# RÉPARTITION DES CLASSES
# ============================================================

st.markdown("### 📊 Répartition des bâtiments par classe")

class_counts = (
    df["charges_classes"]
    .value_counts()
    .sort_index()
    .reset_index()
)

class_counts.columns = ["Classe", "Nombre de bâtiments"]

class_counts["Classe"] = class_counts["Classe"].astype(str)

fig_classes = px.bar(
    class_counts,
    x="Classe",
    y="Nombre de bâtiments",
    text="Nombre de bâtiments",
    title="Nombre de bâtiments par classe énergétique",
    labels={
        "Classe": "Classe énergétique"
    }
)

fig_classes.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig_classes,
    use_container_width=True
)

# ============================================================
# CORRÉLATIONS
# ============================================================

st.markdown("## 🔗 Corrélations")

corr = df.drop(
    columns=["charges_classes"],
    errors="ignore"
).corr()

fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    aspect="auto",
    title="Matrice de corrélation"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# ============================================================
# VARIABLES LES PLUS CORRÉLÉES
# ============================================================

st.markdown("### 🔎 Variables les plus corrélées aux charges totales")

corr_total = (
    df.drop(columns=["charges_classes"])
    .corr()["total_charges"]
    .drop("total_charges")
    .sort_values(
        key=abs,
        ascending=False
    )
)

corr_total_df = corr_total.reset_index()

corr_total_df.columns = [
    "Variable",
    "Corrélation"
]

st.dataframe(
    corr_total_df.style.format(
        {"Corrélation": "{:.3f}"}
    ),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# COMPACITÉ ET CHARGES
# ============================================================

st.markdown("## 🏢 Caractéristiques du bâtiment")

fig_compact = px.scatter(
    df,
    x="relative_compactness",
    y="total_charges",
    color="charges_classes",
    hover_data=[
        "surface_area",
        "wall_area",
        "roof_area",
        "overall_height"
    ],
    labels={
        "relative_compactness": "Compacité relative",
        "total_charges": "Charges totales",
        "charges_classes": "Classe"
    },
    title="Compacité du bâtiment et charges énergétiques"
)

st.plotly_chart(
    fig_compact,
    use_container_width=True
)

# ============================================================
# CONCLUSION
# ============================================================

st.markdown("## 💡 À retenir")

st.markdown("""
L'analyse met en évidence une relation importante entre les
caractéristiques architecturales des bâtiments et leurs besoins
énergétiques.

Les charges de chauffage et de climatisation sont fortement liées.
La variable `total_charges` permet ensuite de construire quatre
classes équilibrées de bâtiments.

Cette classification servira de base à la comparaison de plusieurs
algorithmes de Machine Learning dans la page **Modélisation**.
""")
