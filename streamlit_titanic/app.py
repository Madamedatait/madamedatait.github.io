import streamlit as st

st.set_page_config(
    page_title="Titanic — Survie & Modélisation",
    page_icon="🚢",
    layout="wide",
)

pages = [
    st.Page("pages/0_Exploration.py", title="Exploration", icon="🚢", default=True),
    st.Page("pages/1_DataVisualization.py", title="Visualisation", icon="📊"),
    st.Page("pages/2_Modélisation.py", title="Modélisation", icon="🤖"),
    st.Page("pages/3_Profils_croisés.py", title="Profils croisés", icon="🧩"),
]

pg = st.navigation(pages, position="sidebar")
pg.run()
