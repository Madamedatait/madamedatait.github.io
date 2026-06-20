import streamlit as st
import plotly.express as px
from theme import inject_custom_css, PALETTE
from model_utils import load_data

inject_custom_css()

st.title("📊 Visualisation des données")
st.caption("Qui étaient les passagers du Titanic, et quels facteurs semblent liés à leur survie ?")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Le fichier `data/train.csv` est introuvable.")
    st.stop()

df_display = df.copy()
df_display["Survived_label"] = df_display["Survived"].map({0: "Décédé", 1: "Survivant"})

col1, col2 = st.columns(2)

with col1:
    st.subheader("Répartition survie / décès")
    counts = df_display["Survived_label"].value_counts().reset_index()
    counts.columns = ["statut", "count"]
    fig = px.bar(counts, x="statut", y="count", color="statut",
                 color_discrete_sequence=["#c4b5fd", "#5b21b6"])
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Nombre de passagers", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Répartition par genre")
    counts = df_display["Sex"].value_counts().reset_index()
    counts.columns = ["sex", "count"]
    fig = px.pie(counts, names="sex", values="count", hole=0.45,
                 color_discrete_sequence=["#7c3aed", "#c4b5fd"])
    fig.update_layout(margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("Répartition par classe")
    counts = df_display["Pclass"].value_counts().sort_index().reset_index()
    counts.columns = ["classe", "count"]
    counts["classe"] = counts["classe"].map({1: "1ère classe", 2: "2ème classe", 3: "3ème classe"})
    fig = px.bar(counts, x="classe", y="count", color_discrete_sequence=["#7c3aed"])
    fig.update_layout(xaxis_title="", yaxis_title="Nombre de passagers", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("Distribution de l'âge")
    fig = px.histogram(df_display, x="Age", nbins=30, color_discrete_sequence=["#7c3aed"])
    fig.update_layout(xaxis_title="Âge", yaxis_title="Nombre de passagers", bargap=0.05, margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("Survie selon le genre")
fig = px.histogram(
    df_display, x="Survived_label", color="Sex", barmode="group",
    color_discrete_sequence=["#7c3aed", "#c4b5fd"],
)
fig.update_layout(xaxis_title="", yaxis_title="Nombre de passagers", legend_title="Genre", margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Les femmes ont un taux de survie nettement supérieur — cohérent avec la "
    "consigne « les femmes et les enfants d'abord » lors de l'évacuation."
)

st.subheader("Taux de survie selon la classe")
survival_by_class = df_display.groupby("Pclass")["Survived"].mean().reset_index()
survival_by_class["Pclass"] = survival_by_class["Pclass"].map({1: "1ère classe", 2: "2ème classe", 3: "3ème classe"})
fig = px.line(survival_by_class, x="Pclass", y="Survived", markers=True,
              color_discrete_sequence=["#5b21b6"])
fig.update_layout(xaxis_title="", yaxis_title="Taux de survie", yaxis_tickformat=".0%", margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
st.caption("Le taux de survie diminue nettement à mesure que la classe baisse.")

st.subheader("Âge vs. survie, selon la classe")
fig = px.scatter(
    df_display, x="Age", y="Survived", color="Pclass",
    color_continuous_scale=px.colors.sequential.Purples,
    trendline=None,
)
fig.update_layout(xaxis_title="Âge", yaxis_title="Survie (0 = non, 1 = oui)", margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Corrélations entre variables numériques")
numeric_df = df_display.select_dtypes(include="number")
corr = numeric_df.corr()
fig = px.imshow(
    corr, text_auto=".2f", color_continuous_scale="Purples",
    aspect="auto",
)
fig.update_layout(margin=dict(t=10))
st.plotly_chart(fig, use_container_width=True)
