import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="Préparation — London Fire Brigade",
    page_icon="🛠️",
    layout="wide",
)

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "firefighter_london.csv")
)

st.title("🛠️ Préparation des données")

st.markdown("""
### 🎯 Objectif

Avant de construire notre modèle de Machine Learning, les données
doivent être préparées afin de pouvoir être utilisées correctement
par les algorithmes.

Cette étape comprend notamment la transformation des variables
temporelles, la sélection des variables explicatives et la séparation
entre la variable cible et les données utilisées pour la prédiction.
""")

# ============================================================
# COPIE DE TRAVAIL
# ============================================================

data = df.copy()

# ============================================================
# VARIABLE CIBLE
# ============================================================

st.header("🎯 Variable cible")

target = "AttendanceTimeSeconds"

st.write(
    "La variable cible choisie pour la prédiction est "
    f"**`{target}`**, correspondant au temps d'arrivée des secours "
    "en secondes."
)

# ============================================================
# VARIABLES TEMPORELLES
# ============================================================

st.header("📅 Transformation des variables temporelles")

st.markdown("""
Les variables contenant des dates et des heures peuvent apporter
des informations utiles au modèle. Nous allons extraire plusieurs
caractéristiques temporelles :
- l'année ;
- le mois ;
- le jour de la semaine ;
- l'heure ;
- la minute.
""")

# Conversion des dates
data["DateAndTimeMobilised"] = pd.to_datetime(
    data["DateAndTimeMobilised"],
    errors="coerce"
)

data["DateAndTimeOfCall"] = pd.to_datetime(
    data["DateAndTimeOfCall"],
    errors="coerce"
)

# Création des variables temporelles
data["mobilised_year"] = data["DateAndTimeMobilised"].dt.year
data["mobilised_month"] = data["DateAndTimeMobilised"].dt.month
data["mobilised_dayofweek"] = data["DateAndTimeMobilised"].dt.dayofweek
data["mobilised_hour"] = data["DateAndTimeMobilised"].dt.hour
data["mobilised_minute"] = data["DateAndTimeMobilised"].dt.minute

st.success("✅ Variables temporelles créées.")

temporal_columns = [
    "DateAndTimeMobilised",
    "mobilised_year",
    "mobilised_month",
    "mobilised_dayofweek",
    "mobilised_hour",
    "mobilised_minute",
]

st.dataframe(
    data[temporal_columns].head(10),
    use_container_width=True,
    hide_index=True,
)

# ============================================================
# VARIABLES EXPLICATIVES
# ============================================================

st.header("📊 Sélection des variables")

st.markdown("""
La variable cible **`AttendanceTimeSeconds`** est séparée des variables
explicatives utilisées pour construire le modèle.
""")

# Variables que l'on souhaite utiliser
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
    "mobilised_month",
    "mobilised_dayofweek",
    "mobilised_hour",
    "mobilised_minute",
]

# Vérification des colonnes disponibles
feature_columns = [
    col for col in feature_columns
    if col in data.columns
]

X = data[feature_columns].copy()
y = data[target].copy()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Variables explicatives",
        len(feature_columns)
    )

with col2:
    st.metric(
        "Variable cible",
        target
    )

st.subheader("Variables retenues")

st.dataframe(
    pd.DataFrame({
        "Variable": feature_columns,
        "Type": X.dtypes.astype(str).values,
    }),
    use_container_width=True,
    hide_index=True,
)

# ============================================================
# TYPES DE VARIABLES
# ============================================================

st.header("🔢 Variables numériques et catégorielles")

numeric_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object", "category"]
).columns.tolist()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Variables numériques")
    for col in numeric_features:
        st.write(f"- `{col}`")

with col2:
    st.subheader("Variables catégorielles")
    for col in categorical_features:
        st.write(f"- `{col}`")

# ============================================================
# VALEURS MANQUANTES
# ============================================================

st.header("🧹 Valeurs manquantes")

missing = X.isna().sum()

missing = missing[missing > 0].sort_values(
    ascending=False
)

if len(missing) == 0:
    st.success("✅ Aucune valeur manquante dans les variables explicatives.")
else:
    missing_df = pd.DataFrame({
        "Variable": missing.index,
        "Valeurs manquantes": missing.values,
        "Pourcentage (%)": (
            missing.values / len(X) * 100
        ).round(2),
    })

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# RÉSUMÉ
# ============================================================

st.header("✅ Données prêtes pour la Pipeline")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Observations",
        f"{X.shape[0]:,}"
    )

with col2:
    st.metric(
        "Variables explicatives",
        X.shape[1]
    )

with col3:
    st.metric(
        "Variable cible",
        target
    )

st.info("""
🔄 **Étape suivante :** les variables numériques et catégorielles seront
traitées automatiquement dans une **Pipeline scikit-learn** à l'aide
d'un `ColumnTransformer`.
""")
