import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

import plotly.express as px


st.set_page_config(
    page_title="Modélisation — London Fire Brigade",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "firefighter_london.csv")
)


st.title("🤖 Modélisation")

st.markdown("""
### 🎯 Objectif

L'objectif est maintenant de construire un modèle de Machine Learning
capable de prédire le **temps d'arrivée des secours**.

La variable cible est :

**`AttendanceTimeSeconds`**
""")


# ============================================================
# VARIABLES
# ============================================================

target = "AttendanceTimeSeconds"

feature_columns = [
    "PropertyCategory",
    "PropertyType",
    "IncGeo_BoroughName",
    "IncidentStationGround",
    "PlusCode_Description",
    "DeployedFromStation_Name",
    "NumPumpsAttending",
    "Latitude",
    "Longitude",
]


# Vérification des colonnes disponibles
feature_columns = [
    col for col in feature_columns
    if col in df.columns
]


X = df[feature_columns].copy()
y = df[target].copy()


# ============================================================
# TRAIN / TEST
# ============================================================

st.header("📚 Séparation des données")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Entraînement",
        f"{len(X_train):,} observations"
    )

with col2:
    st.metric(
        "Test",
        f"{len(X_test):,} observations"
    )


# ============================================================
# TYPES DE VARIABLES
# ============================================================

numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()


# ============================================================
# PREPROCESSING
# ============================================================

st.header("⚙️ Prétraitement")

st.markdown("""
Les variables numériques et catégorielles nécessitent des traitements
différents.

- Les variables numériques sont imputées puis standardisées.
- Les variables catégorielles sont imputées puis encodées avec
  `OneHotEncoder`.
- Le tout est regroupé dans un `ColumnTransformer`.
""")


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
# PIPELINE
# ============================================================

st.header("🔗 Pipeline Machine Learning")

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


st.code(
    """
Pipeline(
    preprocessing = ColumnTransformer(
        numérique → imputation + standardisation
        catégoriel → imputation + OneHotEncoder
    ),
    model = RandomForestRegressor()
)
""",
    language="text",
)


# ============================================================
# ENTRAÎNEMENT
# ============================================================

if st.button(
    "🚀 Entraîner le modèle",
    type="primary"
):

    with st.spinner("Entraînement du modèle en cours..."):

        pipeline.fit(
            X_train,
            y_train
        )

        y_pred = pipeline.predict(
            X_test
        )


    st.success("✅ Modèle entraîné avec succès !")


    # ========================================================
    # MÉTRIQUES
    # ========================================================

    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred
        )
    )

    r2 = r2_score(
        y_test,
        y_pred
    )


    st.header("📊 Performances du modèle")


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "MAE",
            f"{mae:.2f} s"
        )

    with col2:
        st.metric(
            "RMSE",
            f"{rmse:.2f} s"
        )

    with col3:
        st.metric(
            "R²",
            f"{r2:.3f}"
        )


    st.markdown("""
    **MAE — Mean Absolute Error**

    Mesure l'erreur absolue moyenne entre le temps réel et le temps
    prédit.

    **RMSE — Root Mean Squared Error**

    Pénalise davantage les erreurs importantes.

    **R²**

    Mesure la proportion de la variabilité de la variable cible
    expliquée par le modèle.
    """)


    # ========================================================
    # RÉEL VS PRÉDIT
    # ========================================================

    st.header("🎯 Temps réel vs temps prédit")

    results = pd.DataFrame({
        "Réel": y_test.values,
        "Prédit": y_pred,
    })


    fig = px.scatter(
        results.sample(
            min(5000, len(results)),
            random_state=42
        ),
        x="Réel",
        y="Prédit",
        title="Comparaison des valeurs réelles et prédites",
        labels={
            "Réel": "AttendanceTimeSeconds réel",
            "Prédit": "AttendanceTimeSeconds prédit",
        },
    )


    # ligne idéale y=x
    min_value = min(
        results["Réel"].min(),
        results["Prédit"].min()
    )

    max_value = max(
        results["Réel"].max(),
        results["Prédit"].max()
    )


    fig.add_shape(
        type="line",
        x0=min_value,
        y0=min_value,
        x1=max_value,
        y1=max_value,
        line=dict(
            dash="dash"
        ),
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ========================================================
    # EXEMPLES DE PRÉDICTIONS
    # ========================================================

    st.header("🔍 Quelques prédictions")

    comparison = pd.DataFrame({
        "Temps réel (s)": y_test.values[:20],
        "Temps prédit (s)": np.round(
            y_pred[:20],
            1
        ),
    })

    comparison["Erreur (s)"] = (
        comparison["Temps prédit (s)"]
        - comparison["Temps réel (s)"]
    ).round(1)


    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )
