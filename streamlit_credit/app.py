import streamlit as st

st.set_page_config(
    page_title="German Credit — Profil & risque",
    page_icon="🏦",
    layout="wide",
)

pages = [
    st.Page("pages/0_Vue_d_ensemble.py", title="Vue d'ensemble", icon="🏦", default=True),
    st.Page("pages/1_Durée_des_prêts.py", title="Durée des prêts", icon="⏳"),
    st.Page("pages/2_Profil_&_risque.py", title="Profil & risque", icon="⚠️"),
    st.Page("pages/3_Comptes_&_comportement.py", title="Comptes & comportement", icon="💳"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
