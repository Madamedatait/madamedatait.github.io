"""
Styles partagés pour une identité visuelle cohérente entre les apps
German Credit et Titanic (mêmes couleurs violet/lavande que le reste
du portfolio madamedatait.com).
"""

import streamlit as st

PALETTE = ["#5b21b6", "#7c3aed", "#8b5cf6", "#a78bfa", "#c4b5fd", "#ede9fe"]
PALETTE_R = list(reversed(PALETTE))


def inject_custom_css():
    st.markdown(
        """
        <style>
        .stMetric {
            background-color: #f5f3ff;
            border: 1px solid #ddd6fe;
            border-radius: 10px;
            padding: 12px 16px;
        }
        section[data-testid="stSidebar"] {
            background-color: #faf9ff;
        }
        h1, h2, h3 {
            color: #4c1d95;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
