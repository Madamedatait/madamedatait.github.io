import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


st.set_page_config(
    page_title="Prédiction — London Fire Brigade",
    page_icon="⏱️",
    layout="wide",
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "firefighter_london.csv")
)


# ============================================================
# TITRE
# ============================================================

st.title("⏱️ Prédiction du temps d'arrivée")

st.markdown("""
### 🎯 Estimer le temps d'arrivée des secours

Cette interface permet d'estimer le **temps d'arrivée d'un véhicule
de secours** à partir des caractéristiques d'une intervention.

Le modèle utilisé est un **Random Forest Regressor** intégré dans une
**Pipeline scikit-learn**.
""")


# ============================================================
# VARIABLES
# ============================================================

target = "AttendanceTimeSeconds"

feature_columns = [
    "PlusCode_Description",
    "PropertyCategory",
    "IncGeo_BoroughName",
    "NumPumpsAttending",
    "Latitude",
    "Longitude",
    "DeployedFromStation_Name",
    "DeployedFromStation_Code",
    "HourOfCall",
    "IncidentGroup",
    "PropertyType",
]


X = df[feature_columns].copy()
y = df[target].copy()


# ============================================================
# TYPES DE VARIABLES
# ============================================================

numeric_features = [
    "NumPumpsAttending",
    "Latitude",
    "Longitude",
    "HourOfCall",
]

categorical_features = [
    "PlusCode_Description",
    "PropertyCategory",
    "IncGeo_BoroughName",
    "DeployedFromStation_Name",
    "DeployedFromStation_Code",
    "IncidentGroup",
    "PropertyType",
]


# ============================================================
# PREPROCESSING
# ============================================================

numeric_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "scaler",
            StandardScaler()
        ),
    ]
)


categorical_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        ),
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "num",
            numeric_transformer,
            numeric_features
        ),
        (
            "cat",
            categorical_transformer,
            categorical_features
        ),
    ]
)


# ============================================================
# MODÈLE
# ============================================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
)


pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("model", model),
    ]
)


# ============================================================
# ENTRAÎNEMENT
# ============================================================

@st.cache_resource
def train_model(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    pipeline.fit(
        X_train,
        y_train
    )

    return pipeline


with st.spinner("Préparation du modèle..."):

    trained_pipeline = train_model(
        X,
        y
    )


st.success("✅ Modèle prêt pour les prédictions.")


# ============================================================
# FORMULAIRE
# ============================================================

st.header("📝 Caractéristiques de l'intervention")

st.markdown(
    "Renseignez les caractéristiques ci-dessous pour obtenir une estimation."
)


with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    # ========================================================
    # COLONNE 1
    # ========================================================

    with col1:

        property_category = st.selectbox(
            "🏢 Catégorie de propriété",
            sorted(
                df["PropertyCategory"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        property_type = st.selectbox(
            "🏠 Type de propriété",
            sorted(
                df["PropertyType"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        borough = st.selectbox(
            "📍 Borough",
            sorted(
                df["IncGeo_BoroughName"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        incident_group = st.selectbox(
            "🚨 Groupe d'intervention",
            sorted(
                df["IncidentGroup"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

    # ========================================================
    # COLONNE 2
    # ========================================================

    with col2:

        plus_code = st.selectbox(
            "📌 Description géographique",
            sorted(
                df["PlusCode_Description"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        station = st.selectbox(
            "🚒 Station de déploiement",
            sorted(
                df["DeployedFromStation_Name"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        station_code = st.selectbox(
            "🔢 Code de la station",
            sorted(
                df["DeployedFromStation_Code"]
                .dropna()
                .astype(str)
                .unique()
            )
        )

        pumps = st.number_input(
            "🚒 Nombre de véhicules mobilisés",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )


    # ========================================================
    # HEURE
    # ========================================================

    st.subheader("🕐 Heure de l'intervention")

    hour = st.slider(
        "Heure de l'appel",
        min_value=0,
        max_value=23,
        value=12,
    )


    # ========================================================
    # LOCALISATION
    # ========================================================

    st.subheader("📍 Localisation")

    col3, col4 = st.columns(2)

    with col3:

        latitude = st.number_input(
            "Latitude",
            value=float(
                df["Latitude"].median()
            ),
            format="%.6f",
        )

    with col4:

        longitude = st.number_input(
            "Longitude",
            value=float(
                df["Longitude"].median()
            ),
            format="%.6f",
        )


    # ========================================================
    # BOUTON
    # ========================================================

    submitted = st.form_submit_button(
        "🚀 Estimer le temps d'arrivée",
        type="primary",
    )


# ============================================================
# PRÉDICTION
# ============================================================

if submitted:

    input_data = pd.DataFrame({
        "PlusCode_Description": [plus_code],
        "PropertyCategory": [property_category],
        "IncGeo_BoroughName": [borough],
        "NumPumpsAttending": [pumps],
        "Latitude": [latitude],
        "Longitude": [longitude],
        "DeployedFromStation_Name": [station],
        "DeployedFromStation_Code": [station_code],
        "HourOfCall": [hour],
        "IncidentGroup": [incident_group],
        "PropertyType": [property_type],
    })


    prediction = trained_pipeline.predict(
        input_data
    )[0]


    # ========================================================
    # RÉSULTAT
    # ========================================================

    st.markdown("---")

    st.header("🎯 Résultat de la prédiction")

    minutes = int(prediction // 60)
    seconds = int(prediction % 60)


    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "⏱️ Temps estimé",
            f"{prediction:.0f} secondes"
        )

    with col2:

        st.metric(
            "🕐 Équivalent",
            f"{minutes} min {seconds:02d} s"
        )


    st.info(
        "ℹ️ Cette estimation est produite par le modèle "
        "Random Forest à partir des caractéristiques renseignées."
    )
