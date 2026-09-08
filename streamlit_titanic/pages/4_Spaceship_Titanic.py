import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Spaceship Titanic — Machine Learning",
    page_icon="🚀",
    layout="wide",
)

st.title("🚀 Spaceship Titanic")
st.subheader("Prédiction des passagers transportés vers une autre dimension")

st.markdown("""
### 🎯 Objectif

Le Spaceship Titanic a perdu une partie de ses passagers lors d'une
collision avec une anomalie spatio-temporelle.

L'objectif est de construire un modèle de Machine Learning capable de
prédire quels passagers ont été **Transported** vers une autre dimension.
""")

# Chargement des données
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

train = pd.read_csv(
    os.path.join(BASE_DIR, "spaceship_train.csv")
)

test = pd.read_csv(
    os.path.join(BASE_DIR, "spaceship_test.csv")
)

st.success("Données chargées avec succès !")

col1, col2 = st.columns(2)

with col1:
    st.metric("Passagers connus", f"{len(train):,}")

with col2:
    st.metric("Passagers à prédire", f"{len(test):,}")

st.markdown("### 👀 Aperçu des données")

st.dataframe(train.head(), use_container_width=True)

st.markdown("### 📊 Exploration des données")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Informations générales")
    st.write(f"**Nombre de lignes :** {train.shape[0]:,}")
    st.write(f"**Nombre de colonnes :** {train.shape[1]}")

with col2:
    st.markdown("#### Variable cible")
    transported_counts = train["Transported"].value_counts()
    transported_pct = train["Transported"].value_counts(normalize=True) * 100

    st.write(
        f"**Transported = True :** "
        f"{transported_counts.get(True, 0):,} "
        f"({transported_pct.get(True, 0):.1f} %)"
    )

    st.write(
        f"**Transported = False :** "
        f"{transported_counts.get(False, 0):,} "
        f"({transported_pct.get(False, 0):.1f} %)"
    )

st.markdown("#### 🔎 Valeurs manquantes")

missing = (
    train.isna()
    .mean()
    .mul(100)
    .sort_values(ascending=False)
    .reset_index()
)

missing.columns = ["Variable", "Valeurs manquantes (%)"]

st.dataframe(
    missing,
    use_container_width=True,
    hide_index=True
)

st.markdown("#### 🧾 Types de variables")

info = pd.DataFrame({
    "Variable": train.columns,
    "Type": train.dtypes.astype(str).values,
    "Valeurs uniques": [
        train[col].nunique(dropna=True)
        for col in train.columns
    ]
})

st.dataframe(
    info,
    use_container_width=True,
    hide_index=True
)

st.markdown("## 🧹 Préparation des données")

st.markdown("""
Pour entraîner un modèle de Machine Learning, les données doivent être
nettoyées et transformées. Les variables inutiles sont supprimées,
les valeurs manquantes sont remplacées et les variables catégorielles
sont encodées numériquement.
""")

# Copie des données
data = train.copy()

# Suppression des variables non utilisées
data = data.drop(
    columns=["Name", "PassengerId", "Cabin"],
    errors="ignore"
)

# Séparation de la cible et des variables explicatives
X = data.drop(columns=["Transported"])
y = data["Transported"]

# Séparation numérique / catégorielle
num_cols = X.select_dtypes(
    include=["int64", "float64"]
).columns

cat_cols = X.select_dtypes(
    include=["object", "bool"]
).columns

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Variables numériques",
        len(num_cols)
    )

with col2:
    st.metric(
        "Variables catégorielles",
        len(cat_cols)
    )

st.markdown("### 🔧 Gestion des valeurs manquantes")

st.write(
    "Variables numériques : remplacement par la **médiane**."
)

st.write(
    "Variables catégorielles : remplacement par la **modalité la plus fréquente**."
)

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

# Séparation entraînement / test
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=16
)

# Imputation numérique
imputer_num = SimpleImputer(strategy="median")

X_train_num = pd.DataFrame(
    imputer_num.fit_transform(X_train[num_cols]),
    columns=num_cols,
    index=X_train.index
)

X_test_num = pd.DataFrame(
    imputer_num.transform(X_test[num_cols]),
    columns=num_cols,
    index=X_test.index
)

# Imputation catégorielle
imputer_cat = SimpleImputer(strategy="most_frequent")

X_train_cat = pd.DataFrame(
    imputer_cat.fit_transform(X_train[cat_cols]),
    columns=cat_cols,
    index=X_train.index
)

