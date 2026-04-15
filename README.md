# PAL — Plateforme AgriLivingLab (MVP)

Ce dépôt contient une plateforme **Living Lab** orientée terrain (agriculteurs) + recherche (chercheurs), construite en **MVP** :
- côté **backend** : API Django 6 + DRF + SimpleJWT + django-cors-headers
- côté **frontend** : Next.js 16 (App Router, webpack) + React 19 + TypeScript + Tailwind 4 + next-pwa

L’objectif du MVP est de :
- permettre aux **agriculteurs** de rejoindre une **expérimentation** et d’envoyer des **observations terrain** (photo/audio/texte)
- permettre aux **chercheurs** de créer des expérimentations, consulter les observations et répondre via **feedback**
- proposer des **formations** audio/vidéo (données statiques côté frontend)
- assurer une UX simple, mobile-first, avec états vides et messages clairs

---

## 1) Architecture

### Backend (Django)
- Dossier : `backend/`
- Stack : Django 6 + Django REST Framework + SimpleJWT + django-cors-headers
- Base de données : SQLite (`db.sqlite3`)
- Média : upload de fichiers (observations) servi via `/media/` en mode `DEBUG`
- Dépendances : `backend/requirements.txt`

### Frontend (Next.js)
- Dossier : `frontend/`
- Stack : Next.js 16.2.3 (App Router, webpack) + React 19 + TypeScript 5 + Tailwind 4 + next-pwa 5
- PWA : manifest (`/manifest.json`) + service worker auto-généré en production
- Polices : Geist Sans / Geist Mono (Google Fonts)
- Auth : tokens JWT stockés en localStorage :
  - `pal_access` (access token)
  - `pal_refresh` (refresh token)
  - `pal_formations_completed` (IDs des formations terminées)

---

## 2) Rôles & navigation

Rôles utilisateurs (`backend/users/models.py` — `UserRole` TextChoices) :
- `FARMER` — agriculteur, peut participer aux expérimentations et envoyer des observations
- `RESEARCHER` — chercheur, peut créer des expérimentations et donner du feedback
- `ADMIN` — administrateur (page placeholder pour le moment)
- `CONTENT_CREATOR` — présent dans le modèle, pas exploité dans l’UX MVP

Modèle User (custom, `AbstractUser`) :
- champs supplémentaires : `role`, `phone`, `language`, `location`

Redirections après login :
- `FARMER` → `/dashboard`
- `RESEARCHER` → `/researcher`
- `ADMIN` → `/admin`
- Support du paramètre `next` : `/login?next=/observations` → redirection vers `next` après login

---

## 3) Pages frontend (routes App Router)

| Route | Composant | Accès | Description |
|---|---|---|---|
| `/` | `page.tsx` | public | Accueil : connexion/inscription ou accès à l’espace |
| `/login` | `login/page.tsx` | public | Formulaire de connexion (username + password) |
| `/register` | `register/page.tsx` | public | Inscription (username, email, role, password) |
| `/dashboard` | `dashboard/page.tsx` | `FARMER` | Dashboard agriculteur : onboarding, boutons observations/expérimentations/formations |
| `/researcher` | `researcher/page.tsx` | `RESEARCHER` | Espace chercheur : mes expérimentations + observations terrain + feedback |
| `/researcher/create-experiment` | `researcher/create-experiment/page.tsx` | `RESEARCHER` | Formulaire de création d’expérimentation |
| `/admin` | `admin/page.tsx` | `ADMIN` | Placeholder admin |
| `/experiments` | `experiments/page.tsx` | auth | Liste des expérimentations + bouton "Participer" (FARMER) |
| `/observations` | `observations/page.tsx` | auth | Envoi d’observation (photo/audio/texte) + liste avec feedbacks |
| `/formations` | `formations/page.tsx` | auth | Liste des formations (audio/vidéo) |
| `/formations/[id]` | `formations/[id]/page.tsx` | auth | Lecteur de formation + progression + marquage terminé |
| `/notifications` | `notifications/page.tsx` | auth | Placeholder MVP |

---

## 4) Fonctionnalités implémentées

### A) Authentification
- **Backend** : register (`RegisterView`), login (`TokenObtainPairView`), refresh (`TokenRefreshView`), me (`MeView`)
- **Frontend** : `AuthContext` gère login/logout/refreshMe, tokens en localStorage
- **Protection des routes** : composant `AuthGate`
  - si non connecté → redirection vers `/login?next=...`
  - vérification du rôle (si `allowedRoles` fourni)
  - écran "Vérification…" pendant le chargement
  - si token invalide → `logout()` + retour `/login`
  - écran "Accès non autorisé" si le rôle ne correspond pas

