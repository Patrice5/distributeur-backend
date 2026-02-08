# ========================================
# GESTION DE LA BASE DE DONNÉES SQLite
# ========================================

import sqlite3
from datetime import datetime
import os

# Nom du fichier de la base de données
NOM_DB = 'distributeur.db'


# ========================================
# FONCTION : Connexion à la base de données
# ========================================

def obtenir_connexion():
    """
    Crée et retourne une connexion à la base de données SQLite
    
    Retourne:
        sqlite3.Connection : Objet de connexion à la base
    """
    # On se connecte à la base (elle sera créée si elle n'existe pas)
    connexion = sqlite3.connect(NOM_DB)
    
    # Cette ligne permet de récupérer les résultats sous forme de dictionnaires
    # Au lieu de tuples, on aura des résultats plus lisibles
    connexion.row_factory = sqlite3.Row
    
    return connexion


# ========================================
# FONCTION : Initialisation de la base
# ========================================

def initialiser_base():
    """
    Crée les tables si elles n'existent pas déjà
    Cette fonction est appelée au démarrage du serveur
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    # ========== TABLE 1 : ventes ==========
    # Stocke chaque boisson servie
    curseur.execute('''
        CREATE TABLE IF NOT EXISTS ventes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            boisson TEXT NOT NULL,
            date_heure DATETIME NOT NULL,
            mode TEXT DEFAULT 'bouton',
            prix REAL DEFAULT 0
        )
    ''')
    
    # ========== TABLE 2 : mesures ==========
    # Stocke les données des capteurs (température, niveaux)
    curseur.execute('''
        CREATE TABLE IF NOT EXISTS mesures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_heure DATETIME NOT NULL,
            temperature REAL,
            niveau_bissap INTEGER,
            niveau_zoom INTEGER,
            niveau_tamarin INTEGER
        )
    ''')
    
    # ========== TABLE 3 : alertes ==========
    # Stocke les alertes système (stock faible, température haute, etc.)
    curseur.execute('''
        CREATE TABLE IF NOT EXISTS alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_heure DATETIME NOT NULL,
            type_alerte TEXT NOT NULL,
            severite TEXT DEFAULT 'info',
            message TEXT,
            boisson TEXT,
            resolu INTEGER DEFAULT 0
        )
    ''')
    
    # On sauvegarde les changements
    connexion.commit()
    
    # On ferme la connexion
    connexion.close()
    
    print("Base de données initialisée avec succès")
    print(f"Fichier : {NOM_DB}")


# ========================================
# FONCTIONS POUR LA TABLE "ventes"
# ========================================

def ajouter_vente(boisson, mode='bouton'):
    """
    Ajoute une nouvelle vente dans la base de données
    
    Arguments:
        boisson (str): 'bissap', 'zoom-koom' ou 'tamarin'
        mode (str): 'bouton' ou 'web'
    
    Retourne:
        int : ID de la vente créée
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    # Date et heure actuelles
    maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Requête SQL INSERT
    curseur.execute('''
        INSERT INTO ventes (boisson, date_heure, mode, prix)
        VALUES (?, ?, ?, ?)
    ''', (boisson, maintenant, mode, 0))  # Prix = 0 pour v1
    
    # ID de la ligne insérée
    id_vente = curseur.lastrowid
    
    connexion.commit()
    connexion.close()
    
    print(f"Vente enregistrée : ID {id_vente} | {boisson} | {mode}")
    
    return id_vente


def obtenir_toutes_ventes():
    """
    Récupère toutes les ventes de la base
    
    Retourne:
        list : Liste de dictionnaires contenant les ventes
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    curseur.execute('''
        SELECT id, boisson, date_heure, mode, prix
        FROM ventes
        ORDER BY date_heure DESC
    ''')
    
    # On récupère tous les résultats
    lignes = curseur.fetchall()
    
    # On transforme en liste de dictionnaires
    ventes = [dict(ligne) for ligne in lignes]
    
    connexion.close()
    
    return ventes


def obtenir_ventes_jour():
    """
    Récupère uniquement les ventes du jour
    
    Retourne:
        list : Ventes d'aujourd'hui
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    # Date d'aujourd'hui au format YYYY-MM-DD
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    
    curseur.execute('''
        SELECT id, boisson, date_heure, mode, prix
        FROM ventes
        WHERE date_heure LIKE ?
        ORDER BY date_heure DESC
    ''', (f"{aujourd_hui}%",))  # Le % signifie "n'importe quoi après"
    
    lignes = curseur.fetchall()
    ventes = [dict(ligne) for ligne in lignes]
    
    connexion.close()
    
    return ventes


