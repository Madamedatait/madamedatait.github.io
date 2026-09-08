import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
)
import plotly.express as px


st.set_page_config(
    page_title="Energy Efficiency — Modélisation",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Modélisation")
st.subheader("Comparaison de trois modèles de classification")


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv(
    os.path.join(BASE_DIR, "ENB_data.csv"),
    sep=";"
)


# ============================================================
# PRÉPARATION DES DONNÉES
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

# Les 8 variables explicatives
data = df.iloc[:, :8]

# Séparation train / test
X_train, X_test, y_train, y_test = train_test_split(
    data,
    charges_classes,
    test_size=0.20,
    random_state=42,
    stratify=charges_classes
)

# Standardisation
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown("""
### 🎯 Objectif

L'objectif est de prédire la **classe énergétique d'un bâtiment**
à partir de ses caractéristiques architecturales.

Trois familles de modèles sont comparées :

- **K-Nearest Neighbors (KNN)**
- **Support Vector Machine (SVM)**
- **Random Forest**

Pour chaque modèle, les hyperparamètres sont sélectionnés à l'aide
d'une validation croisée avec **GridSearchCV**.
""")


# ============================================================
# INDICATEURS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏢 Données d'entraînement",
        f"{len(X_train):,}"
    )

with col2:
    st.metric(
        "🧪 Données de test",
        f"{len(X_test):,}"
    )

with col3:
    st.metric(
        "🎯 Classes",
        "4"
    )

with col4:
    st.metric(
        "📊 Validation croisée",
        "5 folds"
    )


# ============================================================
# ENTRAÎNEMENT DES MODÈLES
# ============================================================

st.markdown("## ⚙️ Recherche des meilleurs modèles")


@st.cache_resource
def train_models(X_train_scaled, y_train):

    # --------------------------------------------------------
    # KNN
    # --------------------------------------------------------

    knn = KNeighborsClassifier()

    param_grid_knn = {
        "n_neighbors": range(2, 51)
    }

    grid_knn = GridSearchCV(
        knn,
        param_grid_knn,
        cv=5,
        scoring="accuracy"
    )

    grid_knn.fit(X_train_scaled, y_train)

    # --------------------------------------------------------
    # SVM
    # --------------------------------------------------------

    svm_model = SVC()

    param_grid_svm = {
        "kernel": ["rbf", "linear"],
        "C": [0.1, 1, 10, 50]
    }

    grid_svm = GridSearchCV(
        svm_model,
        param_grid_svm,
        cv=5,
        scoring="accuracy"
    )

    grid_svm.fit(X_train_scaled, y_train)

    # --------------------------------------------------------
    # RANDOM FOREST
    # --------------------------------------------------------

    rf = RandomForestClassifier(
        random_state=42
    )

    param_grid_rf = {
        "max_features": ["sqrt", "log2", None],
        "min_samples_split": range(2, 31, 2)
    }

    grid_rf = GridSearchCV(
        rf,
        param_grid_rf,
        cv=5,
        scoring="accuracy"
    )

    grid_rf.fit(X_train_scaled, y_train)

    return grid_knn, grid_svm, grid_rf


with st.spinner("🔄 Recherche des meilleurs hyperparamètres..."):
    grid_knn, grid_svm, grid_rf = train_models(
        X_train_scaled,
        y_train
    )


# ============================================================
# RÉSULTATS DES HYPERPARAMÈTRES
# ============================================================

st.markdown("## 🔧 Meilleurs hyperparamètres")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("### 🟢 KNN")

    st.write(
        f"**n_neighbors :** "
        f"{grid_knn.best_params_['n_neighbors']}"
    )

    st.write(
        f"**Score CV :** "
        f"{grid_knn.best_score_:.2%}"
    )


with col2:

    st.markdown("### 🔵 SVM")

    st.write(
        f"**C :** "
        f"{grid_svm.best_params_['C']}"
    )

    st.write(
        f"**Kernel :** "
        f"{grid_svm.best_params_['kernel']}"
    )

    st.write(
        f"**Score CV :** "
        f"{grid_svm.best_score_:.2%}"
    )