### B) Navigation
- Composant : `Navbar.tsx`
- **Desktop** : header sticky en haut (logo PAL + liens + bouton logout)
- **Mobile** : navbar sticky en bas (5 icônes : 🏠 Accueil, 📚 Formations, 🧪 Expérimentations, 📸 Observations, 🔔 Notifications)
- Layout : `pb-20` sur mobile pour éviter que la bottom-nav masque le contenu

### C) Module "Experiments"
#### Backend
- Modèles (`backend/experiments/models.py`) :
  - `Experiment` : `title`, `description`, `protocol`, `created_by` (FK User), `created_at`
  - `Participation` : `user` (FK), `experiment` (FK), `joined_at` + contrainte unique (user, experiment)
- ViewSet (`ExperimentViewSet`) : `get`, `post` uniquement
  - `GET /api/experiments/` — liste (auth)
  - `POST /api/experiments/` — création (RESEARCHER only, vérifié via `IsResearcher`)
  - `POST /api/experiments/{id}/join/` — participation (FARMER only, vérifié via `IsFarmer`)
- Permissions : `IsResearcher`, `IsFarmer` (`backend/experiments/permissions.py`)

#### Frontend
- Liste des expérimentations avec micro-guidage
- Bouton "🧪 Participer" visible uniquement pour les FARMER
- Message succès : "Tu participes maintenant à ce test."
- État vide : "Aucune expérimentation disponible"

### D) Module "Observations"
#### Backend
- Modèle (`backend/observations/models.py`) :
  - `ObservationType` : `IMAGE`, `AUDIO`, `TEXT`
  - `Observation` : `user` (FK), `experiment` (FK optionnelle), `type`, `file` (FileField), `description`, `geo_location`, `created_at`
- ViewSet (`ObservationViewSet`) : parsers `MultiPartParser` + `FormParser`
  - `GET /api/observations/` — liste (FARMER ne voit que ses observations, RESEARCHER voit tout)
  - `POST /api/observations/` — création multipart, `user` auto-rempli
- Serializer : inclut `file_url` (URL absolue via `request.build_absolute_uri`)

#### Frontend
- Bouton principal "📸 Prendre une photo" + bouton secondaire "🎤 Enregistrer audio"
- Preview image/audio après sélection
- Champ texte optionnel + select expérimentation (optionnel)
- Liste "Mes observations" avec affichage des feedbacks reçus
- Badge "Nouveau" sur les feedbacks de moins de 48h

### E) Module "Feedback"
#### Backend
- Modèle (`backend/feedback/models.py`) :
  - `Feedback` : `observation` (FK), `researcher` (FK), `comment`, `created_at`
- Vues :
  - `POST /api/feedback/` — création (RESEARCHER only, `IsResearcher`)
  - `GET /api/feedback/{observation_id}/` — liste par observation (FARMER limité à ses observations)
- Serializer : `researcher` auto-rempli, `created_at` read-only

#### Frontend
- Côté chercheur (`/researcher`) : textarea "Répondre" sous chaque observation + bouton "Envoyer"
- Côté agriculteur (`/observations`) : bloc "Réponse du chercheur" avec fond indigo + badge "Nouveau" si récent (<48h)

### F) Module "Formations"
#### Backend
- Modèles (`backend/formations/models.py`) :
  - `Course` : `title`, `description`, `language` (FR / WOLOF), `type` (audio / video), `content_url`, `created_at`
  - `UserCourse` : `user` (FK), `course` (FK), `completed` (boolean), `progress` (int, optionnel), `created_at` + contrainte unique (user, course)
- ViewSet (`CourseViewSet`) :
  - `GET /api/formations/` — liste des cours (auth)
  - `GET /api/formations/{id}/` — détail d’un cours (auth)
  - `GET /api/formations/my-courses/` — liste des cours de l’utilisateur (auth, avec statut completed)
  - `POST /api/formations/{id}/complete/` — marquer un cours comme terminé (auth, crée/maj UserCourse)
- Seed : `python manage.py seed_courses` — 4 cours (3 FR + 1 WOLOF)

#### Frontend
- Liste (`/formations`) : connectée à l’API backend, titre, type, langue, boutons "▶️ Suivre" / "⏯ Continuer" / "🔄 Revoir" + "⬇️ Télécharger"
- Toggle multilingue : 🌐 Toutes / 🇫🇷 Français / 🇸🇳 Wolof
- Lecteur (`/formations/[id]`) : player audio/vidéo natif, barre de progression, bouton "Marquer comme terminé" (via API), bouton 🌾 "Tester dans mon champ" → `/observations`
- Progression sauvegardée via l’API (`UserCourse`)

