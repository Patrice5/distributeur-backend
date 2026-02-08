# 🛠️ Guide d'installation - Backend Distributeur ESI

Guide complet pour installer et configurer le backend sur différentes plateformes.

---

## 📋 Prérequis

### Matériel
- Ordinateur avec au minimum :
  - 2 Go de RAM
  - 500 Mo d'espace disque
  - Connexion internet (pour installation)

### Logiciels
- **Python 3.9 ou supérieur** (recommandé : Python 3.11)
- **pip** (gestionnaire de paquets Python)
- **Git** (optionnel, pour cloner le projet)

---

## 💻 Installation sur Windows

### Étape 1 : Installer Python

1. Téléchargez Python depuis [python.org](https://www.python.org/downloads/)
2. **Important :** Cochez "Add Python to PATH" lors de l'installation
3. Vérifiez l'installation :
```cmd
python --version
pip --version
```

### Étape 2 : Télécharger le projet

**Option A : Avec Git**
```cmd
git clone https://github.com/votre-repo/distributeur-backend.git
cd distributeur-backend
```

**Option B : Sans Git**
1. Téléchargez le fichier ZIP du projet
2. Extrayez-le dans un dossier (ex: `C:\distributeur-backend`)
3. Ouvrez l'invite de commandes dans ce dossier

### Étape 3 : Créer un environnement virtuel (recommandé)
```cmd
python -m venv venv
venv\Scripts\activate
```

Vous devriez voir `(venv)` au début de votre ligne de commande.

### Étape 4 : Installer les dépendances
```cmd
pip install -r requirements.txt
```

### Étape 5 : Configurer l'environnement
```cmd
copy .env.example .env
```

Modifiez `.env` avec Notepad si nécessaire.

### Étape 6 : Initialiser la base de données
```cmd
python database.py
```

**Résultat attendu :**
```
✅ Base de données initialisée avec succès
📁 Fichier : distributeur.db
```

### Étape 7 : (Optionnel) Générer des données de test
```cmd
python scripts\init_demo.py
```

### Étape 8 : Lancer le serveur
```cmd
python app.py
```

**Résultat :**
```
🚀 Démarrage du serveur...
📍 URL : http://localhost:5000
```

✅ **Le serveur est maintenant accessible sur `http://localhost:5000`**

### Étape 9 : Tester

Ouvrez votre navigateur et allez sur : `http://localhost:5000`

Vous devriez voir :
```json
{
  "message": "🥤 Serveur du Distributeur ESI",
  "version": "3.0",
  "statut": "opérationnel"
}
```

---

## 🐧 Installation sur Linux (Ubuntu/Debian)

### Étape 1 : Installer Python et pip
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv git -y
```

Vérifiez :
```bash
python3 --version
pip3 --version
```

### Étape 2 : Télécharger le projet
```bash
git clone https://github.com/votre-repo/distributeur-backend.git
cd distributeur-backend
```

### Étape 3 : Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate
```

### Étape 4 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 5 : Configurer
```bash
cp .env.example .env
nano .env  # Ou vim, gedit, etc.
```

### Étape 6 : Initialiser la base
```bash
python3 database.py
```

### Étape 7 : Lancer le serveur
```bash
python3 app.py
```

---

## 🍎 Installation sur macOS

### Étape 1 : Installer Homebrew (si pas déjà installé)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Étape 2 : Installer Python
```bash
brew install python3
```

### Étape 3 : Suite identique à Linux

Suivez les étapes 2 à 7 de la section Linux.

---

## 🎓 Installation sur Raspberry Pi (pour serveur local ESI)

### Configuration recommandée
- Raspberry Pi 3B+ ou supérieur
- Raspberry Pi OS Lite (sans interface graphique)
- Carte SD 16 Go minimum
- Alimentation 5V 3A

### Étape 1 : Préparer le Raspberry Pi
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### Étape 2 : Cloner le projet
```bash
cd ~
git clone https://github.com/votre-repo/distributeur-backend.git
cd distributeur-backend
```

### Étape 3 : Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env
```

Modifiez `.env` :
```env
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Étape 4 : Initialiser
```bash
python3 database.py
```

### Étape 5 : Créer un service systemd (démarrage automatique)
```bash
sudo nano /etc/systemd/system/distributeur.service
```

Contenu :
```ini
[Unit]
Description=Distributeur ESI Backend
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/distributeur-backend
Environment="PATH=/home/pi/distributeur-backend/venv/bin"
ExecStart=/home/pi/distributeur-backend/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Activer le service :
```bash
sudo systemctl daemon-reload
sudo systemctl enable distributeur
sudo systemctl start distributeur
sudo systemctl status distributeur
```

### Étape 6 : Trouver l'IP du Raspberry Pi
```bash
hostname -I
```

Le serveur sera accessible sur : `http://IP_DU_RPI:5000`

---

## 🔧 Dépannage

### Problème 1 : "python n'est pas reconnu"

**Windows :**
- Réinstallez Python en cochant "Add to PATH"
- Ou ajoutez manuellement Python au PATH système

**Linux/Mac :**
- Utilisez `python3` au lieu de `python`

### Problème 2 : "pip install" échoue
```bash
# Mettre à jour pip
python -m pip install --upgrade pip

# Réessayer
pip install -r requirements.txt
```

### Problème 3 : "Port 5000 already in use"

**Windows :**
```cmd
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Linux/Mac :**
```bash
lsof -ti:5000 | xargs kill -9
```

Ou changez le port dans `.env` :
```env
FLASK_PORT=8000
```

### Problème 4 : "database is locked"
```bash
# Arrêter tous les processus Python
pkill python

# Relancer
python app.py
```

### Problème 5 : Erreur d'importation de modules
```bash
# Vérifier que l'environnement virtuel est activé
which python  # Linux/Mac
where python  # Windows

# Réinstaller les dépendances
pip install --force-reinstall -r requirements.txt
```

---

## 📊 Vérification de l'installation

### Test 1 : Serveur démarre
```bash
python app.py
```

✅ Vous voyez : "🚀 Démarrage du serveur..."

### Test 2 : API répond
```bash
curl http://localhost:5000/
```

✅ Vous recevez un JSON avec "statut": "opérationnel"

### Test 3 : Tous les tests passent
```bash
python scripts/test_api.py
```

✅ Vous voyez : "🎉 TOUS LES TESTS SONT PASSÉS !"

---

## 🔄 Mise à jour du projet

### Avec Git
```bash
git pull origin main
pip install -r requirements.txt
python app.py
```

### Sans Git

1. Téléchargez la nouvelle version
2. Remplacez tous les fichiers **SAUF** :
   - `.env` (votre configuration)
   - `distributeur.db` (votre base de données)
   - `logs/` (vos logs)
3. Réinstallez les dépendances : `pip install -r requirements.txt`

---

## 🗑️ Désinstallation

### Supprimer l'environnement virtuel
```bash
# Désactiver
deactivate

# Supprimer
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows
```

### Supprimer le projet
```bash
rm -rf distributeur-backend  # Linux/Mac
rmdir /s distributeur-backend  # Windows
```

### Supprimer le service Raspberry Pi
```bash
sudo systemctl stop distributeur
sudo systemctl disable distributeur
sudo rm /etc/systemd/system/distributeur.service
sudo systemctl daemon-reload
```

---

## 📞 Support

En cas de problème :

1. **Consultez les logs :** `logs/serveur.log`
2. **Vérifiez la configuration :** `.env`
3. **Contactez le superviseur :** wilfried.kielem@u-naziboni.net

---

**Dernière mise à jour :** 7 février 2026