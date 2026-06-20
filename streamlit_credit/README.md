# German Credit — Profil des emprunteurs

Application Streamlit explorant un jeu de données de 1 000 emprunteurs ayant
souscrit un prêt bancaire en Allemagne.

## Pages

1. **Vue d'ensemble** (`app.py`) — qui sont les emprunteurs : âge, logement, motif du prêt
2. **Durée des prêts** — court/moyen/long terme, et ce qui les distingue
3. **Profil & risque** — croisement montant / durée / qualification pour repérer les profils les plus exposés

## Lancer en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

L'app s'ouvre automatiquement dans le navigateur sur `http://localhost:8501`.

## Déployer sur Streamlit Community Cloud (gratuit)

1. Pousse ce dossier complet (avec `data/german_credit_data.csv`) dans un repo GitHub
2. Va sur [share.streamlit.io](https://share.streamlit.io), connecte-toi avec GitHub
3. Clique sur "New app", sélectionne le repo et indique `app.py` comme fichier principal
4. Déploie — tu obtiens une URL publique du type `https://ton-app.streamlit.app`

## Structure du projet

```
credit_project/
├── app.py                          # Page d'accueil (Vue d'ensemble)
├── data_utils.py                   # Chargement et nettoyage des données (partagé)
├── data/
│   └── german_credit_data.csv
├── pages/
│   ├── 1_Durée_des_prêts.py
│   └── 2_Profil_&_risque.py
├── .streamlit/
│   └── config.toml                 # Thème (couleurs)
└── requirements.txt
```

## Données

Source : German Credit Data (UCI Machine Learning Repository / Kaggle).
1 000 individus, 9 variables : âge, sexe, niveau de qualification, type de
logement, comptes épargne/courant, montant et durée du crédit, motif du prêt.
