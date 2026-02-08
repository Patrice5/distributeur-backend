# ========================================
# CONFIGURATION DE L'APPLICATION
# ========================================

import os
from datetime import timedelta


class Config:
    """
    Classe de configuration pour l'application Flask
    Les valeurs peuvent être surchargées par des variables d'environnement
    """
    
    # ========== BASE DE DONNÉES ==========
    
    # Nom du fichier de base de données
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'distributeur.db')
    
    
    # ========== SERVEUR FLASK ==========
    
    # Mode debug (True en développement, False en production)
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # Hôte et port
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    
    # Clé secrète pour les sessions (générer une vraie clé en production)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    
    # ========== BOISSONS ==========
    
    # Liste des boissons disponibles
    BOISSONS_VALIDES = ['bissap', 'zoom-koom', 'tamarin']
    
    # Prix des boissons (en FCFA)
    PRIX_BOISSONS = {
        'bissap': 200,
        'zoom-koom': 250,
        'tamarin': 200
    }
    
    
    # ========== SEUILS D'ALERTE ==========
    
    # Niveau minimum avant alerte (en pourcentage)
    SEUIL_NIVEAU_BAS = int(os.getenv('SEUIL_NIVEAU_BAS', 20))
    
    # Température maximum avant alerte (en °C)
    SEUIL_TEMPERATURE_HAUTE = float(os.getenv('SEUIL_TEMPERATURE_HAUTE', 15.0))
    
    # Durée avant considérer la machine hors ligne (en minutes)
    TIMEOUT_MACHINE = int(os.getenv('TIMEOUT_MACHINE', 5))
    
    
    # ========== LOGS ==========
    
    # Dossier des logs
    LOG_DIR = 'logs'
    
    # Nom du fichier de log
    LOG_FILE = os.path.join(LOG_DIR, 'serveur.log')
    
    # Taille max d'un fichier de log (en bytes)
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    
    # Nombre de fichiers de log à conserver
    LOG_BACKUP_COUNT = 3
    
    
    # ========== STATISTIQUES ==========
    
    # Nombre de jours pour les statistiques par défaut
    JOURS_STATS_DEFAUT = 7
    
    
    # ========== CORS ==========
    
    # Origines autorisées pour les requêtes cross-origin
    # En production, spécifier les domaines exacts
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')


class ConfigProduction(Config):
    """Configuration spécifique à la production"""
    
    DEBUG = False
    
    # En production, utiliser des valeurs depuis les variables d'environnement
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    # Logs plus verbeux en production
    LOG_BACKUP_COUNT = 10


class ConfigDeveloppement(Config):
    """Configuration spécifique au développement"""
    
    DEBUG = True


# ========================================
# SÉLECTION DE LA CONFIGURATION
# ========================================

# Détermine quelle config utiliser selon la variable FLASK_ENV
def obtenir_config():
    """
    Retourne la classe de configuration appropriée
    """
    
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        return ConfigProduction()
    else:
        return ConfigDeveloppement()


# Configuration active (à importer dans app.py)
config = obtenir_config()