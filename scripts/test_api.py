# ========================================
# SCRIPT DE TEST DE L'API
# Teste toutes les routes de l'API
# ========================================

import requests
import json
from datetime import datetime


# URL de base du serveur
BASE_URL = "http://localhost:5000"


def print_section(titre):
    """Affiche un titre de section"""
    print("\n" + "=" * 60)
    print(f"  {titre}")
    print("=" * 60)


def test_route(methode, route, data=None, description=""):
    """
    Teste une route de l'API
    
    Arguments:
        methode (str): 'GET', 'POST', 'PUT', etc.
        route (str): Route à tester (ex: '/api/ventes')
        data (dict): Données JSON à envoyer (pour POST/PUT)
        description (str): Description du test
    """
    
    url = BASE_URL + route
    
    print(f"\n🧪 {description}")
    print(f"   {methode} {route}")
    
    try:
        if methode == 'GET':
            response = requests.get(url)
        elif methode == 'POST':
            response = requests.post(url, json=data)
        elif methode == 'PUT':
            response = requests.put(url, json=data)
        else:
            print(f"   ❌ Méthode {methode} non supportée")
            return False
        
        # Afficher le code de statut
        if response.status_code < 300:
            print(f"   ✅ Statut : {response.status_code}")
        else:
            print(f"   ⚠️ Statut : {response.status_code}")
        
        # Afficher un extrait de la réponse
        try:
            data_response = response.json()
            # Afficher seulement les clés principales
            if isinstance(data_response, dict):
                cles = list(data_response.keys())[:3]
                print(f"   📦 Réponse : {cles}...")
            else:
                print(f"   📦 Réponse reçue")
        except:
            print(f"   📦 Réponse non-JSON")
        
        return response.status_code < 300
        
    except requests.exceptions.ConnectionError:
        print(f"   ❌ ERREUR : Impossible de se connecter au serveur")
        print(f"   💡 Vérifiez que le serveur est démarré (python app.py)")
        return False
    except Exception as e:
        print(f"   ❌ ERREUR : {str(e)}")
        return False


def executer_tests():
    """Execute tous les tests"""
    
    print("\n" + "🧪" * 30)
    print("   TESTS DE L'API DISTRIBUTEUR ESI")
    print("🧪" * 30)
    
    resultats = []
    
    # ========== TESTS DE BASE ==========
    
    print_section("1. ROUTES DE BASE")
    
    resultats.append(test_route(
        'GET', '/',
        description="Page d'accueil"
    ))
    
    
    # ========== TESTS VENTES ==========
    
    print_section("2. ROUTES VENTES")
    
    resultats.append(test_route(
        'POST', '/api/vente',
        data={'boisson': 'bissap', 'mode': 'bouton'},
        description="Enregistrer une vente de bissap"
    ))
    
    resultats.append(test_route(
        'POST', '/api/vente',
        data={'boisson': 'zoom-koom', 'mode': 'web'},
        description="Enregistrer une vente de zoom-koom"
    ))
    
    resultats.append(test_route(
        'GET', '/api/ventes',
        description="Récupérer toutes les ventes"
    ))
    
    resultats.append(test_route(
        'GET', '/api/ventes/jour',
        description="Récupérer les ventes du jour"
    ))
    
    
    # ========== TESTS MESURES ==========
    
    print_section("3. ROUTES MESURES")
    
    resultats.append(test_route(
        'POST', '/api/mesure',
        data={
            'temperature': 8.5,
            'niveau_bissap': 70,
            'niveau_zoom': 45,
            'niveau_tamarin': 85
        },
        description="Enregistrer une mesure"
    ))
    
    resultats.append(test_route(
        'GET', '/api/mesure/derniere',
        description="Récupérer la dernière mesure"
    ))
    
    
    # ========== TESTS ÉTAT ==========
    
    print_section("4. ROUTE ÉTAT MACHINE")
    
    resultats.append(test_route(
        'GET', '/api/etat',
        description="État complet de la machine"
    ))
    
    
    # ========== TESTS ALERTES ==========
    
    print_section("5. ROUTES ALERTES")
    
    resultats.append(test_route(
        'GET', '/api/alertes',
        description="Récupérer les alertes actives"
    ))
    
    
    # ========== TESTS STATISTIQUES ==========
    
    print_section("6. ROUTES STATISTIQUES")
    
    resultats.append(test_route(
        'GET', '/api/statistiques',
        description="Statistiques globales"
    ))
    
    resultats.append(test_route(
        'GET', '/api/statistiques/jour',
        description="Statistiques du jour"
    ))
    
    resultats.append(test_route(
        'GET', '/api/statistiques/semaine',
        description="Statistiques de la semaine"
    ))
    
    resultats.append(test_route(
        'GET', '/api/statistiques/populaire',
        description="Boisson la plus populaire"
    ))
    
    
    # ========== TESTS HISTORIQUES ==========
    
    print_section("7. ROUTES HISTORIQUES")
    
    resultats.append(test_route(
        'GET', '/api/historique/niveaux/bissap?jours=7',
        description="Historique niveaux bissap (7 jours)"
    ))
    
    resultats.append(test_route(
        'GET', '/api/historique/temperatures?jours=7',
        description="Historique températures (7 jours)"
    ))
    
    
    # ========== RÉSUMÉ ==========
    
    print_section("RÉSUMÉ DES TESTS")
    
    nb_total = len(resultats)
    nb_reussis = sum(resultats)
    nb_echecs = nb_total - nb_reussis
    
    print(f"\n   Total de tests : {nb_total}")
    print(f"   ✅ Réussis : {nb_reussis}")
    print(f"   ❌ Échoués : {nb_echecs}")
    
    pourcentage = (nb_reussis / nb_total * 100) if nb_total > 0 else 0
    print(f"\n   📊 Taux de réussite : {pourcentage:.1f}%")
    
    if nb_echecs == 0:
        print("\n   🎉 TOUS LES TESTS SONT PASSÉS !")
    else:
        print(f"\n   ⚠️ {nb_echecs} test(s) ont échoué")
    
    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    executer_tests()