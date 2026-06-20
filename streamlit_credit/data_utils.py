"""
Chargement et nettoyage du dataset German Credit Data.
Centralisé ici pour être réutilisé par toutes les pages de l'app.
"""

import pandas as pd
import streamlit as st


JOB_LABELS = {
    0: "Non qualifié, non résident",
    1: "Non qualifié, résident",
    2: "Qualifié",
    3: "Hautement qualifié",
}

DURATION_BINS = [0, 10, 30, 1000]
DURATION_LABELS = ["Court terme (≤10 mois)", "Moyen terme (11-30 mois)", "Long terme (>30 mois)"]


@st.cache_data
def load_data(path: str = "data/german_credit_data.csv") -> pd.DataFrame:
    df = pd.read_csv(path, index_col=0)

    # Harmonise les noms de colonnes (espaces -> underscores, snake_case)
    df = df.rename(columns={
        "Age": "age",
        "Sex": "sex",
        "Job": "job",
        "Housing": "housing",
        "Saving accounts": "saving_accounts",
        "Checking account": "checking_account",
        "Credit amount": "credit_amount",
        "Duration": "duration",
        "Purpose": "purpose",
    })

    # Les comptes épargne/courant manquants signifient probablement "pas de compte"
    # plutôt qu'une vraie donnée manquante : on le rend explicite.
    df["saving_accounts"] = df["saving_accounts"].fillna("aucun compte")
    df["checking_account"] = df["checking_account"].fillna("aucun compte")

    # Libellé plus lisible pour le niveau de qualification
    df["job_label"] = df["job"].map(JOB_LABELS)

    # Catégorie de durée du prêt
    df["duration_categ"] = pd.cut(
        df["duration"], bins=DURATION_BINS, labels=DURATION_LABELS
    )

    return df