### G) Dashboards
- **Farmer** (`/dashboard`) : onboarding en 4 étapes (🎓 Formation → 🌾 Test → 📸 Observation → 💬 Feedback), section 📚 "Mes formations" avec bouton "⏯ Continuer", gros boutons d’accès
- **Researcher** (`/researcher`) : "Mes expérimentations" (filtrées par `created_by`) + "Observations terrain" (toutes) + formulaire feedback intégré
- **Admin** (`/admin`) : placeholder

### H) Notifications
- Page placeholder (`/notifications`) : "Placeholder MVP"

---

## 5) Endpoints API (résumé)

Auth (`/api/auth/`) :
- `POST /api/auth/register/` — inscription (AllowAny)
- `POST /api/auth/login/` — login (TokenObtainPairView → access + refresh)
- `POST /api/auth/refresh/` — refresh token (TokenRefreshView)
- `GET /api/auth/me/` — utilisateur courant (auth)

Experiments (`/api/experiments/`) :
- `GET /api/experiments/` — liste (auth)
- `POST /api/experiments/` — création (RESEARCHER)
- `POST /api/experiments/{id}/join/` — participation (FARMER)

Observations (`/api/observations/`) :
- `GET /api/observations/` — liste (FARMER : ses observations uniquement ; autres : tout)
- `POST /api/observations/` — création multipart (auth)

Feedback (`/api/feedback/`) :
- `POST /api/feedback/` — création (RESEARCHER)
- `GET /api/feedback/{observation_id}/` — liste par observation (FARMER limité à ses observations)

Formations (`/api/formations/`) :
- `GET /api/formations/` — liste des cours (auth)
- `GET /api/formations/{id}/` — détail d’un cours (auth)
- `GET /api/formations/my-courses/` — cours de l’utilisateur avec statut (auth)
- `POST /api/formations/{id}/complete/` — marquer comme terminé (auth)

Admin Django :
- `GET /admin/` — interface d’administration Django

---

## 6) Modèles de données

```
User (AbstractUser)
├── role        CharField (FARMER / RESEARCHER / ADMIN / CONTENT_CREATOR)
├── phone       CharField (blank)
├── language    CharField (blank)
└── location    CharField (blank)

Experiment
├── title       CharField
├── description TextField (blank)
├── protocol    TextField (blank)
├── created_by  FK → User
└── created_at  DateTimeField (auto)

Participation
├── user        FK → User
├── experiment  FK → Experiment
├── joined_at   DateTimeField (auto)
└── UniqueConstraint (user, experiment)

Observation
├── user         FK → User
├── experiment   FK → Experiment (null)
├── type         CharField (image / audio / text)
├── file         FileField (observations/)
├── description  TextField (blank)
├── geo_location CharField (blank)
└── created_at   DateTimeField (auto)

Feedback
├── observation  FK → Observation
├── researcher   FK → User
├── comment      TextField
└── created_at   DateTimeField (auto)

Course
├── title        CharField
├── description  TextField (blank)
├── language     CharField (FR / WOLOF)
├── type         CharField (audio / video)
├── content_url  URLField
└── created_at   DateTimeField (auto)

UserCourse
├── user         FK → User
├── course       FK → Course
├── completed    BooleanField (default=False)
├── progress     PositiveSmallIntegerField (default=0)
├── created_at   DateTimeField (auto)
└── UniqueConstraint (user, course)
```

---

## 7) Lancer le projet en local (Windows)

### Prérequis
- Python 3.13+ avec pip
- Node.js 18+ avec npm

### Backend
1) Ouvrir un terminal dans `backend/`
2) (Optionnel) Créer/activer un venv :
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3) Installer les dépendances :
   ```powershell
   pip install -r requirements.txt
   ```
4) Migrations :
   ```powershell
   python manage.py migrate
   ```
5) (Optionnel) Seed des formations :
   ```powershell
   python manage.py seed_courses
   ```
6) Démarrer l’API :
   - local uniquement : `python manage.py runserver`
   - accès via IP LAN : `python manage.py runserver 0.0.0.0:8000`

### Frontend
1) Ouvrir un terminal dans `frontend/`
2) Installer : `npm install`
3) Démarrer : `npm run dev`
4) Build production : `npm run build`

---

## 8) Notes "dev LAN" (accès via IP, ex. téléphone)

Quand tu ouvres l’app via `http://192.168.x.x:3000`, il faut :
- **Next dev** : autoriser l’origine HMR via `allowedDevOrigins` dans `frontend/next.config.ts` (déjà configuré : `192.168.1.178`, `localhost`, `127.0.0.1`)
- **Django** : `ALLOWED_HOSTS` et `CORS_ALLOWED_ORIGINS` dans `backend/pal_backend/settings.py` doivent inclure l’IP LAN (actuel : `192.168.1.178`)
- **Django** doit écouter sur `0.0.0.0:8000`
- **Frontend** : si `NEXT_PUBLIC_API_BASE_URL` n’est pas défini, `frontend/src/lib/api.ts` utilise `window.location.hostname` comme host fallback (`http://<hostname>:8000`)

