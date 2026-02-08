# ========================================
# IMPORTATION DES BIBLIOTHÈQUES
# ========================================

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Importer la configuration
from config import config

# Imports depuis database.py
from database import (
    initialiser_base,
    ajouter_vente,
    obtenir_toutes_ventes,
    obtenir_ventes_jour,
    compter_ventes_jour,
    ajouter_mesure,
    obtenir_derniere_mesure,
    ajouter_alerte,
    obtenir_alertes_actives,
    resoudre_alerte
)

# Imports depuis services/statistiques.py
from services.statistiques import (
    statistiques_globales,
    statistiques_ventes_jour,
    statistiques_ventes_semaine,
    boisson_la_plus_populaire,
    ventes_par_heure_aujourdhui,
    historique_niveaux,
    consommation_moyenne_par_jour,
    temperature_moyenne_jour,
    historique_temperatures
)


# ========================================
# CONFIGURATION DU LOGGING
# ========================================

# Créer le dossier logs s'il n'existe pas
if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=config.LOG_MAX_SIZE,
            backupCount=config.LOG_BACKUP_COUNT
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ========================================
# CRÉATION DE L'APPLICATION FLASK
# ========================================

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Configuration CORS
if config.CORS_ORIGINS == '*':
    CORS(app)
else:
    CORS(app, origins=config.CORS_ORIGINS.split(','))

# Liste des boissons valides (depuis config)
BOISSONS_VALIDES = config.BOISSONS_VALIDES


# ========================================
# GESTIONNAIRE D'ERREURS GLOBAL
# ========================================

@app.errorhandler(404)
def page_non_trouvee(e):
    """Gère les erreurs 404 (route inexistante)"""
    logger.warning(f"Route inexistante demandée : {request.url}")
    return jsonify({
        'erreur': 'Route inexistante',
        'url_demandee': request.url
    }), 404


@app.errorhandler(500)
def erreur_serveur(e):
    """Gère les erreurs 500 (erreur interne du serveur)"""
    logger.error(f"Erreur serveur : {str(e)}")
    return jsonify({
        'erreur': 'Erreur interne du serveur',
        'details': str(e)
    }), 500


# ========================================
# ROUTES DE L'API
# ========================================

# ROUTE 1 : Page d'accueil
@app.route('/')
def accueil():
    """Route de test"""
    logger.info("Page d'accueil visitée")
    return jsonify({
        'message': 'Serveur du Distributeur ESI',
        'version': '3.0',
        'statut': 'opérationnel',
        'endpoints_disponibles': {
            'ventes': '/api/ventes',
            'etat': '/api/etat',
            'statistiques': '/api/statistiques',
            'alertes': '/api/alertes'
        }
    })


# ========================================
# ROUTES POUR LES VENTES
# ========================================

@app.route('/api/vente', methods=['POST'])
def nouvelle_vente():
    """Enregistre une nouvelle vente"""
    
    try:
        donnees = request.get_json()
        
        if not donnees or 'boisson' not in donnees:
            logger.warning("Tentative d'enregistrement de vente sans données")
            return jsonify({'erreur': 'Le champ "boisson" est obligatoire'}), 400
        
        boisson = donnees['boisson']
        mode = donnees.get('mode', 'bouton')
        
        if boisson not in BOISSONS_VALIDES:
            logger.warning(f"Boisson invalide demandée : {boisson}")
            return jsonify({
                'erreur': f'Boisson invalide. Choix : {", ".join(BOISSONS_VALIDES)}'
            }), 400
        
        id_vente = ajouter_vente(boisson, mode)
        logger.info(f"Vente enregistrée : {boisson} (mode: {mode})")
        
        return jsonify({
            'succes': True,
            'message': f'Vente de {boisson} enregistrée',
            'id': id_vente,
            'boisson': boisson,
            'mode': mode
        }), 201
        
    except Exception as e:
        logger.error(f"Erreur lors de l'enregistrement de vente : {str(e)}")
        return jsonify({'erreur': 'Erreur serveur', 'details': str(e)}), 500


