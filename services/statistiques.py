# ========================================
# MODULE DE STATISTIQUES
# Calculs avancés pour le dashboard admin
# ========================================

from database import obtenir_connexion
from datetime import datetime, timedelta


# ========================================
# STATISTIQUES DES VENTES
# ========================================

def statistiques_ventes_jour():
    """
    Calcule les statistiques des ventes du jour
    
    Retourne:
        dict : Statistiques détaillées
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    
    # Total des ventes du jour
    curseur.execute('''
        SELECT COUNT(*) as total
        FROM ventes
        WHERE date_heure LIKE ?
    ''', (f"{aujourd_hui}%",))
    
    total = curseur.fetchone()['total']
    
    # Ventes par boisson
    curseur.execute('''
        SELECT boisson, COUNT(*) as nombre
        FROM ventes
        WHERE date_heure LIKE ?
        GROUP BY boisson
        ORDER BY nombre DESC
    ''', (f"{aujourd_hui}%",))
    
    ventes_par_boisson = {}
    lignes = curseur.fetchall()
    
    for ligne in lignes:
        ventes_par_boisson[ligne['boisson']] = ligne['nombre']
    
    # Ventes par mode (bouton vs web)
    curseur.execute('''
        SELECT mode, COUNT(*) as nombre
        FROM ventes
        WHERE date_heure LIKE ?
        GROUP BY mode
    ''', (f"{aujourd_hui}%",))
    
    ventes_par_mode = {}
    lignes = curseur.fetchall()
    
    for ligne in lignes:
        ventes_par_mode[ligne['mode']] = ligne['nombre']
    
    connexion.close()
    
    return {
        'total_ventes': total,
        'par_boisson': ventes_par_boisson,
        'par_mode': ventes_par_mode
    }


def statistiques_ventes_semaine():
    """
    Calcule les statistiques de la semaine
    
    Retourne:
        dict : Statistiques de la semaine
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    # Date d'il y a 7 jours
    il_y_a_7_jours = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    # Total de la semaine
    curseur.execute('''
        SELECT COUNT(*) as total
        FROM ventes
        WHERE date_heure >= ?
    ''', (il_y_a_7_jours,))
    
    total = curseur.fetchone()['total']
    
    # Ventes par boisson
    curseur.execute('''
        SELECT boisson, COUNT(*) as nombre
        FROM ventes
        WHERE date_heure >= ?
        GROUP BY boisson
        ORDER BY nombre DESC
    ''', (il_y_a_7_jours,))
    
    ventes_par_boisson = {}
    lignes = curseur.fetchall()
    
    for ligne in lignes:
        ventes_par_boisson[ligne['boisson']] = ligne['nombre']
    
    # Ventes par jour
    curseur.execute('''
        SELECT DATE(date_heure) as jour, COUNT(*) as nombre
        FROM ventes
        WHERE date_heure >= ?
        GROUP BY DATE(date_heure)
        ORDER BY jour
    ''', (il_y_a_7_jours,))
    
    ventes_par_jour = {}
    lignes = curseur.fetchall()
    
    for ligne in lignes:
        ventes_par_jour[ligne['jour']] = ligne['nombre']
    
    connexion.close()
    
    return {
        'total_ventes': total,
        'par_boisson': ventes_par_boisson,
        'par_jour': ventes_par_jour
    }


def boisson_la_plus_populaire():
    """
    Trouve la boisson la plus vendue (de tous les temps)
    
    Retourne:
        dict : Boisson la plus populaire
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    curseur.execute('''
        SELECT boisson, COUNT(*) as nombre
        FROM ventes
        GROUP BY boisson
        ORDER BY nombre DESC
        LIMIT 1
    ''')
    
    resultat = curseur.fetchone()
    connexion.close()
    
    if resultat:
        return {
            'boisson': resultat['boisson'],
            'nombre_ventes': resultat['nombre']
        }
    else:
        return {
            'boisson': None,
            'nombre_ventes': 0
        }


def ventes_par_heure_aujourdhui():
    """
    Répartition des ventes par heure aujourd'hui
    Utile pour identifier les heures de pointe
    
    Retourne:
        dict : {heure: nombre_ventes}
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    
    # On extrait l'heure de chaque vente
    curseur.execute('''
        SELECT 
            CAST(strftime('%H', date_heure) AS INTEGER) as heure,
            COUNT(*) as nombre
        FROM ventes
        WHERE date_heure LIKE ?
        GROUP BY heure
        ORDER BY heure
    ''', (f"{aujourd_hui}%",))
    
    ventes_par_heure = {}
    lignes = curseur.fetchall()
    
    for ligne in lignes:
        # On formate l'heure : 8 → "08h", 14 → "14h"
        heure_formatee = f"{ligne['heure']:02d}h"
        ventes_par_heure[heure_formatee] = ligne['nombre']
    
    connexion.close()
    
    return ventes_par_heure


# ========================================
# STATISTIQUES DES NIVEAUX
# ========================================

