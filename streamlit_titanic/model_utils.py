"""
Chargement des données et entraînement des modèles pour le projet Titanic.
"""

import os
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

CAT_COLS = ["Pclass", "Sex", "Embarked"]
NUM_COLS = ["Age", "Fare", "SibSp", "Parch"]


@st.cache_data
def load_data(path: str = "data/train.csv") -> pd.DataFrame:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, path)
    return pd.read_csv(full_path)


@st.cache_data
def prepare_features(df: pd.DataFrame):
    """Nettoie et encode les variables explicatives, retourne X et y."""
    work = df.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"], errors="ignore")
    y = work["Survived"]

    x_cat = work[CAT_COLS].copy()
    x_num = work[NUM_COLS].copy()

    for col in x_cat.columns:
        x_cat[col] = x_cat[col].fillna(x_cat[col].mode()[0])
    for col in x_num.columns:
        x_num[col] = x_num[col].fillna(x_num[col].median())

    x_cat_encoded = pd.get_dummies(x_cat, columns=x_cat.columns)
    x = pd.concat([x_cat_encoded, x_num], axis=1)

    return x, y


@st.cache_resource
def train_model(model_name: str, x_train, y_train, x_test_scaled_cols):
    """Entraîne le modèle choisi. Mis en cache pour éviter le ré-entraînement
    à chaque interaction de l'utilisateur."""
    if model_name == "Random Forest":
        clf = RandomForestClassifier(random_state=123)
    elif model_name == "SVM":
        clf = SVC(probability=True, random_state=123)
    elif model_name == "Régression logistique":
        clf = LogisticRegression(max_iter=1000)
    else:
        raise ValueError(f"Modèle inconnu : {model_name}")

    clf.fit(x_train, y_train)
    return clf


@st.cache_data
def split_and_scale(_x: pd.DataFrame, _y: pd.Series):
    x_train, x_test, y_train, y_test = train_test_split(
        _x, _y, test_size=0.2, random_state=123
    )
    scaler = StandardScaler()
    x_train = x_train.copy()
    x_test = x_test.copy()
    x_train[NUM_COLS] = scaler.fit_transform(x_train[NUM_COLS])
    x_test[NUM_COLS] = scaler.transform(x_test[NUM_COLS])
    return x_train, x_test, y_train, y_test


def get_scores(clf, x_test, y_test):
    y_pred = clf.predict(x_test)
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
    }
