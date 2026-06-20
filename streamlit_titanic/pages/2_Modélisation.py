import streamlit as st
import plotly.express as px
import pandas as pd
from theme import inject_custom_css
from model_utils import load_data, prepare_features, split_and_scale, train_model, get_scores

st.set_page_config(page_title="Titanic — Modélisation", page_icon="🤖", layout="wide")
inject_custom_css()

st.title("🤖 Modélisation")
st.caption(
    "Trois modèles de classification entraînés pour prédire la survie d'un "
    "passager à partir de sa classe, son genre, son âge, son tarif et sa famille à bord."
)

try:
    df = load_data()
except FileNotFoundError:
    st.error("Le fichier `data/train.csv` est introuvable.")
    st.stop()

x, y = prepare_features(df)
x_train, x_test, y_train, y_test = split_and_scale(x, y)

choix = ["Random Forest", "SVM", "Régression logistique"]
option = st.selectbox("Choix du modèle", choix)

with st.spinner(f"Entraînement du modèle {option}..."):
    clf = train_model(option, x_train, y_train, tuple(x_test.columns))

scores = get_scores(clf, x_test, y_test)

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Performance")
    st.metric("Précision (accuracy)", f"{scores['accuracy'] * 100:.1f} %")
    st.caption(f"Mesurée sur {len(y_test)} passagers de test (20 % du jeu de données).")

with col2:
    st.subheader("Matrice de confusion")
    cm = scores["confusion_matrix"]
    cm_df = pd.DataFrame(
        cm,
        index=["Réel : Décédé", "Réel : Survivant"],
        columns=["Prédit : Décédé", "Prédit : Survivant"],
    )
    fig = px.imshow(
        cm_df, text_auto=True, color_continuous_scale="Purples",
        aspect="auto",
    )
    fig.update_layout(margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)

st.divider()

if option == "Random Forest":
    st.subheader("Importance des variables")
    importances = pd.Series(clf.feature_importances_, index=x_train.columns)
    importances = importances.sort_values(ascending=True).reset_index()
    importances.columns = ["variable", "importance"]
    fig = px.bar(
        importances, x="importance", y="variable", orientation="h",
        color_discrete_sequence=["#7c3aed"],
    )
    fig.update_layout(xaxis_title="Importance", yaxis_title="", margin=dict(t=10))
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        "Le genre et le tarif payé sont généralement les variables les plus "
        "discriminantes pour ce modèle."
    )

with st.expander("Comparer les 3 modèles d'un coup"):
    st.write("Entraîne et compare l'accuracy des trois modèles sur le même jeu de test.")
    if st.button("Lancer la comparaison"):
        results = []
        for name in choix:
            model = train_model(name, x_train, y_train, tuple(x_test.columns))
            acc = get_scores(model, x_test, y_test)["accuracy"]
            results.append({"Modèle": name, "Accuracy": acc})
        results_df = pd.DataFrame(results).sort_values("Accuracy", ascending=False)
        fig = px.bar(
            results_df, x="Modèle", y="Accuracy", color_discrete_sequence=["#7c3aed"],
        )
        fig.update_layout(yaxis_tickformat=".0%", margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(results_df, use_container_width=True)
