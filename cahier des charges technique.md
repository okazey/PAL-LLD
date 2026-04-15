# Cahier des charges technique — AgriLivingLab Platform (ALP)

## 1. Présentation technique du projet

### Nom du projet

AgriLivingLab Platform (ALP)

### Objectif technique

Développer une plateforme numérique (web + mobile) permettant :

- La formation agricole (e-learning)
- La collecte de données terrain
- L’expérimentation participative (Living Lab)
- L’interaction entre agriculteurs, chercheurs et étudiants

## 2. Vision produit (important pour développeurs)

La plateforme doit être conçue comme :

- Un système évolutif combinant LMS + réseau communautaire + outil de collecte terrain + moteur d’expérimentation

> **Note**
> Ce n’est PAS un Moodle classique.

## 3. Types d’utilisateurs (RBAC — Role Based Access Control)

### Agriculteur

- Accéder aux formations
- Télécharger contenus
- Envoyer données terrain (photo, audio, texte)
- Participer aux tests

### Formateur / Chercheur

- Créer contenus
- Lancer expérimentations
- Analyser données

### Administrateur

- Gestion plateforme
- Validation contenus
- Gestion utilisateurs

### Étudiant (optionnel)

- Co-création de contenu
- Analyse données

## 4. Modules fonctionnels (core system)

### Module 1 : Learning (LMS)

#### Fonctionnalités

- Création de cours
- Modules (vidéo, audio, texte)
- Quiz
- Progression utilisateur
- Certificats

#### Contraintes

- Vidéos compressées
- Support audio prioritaire
- Multilingue (FR + Wolof)

### Module 2 : Living Lab (innovation core)

#### Fonctionnalités clés

- Soumission d’observations terrain
  - Texte
  - Photo
  - Audio
- Participation à expérimentations
  - Ex : “tester engrais X”
  - Formulaires dynamiques
  - Feedback utilisateur

#### Bonus (phase 2)

- Géolocalisation des données
- Timeline des cultures

### Module 3 : Data & Analytics

- Dashboard admin
  - Taux d’adoption
  - Progression
  - Données terrain
- Dashboard chercheurs
  - Analyse des expérimentations
  - Export données (CSV)

### Module 4 : Communauté

- Forum simple
- Commentaires
- Groupes (par région)

### Module 5 : Offline mode (critique)

- Téléchargement cours
- Synchronisation différée
- Stockage local (mobile)

## 5. Architecture technique recommandée

### Architecture globale

#### Option recommandée (scalable)

- Frontend
  - Web : React.js / Next.js
  - Mobile : Flutter (ou PWA si budget limité)
- Backend
  - Framework : Django / Flask (Python)
  - API : REST ou GraphQL
- Base de données
  - PostgreSQL
- Stockage fichiers
  - AWS S3 / MinIO

#### Alternative rapide (MVP)

- Moodle (backend LMS)
- API custom pour Living Lab
- App mobile connectée à Moodle

> **Note**
> Recommandé si tu veux aller vite.

## 6. Sécurité & accès

- Authentification JWT
- Rôles utilisateurs
- Chiffrement des données sensibles
- Sauvegardes automatiques

## 7. Contraintes techniques clés

### Connectivité faible

- Lazy loading
- Cache local
- Sync différée

### Compatibilité

- Android priorité
- Bas de gamme (≤2GB RAM)

### Langues

- FR + Wolof
- Architecture i18n

## 8. API principales (exemples)

### Auth

- POST /auth/register
- POST /auth/login

### Learning

- GET /courses
- GET /courses/{id}
- POST /progress

### Living Lab

- POST /observations
- GET /experiments
- POST /participation

### Data

- GET /analytics

## 9. Modèle de données simplifié

- User
  - id
  - role
  - name
  - location
- Course
  - id
  - title
  - language
  - content_type
- Observation
  - id
  - user_id
  - type (photo/audio/text)
  - description
  - timestamp
- Experiment
  - id
  - title
  - protocol
  - participants

## 10. Workflow Living Lab (crucial)

- Création d’une expérimentation (chercheur)
- Notification aux agriculteurs
- Participation terrain
- Collecte données
- Analyse
- Amélioration des pratiques

> **Note**
> Le système doit supporter ce cycle.

## 11. MVP (Minimum Viable Product)

### Objectif

Version test terrain.

### Features MVP

- Inscription utilisateur
- Accès cours (audio + vidéo)
- Téléchargement offline
- Soumission observation (photo + texte)
- Dashboard simple admin

> **Note**
> Pas de complexité inutile.

## 12. Backlog initial (Windsurf ready)

### Sprint 1

- Authentification
- Gestion utilisateurs

### Sprint 2

- Module cours
- Lecture vidéo/audio

### Sprint 3

- Upload observation
- Stockage fichiers

### Sprint 4

- Offline mode basique

### Sprint 5

- Dashboard admin

## 13. Tests

- Tests utilisateurs (agriculteurs réels)
- Tests offline
- Tests performance

> **Note**
> Living Lab = test terrain obligatoire.

## 14. Scalabilité

Prévoir :

- Montée en charge
- Multi-région
- Ajout IA (plus tard)

## 15. Points critiques à ne pas rater

- Faire une plateforme lourde : non
- Ignorer le offline : non
- Négliger le terrain : non

- Simplicité : oui
- Mobile-first : oui
- Data terrain : oui
- Boucle d’amélioration : oui

## Résumé pour Windsurf

Tu peux lui donner ça comme instruction clé :

Construire une plateforme modulaire combinant LMS + collecte de données terrain + système d’expérimentation agricole, optimisée pour faible connectivité, mobile-first, avec support multilingue (français/wolof) et architecture évolutive.