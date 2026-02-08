# ========================================
# SCRIPT D'INITIALISATION AVEC DONNÉES DE DÉMO
# Crée des données de test pour tester l'application
# ========================================

import sys
import os

# Ajouter le dossier parent au path pour pouvoir importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import (
    initialiser_base,
    ajouter_vente,
    ajouter_mesure,
    ajouter_alerte
)
from datetime import datetime, timedelta
import random


def generer_donnees_demo():
    """
    Génère des données de démonstration pour tester l'application
    """
    
    print("\nGÉNÉRATION DES DONNÉES DE DÉMONSTRATION\n")
    
    # Initialiser la base
    print("Initialisation de la base de données...")
    initialiser_base()
    
    boissons = ['bissap', 'zoom-koom', 'tamarin']
    modes = ['bouton', 'web']
    
    # ========== VENTES DES 7 DERNIERS JOURS ==========
    
    print("\nCréation de ventes sur 7 jours...")
    
    total_ventes = 0
    
    for jour in range(7, 0, -1):  # De 7 jours en arrière à aujourd'hui
        date = datetime.now() - timedelta(days=jour)
        
        # Entre 10 et 30 ventes par jour
        nb_ventes_jour = random.randint(10, 30)
        
        for _ in range(nb_ventes_jour):
            boisson = random.choice(boissons)
            mode = random.choice(modes)
            
            # Heures de travail : 8h à 17h
            heure = random.randint(8, 17)
            minute = random.randint(0, 59)
            
            # Modifier temporairement datetime pour insérer avec la bonne date
            # (Note : ceci est pour la démo, en vrai l'ESP32 envoie en temps réel)
            
            ajouter_vente(boisson, mode)
            total_ventes += 1
        
        print(f"  Jour -{jour} : {nb_ventes_jour} ventes")
    
    print(f"\nTotal : {total_ventes} ventes créées")
    
    
    # ========== MESURES DES 7 DERNIERS JOURS ==========
    
    print("\nCréation de mesures sur 7 jours...")
    
    total_mesures = 0
    
    for jour in range(7, 0, -1):
        # 4 mesures par jour (toutes les 6h)
        for heure in [6, 12, 18, 23]:
            # Température entre 7 et 10°C
            temperature = round(random.uniform(7.0, 10.0), 1)
            
            # Niveaux qui diminuent progressivement
            niveau_bissap = max(20, 100 - (7 - jour) * 10 + random.randint(-5, 5))
            niveau_zoom = max(15, 100 - (7 - jour) * 12 + random.randint(-5, 5))
            niveau_tamarin = max(25, 100 - (7 - jour) * 8 + random.randint(-5, 5))
            
            ajouter_mesure(temperature, niveau_bissap, niveau_zoom, niveau_tamarin)
            total_mesures += 1
    
    print(f"{total_mesures} mesures créées")
    
    
    # ========== ALERTES ==========
    
    print("\nCréation d'alertes...")
    
    # Alerte stock faible
    ajouter_alerte(
        'stock_faible',
        'Niveau de zoom-koom faible (18%)',
        'attention',
        'zoom-koom'
    )
    
    # Alerte température (résolue)
    ajouter_alerte(
        'temperature_haute',
        'Température élevée détectée (16.2°C)',
        'critique',
        None
    )
    
    print("2 alertes créées")
    
    
    print("\n" + "=" * 60)
    print("DONNÉES DE DÉMONSTRATION CRÉÉES AVEC SUCCÈS !")
    print("=" * 60)
    print("\nVous pouvez maintenant tester l'application avec :")
    print("  - Des ventes sur 7 jours")
    print("  - Des mesures régulières")
    print("  - Des alertes de test")
    print("\nLancez le serveur : python app.py")
    print("Testez les stats : GET http://localhost:5000/api/statistiques")
    print()


if __name__ == '__main__':
    generer_donnees_demo()