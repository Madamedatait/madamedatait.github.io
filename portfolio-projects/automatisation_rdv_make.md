# ⚙️ Automatisation de Prise de Rendez-vous — Make

**Auteure :** Lavinia Bulgarean-Haiduc
**Stack :** Make (Integromat), Google Sheets, Google Calendar
**Objectif :** Éliminer la saisie manuelle des rendez-vous en connectant un formulaire de prise de rendez-vous directement à un agenda partagé.

---

## 📋 Contexte

Ce scénario s'adresse à tout professionnel qui gère des rendez-vous (cabinet médical, consultant, salon, coach...) et qui perd du temps à reporter manuellement chaque nouvelle demande dans son agenda.

**Cas d'usage concret :** un patient remplit un formulaire en ligne avec son prénom, son nom et la date souhaitée pour un rendez-vous. Cette réponse s'enregistre automatiquement dans une feuille Google Sheets. Sans automatisation, quelqu'un doit ensuite ouvrir le calendrier et créer l'événement à la main — une tâche répétitive, source d'oublis et d'erreurs de saisie.

**Avec Make, ce processus devient entièrement automatique** : dès qu'une nouvelle ligne apparaît dans le Google Sheets, un événement est créé instantanément dans Google Calendar, avec le bon nom de patient et le bon créneau horaire — sans aucune intervention humaine.

---

## 🔧 Architecture du scénario

Le scénario s'articule autour de **3 modules** :

```
[1] Google Sheets          [2] Formatage de date        [3] Google Calendar
 Watch Rows         ───►      (Set Variable)        ───►    Create Event
 (nouvelle réponse                (normalisation                (création de
  au formulaire)                   du format date)                l'événement)
```

### Module 1 — Google Sheets : Watch Rows

Ce module surveille en continu la feuille "Rendez-vous" et déclenche le scénario dès qu'une nouvelle ligne est ajoutée (donc dès qu'un patient valide le formulaire). Il récupère automatiquement toutes les colonnes : horodatage, prénom, nom et date du rendez-vous souhaitée.

```json
{
  "module": "google-sheets:watchRows",
  "parameters": {
    "mode": "fromAll",
    "sheetId": "Rendez-vous",
    "includesHeaders": true
  }
}
```

### Module 2 — Normalisation de la date

Les dates issues d'un Google Forms arrivent souvent dans un format texte non standard (avec des "/"). Ce module les convertit dans un format compatible avec Google Calendar, en remplaçant les séparateurs :

```
New_Date = replace(Date_du_rendez-vous, "/", "-")
```

C'est une étape de nettoyage de données essentielle : sans cette conversion, Google Calendar peut mal interpréter la date ou rejeter l'événement.

### Module 3 — Google Calendar : Create Event

Ce module crée l'événement final dans l'agenda, avec un mapping dynamique basé sur les données récupérées :

```json
{
  "summary": "Rendez-vous avec {{Prénom}} {{Nom}}",
  "start": "{{New_Date}} 10:00",
  "end": "{{New_Date}} 11:00",
  "calendar": "Calendrier_Médecin",
  "visibility": "default"
}
```

Le titre de l'événement est généré automatiquement à partir du prénom et du nom du patient, et le créneau est fixé de 10h à 11h (un seul rendez-vous standardisé par jour, conformément au cas d'usage).

---

## 💡 Valeur ajoutée pour un client

Ce type d'automatisation permet de :

- **Supprimer une tâche répétitive et chronophage** — plus besoin de vérifier le formulaire et de reporter manuellement chaque demande
- **Éliminer les erreurs de saisie** — le nom et la date sont repris automatiquement, sans risque de faute de frappe
- **Réagir instantanément** — l'événement apparaît dans l'agenda dès la soumission du formulaire, pas en fin de journée
- **Gagner en fiabilité** — aucun rendez-vous oublié faute de temps pour la saisie manuelle

---

## 🔁 Adaptable à d'autres contextes

La même logique (formulaire → tableur → agenda) s'applique facilement à d'autres métiers : prise de rendez-vous chez un coach, réservation de créneaux pour un consultant, inscriptions à un atelier, demandes de rappel commercial... Le scénario peut être enrichi avec des modules supplémentaires : envoi d'un email de confirmation au patient, notification Slack à l'équipe, ou vérification de disponibilité avant la création de l'événement.

---
*Projet réalisé dans le cadre de ma formation Data Analyst · [madamedatait.com](https://madamedatait.com)*
