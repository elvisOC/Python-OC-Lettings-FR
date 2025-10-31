## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

# Déploiement

## Vue d’ensemble

Le déploiement du projet **Python-OC-Lettings-FR** est automatisé avec **GitHub Actions** (CI) et **Render** (CD).  
Chaque commit poussé sur la branche `master` déclenche, si tout passe :

1. Lint / tests / couverture (CI)  
2. Build et push de l'image Docker (si activé)  
3. Déclenchement du déploiement sur Render via l'API (CD)  
4. Notification d'une release vers **Sentry** pour le suivi et la traçabilité

---

## Configuration requise

### Technologies
- Django 5.x, Python 3.11+  
- Docker (pour build d'image)  
- Render.com (hébergement) ou VPS (alternative)  
- GitHub Actions (CI/CD)  
- Sentry (supervision / release tracking)

### Arborescence utile

```bash
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # Pipeline GitHub Actions
├── oc_lettings_site/
│   └── settings.py            # Config Django (env, Whitenoise, Sentry)
├── entrypoint.sh              # Script exécuté au démarrage (collectstatic, migrate, gunicorn)
├── requirements.txt
├── README.md
└── manage.py
```

## Variables d’environnement nécessaires

Les variables doivent être définies **sur Render** (ou VPS) et certains secrets **dans GitHub**.

### A définir sur Render (Dashboard → Environment)
| Nom | Rôle | Exemple |
|-----|------|---------|
| `SECRET_KEY` | Clé Django (obligatoire en prod) | `p7&f3r8a9...` |
| `DEBUG` | Mode debug | `False` |
| `ALLOWED_HOSTS` | Domaines autorisés (sans `https://`) | `python-oc-lettings-fr-y4n6.onrender.com` |
| `SENTRY_DSN` | DSN Sentry pour capturer erreurs | `https://...ingest.sentry.io/...` |

> **Ne jamais** committer `.env` ou secrets dans le dépôt.

### Secrets GitHub requis (Settings → Secrets and variables → Actions)
| Nom | Usage |
|-----|-------|
| `RENDER_API_KEY` | Appel API pour déclencher un deploy sur Render |
| `RENDER_SERVICE_ID` | ID du service Render (visible dans l'URL du service) |
| `DOCKERHUB_TOKEN` | (si push d'image Docker vers DockerHub) |
| `SENTRY_AUTH_TOKEN` | Token Sentry pour créer les releases (voir scopes) |
| `SENTRY_ORG` | Slug de l'organisation Sentry (`de-geitere-elvis`) |
| `SENTRY_PROJECT` | Slug du projet Sentry (`oc-lettings`) |
