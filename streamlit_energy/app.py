import streamlit as st

st.set_page_config(
    page_title="Energy Efficiency — Machine Learning",
    page_icon="🏢",
    layout="wide",
)

pages = [
    st.Page(
        "pages/1_Exploration.py",
        title="Exploration",
        icon="🔎",
        default=True,
    ),
    st.Page(
        "pages/2_Analyse_energetique.py",
        title="Analyse énergétique",
        icon="📊",
    ),
    st.Page(
        "pages/3_Modelisation.py",
        title="Modélisation",
        icon="🤖",
    ),
    st.Page(
        "pages/4_Prediction.py",
        title="Prédiction",
        icon="🏢",
    ),
]

pg = st.navigation(
    pages,
    position="sidebar"
)

pg.run()