with col3:

    st.markdown("### 🟠 Random Forest")

    st.write(
        f"**max_features :** "
        f"{grid_rf.best_params_['max_features']}"
    )

    st.write(
        f"**min_samples_split :** "
        f"{grid_rf.best_params_['min_samples_split']}"
    )

    st.write(
        f"**Score CV :** "
        f"{grid_rf.best_score_:.2%}"
    )


# ============================================================
# PRÉDICTIONS
# ============================================================

y_pred_knn = grid_knn.predict(X_test_scaled)
y_pred_svm = grid_svm.predict(X_test_scaled)
y_pred_rf = grid_rf.predict(X_test_scaled)


accuracy_knn = accuracy_score(
    y_test,
    y_pred_knn
)

accuracy_svm = accuracy_score(
    y_test,
    y_pred_svm
)

accuracy_rf = accuracy_score(
    y_test,
    y_pred_rf
)


# ============================================================
# COMPARAISON
# ============================================================

st.markdown("## 📊 Performance sur le jeu de test")

results = pd.DataFrame({
    "Modèle": [
        "KNN",
        "SVM",
        "Random Forest"
    ],
    "Accuracy": [
        accuracy_knn,
        accuracy_svm,
        accuracy_rf
    ]
})

st.dataframe(
    results.style.format(
        {"Accuracy": "{:.2%}"}
    ),
    use_container_width=True,
    hide_index=True
)


fig = px.bar(
    results,
    x="Modèle",
    y="Accuracy",
    text="Accuracy",
    title="Comparaison des performances"
)

fig.update_traces(
    texttemplate="%{text:.2%}",
    textposition="outside"
)

fig.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# MODÈLE GAGNANT
# ============================================================

best_model_name = results.loc[
    results["Accuracy"].idxmax(),
    "Modèle"
]

best_accuracy = results["Accuracy"].max()


st.markdown("## 🏆 Modèle le plus performant")

if best_model_name == "Random Forest":

    st.success(
        f"🏆 **Random Forest** est le modèle le plus performant "
        f"avec une accuracy de **{best_accuracy:.2%}** sur le jeu de test."
    )

else:

    st.success(
        f"🏆 **{best_model_name}** est le modèle le plus performant "
        f"avec une accuracy de **{best_accuracy:.2%}**."
    )


# ============================================================
# MATRICES DE CONFUSION
# ============================================================

st.markdown("## 🔢 Matrices de confusion")

model_choice = st.selectbox(
    "Choisissez un modèle",
    [
        "KNN",
        "SVM",
        "Random Forest"
    ]
)


if model_choice == "KNN":
    cm = confusion_matrix(y_test, y_pred_knn)

elif model_choice == "SVM":
    cm = confusion_matrix(y_test, y_pred_svm)

else:
    cm = confusion_matrix(y_test, y_pred_rf)


fig_cm = px.imshow(
    cm,
    text_auto=True,
    x=["Classe 0", "Classe 1", "Classe 2", "Classe 3"],
    y=["Classe 0", "Classe 1", "Classe 2", "Classe 3"],
    labels={
        "x": "Classe prédite",
        "y": "Classe réelle",
        "color": "Nombre"
    },
    title=f"Matrice de confusion — {model_choice}"
)

st.plotly_chart(
    fig_cm,
    use_container_width=True
)


# ============================================================
# CONCLUSION
# ============================================================

st.markdown("## 💡 Conclusion")

st.markdown("""
La comparaison montre que les trois modèles permettent de distinguer
les quatre niveaux de charges énergétiques.

Le **Random Forest** obtient la meilleure performance sur l'ensemble
de test avec une accuracy de **96,10 %** dans l'étude réalisée.

La recherche d'hyperparamètres avec `GridSearchCV` permet de sélectionner
automatiquement les configurations les plus performantes à partir
d'une validation croisée.
""")