def historique_niveaux(boisson, jours=7):
    """
    Historique des niveaux d'une boisson sur X jours
    
    Arguments:
        boisson (str): 'bissap', 'zoom' ou 'tamarin'
        jours (int): Nombre de jours à récupérer
    
    Retourne:
        list : Historique des niveaux
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    il_y_a_x_jours = (datetime.now() - timedelta(days=jours)).strftime("%Y-%m-%d")
    
    # Nom de la colonne selon la boisson
    if boisson == 'bissap':
        colonne_niveau = 'niveau_bissap'
    elif boisson == 'zoom-koom' or boisson == 'zoom':
        colonne_niveau = 'niveau_zoom'
    elif boisson == 'tamarin':
        colonne_niveau = 'niveau_tamarin'
    else:
        connexion.close()
        return []
    
    # Requête dynamique avec le nom de colonne
    requete = f'''
        SELECT date_heure, {colonne_niveau} as niveau
        FROM mesures
        WHERE date_heure >= ?
        ORDER BY date_heure
    '''
    
    curseur.execute(requete, (il_y_a_x_jours,))
    
    lignes = curseur.fetchall()
    historique = [dict(ligne) for ligne in lignes]
    
    connexion.close()
    
    return historique


def consommation_moyenne_par_jour():
    """
    Calcule la consommation moyenne de chaque boisson par jour
    Permet d'estimer quand réapprovisionner
    
    Retourne:
        dict : Consommation moyenne par boisson
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    # On compte le nombre de jours où il y a eu au moins 1 vente
    curseur.execute('''
        SELECT COUNT(DISTINCT DATE(date_heure)) as nb_jours
        FROM ventes
    ''')
    
    nb_jours = curseur.fetchone()['nb_jours']
    
    if nb_jours == 0:
        connexion.close()
        return {
            'bissap': 0,
            'zoom-koom': 0,
            'tamarin': 0
        }
    
    # Ventes totales par boisson
    curseur.execute('''
        SELECT boisson, COUNT(*) as total
        FROM ventes
        GROUP BY boisson
    ''')
    
    lignes = curseur.fetchall()
    
    moyennes = {
        'bissap': 0,
        'zoom-koom': 0,
        'tamarin': 0
    }
    
    for ligne in lignes:
        moyenne = ligne['total'] / nb_jours
        moyennes[ligne['boisson']] = round(moyenne, 1)  # Arrondi à 1 décimale
    
    connexion.close()
    
    return moyennes


# ========================================
# STATISTIQUES DE TEMPÉRATURE
# ========================================

def temperature_moyenne_jour():
    """
    Calcule la température moyenne du jour
    
    Retourne:
        float : Température moyenne ou None
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    aujourd_hui = datetime.now().strftime("%Y-%m-%d")
    
    curseur.execute('''
        SELECT AVG(temperature) as moyenne
        FROM mesures
        WHERE date_heure LIKE ?
    ''', (f"{aujourd_hui}%",))
    
    resultat = curseur.fetchone()
    connexion.close()
    
    if resultat and resultat['moyenne']:
        return round(resultat['moyenne'], 1)
    else:
        return None


def historique_temperatures(jours=7):
    """
    Historique des températures sur X jours
    
    Arguments:
        jours (int): Nombre de jours
    
    Retourne:
        list : Historique des températures
    """
    
    connexion = obtenir_connexion()
    curseur = connexion.cursor()
    
    il_y_a_x_jours = (datetime.now() - timedelta(days=jours)).strftime("%Y-%m-%d")
    
    curseur.execute('''
        SELECT date_heure, temperature
        FROM mesures
        WHERE date_heure >= ?
        ORDER BY date_heure
    ''', (il_y_a_x_jours,))
    
    lignes = curseur.fetchall()
    historique = [dict(ligne) for ligne in lignes]
    
    connexion.close()
    
    return historique


# ========================================
# STATISTIQUES GLOBALES (RÉSUMÉ)
# ========================================

def statistiques_globales():
    """
    Retourne un résumé complet de toutes les statistiques
    Utilisé par la route /api/statistiques
    
    Retourne:
        dict : Toutes les statistiques importantes
    """
    
    stats_jour = statistiques_ventes_jour()
    stats_semaine = statistiques_ventes_semaine()
    plus_populaire = boisson_la_plus_populaire()
    conso_moyenne = consommation_moyenne_par_jour()
    temp_moyenne = temperature_moyenne_jour()
    
    return {
        'aujourdhui': stats_jour,
        'cette_semaine': stats_semaine,
        'boisson_plus_populaire': plus_populaire,
        'consommation_moyenne_jour': conso_moyenne,
        'temperature_moyenne_jour': temp_moyenne,
        'ventes_par_heure': ventes_par_heure_aujourdhui()
    }


# ========================================
# FONCTION DE TEST (optionnelle)
# ========================================

def tester_statistiques():
    """
    Teste les fonctions de statistiques
    Peut être exécuté avec : python services/statistiques.py
    """
    print("\nTest des statistiques\n")
    
    print("--- Stats du jour ---")
    stats = statistiques_ventes_jour()
    print(f"Total ventes : {stats['total_ventes']}")
    print(f"Par boisson : {stats['par_boisson']}")
    
    print("\n--- Boisson la plus populaire ---")
    pop = boisson_la_plus_populaire()
    print(f"{pop['boisson']} avec {pop['nombre_ventes']} ventes")
    
    print("\n--- Ventes par heure ---")
    par_heure = ventes_par_heure_aujourdhui()
    for heure, nombre in par_heure.items():
        print(f"  {heure} : {nombre} ventes")
    
    print("\n--- Consommation moyenne/jour ---")
    conso = consommation_moyenne_par_jour()
    for boisson, moyenne in conso.items():
        print(f"  {boisson} : {moyenne} ventes/jour")
    
    print("\n--- Température moyenne ---")
    temp = temperature_moyenne_jour()
    print(f"Température moyenne : {temp}°C")
    
    print("\nTests terminés !\n")


if __name__ == '__main__':
    tester_statistiques()