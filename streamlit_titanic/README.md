# 🚢 Titanic & 🚀 Spaceship Titanic — Machine Learning

Application **Streamlit** consacrée à l'analyse et à la modélisation de deux jeux de données Titanic.

Le projet commence avec le **Titanic historique**, basé sur les données de 891 passagers, puis s'étend au **Spaceship Titanic**, un jeu de données plus récent contenant 13 000 passagers environ.

L'objectif est de mettre en pratique différentes étapes d'un projet de Data Science : exploration des données, visualisation, préparation des données, entraînement de modèles de Machine Learning et analyse des erreurs.

## 📊 Partie 1 — Titanic

La première partie du projet utilise le jeu de données classique du Titanic, contenant **891 passagers**.

L'objectif est de prédire la variable **`Survived`**, indiquant si un passager a survécu au naufrage.

### Pages

1. **Exploration** (`0_Exploration.py`)

   * aperçu des données
   * statistiques descriptives
   * analyse des variables
   * valeurs manquantes

2. **Visualisation** (`1_DataVisualization.py`)

   * répartition des survivants
   * analyse selon le sexe
   * analyse selon la classe
   * distribution des âges
   * corrélations
   * visualisations interactives

3. **Modélisation** (`2_Modélisation.py`)

   * préparation des données
   * gestion des valeurs manquantes
   * encodage des variables catégorielles
   * séparation entraînement/test
   * comparaison de modèles de classification
   * matrice de confusion
   * importance des variables

4. **Profils croisés** (`3_Profils_croisés.py`)

   * analyse croisée de plusieurs caractéristiques des passagers
   * identification de profils associés à la survie

---

# 🚀 Partie 2 — Spaceship Titanic

La deuxième partie reprend le principe du Titanic dans un contexte futuriste.

Le **Spaceship Titanic** a perdu une partie de ses passagers après une collision avec une anomalie spatio-temporelle.

L'objectif est de construire un modèle de Machine Learning capable de prédire si un passager a été **`Transported`** vers une autre dimension.

Cette partie utilise les données Kaggle du **Spaceship Titanic** :

* **8 693 passagers** avec une destination connue pour l'entraînement
* **4 277 passagers** dont le destin doit être prédit

### Données utilisées

* `spaceship_train.csv` — données d'entraînement
* `spaceship_test.csv` — passagers dont la destination doit être prédite

### Préparation des données

Les étapes de préparation comprennent notamment :

* suppression des variables non utilisées (`Name`, `PassengerId`, `Cabin`)
* séparation des variables numériques et catégorielles
* gestion des valeurs manquantes
* imputation par la médiane pour les variables numériques
* imputation par la modalité la plus fréquente pour les variables catégorielles
* encodage One-Hot des variables catégorielles
* séparation du jeu d'entraînement et du jeu de test

### Modélisation

Deux familles de modèles sont comparées :

* **Régression logistique**
* **Random Forest**

Les performances sont étudiées à l'aide de plusieurs métriques :

* Accuracy
* Precision
* Recall
* F1-score
* matrice de confusion

Une attention particulière est portée aux **faux positifs et faux négatifs**, car l'objectif est d'obtenir une estimation aussi fiable que possible du nombre de passagers à secourir.

### Analyse des erreurs

Une section spécifique permet également d'analyser les erreurs du modèle :

* nombre total d'erreurs
* faux positifs
* faux négatifs
* exemples de passagers mal classés
* matrice de confusion

Cette analyse permet de mieux comprendre **où et pourquoi le modèle se trompe**.

---

## 🛠️ Technologies utilisées

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Plotly
* Matplotlib / Seaborn selon les visualisations

## ▶️ Lancer le projet en local

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Puis lancer l'application :

```bash
streamlit run app.py
```

## ☁️ Application en ligne

L'application est disponible sur Streamlit Community Cloud :

**Spaceship Titanic — Machine Learning**

https://madamedatait-titanic.streamlit.app/

## 📁 Structure du projet

```text
streamlit_titanic/
│
├── app.py
├── model_utils.py
├── theme.py
├── requirements.txt
│
├── train.csv
│
├── spaceship_train.csv
├── spaceship_test.csv
│
├── pages/
│   ├── 0_Exploration.py
│   ├── 1_DataVisualization.py
│   ├── 2_Modélisation.py
│   ├── 3_Profils_croisés.py
│   └── 4_Spaceship_Titanic.py
│
└── .streamlit/
    └── config.toml
```

## 🎯 Compétences mises en pratique

Ce projet permet de mettre en évidence plusieurs compétences en Data Science et Machine Learning :

* exploration et compréhension d'un jeu de données
* analyse statistique
* visualisation de données
* traitement des valeurs manquantes
* sélection de variables
* encodage des variables catégorielles
* normalisation des données
* séparation train/test
* entraînement de modèles de classification
* comparaison de modèles
* évaluation avec différentes métriques
* analyse des erreurs
* interprétation d'une matrice de confusion
* développement d'une application interactive avec Streamlit
* organisation d'un projet Data Science dans GitHub

## 💡 Objectif du projet

Au-delà de la performance pure des modèles, ce projet montre la mise en œuvre d'un **workflow complet de Data Science**, depuis l'exploration des données jusqu'à leur utilisation dans une application interactive.

L'ajout du **Spaceship Titanic** permet également de montrer l'évolution du projet vers un problème de Machine Learning plus complet, avec davantage de variables, des valeurs manquantes et une problématique métier autour des erreurs de prédiction.
