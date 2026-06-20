# Titanic — Prédiction de survie

Application Streamlit explorant le jeu de données Titanic (891 passagers) et
comparant trois modèles de classification binaire pour prédire la survie.

## Pages

1. **Exploration** (`app.py`) — aperçu des données, statistiques descriptives, valeurs manquantes
2. **DataVisualization** — répartitions (survie, genre, classe, âge), corrélations
3. **Modélisation** — entraînement et comparaison de 3 modèles (Random Forest, SVM, Régression logistique), matrice de confusion, importance des variables

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Déployer sur Streamlit Community Cloud (gratuit)

1. Pousse ce dossier complet (avec `data/train.csv`) dans un repo GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io), connecte-toi avec GitHub
3. "New app" → sélectionne le repo → fichier principal `app.py`
4. Déploie

## Structure du projet

```
titanic_project/
├── app.py                          # Page d'accueil (Exploration)
├── model_utils.py                  # Chargement des données + entraînement des modèles
├── theme.py                        # Styles partagés (cohérence visuelle)
├── data/
│   └── train.csv
├── pages/
│   ├── 1_DataVisualization.py
│   └── 2_Modélisation.py
├── .streamlit/
│   └── config.toml                 # Thème (couleurs)
└── requirements.txt
```

## Changements par rapport à la version initiale

- Code réorganisé en plusieurs fichiers (plus lisible, plus facile à maintenir)
- Mise en cache des données et des modèles (`st.cache_data` / `st.cache_resource`) :
  les modèles ne sont plus ré-entraînés à chaque interaction
- Graphiques Matplotlib/Seaborn remplacés par Plotly (interactifs, cohérents avec
  le projet German Credit)
- Matrice de confusion affichée en heatmap plutôt qu'en tableau brut
- Comparaison des 3 modèles en un clic
- Thème violet harmonisé avec le reste du portfolio
