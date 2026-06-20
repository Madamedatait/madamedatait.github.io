import streamlit as st
import plotly.express as px
from data_utils import load_data
from theme import inject_custom_css

inject_custom_css()

df = load_data()

st.title("⚠️ Profil & risque")
st.caption(
    "On considère ici qu'un prêt cumule davantage de risque lorsqu'il combine "
    "un montant élevé et une durée longue. Quels profils d'emprunteurs sont "
    "le plus exposés à cette combinaison ?"
)

# Score de risque simple : produit normalisé montant x durée
df["risk_score"] = (
    (df["credit_amount"] - df["credit_amount"].min()) / (df["credit_amount"].max() - df["credit_amount"].min())
    + (df["duration"] - df["duration"].min()) / (df["duration"].max() - df["duration"].min())
) / 2

st.sidebar.header("Filtres")
job_filter = st.sidebar.multiselect(
    "Niveau de qualification", sorted(df["job_label"].unique()), default=sorted(df["job_label"].unique())
)
housing_filter = st.sidebar.multiselect(
    "Logement", sorted(df["housing"].unique()), default=sorted(df["housing"].unique())
)

filtered = df[df["job_label"].isin(job_filter) & df["housing"].isin(housing_filter)]

if filtered.empty:
    st.warning("Aucun emprunteur ne correspond à ces filtres.")
    st.stop()

st.sidebar.markdown(f"**{len(filtered)}** emprunteurs sélectionnés sur {len(df)}")

col1, col2, col3 = st.columns(3)
col1.metric("Score de risque moyen", f"{filtered['risk_score'].mean():.2f} / 1")
col2.metric("Crédit moyen", f"{filtered['credit_amount'].mean():,.0f} DM".replace(",", " "))
col3.metric("Durée moyenne", f"{filtered['duration'].mean():.0f} mois")

st.divider()

st.subheader("Montant vs. durée du prêt, par niveau de qualification")
fig_scatter = px.scatter(
    filtered, x="duration", y="credit_amount", color="job_label",
    size="age", hover_data=["housing", "purpose", "age"],
    color_discrete_sequence=px.colors.sequential.Purples_r,
)
fig_scatter.update_layout(
    xaxis_title="Durée (mois)", yaxis_title="Montant du crédit (DM)",
    legend_title="Qualification", margin=dict(t=10),
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption(
    "Chaque point est un emprunteur ; la taille du point reflète son âge. "
    "Les profils les plus exposés se situent en haut à droite du graphique : "
    "montant élevé et longue durée de remboursement."
)

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Score de risque par logement")
    fig_box_housing = px.box(
        filtered, x="housing", y="risk_score", color="housing",
        color_discrete_sequence=["#c4b5fd", "#8b5cf6", "#5b21b6"],
    )
    fig_box_housing.update_layout(
        xaxis_title="", yaxis_title="Score de risque",
        showlegend=False, margin=dict(t=10),
    )
    st.plotly_chart(fig_box_housing, use_container_width=True)

with col_right:
    st.subheader("Score de risque par qualification")
    fig_box_job = px.box(
        filtered, x="job_label", y="risk_score", color="job_label",
        color_discrete_sequence=px.colors.sequential.Purples,
    )
    fig_box_job.update_layout(
        xaxis_title="", yaxis_title="Score de risque",
        showlegend=False, margin=dict(t=10),
    )
    st.plotly_chart(fig_box_job, use_container_width=True)

st.divider()
st.subheader("Top 10 des profils les plus exposés")
top_risk = filtered.nlargest(10, "risk_score")[
    ["age", "sex", "job_label", "housing", "credit_amount", "duration", "purpose", "risk_score"]
].reset_index(drop=True)
top_risk["risk_score"] = top_risk["risk_score"].round(2)
st.dataframe(top_risk, use_container_width=True)
