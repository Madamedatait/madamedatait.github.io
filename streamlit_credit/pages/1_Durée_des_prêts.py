import streamlit as st
import plotly.express as px
from data_utils import load_data
from theme import inject_custom_css

st.set_page_config(page_title="German Credit — Durée des prêts", page_icon="⏳", layout="wide")
inject_custom_css()

df = load_data()

st.title("⏳ Durée des prêts")
st.caption(
    "Les prêts sont classés en trois catégories selon leur durée : court terme "
    "(≤10 mois), moyen terme (11-30 mois) et long terme (>30 mois). "
    "Qu'est-ce qui distingue ces trois groupes ?"
)

# --- Filtres (mêmes filtres que la page d'accueil, indépendants ici) ---
st.sidebar.header("Filtres")
purposes = sorted(df["purpose"].unique())
selected_purposes = st.sidebar.multiselect("Motif du prêt", purposes, default=purposes)
housing_options = sorted(df["housing"].unique())
selected_housing = st.sidebar.multiselect("Logement", housing_options, default=housing_options)

filtered = df[df["purpose"].isin(selected_purposes) & df["housing"].isin(selected_housing)]

if filtered.empty:
    st.warning("Aucun emprunteur ne correspond à ces filtres.")
    st.stop()

st.sidebar.markdown(f"**{len(filtered)}** emprunteurs sélectionnés sur {len(df)}")

# --- Répartition des catégories ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Répartition")
    categ_counts = filtered["duration_categ"].value_counts().reindex(
        ["Court terme (≤10 mois)", "Moyen terme (11-30 mois)", "Long terme (>30 mois)"]
    ).reset_index()
    categ_counts.columns = ["categorie", "count"]
    fig_pie = px.pie(
        categ_counts, names="categorie", values="count", hole=0.45,
        color_discrete_sequence=["#c4b5fd", "#8b5cf6", "#5b21b6"],
    )
    fig_pie.update_layout(margin=dict(t=10), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Distribution de la durée (en mois)")
    fig_hist = px.histogram(
        filtered, x="duration", nbins=25,
        color_discrete_sequence=["#7c3aed"],
    )
    fig_hist.update_layout(
        xaxis_title="Durée (mois)", yaxis_title="Nombre de prêts",
        bargap=0.05, margin=dict(t=10),
    )
    st.plotly_chart(fig_hist, use_container_width=True)

st.divider()

# --- Ce qui distingue les groupes ---
st.subheader("Montant du crédit selon la durée")
fig_box = px.box(
    filtered, x="duration_categ", y="credit_amount",
    category_orders={"duration_categ": ["Court terme (≤10 mois)", "Moyen terme (11-30 mois)", "Long terme (>30 mois)"]},
    color="duration_categ",
    color_discrete_sequence=["#c4b5fd", "#8b5cf6", "#5b21b6"],
)
fig_box.update_layout(
    xaxis_title="", yaxis_title="Montant du crédit (DM)",
    showlegend=False, margin=dict(t=10),
)
st.plotly_chart(fig_box, use_container_width=True)
st.caption(
    "Sans surprise, les prêts longs portent sur des montants plus élevés — "
    "ce qui suggère que la durée est avant tout dimensionnée pour rendre "
    "la mensualité supportable."
)

st.subheader("Motif du prêt selon la durée")
purpose_duration = (
    filtered.groupby(["purpose", "duration_categ"], observed=True)
    .size()
    .reset_index(name="count")
)
fig_stacked = px.bar(
    purpose_duration, x="purpose", y="count", color="duration_categ",
    category_orders={"duration_categ": ["Court terme (≤10 mois)", "Moyen terme (11-30 mois)", "Long terme (>30 mois)"]},
    color_discrete_sequence=["#c4b5fd", "#8b5cf6", "#5b21b6"],
)
fig_stacked.update_layout(
    xaxis_title="", yaxis_title="Nombre de prêts",
    legend_title="Durée", margin=dict(t=10),
)
st.plotly_chart(fig_stacked, use_container_width=True)
