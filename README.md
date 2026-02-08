# 🥤 Distributeur Intelligent de Boissons Locales - Backend

Backend du projet de distributeur intelligent pour l'ESI (École Supérieure d'Informatique) - Université Nazi BONI.

## 📋 Description

API REST développée avec Flask pour gérer :
- ✅ Enregistrement des ventes de boissons (bissap, zoom-koom, tamarin)
- ✅ Collecte des données des capteurs (température, niveaux)
- ✅ Système d'alertes automatiques
- ✅ Statistiques en temps réel
- ✅ Dashboard administrateur

---

## 🛠️ Technologies utilisées

- **Python 3.11**
- **Flask 3.0** - Framework web
- **SQLite** - Base de données
- **SQL pur** - Pas d'ORM
- **Gunicorn** - Serveur de production

---

## 📦 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd distributeur-backend
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Modifier .env selon vos besoins
```

4. **Initialiser la base de données**
```bash
python database.py
```

5. **Lancer le serveur**
```bash
python app.py
```

Le serveur sera accessible sur `http://localhost:5000`

---

## 🧪 Tests

### Générer des données de démo
```bash
python scripts/init_demo.py
```

Crée :
- 100+ ventes sur 7 jours
- Mesures régulières
- Alertes de test

### Tester toutes les routes API
```bash
python scripts/test_api.py
```

Teste automatiquement toutes les routes de l'API.

---

## 📚 Documentation

- **[API.md](docs/API.md)** - Documentation complète de l'API
- **[INSTALLATION.md](docs/INSTALLATION.md)** - Guide d'installation détaillé
- **[DEPLOIEMENT.md](docs/DEPLOIEMENT.md)** - Guide de déploiement sur Render.com

---

## 🚀 Déploiement sur Render.com

Voir le guide complet : [docs/DEPLOIEMENT.md](docs/DEPLOIEMENT.md)

**Résumé rapide :**

1. Créer un compte sur render.com
2. Créer un nouveau Web Service
3. Connecter votre repo GitHub
4. Render détecte automatiquement Flask
5. Déploiement en un clic !

---

## 📊 Routes API principales

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Page d'accueil |
| POST | `/api/vente` | Enregistrer une vente |
| GET | `/api/ventes` | Toutes les ventes |
| POST | `/api/mesure` | Enregistrer une mesure |
| GET | `/api/etat` | État de la machine |
| GET | `/api/statistiques` | Stats complètes |
| GET | `/api/alertes` | Alertes actives |

Documentation complète : [docs/API.md](docs/API.md)

---

## 📁 Structure du projet
```
distributeur-backend/
├── app.py                  # Application principale
├── database.py             # Gestion BDD
├── config.py               # Configuration
├── services/
│   └── statistiques.py    # Calculs statistiques
├── scripts/
│   ├── init_demo.py       # Données de test
│   └── test_api.py        # Tests API
├── docs/                   # Documentation
└── logs/                   # Fichiers de logs
```

---

## 👥 Équipe

**Projet tutoré L3 IRS - Thème 20**

- Membre 1 : [Nom]
- Membre 2 : [Nom]

**Superviseur :** M. Kiélem Wilfried Albert Duniwangda

**Année universitaire :** 2025-2026

---

## 📝 Licence

Projet académique - Université Nazi BONI - ESI

---

## 📞 Contact

Pour toute question :
- Email superviseur : wilfried.kielem@u-naziboni.net
- Téléphone : 58 49 84 77