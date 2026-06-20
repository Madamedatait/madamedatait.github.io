import streamlit as st
import pandas as pd
import plotly.express as px
from data_utils import load_data
from theme import inject_custom_css

inject_custom_css()

st.title("💳 Comptes & comportement")
st.caption(
    "Le type de compte épargne et de compte courant détenu par un emprunteur "
    "en dit long sur sa situation financière. On croise ici ces deux variables "
    "avec le profil démographique et les caractéristiques du prêt."
)

df = load_data()

ACCOUNT_ORDER = ["aucun compte", "little", "moderate", "quite rich", "rich"]
ACCOUNT_LABELS = {
    "aucun compte": "Aucun compte", "little": "Faible", "moderate": "Modéré",
    "quite rich": "Assez élevé", "rich": "Élevé",
}
df["saving_label"] = df["saving_accounts"].map(ACCOUNT_LABELS)
df["checking_label"] = df["checking_account"].map(ACCOUNT_LABELS)
label_order = [ACCOUNT_LABELS[k] for k in ACCOUNT_ORDER]

st.divider()

# --- 1. Compte épargne x genre ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Compte épargne selon le genre")
    cross1 = pd.crosstab(df["sex"], df["saving_label"], normalize="index").reindex(columns=label_order) * 100
    cross1 = cross1.reset_index().melt(id_vars="sex", var_name="saving_label", value_name="pct")
    cross1["sex"] = cross1["sex"].map({"male": "Homme", "female": "Femme"})
    fig1 = px.bar(
        cross1, x="saving_label", y="pct", color="sex", barmode="group",
        category_orders={"saving_label": label_order},
        color_discrete_sequence=["#5b21b6", "#c4b5fd"],
    )
    fig1.update_layout(
        xaxis_title="", yaxis_title="% des emprunteurs", legend_title="Genre", margin=dict(t=10),
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Compte courant selon le logement")
    cross2 = pd.crosstab(df["housing"], df["checking_label"], normalize="index").reindex(columns=label_order) * 100
    cross2 = cross2.reset_index().melt(id_vars="housing", var_name="checking_label", value_name="pct")
    fig2 = px.bar(
        cross2, x="checking_label", y="pct", color="housing", barmode="group",
        category_orders={"checking_label": label_order},
        color_discrete_sequence=["#7c3aed", "#a78bfa", "#ede9fe"],
    )
    fig2.update_layout(
        xaxis_title="", yaxis_title="% des emprunteurs", legend_title="Logement", margin=dict(t=10),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- 2. Montant du crédit selon le compte épargne ---
st.subheader("Montant du crédit selon le niveau d'épargne")
fig3 = px.box(
    df, x="saving_label", y="credit_amount",
    category_orders={"saving_label": label_order},
    color="saving_label",
    color_discrete_sequence=["#ede9fe", "#c4b5fd", "#a78bfa", "#8b5cf6", "#5b21b6"],
)
fig3.update_layout(
    xaxis_title="", yaxis_title="Montant du crédit (DM)", showlegend=False, margin=dict(t=10),
)
st.plotly_chart(fig3, use_container_width=True)
st.caption(
    "Contrairement à l'intuition, les emprunteurs sans compte épargne ne sont "
    "pas systématiquement ceux qui empruntent le moins — le montant emprunté "
    "dépend surtout du motif du prêt."
)

st.divider()

# --- 3. Combinaison épargne + trésorerie faibles ---
st.subheader("Emprunteurs cumulant peu d'épargne et peu de trésorerie")
df["situation_tendue"] = (df["saving_accounts"] == "little") & (df["checking_account"] == "little")
n_tendue = df["situation_tendue"].sum()
pct_tendue = n_tendue / len(df) * 100

col_a, col_b = st.columns([1, 2])
with col_a:
    st.metric("Emprunteurs concernés", f"{n_tendue}", f"{pct_tendue:.0f} % du total")
    st.caption(
        "Profils ayant à la fois un compte épargne **et** un compte courant "
        "classés comme « faible »."
    )

with col_b:
    situation_df = df.copy()
    situation_df["Situation"] = situation_df["situation_tendue"].map({True: "Épargne et trésorerie faibles", False: "Autre situation"})
    fig4 = px.histogram(
        situation_df, x="duration_categ", color="Situation", barmode="group",
        category_orders={"duration_categ": ["Court terme (≤10 mois)", "Moyen terme (11-30 mois)", "Long terme (>30 mois)"]},
        color_discrete_sequence=["#5b21b6", "#ede9fe"],
    )
    fig4.update_layout(xaxis_title="", yaxis_title="Nombre d'emprunteurs", legend_title="", margin=dict(t=10))
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --- 4. Heatmap croisée épargne x trésorerie ---
st.subheader("Combinaisons compte épargne × compte courant")
cross5 = pd.crosstab(df["saving_label"], df["checking_label"])
cross5 = cross5.reindex(index=label_order, columns=label_order, fill_value=0)
fig5 = px.imshow(
    cross5, text_auto=True, color_continuous_scale="Purples", aspect="auto",
)
fig5.update_layout(xaxis_title="Compte courant", yaxis_title="Compte épargne", margin=dict(t=10))
st.plotly_chart(fig5, use_container_width=True)
st.caption(
    "La combinaison la plus fréquente reste « faible / faible » — la majorité "
    "des emprunteurs de ce jeu de données ont une situation financière modeste."
)