X_test_cat = pd.DataFrame(
    imputer_cat.transform(X_test[cat_cols]),
    columns=cat_cols,
    index=X_test.index
)

st.markdown("### 🔢 Encodage des variables catégorielles")

from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

X_train_cat_encoded = pd.DataFrame(
    encoder.fit_transform(X_train_cat),
    columns=encoder.get_feature_names_out(cat_cols),
    index=X_train.index
)

X_test_cat_encoded = pd.DataFrame(
    encoder.transform(X_test_cat),
    columns=encoder.get_feature_names_out(cat_cols),
    index=X_test.index
)

# Reconstitution des jeux de données
X_train_final = pd.concat(
    [X_train_num, X_train_cat_encoded],
    axis=1
)

X_test_final = pd.concat(
    [X_test_num, X_test_cat_encoded],
    axis=1
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Jeu d'entraînement",
        f"{X_train_final.shape[0]:,} lignes × {X_train_final.shape[1]} variables"
    )

with col2:
    st.metric(
        "Jeu de test",
        f"{X_test_final.shape[0]:,} lignes × {X_test_final.shape[1]} variables"
    )

st.success("✅ Préparation des données terminée.")



# ============================================================
# 🤖 MODÉLISATION
# ============================================================

st.markdown("## 🤖 Modélisation")

st.markdown("""
Nous allons comparer deux modèles de classification issus de familles
différentes afin de prédire si un passager a été transporté vers une
autre dimension.
""")

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Modèle 1 : Régression logistique
logistic_model = LogisticRegression(
    max_iter=1000,
    random_state=16
)

# Modèle 2 : Random Forest
rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=16
)

# Entraînement
logistic_model.fit(X_train_final, y_train)
rf_model.fit(X_train_final, y_train)

# Prédictions
y_pred_logistic = logistic_model.predict(X_test_final)
y_pred_rf = rf_model.predict(X_test_final)

# Fonction d'évaluation
def evaluate_model(y_true, y_pred):
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred),
        "Recall": recall_score(y_true, y_pred),
        "F1-score": f1_score(y_true, y_pred)
    }

scores_logistic = evaluate_model(
    y_test,
    y_pred_logistic
)

scores_rf = evaluate_model(
    y_test,
    y_pred_rf
)

# Tableau comparatif
results = pd.DataFrame(
    [scores_logistic, scores_rf],
    index=["Régression logistique", "Random Forest"]
)

st.markdown("### 📊 Comparaison des modèles")

st.dataframe(
    results.style.format("{:.3f}"),
    use_container_width=True
)

st.markdown("### 🏆 Modèle sélectionné")

st.info("""
Pour notre problème, nous cherchons notamment à contrôler le nombre
de faux positifs et de faux négatifs afin d'obtenir une estimation
fiable du nombre de passagers à secourir.
""")

if scores_logistic["F1-score"] >= scores_rf["F1-score"]:
    best_model = logistic_model
    best_model_name = "Régression logistique"
else:
    best_model = rf_model
    best_model_name = "Random Forest"

st.success(
    f"🏆 Modèle sélectionné : **{best_model_name}**"
)

# ============================================================
# 🔍 ANALYSE DES ERREURS
# ============================================================

st.markdown("## 🔍 Analyse des erreurs")

st.markdown("""
L'analyse des erreurs permet d'identifier les passagers pour lesquels
le modèle s'est trompé.

- **Faux positif (FP)** : le modèle prédit `Transported = True`,
  alors que le passager n'a pas été transporté.
- **Faux négatif (FN)** : le modèle prédit `Transported = False`,
  alors que le passager a réellement été transporté.
""")

# Prédictions du meilleur modèle
y_pred_best = best_model.predict(X_test_final)

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred_best)

tn, fp, fn, tp = cm.ravel()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Vrais négatifs", tn)

with col2:
    st.metric("Faux positifs", fp)

with col3:
    st.metric("Faux négatifs", fn)

with col4:
    st.metric("Vrais positifs", tp)


st.markdown("### 📊 Matrice de confusion")

cm_df = pd.DataFrame(
    cm,
    index=["Réel : False", "Réel : True"],
    columns=["Prédit : False", "Prédit : True"]
)

st.dataframe(
    cm_df,
    use_container_width=True
)


