import streamlit as st
import pandas as pd
import plotly.express as px
from theme import inject_custom_css, PALETTE
from model_utils import load_data

st.set_page_config(page_title="Titanic — Profils croisés", page_icon="🧩", layout="wide")
inject_custom_css()

st.title("🧩 Profils croisés")
st.caption(
    "Un seul facteur ne suffit pas à expliquer qui a survécu : ici on combine "
    "plusieurs variables à la fois — classe, genre, âge, famille à bord, tarif "
    "et titre social — pour affiner le tableau."
)

try:
    df = load_data()
except FileNotFoundError:
    st.error("Le fichier `data/train.csv` est introuvable.")
    st.stop()

df = df.copy()
df["Survived_label"] = df["Survived"].map({0: "Décédé", 1: "Survivant"})
df["Pclass_label"] = df["Pclass"].map({1: "1ère classe", 2: "2ème classe", 3: "3ème classe"})

# --- Taille de la famille à bord ---
df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
df["Voyage"] = df["FamilySize"].apply(lambda n: "Seul(e)" if n == 1 else ("Petite famille (2-4)" if n <= 4 else "Famille nombreuse (5+)"))

# --- Titre extrait du nom ---
df["Title"] = df["Name"].str.extract(r",\s*([^\.]*)\.")
title_map = {
    "Mr": "Mr", "Mrs": "Mrs", "Miss": "Miss", "Master": "Master",
    "Mlle": "Miss", "Mme": "Mrs", "Ms": "Miss",
}
df["Title"] = df["Title"].map(title_map).fillna("Autre (noblesse, clergé, militaire...)")

st.divider()

# --- 1. Classe x Genre x Survie ---
st.subheader("Survie selon la classe et le genre")
cross1 = df.groupby(["Pclass_label", "Sex"], observed=True)["Survived"].mean().reset_index()
cross1["Sex"] = cross1["Sex"].map({"male": "Homme", "female": "Femme"})
fig1 = px.bar(
    cross1, x="Pclass_label", y="Survived", color="Sex", barmode="group",
    category_orders={"Pclass_label": ["1ère classe", "2ème classe", "3ème classe"]},
    color_discrete_sequence=["#5b21b6", "#c4b5fd"],
)
fig1.update_layout(
    xaxis_title="", yaxis_title="Taux de survie", yaxis_tickformat=".0%",
    legend_title="Genre", margin=dict(t=10),
)
st.plotly_chart(fig1, use_container_width=True)
st.caption(
    "Être une femme protège dans toutes les classes, mais l'effet de la classe "
    "reste très marqué : une femme de 1ère classe a beaucoup plus de chances de "
    "survie qu'une femme de 3ème classe."
)

st.divider()

# --- 2. Famille à bord x Survie ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Survie selon la taille de la famille")
    voyage_order = ["Seul(e)", "Petite famille (2-4)", "Famille nombreuse (5+)"]
    cross2 = df.groupby("Voyage", observed=True)["Survived"].mean().reindex(voyage_order).reset_index()
    fig2 = px.bar(
        cross2, x="Voyage", y="Survived",
        category_orders={"Voyage": voyage_order},
        color_discrete_sequence=["#7c3aed"],
    )
    fig2.update_layout(xaxis_title="", yaxis_title="Taux de survie", yaxis_tickformat=".0%", margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Les petites familles (2 à 4 personnes) survivent mieux que les passagers seuls ou en famille nombreuse — un compromis entre l'entraide et la difficulté à évacuer un grand groupe.")

with col2:
    st.subheader("Survie selon le titre social")
    title_order = df["Title"].value_counts().index.tolist()
    cross3 = df.groupby("Title", observed=True)["Survived"].mean().reindex(title_order).reset_index()
    fig3 = px.bar(
        cross3, x="Title", y="Survived",
        color_discrete_sequence=["#8b5cf6"],
    )
    fig3.update_layout(xaxis_title="", yaxis_title="Taux de survie", yaxis_tickformat=".0%", margin=dict(t=10))
    st.plotly_chart(fig3, use_container_width=True)
    st.caption("Le titre extrait du nom reflète à la fois l'âge et le statut social — \"Master\" désignait les jeunes garçons.")

st.divider()

# --- 3. Tarif x Port d'embarquement x Survie ---
st.subheader("Tarif payé et port d'embarquement")
embarked_map = {"S": "Southampton", "C": "Cherbourg", "Q": "Queenstown"}
df["Embarked_label"] = df["Embarked"].map(embarked_map)
fig4 = px.box(
    df.dropna(subset=["Embarked_label"]), x="Embarked_label", y="Fare", color="Survived_label",
    color_discrete_sequence=["#c4b5fd", "#5b21b6"],
    points=False,
)
fig4.update_layout(
    xaxis_title="Port d'embarquement", yaxis_title="Tarif payé (£)",
    legend_title="", margin=dict(t=10),
)
st.plotly_chart(fig4, use_container_width=True)
st.caption(
    "Les passagers embarqués à Cherbourg ont en moyenne payé des tarifs plus "
    "élevés — cohérent avec une plus forte proportion de 1ère classe à ce port."
)

st.divider()

# --- 4. Heatmap croisée classe x titre ---
st.subheader("Répartition des titres par classe")
cross4 = pd.crosstab(df["Title"], df["Pclass_label"])
cross4 = cross4[["1ère classe", "2ème classe", "3ème classe"]]
fig5 = px.imshow(
    cross4, text_auto=True, color_continuous_scale="Purples", aspect="auto",
)
fig5.update_layout(xaxis_title="", yaxis_title="", margin=dict(t=10))
st.plotly_chart(fig5, use_container_width=True)