@app.route('/api/ventes', methods=['GET'])
def obtenir_ventes():
    """Retourne toutes les ventes"""
    
    try:
        ventes = obtenir_toutes_ventes()
        return jsonify({
            'succes': True,
            'nombre_ventes': len(ventes),
            'ventes': ventes
        }), 200
    except Exception as e:
        logger.error(f"Erreur récupération ventes : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/ventes/jour', methods=['GET'])
def ventes_jour():
    """Ventes d'aujourd'hui"""
    
    try:
        ventes = obtenir_ventes_jour()
        aujourd_hui = datetime.now().strftime("%Y-%m-%d")
        
        return jsonify({
            'succes': True,
            'date': aujourd_hui,
            'nombre_ventes': len(ventes),
            'ventes': ventes
        }), 200
    except Exception as e:
        logger.error(f"Erreur récupération ventes du jour : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


# ========================================
# ROUTES POUR LES MESURES
# ========================================

@app.route('/api/mesure', methods=['POST'])
def nouvelle_mesure():
    """Enregistre une mesure des capteurs"""
    
    try:
        donnees = request.get_json()
        
        if not donnees:
            return jsonify({'erreur': 'Aucune donnée reçue'}), 400
        
        temperature = donnees.get('temperature', 0)
        niveau_bissap = donnees.get('niveau_bissap', 0)
        niveau_zoom = donnees.get('niveau_zoom', 0)
        niveau_tamarin = donnees.get('niveau_tamarin', 0)
        
        id_mesure = ajouter_mesure(temperature, niveau_bissap, niveau_zoom, niveau_tamarin)
        
        # Vérification automatique des alertes
        if niveau_bissap < 20:
            ajouter_alerte('stock_faible', f'Niveau de bissap faible ({niveau_bissap}%)', 'attention', 'bissap')
            logger.warning(f"Alerte : Niveau bissap faible ({niveau_bissap}%)")
        
        if niveau_zoom < 20:
            ajouter_alerte('stock_faible', f'Niveau de zoom-koom faible ({niveau_zoom}%)', 'attention', 'zoom-koom')
            logger.warning(f"Alerte : Niveau zoom-koom faible ({niveau_zoom}%)")
        
        if niveau_tamarin < 20:
            ajouter_alerte('stock_faible', f'Niveau de tamarin faible ({niveau_tamarin}%)', 'attention', 'tamarin')
            logger.warning(f"Alerte : Niveau tamarin faible ({niveau_tamarin}%)")
        
        if temperature > 15:
            ajouter_alerte('temperature_haute', f'Température élevée ({temperature}°C)', 'critique', None)
            logger.warning(f"Alerte : Température élevée ({temperature}°C)")
        
        logger.info(f"Mesure enregistrée : {temperature}°C, Bissap {niveau_bissap}%, Zoom {niveau_zoom}%, Tamarin {niveau_tamarin}%")
        
        return jsonify({
            'succes': True,
            'message': 'Mesure enregistrée',
            'id': id_mesure
        }), 201
        
    except Exception as e:
        logger.error(f"Erreur enregistrement mesure : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/mesure/derniere', methods=['GET'])
def derniere_mesure():
    """Dernière mesure enregistrée"""
    
    try:
        mesure = obtenir_derniere_mesure()
        
        if mesure:
            return jsonify({
                'succes': True,
                'mesure': mesure
            }), 200
        else:
            return jsonify({
                'succes': False,
                'message': 'Aucune mesure enregistrée'
            }), 404
            
    except Exception as e:
        logger.error(f"Erreur récupération dernière mesure : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


# ========================================
# ROUTES POUR L'ÉTAT DE LA MACHINE
# ========================================

@app.route('/api/etat', methods=['GET'])
def etat_machine():
    """État complet de la machine"""
    
    try:
        mesure = obtenir_derniere_mesure()
        nb_ventes = compter_ventes_jour()
        alertes = obtenir_alertes_actives()
        
        if mesure:
            etat = {
                'succes': True,
                'statut_machine': 'en_ligne',
                'temperature': mesure['temperature'],
                'niveaux': {
                    'bissap': mesure['niveau_bissap'],
                    'zoom': mesure['niveau_zoom'],
                    'tamarin': mesure['niveau_tamarin']
                },
                'ventes_jour': nb_ventes,
                'nombre_alertes': len(alertes),
                'derniere_mise_a_jour': mesure['date_heure']
            }
        else:
            etat = {
                'succes': False,
                'statut_machine': 'hors_ligne',
                'message': 'Aucune donnée reçue de l\'ESP32'
            }
        
        return jsonify(etat), 200
        
    except Exception as e:
        logger.error(f"Erreur récupération état machine : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


# ========================================
# ROUTES POUR LES ALERTES
# ========================================

@app.route('/api/alertes', methods=['GET'])
def obtenir_alertes():
    """Alertes actives"""
    
    try:
        alertes = obtenir_alertes_actives()
        
        return jsonify({
            'succes': True,
            'nombre_alertes': len(alertes),
            'alertes': alertes
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur récupération alertes : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/alerte/<int:id_alerte>/resoudre', methods=['PUT'])
def resoudre_alerte_route(id_alerte):
    """Résoudre une alerte"""
    
    try:
        resoudre_alerte(id_alerte)
        logger.info(f"Alerte {id_alerte} résolue")
        
        return jsonify({
            'succes': True,
            'message': f'Alerte {id_alerte} résolue'
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur résolution alerte : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


# ========================================
# ROUTES POUR LES STATISTIQUES 
# ========================================

@app.route('/api/statistiques', methods=['GET'])
def statistiques():
    """
    Statistiques globales complètes
    Retourne toutes les stats importantes pour le dashboard
    """
    
    try:
        stats = statistiques_globales()
        logger.info("Statistiques globales générées")
        
        return jsonify({
            'succes': True,
            'statistiques': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur génération statistiques : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/statistiques/jour', methods=['GET'])
def stats_jour():
    """Statistiques du jour uniquement"""
    
    try:
        stats = statistiques_ventes_jour()
        
        return jsonify({
            'succes': True,
            'statistiques': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur stats jour : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/statistiques/semaine', methods=['GET'])
def stats_semaine():
    """Statistiques de la semaine"""
    
    try:
        stats = statistiques_ventes_semaine()
        
        return jsonify({
            'succes': True,
            'statistiques': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur stats semaine : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/statistiques/populaire', methods=['GET'])
def stat_populaire():
    """Boisson la plus populaire"""
    
    try:
        populaire = boisson_la_plus_populaire()
        
        return jsonify({
            'succes': True,
            'boisson_populaire': populaire
        }), 200
        
    except Exception as e:
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/historique/niveaux/<boisson>', methods=['GET'])
def historique_niveaux_route(boisson):
    """
    Historique des niveaux d'une boisson
    URL : /api/historique/niveaux/bissap?jours=7
    """
    
    try:
        # Récupérer le paramètre 'jours' (par défaut 7)
        jours = request.args.get('jours', default=7, type=int)
        
        if boisson not in ['bissap', 'zoom-koom', 'zoom', 'tamarin']:
            return jsonify({'erreur': 'Boisson invalide'}), 400
        
        historique = historique_niveaux(boisson, jours)
        
        return jsonify({
            'succes': True,
            'boisson': boisson,
            'periode_jours': jours,
            'historique': historique
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur historique niveaux : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


@app.route('/api/historique/temperatures', methods=['GET'])
def historique_temp_route():
    """
    Historique des températures
    URL : /api/historique/temperatures?jours=7
    """
    
    try:
        jours = request.args.get('jours', default=7, type=int)
        
        historique = historique_temperatures(jours)
        
        return jsonify({
            'succes': True,
            'periode_jours': jours,
            'historique': historique
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur historique températures : {str(e)}")
        return jsonify({'erreur': str(e)}), 500


# ========================================
# LANCEMENT DU SERVEUR
# ========================================

if __name__ == '__main__':
    logger.info("=" * 60)
    logger.info("DÉMARRAGE DU SERVEUR DISTRIBUTEUR ESI")
    logger.info(f"Environnement : {os.getenv('FLASK_ENV', 'development')}")
    logger.info(f"Debug : {config.DEBUG}")
    logger.info("=" * 60)
    
    # Initialiser la base
    logger.info("Initialisation de la base de données...")
    initialiser_base()
    
    logger.info(f"Serveur Flask démarré sur {config.HOST}:{config.PORT}")
    logger.info(f"URL : http://localhost:{config.PORT}")
    logger.info(f"API : http://localhost:{config.PORT}/api/etat")
    logger.info(f"Stats : http://localhost:{config.PORT}/api/statistiques")
    logger.info("=" * 60)
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)