# ------------------------------------------------------------
# Analyse des faux positifs / faux négatifs
# ------------------------------------------------------------

st.markdown("### ❌ Où le modèle se trompe-t-il ?")

errors = X_test.copy()

errors["Réel"] = y_test
errors["Prédit"] = y_pred_best

errors["Erreur"] = errors["Réel"] != errors["Prédit"]

errors_only = errors[errors["Erreur"]].copy()

st.write(
    f"Le modèle a commis **{len(errors_only)} erreurs** "
    f"sur **{len(y_test)} passagers** du jeu de test."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔴 Faux positifs")
    
    false_positive = errors[
        (errors["Réel"] == False) &
        (errors["Prédit"] == True)
    ]
    
    st.metric(
        "Nombre de faux positifs",
        len(false_positive)
    )

with col2:
    st.markdown("#### 🟠 Faux négatifs")
    
    false_negative = errors[
        (errors["Réel"] == True) &
        (errors["Prédit"] == False)
    ]
    
    st.metric(
        "Nombre de faux négatifs",
        len(false_negative)
    )


st.markdown("### 👀 Exemple d'erreurs")

st.dataframe(
    errors_only.head(20),
    use_container_width=True
)

import plotly.figure_factory as ff

fig_cm = ff.create_annotated_heatmap(
    cm,
    x=["Prédit : False", "Prédit : True"],
    y=["Réel : False", "Réel : True"],
    colorscale="Blues"
)

fig_cm.update_layout(
    title="Matrice de confusion",
    xaxis_title="Prédiction",
    yaxis_title="Valeur réelle"
)

st.plotly_chart(
    fig_cm,
    use_container_width=True
)

st.markdown("### 💡 Interprétation")

st.markdown(f"""
Le modèle sélectionné est **{best_model_name}**.

Sur le jeu de test, il a correctement classé **{accuracy_score(y_test, y_pred_best) * 100:.1f} %**
des passagers.

Il a identifié **{tp} passagers transportés** correctement et
**{fn} passagers transportés** ont été manqués par le modèle.

À l'inverse, **{fp} passagers non transportés** ont été considérés à tort
comme transportés.

Cette analyse permet de mieux comprendre les limites du modèle et de
ne pas se limiter à une seule métrique de performance.
""")

# ============================================================
# 🚀 PRÉDICTION DES PASSAGERS INCONNUS
# ============================================================

st.markdown("## 🚀 Prédiction sur les passagers inconnus")

st.markdown("""
Nous appliquons maintenant le même prétraitement au jeu de données
contenant les passagers dont le destin est inconnu.
""")

# Copie du jeu de données inconnu
missing = test.copy()

# Suppression des variables non utilisées
missing = missing.drop(
    columns=["Name", "PassengerId", "Cabin"],
    errors="ignore"
)

# Séparation numérique / catégorielle
missing_num = missing.select_dtypes(
    include=["int64", "float64"]
).columns

missing_cat = missing.select_dtypes(
    include=["object", "bool"]
).columns

# Imputation numérique
missing_num_imputed = pd.DataFrame(
    imputer_num.transform(missing[missing_num]),
    columns=missing_num,
    index=missing.index
)

# Imputation catégorielle
missing_cat_imputed = pd.DataFrame(
    imputer_cat.transform(missing[missing_cat]),
    columns=missing_cat,
    index=missing.index
)

# Encodage catégoriel
missing_cat_encoded = pd.DataFrame(
    encoder.transform(missing_cat_imputed),
    columns=encoder.get_feature_names_out(missing_cat),
    index=missing.index
)

# Reconstitution
X_missing_final = pd.concat(
    [
        missing_num_imputed,
        missing_cat_encoded
    ],
    axis=1
)

# Prédictions avec le meilleur modèle
predictions = best_model.predict(X_missing_final)

# Nombre de passagers transportés
nb_transported = int(predictions.sum())
nb_not_transported = len(predictions) - nb_transported

st.markdown("### 🔮 Résultat des prédictions")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "🚀 Passagers prédits comme transportés",
        f"{nb_transported:,}"
    )

with col2:
    st.metric(
        "🛬 Passagers prédits comme non transportés",
        f"{nb_not_transported:,}"
    )

st.success(
    f"Selon le modèle **{best_model_name}**, "
    f"environ **{nb_transported:,} passagers** parmi les "
    f"{len(test):,} passagers inconnus auraient été transportés "
    f"vers une autre dimension."
)
