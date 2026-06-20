import streamlit as st
import plotly.express as px
from data_utils import load_data
from theme import inject_custom_css

inject_custom_css()

df = load_data()

st.title("🏦 Profil des emprunteurs")
st.caption(
    "Exploration d'un jeu de données de 1 000 emprunteurs ayant souscrit un prêt "
    "bancaire en Allemagne — âge, situation, motif et montant du crédit."
)

# --- Filtres dans la sidebar, partagés visuellement avec les autres pages ---
st.sidebar.header("Filtres")

purposes = sorted(df["purpose"].unique())
selected_purposes = st.sidebar.multiselect(
    "Motif du prêt", purposes, default=purposes
)

age_min, age_max = int(df["age"].min()), int(df["age"].max())
selected_age = st.sidebar.slider(
    "Tranche d'âge", age_min, age_max, (age_min, age_max)
)

housing_options = sorted(df["housing"].unique())
selected_housing = st.sidebar.multiselect(
    "Logement", housing_options, default=housing_options
)

filtered = df[
    df["purpose"].isin(selected_purposes)
    & df["age"].between(*selected_age)
    & df["housing"].isin(selected_housing)
]

st.sidebar.markdown(f"**{len(filtered)}** emprunteurs sélectionnés sur {len(df)}")

if filtered.empty:
    st.warning("Aucun emprunteur ne correspond à ces filtres. Élargis la sélection dans la barre latérale.")
    st.stop()

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Emprunteurs", f"{len(filtered):,}".replace(",", " "))
col2.metric("Âge moyen", f"{filtered['age'].mean():.0f} ans")
col3.metric("Crédit moyen", f"{filtered['credit_amount'].mean():,.0f} DM".replace(",", " "))
col4.metric("Durée moyenne", f"{filtered['duration'].mean():.0f} mois")

st.divider()

# --- Visualisations ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Répartition par âge")
    fig_age = px.histogram(
        filtered, x="age", nbins=20,
        color_discrete_sequence=["#7c3aed"],
    )
    fig_age.update_layout(
        xaxis_title="Âge", yaxis_title="Nombre d'emprunteurs",
        bargap=0.05, margin=dict(t=10),
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col_right:
    st.subheader("Motif du prêt")
    purpose_counts = filtered["purpose"].value_counts().reset_index()
    purpose_counts.columns = ["purpose", "count"]
    fig_purpose = px.bar(
        purpose_counts, x="count", y="purpose", orientation="h",
        color_discrete_sequence=["#7c3aed"],
    )
    fig_purpose.update_layout(
        xaxis_title="Nombre d'emprunteurs", yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        margin=dict(t=10),
    )
    st.plotly_chart(fig_purpose, use_container_width=True)

col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Type de logement")
    housing_counts = filtered["housing"].value_counts().reset_index()
    housing_counts.columns = ["housing", "count"]
    fig_housing = px.pie(
        housing_counts, names="housing", values="count", hole=0.45,
        color_discrete_sequence=px.colors.sequential.Purples_r,
    )
    fig_housing.update_layout(margin=dict(t=10))
    st.plotly_chart(fig_housing, use_container_width=True)

with col_right2:
    st.subheader("Niveau de qualification")
    job_counts = filtered["job_label"].value_counts().reset_index()
    job_counts.columns = ["job_label", "count"]
    fig_job = px.bar(
        job_counts, x="job_label", y="count",
        color_discrete_sequence=["#a78bfa"],
    )
    fig_job.update_layout(
        xaxis_title="", yaxis_title="Nombre d'emprunteurs",
        margin=dict(t=10),
    )
    st.plotly_chart(fig_job, use_container_width=True)

st.divider()
with st.expander("Voir les données filtrées"):
    st.dataframe(
        filtered[["age", "sex", "job_label", "housing", "saving_accounts",
                   "checking_account", "credit_amount", "duration", "purpose"]],
        use_container_width=True,
    )