---

## 9) Configuration JWT

Défini dans `backend/pal_backend/settings.py` :
- Access token : 60 minutes
- Refresh token : 7 jours

---

## 10) Choix MVP / principes

- Pas de logique avancée de refresh token côté frontend (MVP)
- Pas de SSR complexifié
- UX mobile-first : boutons plus gros, spacing, messages courts, états vides explicites
- Message pédagogique "Apprends puis teste dans ton champ" présent partout (formations, observations, expérimentations, dashboard)
- Flux pédagogique : 🎓 Formation → 🌾 Expérimentation → 📸 Observation → 💬 Feedback
- Multilingue : toggle FR/WOLOF sur les formations, au moins 1 contenu wolof
- Formations dynamiques via API backend (plus de données statiques)
- Notifications en placeholder
- Admin en placeholder
- PWA configuré (service worker en production uniquement, désactivé en dev)

---

## 11) Où continuer (idées simples, sans complexifier)

- Implémenter la page Notifications (liste des feedbacks reçus, etc.)
- Implémenter la page Admin (gestion utilisateurs, contenus, statistiques)
- Ajouter plus de contenus wolof
- Harmoniser les micro-textes (ton/phrases) sur toutes les pages
- Ajouter 1-2 composants UI réutilisables (Alert/EmptyState) pour éviter duplication
- Ajouter une page healthcheck côté backend
- Ajouter des icônes PWA dans `manifest.json`

---

## 12) Repères fichiers importants

Backend :
- `backend/requirements.txt` — dépendances Python
- `backend/pal_backend/settings.py` — CORS, ALLOWED_HOSTS, MEDIA, JWT, INSTALLED_APPS
- `backend/pal_backend/urls.py` — routes API racines
- `backend/users/models.py` — custom User + UserRole
- `backend/users/serializers.py` — RegisterSerializer, UserPublicSerializer
- `backend/users/views.py` — RegisterView, MeView
- `backend/users/urls.py` — register, login, refresh, me
- `backend/experiments/models.py` — Experiment, Participation
- `backend/experiments/views.py` — ExperimentViewSet (list, create, join)
- `backend/experiments/permissions.py` — IsResearcher, IsFarmer
- `backend/observations/models.py` — Observation, ObservationType
- `backend/observations/views.py` — ObservationViewSet
- `backend/observations/serializers.py` — ObservationSerializer (avec file_url)
- `backend/feedback/models.py` — Feedback
- `backend/feedback/views.py` — FeedbackCreateView, FeedbackByObservationView
- `backend/feedback/permissions.py` — IsResearcher
- `backend/formations/models.py` — Course, UserCourse
- `backend/formations/views.py` — CourseViewSet (list, retrieve, my-courses, complete)
- `backend/formations/serializers.py` — CourseSerializer, UserCourseSerializer
- `backend/formations/management/commands/seed_courses.py` — seed 4 cours (3 FR + 1 WOLOF)

Frontend :
- `frontend/package.json` — dépendances (Next 16, React 19, Tailwind 4, next-pwa)
- `frontend/next.config.ts` — PWA + allowedDevOrigins
- `frontend/public/manifest.json` — manifest PWA
- `frontend/src/context/AuthContext.tsx` — AuthProvider, useAuth (login, logout, refreshMe)
- `frontend/src/components/AuthGate.tsx` — protection des routes par rôle
- `frontend/src/components/Navbar.tsx` — navigation desktop + mobile bottom bar
- `frontend/src/lib/api.ts` — client API (authFetch, toutes les fonctions d’appel API)
- `frontend/src/lib/formations.ts` — données statiques des formations
- `frontend/src/app/layout.tsx` — layout racine (Providers + Navbar)
- `frontend/src/app/providers.tsx` — AuthProvider wrapper
- `frontend/src/app/page.tsx` — page d’accueil
- `frontend/src/app/login/page.tsx` — page de connexion
- `frontend/src/app/register/page.tsx` — page d’inscription
- `frontend/src/app/dashboard/page.tsx` — dashboard agriculteur
- `frontend/src/app/researcher/page.tsx` — espace chercheur
- `frontend/src/app/researcher/create-experiment/page.tsx` — création expérimentation
- `frontend/src/app/admin/page.tsx` — placeholder admin
- `frontend/src/app/experiments/page.tsx` — liste expérimentations
- `frontend/src/app/observations/page.tsx` — observations + feedbacks
- `frontend/src/app/formations/page.tsx` — liste formations
- `frontend/src/app/formations/[id]/page.tsx` — lecteur formation
- `frontend/src/app/notifications/page.tsx` — placeholder notifications
