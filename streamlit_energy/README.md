# 🏢 Energy Efficiency — Machine Learning

Application interactive Streamlit consacrée à l'analyse et à la classification de l'efficacité énergétique de bâtiments résidentiels.

🌐 **Application en ligne :**  
https://madamedatait-energy.streamlit.app/

---

## 🎯 Présentation du projet

Ce projet utilise le dataset **Energy Efficiency** afin d'analyser les caractéristiques architecturales de bâtiments résidentiels et leur impact sur les charges énergétiques.

Le dataset contient **768 configurations de bâtiments** décrites par différentes caractéristiques architecturales, notamment la compacité, la surface, la hauteur, l'orientation et la surface vitrée.

L'objectif est de construire un modèle de **Machine Learning** capable de classer les bâtiments selon leur niveau de charges énergétiques.

---

## 📊 Données

Le dataset contient notamment les variables suivantes :

- Relative Compactness
- Surface Area
- Wall Area
- Roof Area
- Overall Height
- Orientation
- Glazing Area
- Glazing Area Distribution
- Heating Load
- Cooling Load

Les deux variables énergétiques principales sont :

- 🔥 `Heating Load`
- ❄️ `Cooling Load`

---

## 🧠 Objectif Machine Learning

Les charges de chauffage et de climatisation sont combinées afin de créer une nouvelle variable :

```text
total_charges = heating_load + cooling_load
