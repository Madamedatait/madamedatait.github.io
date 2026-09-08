import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


st.set_page_config(
    page_title="Energy Efficiency — Prédiction",
    page_icon="🏢",
    layout="wide",
)


st.title("🏢 Prédiction énergétique")
st.subheader("Prédire la classe énergétique d'un bâtiment")


st.markdown("""
### 🎯 Prédiction interactive

Le modèle **Random Forest**, sélectionné lors de la phase de
modélisation, est utilisé pour prédire la classe énergétique d'un
nouveau bâtiment à partir de ses caractéristiques architecturales.

Les quatre classes correspondent à des niveaux croissants de
charges énergétiques totales.
""")


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_excel(
    os.path.join(BASE_DIR, "ENB_data.xlsx")
)

df.columns = [
    "relative_compactness",
    "surface_area",
    "wall_area",
    "roof_area",
    "overall_height",
    "orientation",
    "glazing_area",
    "glazing_area_distribution",
    "heating_load",
    "cooling_load"
]


# ============================================================
# CRÉATION DE LA VARIABLE CIBLE
# ============================================================

df["total_charges"] = (
    df["heating_load"] +
    df["cooling_load"]
)

q1 = df["total_charges"].quantile(0.25)
q2 = df["total_charges"].quantile(0.50)
q3 = df["total_charges"].quantile(0.75)

charges_classes = pd.cut(
    df["total_charges"],
    bins=[-np.inf, q1, q2, q3, np.inf],
    labels=[0, 1, 2, 3]
)


# ============================================================
# DONNÉES D'ENTRAÎNEMENT
# ============================================================

data = df.iloc[:, :8]

X_train, X_test, y_train, y_test = train_test_split(
    data,
    charges_classes,
    test_size=0.20,
    random_state=42,
    stratify=charges_classes
)


# ============================================================
# STANDARDISATION
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# ENTRAÎNEMENT RANDOM FOREST
# ============================================================

@st.cache_resource
def train_random_forest(X_train_scaled, y_train):

    rf = RandomForestClassifier(
        random_state=42
    )

    param_grid = {
        "max_features": ["sqrt", "log2", None],
        "min_samples_split": range(2, 31, 2)
    }

    grid = GridSearchCV(
        rf,
        param_grid,
        cv=5,
        scoring="accuracy"
    )

    grid.fit(X_train_scaled, y_train)

    return grid.best_estimator_, grid.best_params_


with st.spinner("🤖 Préparation du modèle..."):

    model, best_params = train_random_forest(
        X_train_scaled,
        y_train
    )


# ============================================================
# FORMULAIRE
# ============================================================

st.markdown("## 🏗️ Caractéristiques du bâtiment")

st.markdown(
    "Renseignez les caractéristiques du bâtiment pour obtenir "
    "une prédiction."
)


col1, col2 = st.columns(2)


with col1:

    relative_compactness = st.number_input(
        "Compacité relative",
        min_value=0.0,
        max_value=1.0,
        value=0.75,
        step=0.01
    )

    surface_area = st.number_input(
        "Surface totale",
        min_value=0.0,
        value=500.0,
        step=10.0
    )

    wall_area = st.number_input(
        "Surface des murs",
        min_value=0.0,
        value=300.0,
        step=10.0
    )

    roof_area = st.number_input(
        "Surface du toit",
        min_value=0.0,
        value=150.0,
        step=10.0
    )


with col2:

    overall_height = st.number_input(
        "Hauteur globale",
        min_value=0.0,
        value=3.5,
        step=0.1
    )

    orientation = st.selectbox(
        "Orientation",
        options=[2, 3, 4, 5],
        format_func=lambda x: {
            2: "2 — Nord",
            3: "3 — Est",
            4: "4 — Sud",
            5: "5 — Ouest"
        }.get(x, str(x))
    )

    glazing_area = st.number_input(
        "Surface vitrée",
        min_value=0.0,
        max_value=1.0,
        value=0.25,
        step=0.01
    )

    glazing_distribution = st.selectbox(
        "Distribution de la surface vitrée",
        options=[0, 1, 2, 3, 4, 5]
    )


# ============================================================
# PRÉDICTION
# ============================================================

st.markdown("---")

if st.button(
    "🚀 Prédire la classe énergétique",
    use_container_width=True
):

    new_building = pd.DataFrame({
        "relative_compactness": [relative_compactness],
        "surface_area": [surface_area],
        "wall_area": [wall_area],
        "roof_area": [roof_area],
        "overall_height": [overall_height],
        "orientation": [orientation],
        "glazing_area": [glazing_area],
        "glazing_area_distribution": [glazing_distribution]
    })

    new_building_scaled = scaler.transform(
        new_building
    )

    prediction = model.predict(
        new_building_scaled
    )[0]

    probabilities = model.predict_proba(
        new_building_scaled
    )[0]

    prediction = int(prediction)


    # ========================================================
    # RÉSULTAT
    # ========================================================

    st.markdown("## 🎯 Résultat")

    descriptions = {
        0: "Faibles charges énergétiques",
        1: "Charges énergétiques modérées",
        2: "Charges énergétiques élevées",
        3: "Très fortes charges énergétiques"
    }

    if prediction == 0:

        st.success(
            f"### 🟢 Classe {prediction}"
        )

    elif prediction == 1:

        st.info(
            f"### 🔵 Classe {prediction}"
        )

    elif prediction == 2:

        st.warning(
            f"### 🟠 Classe {prediction}"
        )

    else:

        st.error(
            f"### 🔴 Classe {prediction}"
        )


    st.write(
        f"**{descriptions[prediction]}**"
    )


    # ========================================================
    # PROBABILITÉS
    # ========================================================

    st.markdown("### 📊 Probabilité par classe")

    probability_df = pd.DataFrame({
        "Classe": [
            "Classe 0",
            "Classe 1",
            "Classe 2",
            "Classe 3"
        ],
        "Probabilité": probabilities
    })

    st.bar_chart(
        probability_df.set_index("Classe")
    )


    # ========================================================
    # CONFIANCE
    # ========================================================

    confidence = probabilities[prediction]

    st.metric(
        "Confiance du modèle",
        f"{confidence:.1%}"
    )


# ============================================================
# INFORMATIONS DU MODÈLE
# ============================================================

st.markdown("---")

st.markdown("## 🤖 Modèle utilisé")

col1, col2 = st.columns(2)

with col1:

    st.write(
        "**Algorithme :** Random Forest"
    )

    st.write(
        "**Validation croisée :** 5 folds"
    )

with col2:

    st.write(
        f"**max_features :** "
        f"{best_params['max_features']}"
    )

    st.write(
        f"**min_samples_split :** "
        f"{best_params['min_samples_split']}"
    )


st.markdown("""
### 💡 À retenir

Cette interface transforme le modèle de Machine Learning en un outil
interactif : à partir des caractéristiques architecturales d'un
bâtiment, le modèle estime directement son niveau de charges
énergétiques.

La prédiction repose sur le **Random Forest optimisé par GridSearchCV**,
le modèle ayant obtenu les meilleures performances lors de la
comparaison des algorithmes.
""")
