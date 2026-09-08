import streamlit as st

st.set_page_config(
    page_title="London Fire Brigade — Machine Learning",
    page_icon="🚒",
    layout="wide",
)

pages = {
    "Projet": [
        st.Page(
            "app.py",
            title="Accueil",
            icon="🏠",
        ),
        st.Page(
            "pages/1_Exploration.py",
            title="Exploration",
            icon="🔎",
        ),
    ]
}

pg = st.navigation(pages)

if pg.url_path == "accueil":
    st.title("🚒 London Fire Brigade")
    st.subheader("Pipeline de Machine Learning pour prédire le temps d'arrivée des secours")

    st.markdown("""
    ### 🎯 Objectif

    Ce projet utilise des données du **London Fire Brigade** afin
    d'analyser les interventions des services de secours et de construire
    un modèle de Machine Learning capable de prédire le **temps d'arrivée
    des secours**.

    L'objectif est de mettre en place une véritable **Pipeline de Machine
    Learning**, depuis la préparation des données jusqu'à la prédiction.
    """)

    st.markdown("""
    ### 📊 Les données

    Le jeu de données combine des informations relatives aux
    **interventions** et aux **mobilisations des véhicules** du London Fire Brigade.

    Chaque observation correspond à une mobilisation associée à une intervention.

    La variable cible est :

    - ⏱️ **`AttendanceTimeSeconds`** — temps d'arrivée sur les lieux,
      exprimé en secondes.
    """)

    st.markdown("""
    ### 🧠 Approche Machine Learning

    Le projet suit plusieurs étapes :

    1. 🔎 Exploration et audit des données
    2. 🧹 Préparation des données
    3. ⚙️ Feature engineering
    4. 🔄 Construction d'une Pipeline scikit-learn
    5. 🤖 Entraînement du modèle
    6. 📊 Évaluation des performances
    7. ⏱️ Prédiction du temps d'arrivée
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Observations", "100 000")

    with col2:
        st.metric("Variables", "15")

    with col3:
        st.metric("Variable cible", "AttendanceTimeSeconds")