def compter_ventes_jour():
    """
    Compte le nombre de ventes aujourd'hui
    
    Retourne:
        int : Nombre de ventes
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    
    curseur.execute('''
        SELECT COUNT(*) as total
        FROM ventes
        WHERE date_heure LIKE ?
    ''', (f"{aujourd_hui}%",))
    
    resultat = curseur.fetchone()
    total = resultat['total']
    
    connexion.close()
    
    return total


# ========================================
# FONCTIONS POUR LA TABLE "mesures"
# ========================================

def ajouter_mesure(temperature, niveau_bissap, niveau_zoom, niveau_tamarin):
    """
    Ajoute une mesure des capteurs dans la base
    
    Arguments:
        temperature (float): Température en °C
        niveau_bissap (int): Pourcentage 0-100
        niveau_zoom (int): Pourcentage 0-100
        niveau_tamarin (int): Pourcentage 0-100
    
    Retourne:
        int : ID de la mesure créée
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    curseur.execute('''
        INSERT INTO mesures (date_heure, temperature, niveau_bissap, niveau_zoom, niveau_tamarin)
        VALUES (?, ?, ?, ?, ?)
    ''', (maintenant, temperature, niveau_bissap, niveau_zoom, niveau_tamarin))
    
    id_mesure = curseur.lastrowid
    
    connexion.commit()
    connexion.close()
    
    print(f"Mesure enregistrée : ID {id_mesure} | {temperature}°C")
    
    return id_mesure


def obtenir_derniere_mesure():
    """
    Récupère la mesure la plus récente
    
    Retourne:
        dict : Dernière mesure ou None
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    curseur.execute('''
        SELECT *
        FROM mesures
        ORDER BY date_heure DESC
        LIMIT 1
    ''')
    
    ligne = curseur.fetchone()
    
    connexion.close()
    
    if ligne:
        return dict(ligne)
    else:
        return None


# ========================================
# FONCTIONS POUR LA TABLE "alertes"
# ========================================

def ajouter_alerte(type_alerte, message, severite='info', boisson=None):
    """
    Ajoute une alerte dans la base
    
    Arguments:
        type_alerte (str): 'stock_faible', 'temperature_haute', 'erreur'
        message (str): Description de l'alerte
        severite (str): 'info', 'attention', 'critique'
        boisson (str): Boisson concernée (optionnel)
    
    Retourne:
        int : ID de l'alerte créée
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    maintenant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    curseur.execute('''
        INSERT INTO alertes (date_heure, type_alerte, severite, message, boisson, resolu)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (maintenant, type_alerte, severite, message, boisson, 0))
    
    id_alerte = curseur.lastrowid
    
    connexion.commit()
    connexion.close()
    
    print(f"Alerte créée : {message}")
    
    return id_alerte


def obtenir_alertes_actives():
    """
    Récupère toutes les alertes non résolues
    
    Retourne:
        list : Alertes actives
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    curseur.execute('''
        SELECT *
        FROM alertes
        WHERE resolu = 0
        ORDER BY date_heure DESC
    ''')
    
    lignes = curseur.fetchall()
    alertes = [dict(ligne) for ligne in lignes]
    
    connexion.close()
    
    return alertes


def resoudre_alerte(id_alerte):
    """
    Marque une alerte comme résolue
    
    Arguments:
        id_alerte (int): ID de l'alerte à résoudre
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    curseur.execute('''
        UPDATE alertes
        SET resolu = 1
        WHERE id = ?
    ''', (id_alerte,))
    
    connexion.commit()
    connexion.close()
    
    print(f"Alerte {id_alerte} résolue")


# ========================================
# FONCTION DE TEST (optionnelle)
# ========================================

def tester_base():
    """
    Fonction pour tester la base de données
    Peut être exécutée avec : python database.py
    """
    print("\nTest de la base de données\n")
    
    # Initialiser la base
    initialiser_base()
    
    # Test 1 : Ajouter une vente
    print("\n--- Test 1 : Ajout d'une vente ---")
    ajouter_vente('bissap', 'bouton')
    
    # Test 2 : Récupérer toutes les ventes
    print("\n--- Test 2 : Récupération des ventes ---")
    ventes = obtenir_toutes_ventes()
    print(f"Nombre de ventes : {len(ventes)}")
    for v in ventes:
        print(f"  - {v['boisson']} à {v['date_heure']}")
    
    # Test 3 : Ajouter une mesure
    print("\n--- Test 3 : Ajout d'une mesure ---")
    ajouter_mesure(8.5, 70, 45, 85)
    
    # Test 4 : Récupérer la dernière mesure
    print("\n--- Test 4 : Dernière mesure ---")
    mesure = obtenir_derniere_mesure()
    if mesure:
        print(f"  Température : {mesure['temperature']}°C")
        print(f"  Niveaux : Bissap {mesure['niveau_bissap']}%, Zoom {mesure['niveau_zoom']}%, Tamarin {mesure['niveau_tamarin']}%")
    
    # Test 5 : Ajouter une alerte
    print("\n--- Test 5 : Ajout d'une alerte ---")
    ajouter_alerte('stock_faible', 'Niveau de zoom-koom faible (18%)', 'attention', 'zoom-koom')
    
    # Test 6 : Récupérer les alertes
    print("\n--- Test 6 : Alertes actives ---")
    alertes = obtenir_alertes_actives()
    print(f"Nombre d'alertes : {len(alertes)}")
    for a in alertes:
        print(f"  - [{a['severite']}] {a['message']}")
    
    print("\nTests terminés !\n")


# Si on exécute ce fichier directement, on lance les tests
if __name__ == '__main__':
    tester_base()