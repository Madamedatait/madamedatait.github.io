🚒 London Fire Brigade — Machine Learning

Application interactive Streamlit consacrée à l'analyse et à la prédiction du temps d'arrivée des secours du London Fire Brigade.

🌐 **Application en ligne :**  
https://madamedatait-firefighter.streamlit.app/


🎯 Présentation du projet

Ce projet analyse des données d'interventions du **London Fire Brigade** afin d'étudier les caractéristiques associées au temps d'arrivée des secours.

L'objectif est de construire une solution de **Machine Learning** capable d'estimer le temps nécessaire aux secours pour arriver sur le lieu d'une intervention à partir de différentes caractéristiques disponibles au moment de l'appel.

Le projet combine ainsi **analyse de données, préparation des variables, Machine Learning et développement d'une application interactive avec Streamlit**.


📊 Données

Le dataset utilisé contient **15 variables** décrivant les interventions et leur contexte.

Les principales informations disponibles sont :

- `IncidentNumber` — identifiant de l'intervention
- `DateAndTimeMobilised` — date et heure de mobilisation
- `AttendanceTimeSeconds` — temps d'arrivée en secondes
- `PlusCode_Description` — description géographique
- `PropertyCategory` — catégorie de propriété
- `IncGeo_BoroughName` — borough de l'intervention
- `NumPumpsAttending` — nombre de véhicules mobilisés
- `Latitude` — latitude du lieu de l'intervention
- `Longitude` — longitude du lieu de l'intervention
- `DeployedFromStation_Name` — station de déploiement
- `DeployedFromStation_Code` — code de la station
- `DateAndTimeOfCall` — date et heure de l'appel
- `HourOfCall` — heure de l'appel
- `IncidentGroup` — groupe d'intervention
- `PropertyType` — type de propriété

La variable cible utilisée pour la prédiction est :

AttendanceTimeSeconds
