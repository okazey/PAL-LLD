# PLAN D’ACTION — PAL (Plateforme AgriLivingLab)
Base de travail:
C:\WEBDEV\LivingLAB\cahier des charges technique.md
C:\WEBDEV\LivingLAB\cahier des charges.md

## Contexte

Tu es un architecte logiciel senior, développeur fullstack et product builder.

Ta mission est de concevoir et développer une plateforme appelée :

**PAL — Plateforme AgriLivingLab**

## Objectif

Construire une plateforme numérique combinant :

- Formation agricole (LMS)
- Collecte de données terrain
- Expérimentation participative (Living Lab)
- Système de notification
- Analyse et suivi d’impact

## Contrainte fondamentale

La plateforme doit être :

- Un simple LMS : interdit
- Un système Living Lab interactif et évolutif : obligatoire

## Utilisateurs (RBAC)

Implémenter les rôles suivants :

- FARMER
- RESEARCHER
- ADMIN
- CONTENT_CREATOR (optionnel)

## Scénarios utilisateurs (User Flows)

### Scénario 1 — Formation

- Un agriculteur crée un compte
- Il accède à un module en wolof
- Il télécharge le contenu
- Il suit la formation offline
- Il complète un quiz

### Scénario 2 — Expérimentation

- Un chercheur crée une expérimentation
- Les agriculteurs reçoivent une notification
- L’agriculteur participe
- Il envoie photo + commentaire
- Le chercheur analyse

### Scénario 3 — Observation terrain

- L’agriculteur observe un problème
- Il envoie photo + audio
- Le système stocke
- Le chercheur consulte et répond

## Architecture technique

- Backend
  - Django + Django REST Framework
  - Authentification JWT
- Frontend
  - Web : React / Next.js
  - Mobile : Flutter ou PWA
- Base de données
  - PostgreSQL
- Stockage
  - Fichiers médias (images/audio) via S3 ou équivalent

### Structure backend

- /users
- /courses
- /observations
- /experiments
- /participations
- /feedback
- /notifications
- /analytics
- /media

## Modèle de données

### User

- id
- name
- phone
- role
- language
- location

### Course

- id
- title
- language
- type (video/audio/text)
- downloadable

### Experiment

- id
- title
- description
- protocol
- created_by
- start_date
- end_date

### Participation

- id
- user_id
- experiment_id
- status
- joined_at

### Observation

- id
- user_id
- experiment_id (nullable)
- type (image/audio/text)
- file_url
- description
- geo_location
- created_at

### Feedback

- id
- observation_id
- researcher_id
- comment
- created_at

### Notification

- id
- user_id
- type
- message
- read

## API à implémenter

### Auth

- POST /auth/register
- POST /auth/login

### Courses

- GET /courses
- GET /courses/{id}
- POST /courses

### Experiments

- POST /experiments
- GET /experiments
- POST /experiments/{id}/join

### Observations

- POST /observations
- GET /observations
- GET /observations/{id}

### Feedback

- POST /feedback
- GET /feedback/{observation}

### Notifications

- GET /notifications
- POST /notifications/send

### Analytics

- GET /analytics/dashboard

## Modules fonctionnels

### Formation (LMS)

- Cours audio, vidéo, texte
- Audio prioritaire
- Quiz
- Progression
- Certification
- Téléchargement offline

### Living Lab (core)

- Observations
  - Envoi photo/audio/texte
  - Description
  - Géolocalisation optionnelle
- Expérimentations
  - Création par chercheur
  - Protocole
  - Participation agriculteurs
  - Suivi
- Feedback
  - Réponse chercheurs
  - Amélioration continue

### Notifications

Types :

- Nouvelle formation
- Nouvelle expérimentation
- Rappel participation

Canaux :

- In-app
- SMS (priorité)
- Push (optionnel)

### Offline mode (critique)

- Téléchargement contenu
- Stockage local
- Synchronisation différée

Implémentation :

- Local storage / SQLite
- File queue sync

### Analytics

Dashboard :

- Utilisateurs actifs
- Progression
- Participation
- Données terrain

### Communauté

- Forum simple
- Commentaires
- Groupes régionaux

## Workflow Living Lab

Implémenter ce cycle :

- Création d’expérimentation
- Notification
- Participation
- Collecte données
- Analyse
- Feedback
- Amélioration

Fonctionnalités associées :

- Statut expérimentations
- Suivi participants
- Timeline des observations

## UX / UI

Contraintes :

- Interface très simple
- Gros boutons
- Icônes visuelles
- Audio privilégié
- Navigation minimale

## Écrans à créer

### Agriculteur

- Accueil
- Cours
- Lecteur audio/vidéo
- Envoyer observation
- Notifications

### Chercheur

- Dashboard
- Créer expérimentation
- Analyser données

### Admin

- Gestion utilisateurs
- Contenus
- Statistiques

## Dashboard impact

Indicateurs :

- Utilisateurs actifs
- Taux de complétion
- Participation aux expérimentations
- Volume de données terrain

## Test terrain intégré

Le système doit permettre :

- Collecte feedback utilisateur
- Amélioration continue
- Validation terrain

## Contraintes techniques

- Faible connectivité
- Android bas de gamme
- Optimisation performance
- Simplicité maximale

## Règles de développement

- Ne pas sur-complexifier
- Prioriser usage terrain
- Optimiser rapidité
- Intégrer Living Lab dès le cœur du système

## Livrables attendus

- Backend API complet
- Frontend fonctionnel (web + mobile)
- Base de données structurée
- Système offline opérationnel
- Dashboard analytics

## Résumé final

Construire une plateforme :

- LMS + données terrain + expérimentation + analytics
- Optimisée pour environnement africain
- Avec logique Living Lab native

## Instruction finale

Toujours concevoir PAL comme :

- Une plateforme vivante d’innovation agricole
- Et non comme un simple système de formation