# 🚀 Guide de déploiement - Render.com

Guide complet pour déployer le backend du distributeur ESI sur Render.com gratuitement.

---

## 📋 Table des matières

1. [Pourquoi Render.com ?](#pourquoi-rendercom)
2. [Prérequis](#prérequis)
3. [Préparation du projet](#préparation-du-projet)
4. [Déploiement sur Render](#déploiement-sur-render)
5. [Configuration des variables d'environnement](#configuration-des-variables-denvironnement)
6. [Vérification du déploiement](#vérification-du-déploiement)
7. [Mise à jour de l'application](#mise-à-jour-de-lapplication)
8. [Surveillance et logs](#surveillance-et-logs)
9. [Limitations du plan gratuit](#limitations-du-plan-gratuit)
10. [Dépannage](#dépannage)

---

## 🤔 Pourquoi Render.com ?

### Avantages

✅ **Gratuit** - Plan gratuit généreux (750h/mois)  
✅ **Simple** - Déploiement en quelques clics  
✅ **Automatique** - Redéploiement à chaque push Git  
✅ **HTTPS** - Certificat SSL gratuit  
✅ **Logs** - Interface de visualisation des logs  
✅ **Base de données** - PostgreSQL gratuit (optionnel)

### Alternatives

| Service | Gratuit | Complexité | Recommandé pour |
|---------|---------|------------|-----------------|
| **Render.com** | ✅ Oui | ⭐ Facile | ✅ Projets étudiants |
| Railway.app | ⚠️ Limité | ⭐ Facile | Petits projets |
| Heroku | ❌ Non | ⭐⭐ Moyen | Production |
| PythonAnywhere | ✅ Oui | ⭐⭐ Moyen | Projets Python |
| AWS/Azure | ⚠️ Crédit étudiant | ⭐⭐⭐ Complexe | Apprentissage cloud |

**Choix recommandé pour ce projet : Render.com** 🎯

---

## 📦 Prérequis

### 1. Compte GitHub

Vous devez avoir :
- ✅ Un compte GitHub actif
- ✅ Votre projet poussé sur GitHub

**Créer un compte GitHub :**
1. Allez sur [github.com](https://github.com)
2. Cliquez sur "Sign up"
3. Suivez les instructions

### 2. Compte Render.com

**Créer un compte Render :**
1. Allez sur [render.com](https://render.com)
2. Cliquez sur "Get Started"
3. **Connectez-vous avec GitHub** (recommandé)

✅ Aucune carte bancaire requise pour le plan gratuit !

---

## 🔧 Préparation du projet

### Étape 1 : Vérifier les fichiers requis

Votre projet doit contenir ces fichiers à la racine :
```
distributeur-backend/
├── app.py                 ✅ Fichier principal
├── requirements.txt       ✅ Dépendances
├── Procfile              ✅ Commande de démarrage
├── runtime.txt           ✅ Version Python
├── database.py           ✅ Gestion BDD
├── config.py             ✅ Configuration
├── .env.example          ✅ Exemple de config
├── services/             ✅ Modules
└── scripts/              ✅ Scripts
```

### Étape 2 : Vérifier Procfile

Le fichier `Procfile` doit contenir :
```
web: gunicorn app:app
```

**🎓 Explication :**
- `web` : Type de service
- `gunicorn` : Serveur de production Python
- `app:app` : `app` (fichier) `:` `app` (variable Flask)

### Étape 3 : Vérifier requirements.txt
```txt
Flask==3.0.0
Flask-CORS==4.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

**⚠️ Important :** `gunicorn` doit être présent !

### Étape 4 : Vérifier runtime.txt
```
python-3.11.0
```

Ou toute version Python 3.9+

### Étape 5 : Créer un fichier .gitignore

Créez `.gitignore` à la racine :
```
# Environnement virtuel
venv/
env/

# Variables d'environnement
.env

# Base de données locale
*.db

# Logs
logs/
*.log

# Python
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/
```

**🎓 Pourquoi ?** On ne veut pas pousser les fichiers sensibles sur GitHub.

---

## 🌐 Pousser le projet sur GitHub

### Si vous n'avez pas encore de repo GitHub
```bash
# 1. Initialiser Git dans votre projet
cd distributeur-backend
git init

# 2. Ajouter tous les fichiers
git add .

# 3. Premier commit
git commit -m "Initial commit - Backend distributeur ESI"

# 4. Créer un nouveau repo sur GitHub
# Allez sur github.com → New repository → Nom: "distributeur-backend"

# 5. Lier votre projet au repo GitHub
git remote add origin https://github.com/VOTRE_USERNAME/distributeur-backend.git

# 6. Pousser le code
git branch -M main
git push -u origin main
```

### Si vous avez déjà un repo GitHub
```bash
git add .
git commit -m "Préparation pour déploiement Render"
git push origin main
```

✅ **Votre code est maintenant sur GitHub !**

---

## 🚀 Déploiement sur Render

### Étape 1 : Se connecter à Render

1. Allez sur [dashboard.render.com](https://dashboard.render.com)
2. Connectez-vous avec GitHub

### Étape 2 : Créer un nouveau Web Service

1. Cliquez sur **"New +"** en haut à droite
2. Sélectionnez **"Web Service"**

### Étape 3 : Connecter votre repo GitHub

**Option A : Repo public**
1. Cherchez votre repo : `distributeur-backend`
2. Cliquez sur **"Connect"**

**Option B : Repo privé**
1. Cliquez sur **"Configure account"**
2. Autorisez Render à accéder à vos repos privés
3. Retournez et sélectionnez votre repo

### Étape 4 : Configurer le service

**Remplissez le formulaire :**

| Champ | Valeur |
|-------|--------|
| **Name** | `distributeur-esi-backend` |
| **Region** | Frankfurt (EU Central) |
| **Branch** | `main` |
| **Root Directory** | (vide) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | **Free** |

**🎓 Explication :**
- **Name** : URL de votre app sera `https://distributeur-esi-backend.onrender.com`
- **Region** : Choisir le plus proche (Europe)
- **Build Command** : Installe les dépendances
- **Start Command** : Lance le serveur (depuis Procfile)

### Étape 5 : Configurer les variables d'environnement

Descendez jusqu'à **"Environment Variables"** et ajoutez :

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `FLASK_DEBUG` | `False` |
| `FLASK_HOST` | `0.0.0.0` |
| `FLASK_PORT` | `10000` |
| `SECRET_KEY` | `GENEREZ_UNE_CLE_ALEATOIRE_ICI` |
| `DATABASE_NAME` | `distributeur.db` |
| `SEUIL_NIVEAU_BAS` | `20` |
| `SEUIL_TEMPERATURE_HAUTE` | `15.0` |
| `CORS_ORIGINS` | `*` |

**🔐 Générer une SECRET_KEY sécurisée :**
```python
import secrets
print(secrets.token_hex(32))
```

Copiez le résultat dans `SECRET_KEY`.

### Étape 6 : Lancer le déploiement

1. Cliquez sur **"Create Web Service"** en bas
2. Render commence le déploiement

**Vous verrez :**
```
==> Cloning from https://github.com/VOTRE_USERNAME/distributeur-backend...
==> Installing dependencies...
==> Building...
==> Deploying...
==> Your service is live 🎉
```

⏱️ **Temps de déploiement :** 2-5 minutes

---

## ✅ Vérification du déploiement

### Étape 1 : Trouver l'URL de votre app

En haut de la page, vous verrez :
```
https://distributeur-esi-backend.onrender.com
```

### Étape 2 : Tester l'API

**Dans votre navigateur :**
```
https://distributeur-esi-backend.onrender.com/
```

**Résultat attendu :**
```json
{
  "message": "🥤 Serveur du Distributeur ESI",
  "version": "3.0",
  "statut": "opérationnel"
}
```

### Étape 3 : Tester une route API
```
https://distributeur-esi-backend.onrender.com/api/etat
```

**Résultat :**
```json
{
  "succes": false,
  "statut_machine": "hors_ligne",
  "message": "Aucune donnée reçue de l'ESP32"
}
```

✅ **C'est normal !** L'ESP32 n'envoie pas encore de données.

### Étape 4 : Tester avec Postman

**POST** `https://distributeur-esi-backend.onrender.com/api/vente`

Body :
```json
{
  "boisson": "bissap",
  "mode": "web"
}
```

**Résultat :**
```json
{
  "succes": true,
  "message": "Vente de bissap enregistrée",
  "id": 1
}
```

🎉 **Félicitations ! Votre API est en ligne !**

---

## 🔄 Mise à jour de l'application

### Déploiement automatique

**Render redéploie automatiquement à chaque push sur GitHub !**
```bash
# 1. Modifier votre code localement
nano app.py

# 2. Commit et push
git add .
git commit -m "Amélioration de l'API"
git push origin main

# 3. Render détecte le push et redéploie automatiquement
```

Vous verrez dans le dashboard Render :
```
==> Deploy triggered by push to main
==> Building...
==> Deploying...
==> Live (v2) 🎉
```

### Déploiement manuel

Si vous voulez forcer un redéploiement :

1. Allez sur le dashboard Render
2. Cliquez sur **"Manual Deploy"** en haut à droite
3. Sélectionnez **"Deploy latest commit"**

---

## 📊 Surveillance et logs

### Voir les logs en temps réel

1. Dashboard Render → Votre service
2. Onglet **"Logs"**
3. Vous verrez tous les logs du serveur

**Exemple :**
```
2026-02-07 16:30:12 - INFO - DÉMARRAGE DU SERVEUR DISTRIBUTEUR ESI
2026-02-07 16:32:45 - INFO - Vente enregistrée : bissap (mode: bouton)
```

### Télécharger les logs

Cliquez sur **"Download logs"** pour sauvegarder localement.

### Alertes (plan payant)

Sur le plan gratuit, vous pouvez uniquement consulter les logs manuellement.

---

## ⚠️ Limitations du plan gratuit

### Temps d'inactivité

❌ **Le serveur s'endort après 15 minutes d'inactivité**

**Impact :**
- Première requête après inactivité : ~30 secondes de délai
- Requêtes suivantes : normales

**Solutions :**
1. **Accepter le délai** (OK pour projet étudiant)
2. **Pinger le serveur toutes les 14 minutes** (script externe)
3. **Passer au plan payant** ($7/mois = serveur toujours actif)

### Limites mensuelles

| Ressource | Limite gratuite |
|-----------|-----------------|
| Heures d'activité | 750h/mois |
| Bande passante | 100 GB/mois |
| Build minutes | 500 min/mois |
| Stockage | Éphémère (réinitialisé) |

**🎓 Explication "Stockage éphémère" :**
- La base de données SQLite est **réinitialisée à chaque redéploiement**
- Pour persistance, il faut utiliser PostgreSQL (gratuit sur Render)

### Solution : Utiliser PostgreSQL (optionnel)

**Si vous voulez des données persistantes :**

1. Créer une base PostgreSQL sur Render
2. Modifier `database.py` pour utiliser PostgreSQL au lieu de SQLite
3. Ajouter `psycopg2-binary` à `requirements.txt`

**Pour ce projet étudiant, SQLite est suffisant** ✅

---

## 🔧 Dépannage

### Problème 1 : "Build failed"

**Cause :** Erreur dans `requirements.txt` ou dépendances manquantes

**Solution :**
1. Vérifiez les logs de build
2. Testez localement : `pip install -r requirements.txt`
3. Corrigez et re-push

### Problème 2 : "Application Error"

**Cause :** Erreur dans le code Python

**Solution :**
1. Consultez les logs Render
2. Reproduisez l'erreur localement
3. Corrigez et re-push

### Problème 3 : "Service unavailable"

**Cause :** Le serveur s'est endormi (inactivité > 15 min)

**Solution :**
- Attendez ~30 secondes, le serveur se réveille automatiquement

### Problème 4 : CORS errors

**Symptôme :** Erreur dans le navigateur :
```
Access to fetch has been blocked by CORS policy
```

**Solution :**
Vérifiez la variable d'environnement `CORS_ORIGINS` sur Render :
```
CORS_ORIGINS=*
```

Ou spécifiez votre domaine :
```
CORS_ORIGINS=https://votre-frontend.com
```

### Problème 5 : Base de données vide après redéploiement

**Cause :** SQLite est éphémère sur Render

**Solution :**
- Créer des données de test automatiquement au démarrage
- Ou utiliser PostgreSQL pour persistence

**Script automatique :**

Modifiez `app.py` :
```python
if __name__ == '__main__':
    initialiser_base()
    
    # En production, créer des données de démo si la base est vide
    if os.getenv('FLASK_ENV') == 'production':
        if compter_ventes_jour() == 0:
            logger.info("Base vide détectée, création de données de démo...")
            from scripts.init_demo import generer_donnees_demo
            generer_donnees_demo()
    
    app.run(...)
```

### Problème 6 : Variables d'environnement non reconnues

**Solution :**
1. Dashboard Render → Votre service
2. Onglet **"Environment"**
3. Vérifiez que toutes les variables sont présentes
4. Cliquez sur **"Save Changes"**
5. Le service redémarre automatiquement

---

## 🔗 Configurer l'ESP32 pour Render

### Modifier l'URL dans le code ESP32

Au lieu de :
```cpp
String serverURL = "http://192.168.1.100:5000";
```

Utilisez :
```cpp
String serverURL = "https://distributeur-esi-backend.onrender.com";
```

**⚠️ Important :** Utilisez `https://` (pas `http://`)

### Exemple complet
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* serverURL = "https://distributeur-esi-backend.onrender.com";

void envoyerVente(String boisson) {
  HTTPClient http;
  
  String url = String(serverURL) + "/api/vente";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  StaticJsonDocument<200> doc;
  doc["boisson"] = boisson;
  doc["mode"] = "bouton";
  
  String requestBody;
  serializeJson(doc, requestBody);
  
  int httpCode = http.POST(requestBody);
  
  if (httpCode == 201) {
    Serial.println("✅ Vente enregistrée sur Render");
  } else {
    Serial.printf("❌ Erreur: %d\n", httpCode);
  }
  
  http.end();
}
```

---

## 📈 Monitoring du service

### Dashboard Render

Le dashboard vous montre :
- ✅ État du service (Live / Building / Failed)
- 📊 Utilisation CPU/RAM
- 📈 Requêtes par minute
- 🕐 Temps de réponse
- 💾 Bande passante utilisée

### Health checks

Render ping automatiquement votre service toutes les X minutes.

**Endpoint de health check :**
```
GET https://votre-app.onrender.com/
```

Si le serveur ne répond pas, Render le redémarre automatiquement.

---

## 💰 Passer au plan payant (optionnel)

| Plan | Prix | Avantages |
|------|------|-----------|
| **Starter** | $7/mois | • Pas d'endormissement<br>• 1 Go RAM<br>• Priorité build |
| **Standard** | $25/mois | • 2 Go RAM<br>• Autoscaling<br>• Support prioritaire |

**Pour ce projet étudiant, le plan gratuit suffit largement** ✅

---

## 📞 Support Render

- **Documentation :** [docs.render.com](https://docs.render.com)
- **Community :** [community.render.com](https://community.render.com)
- **Status page :** [status.render.com](https://status.render.com)

---

## ✅ Checklist finale

Avant de considérer le déploiement terminé :

- [ ] L'URL publique fonctionne
- [ ] La route `/` retourne le JSON attendu
- [ ] Les routes `/api/vente` et `/api/etat` fonctionnent
- [ ] Les logs sont visibles dans le dashboard
- [ ] Les variables d'environnement sont configurées
- [ ] L'ESP32 peut communiquer avec l'URL Render (tester)
- [ ] Le dashboard frontend peut récupérer les données

---

## 🎯 Résumé

**Ce que vous avez maintenant :**
- ✅ API backend accessible publiquement
- ✅ URL HTTPS sécurisée
- ✅ Déploiement automatique à chaque push GitHub
- ✅ Logs centralisés
- ✅ Gratuit pendant toute la durée du projet

**URL finale :**
```
https://distributeur-esi-backend.onrender.com
```

**Prochaines étapes :**
1. ✅ Backend déployé
2. 🔄 Développer le code ESP32
3. 🔄 Créer le frontend (dashboard)

---

## 📝 Notes importantes pour le rapport

**À mentionner dans votre rapport :**

1. **Choix technologique justifié**
   - Render.com choisi pour sa simplicité et gratuité
   - Plan gratuit suffisant pour un projet étudiant
   - Alternative : Raspberry Pi local (plus de contrôle, mais maintenance)

2. **Architecture cloud**
   - Backend hébergé sur serveurs européens (Frankfurt)
   - Certificat SSL automatique
   - Scalabilité possible si besoin

3. **Limitations acceptées**
   - Endormissement après 15 min (acceptable pour démo)
   - Base de données SQLite éphémère (solution : PostgreSQL)
   - 750h/mois largement suffisant

4. **Avantages démontrés**
   - Accessible depuis n'importe où (ESP32, dashboard, mobile)
   - Pas de configuration serveur complexe
   - Déploiement en 5 minutes

---

**Dernière mise à jour :** 7 février 2026

**Auteurs :** Équipe Projet Distributeur ESI - L3 IRS
```

---

## 🎉 RÉCAPITULATIF COMPLET DU BACKEND

Félicitations ! Vous avez maintenant un **backend production-ready complet** :

### ✅ Ce qui est terminé

1. **Code backend Python/Flask**
   - ✅ Toutes les routes API fonctionnelles
   - ✅ Base de données SQLite avec SQL pur
   - ✅ Système de statistiques avancées
   - ✅ Alertes automatiques
   - ✅ Gestion d'erreurs robuste
   - ✅ Logs système

2. **Configuration**
   - ✅ Variables d'environnement (`.env`)
   - ✅ Config dev/production séparées
   - ✅ Fichiers de déploiement (Procfile, runtime.txt)

3. **Scripts utilitaires**
   - ✅ `init_demo.py` - Données de test
   - ✅ `test_api.py` - Tests automatisés

4. **Documentation**
   - ✅ `README.md` - Documentation principale
   - ✅ `docs/API.md` - Documentation API complète
   - ✅ `docs/INSTALLATION.md` - Guide d'installation
   - ✅ `docs/DEPLOIEMENT.md` - Guide déploiement Render

---

## 📊 Structure finale complète
```
distributeur-backend/
│
├── app.py                          ✅ Application Flask principale
├── database.py                     ✅ Gestion base de données
├── config.py                       ✅ Configuration
│
├── requirements.txt                ✅ Dépendances Python
├── Procfile                        ✅ Commande démarrage (Render)
├── runtime.txt                     ✅ Version Python
├── .env                            ✅ Variables d'environnement
├── .env.example                    ✅ Exemple de configuration
├── .gitignore                      ✅ Fichiers à ignorer
│
├── services/                       ✅ Modules logique métier
│   ├── __init__.py
│   └── statistiques.py            ✅ Calculs statistiques
│
├── scripts/                        ✅ Scripts utilitaires
│   ├── init_demo.py               ✅ Données de démonstration
│   └── test_api.py                ✅ Tests automatisés
│
├── docs/                           ✅ Documentation
│   ├── API.md                     ✅ Doc API complète
│   ├── INSTALLATION.md            ✅ Guide installation
│   └── DEPLOIEMENT.md             ✅ Guide déploiement
│
├── logs/                           ✅ Fichiers de logs
│   └── serveur.log
│
├── distributeur.db                 ✅ Base de données SQLite
│
└── README.md                       ✅ Documentation principale