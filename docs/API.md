# 📖 Documentation API - Distributeur ESI

Documentation complète de l'API REST du distributeur intelligent de boissons locales.

**URL de base :** `http://localhost:5000`  
**URL de production :** `https://votre-app.onrender.com`

---

## 📋 Table des matières

1. [Authentification](#authentification)
2. [Format des réponses](#format-des-réponses)
3. [Codes d'erreur](#codes-derreur)
4. [Routes - Ventes](#routes-ventes)
5. [Routes - Mesures](#routes-mesures)
6. [Routes - État machine](#routes-état-machine)
7. [Routes - Alertes](#routes-alertes)
8. [Routes - Statistiques](#routes-statistiques)
9. [Routes - Historiques](#routes-historiques)
10. [Exemples d'utilisation](#exemples-dutilisation)

---

## 🔐 Authentification

**Version actuelle (v1.0) :** Aucune authentification requise.

**Version future (v2.0) :** API Key dans les headers
```http
Authorization: Bearer YOUR_API_KEY
```

---

## 📦 Format des réponses

Toutes les réponses sont au format **JSON**.

### Réponse de succès
```json
{
  "succes": true,
  "message": "Opération réussie",
  "data": { ... }
}
```

### Réponse d'erreur
```json
{
  "erreur": "Description de l'erreur",
  "details": "Informations supplémentaires"
}
```

---

## ⚠️ Codes d'erreur

| Code | Signification | Description |
|------|---------------|-------------|
| 200 | OK | Requête réussie |
| 201 | Created | Ressource créée avec succès |
| 400 | Bad Request | Données invalides ou manquantes |
| 404 | Not Found | Ressource inexistante |
| 500 | Internal Server Error | Erreur interne du serveur |

---

## 🥤 Routes - Ventes

### POST /api/vente

Enregistre une nouvelle vente de boisson.

**Utilisé par :** ESP32 (après chaque distribution)

#### Requête
```http
POST /api/vente
Content-Type: application/json

{
  "boisson": "bissap",
  "mode": "bouton"
}
```

#### Paramètres

| Champ | Type | Obligatoire | Valeurs possibles | Description |
|-------|------|-------------|-------------------|-------------|
| boisson | string | ✅ Oui | `bissap`, `zoom-koom`, `tamarin` | Type de boisson servie |
| mode | string | ❌ Non (défaut: `bouton`) | `bouton`, `web` | Mode de commande |

#### Réponse succès (201)
```json
{
  "succes": true,
  "message": "Vente de bissap enregistrée",
  "id": 42,
  "boisson": "bissap",
  "mode": "bouton"
}
```

#### Réponse erreur (400)
```json
{
  "erreur": "Boisson invalide. Choix : bissap, zoom-koom, tamarin"
}
```

#### Exemple avec curl
```bash
curl -X POST http://localhost:5000/api/vente \
  -H "Content-Type: application/json" \
  -d '{"boisson": "bissap", "mode": "bouton"}'
```

#### Exemple avec Python (ESP32)
```python
import requests

url = "http://192.168.1.100:5000/api/vente"
data = {
    "boisson": "bissap",
    "mode": "bouton"
}

response = requests.post(url, json=data)
print(response.json())
```

---

### GET /api/ventes

Récupère toutes les ventes enregistrées.

**Utilisé par :** Dashboard administrateur

#### Requête
```http
GET /api/ventes
```

#### Réponse (200)
```json
{
  "succes": true,
  "nombre_ventes": 2,
  "ventes": [
    {
      "id": 2,
      "boisson": "zoom-koom",
      "date_heure": "2026-02-07 15:30:45",
      "mode": "web",
      "prix": 0
    },
    {
      "id": 1,
      "boisson": "bissap",
      "date_heure": "2026-02-07 14:23:12",
      "mode": "bouton",
      "prix": 0
    }
  ]
}
```

**Note :** Les ventes sont triées par date décroissante (plus récentes en premier).

---

### GET /api/ventes/jour

Récupère uniquement les ventes du jour.

**Utilisé par :** Dashboard (widget "Ventes du jour")

#### Requête
```http
GET /api/ventes/jour
```

#### Réponse (200)
```json
{
  "succes": true,
  "date": "2026-02-07",
  "nombre_ventes": 47,
  "ventes": [
    {
      "id": 47,
      "boisson": "tamarin",
      "date_heure": "2026-02-07 16:45:12",
      "mode": "web",
      "prix": 0
    },
    ...
  ]
}
```

---

## 🌡️ Routes - Mesures

### POST /api/mesure

Enregistre une mesure des capteurs (température + niveaux).

**Utilisé par :** ESP32 (toutes les 30 secondes)

#### Requête
```http
POST /api/mesure
Content-Type: application/json

{
  "temperature": 8.5,
  "niveau_bissap": 70,
  "niveau_zoom": 45,
  "niveau_tamarin": 85
}
```

#### Paramètres

| Champ | Type | Obligatoire | Plage | Unité | Description |
|-------|------|-------------|-------|-------|-------------|
| temperature | float | ✅ Oui | -10 à 50 | °C | Température mesurée |
| niveau_bissap | integer | ✅ Oui | 0 à 100 | % | Niveau du réservoir bissap |
| niveau_zoom | integer | ✅ Oui | 0 à 100 | % | Niveau du réservoir zoom-koom |
| niveau_tamarin | integer | ✅ Oui | 0 à 100 | % | Niveau du réservoir tamarin |

#### Réponse (201)
```json
{
  "succes": true,
  "message": "Mesure enregistrée",
  "id": 123
}
```

#### ⚠️ Alertes automatiques

Cette route déclenche automatiquement des alertes si :
- Un niveau < 20% → Alerte "stock_faible"
- Température > 15°C → Alerte "temperature_haute"

**Exemple :**
```json
// Envoi avec niveau_zoom = 18%
→ Crée automatiquement une alerte "Niveau de zoom-koom faible (18%)"
```

---

### GET /api/mesure/derniere

Récupère la mesure la plus récente.

**Utilisé par :** Dashboard (affichage en temps réel)

#### Requête
```http
GET /api/mesure/derniere
```

#### Réponse (200)
```json
{
  "succes": true,
  "mesure": {
    "id": 156,
    "date_heure": "2026-02-07 16:52:30",
    "temperature": 8.5,
    "niveau_bissap": 70,
    "niveau_zoom": 45,
    "niveau_tamarin": 85
  }
}
```

#### Réponse si aucune mesure (404)
```json
{
  "succes": false,
  "message": "Aucune mesure enregistrée"
}
```

---

## 🖥️ Routes - État machine

### GET /api/etat

Retourne un résumé complet de l'état actuel de la machine.

**Utilisé par :** Dashboard (page principale), Application mobile

**Cette route est la plus importante pour le monitoring en temps réel.**

#### Requête
```http
GET /api/etat
```

#### Réponse - Machine en ligne (200)
```json
{
  "succes": true,
  "statut_machine": "en_ligne",
  "temperature": 8.5,
  "niveaux": {
    "bissap": 70,
    "zoom": 45,
    "tamarin": 85
  },
  "ventes_jour": 47,
  "nombre_alertes": 1,
  "derniere_mise_a_jour": "2026-02-07 16:52:30"
}
```

#### Réponse - Machine hors ligne (200)
```json
{
  "succes": false,
  "statut_machine": "hors_ligne",
  "message": "Aucune donnée reçue de l'ESP32"
}
```

**Note :** La machine est considérée "hors_ligne" si aucune mesure n'a été reçue depuis > 5 minutes.

---

## 🔔 Routes - Alertes

### GET /api/alertes

Récupère toutes les alertes non résolues.

**Utilisé par :** Dashboard (notification badge)

#### Requête
```http
GET /api/alertes
```

#### Réponse (200)
```json
{
  "succes": true,
  "nombre_alertes": 2,
  "alertes": [
    {
      "id": 12,
      "date_heure": "2026-02-07 16:30:12",
      "type_alerte": "stock_faible",
      "severite": "attention",
      "message": "Niveau de zoom-koom faible (18%)",
      "boisson": "zoom-koom",
      "resolu": 0
    },
    {
      "id": 11,
      "date_heure": "2026-02-07 15:45:00",
      "type_alerte": "temperature_haute",
      "severite": "critique",
      "message": "Température élevée (16.2°C)",
      "boisson": null,
      "resolu": 0
    }
  ]
}
```

#### Types d'alertes

| Type | Sévérité | Description |
|------|----------|-------------|
| `stock_faible` | attention | Niveau réservoir < 20% |
| `temperature_haute` | critique | Température > 15°C |
| `erreur` | critique | Erreur système ESP32 |

---

### PUT /api/alerte/:id/resoudre

Marque une alerte comme résolue.

**Utilisé par :** Dashboard administrateur

#### Requête
```http
PUT /api/alerte/12/resoudre
```

#### Réponse (200)
```json
{
  "succes": true,
  "message": "Alerte 12 résolue"
}
```

#### Exemple avec curl
```bash
curl -X PUT http://localhost:5000/api/alerte/12/resoudre
```

---

## 📊 Routes - Statistiques

### GET /api/statistiques

Retourne toutes les statistiques importantes pour le dashboard.

**Utilisé par :** Dashboard (page statistiques complète)

**⚠️ Cette route peut être lente si beaucoup de données (> 1000 ventes).**

#### Requête
```http
GET /api/statistiques
```

#### Réponse (200)
```json
{
  "succes": true,
  "statistiques": {
    "aujourdhui": {
      "total_ventes": 47,
      "par_boisson": {
        "bissap": 28,
        "zoom-koom": 12,
        "tamarin": 7
      },
      "par_mode": {
        "bouton": 35,
        "web": 12
      }
    },
    "cette_semaine": {
      "total_ventes": 312,
      "par_boisson": {
        "bissap": 180,
        "zoom-koom": 85,
        "tamarin": 47
      },
      "par_jour": {
        "2026-02-01": 42,
        "2026-02-02": 38,
        "2026-02-03": 51,
        "2026-02-04": 45,
        "2026-02-05": 48,
        "2026-02-06": 41,
        "2026-02-07": 47
      }
    },
    "boisson_plus_populaire": {
      "boisson": "bissap",
      "nombre_ventes": 180
    },
    "consommation_moyenne_jour": {
      "bissap": 25.7,
      "zoom-koom": 12.1,
      "tamarin": 6.7
    },
    "temperature_moyenne_jour": 8.3,
    "ventes_par_heure": {
      "08h": 3,
      "09h": 7,
      "10h": 9,
      "11h": 6,
      "12h": 5,
      "13h": 4,
      "14h": 8,
      "15h": 3,
      "16h": 2
    }
  }
}
```

---

### GET /api/statistiques/jour

Statistiques du jour uniquement (plus rapide).

#### Requête
```http
GET /api/statistiques/jour
```

#### Réponse (200)
```json
{
  "succes": true,
  "statistiques": {
    "total_ventes": 47,
    "par_boisson": {
      "bissap": 28,
      "zoom-koom": 12,
      "tamarin": 7
    },
    "par_mode": {
      "bouton": 35,
      "web": 12
    }
  }
}
```

---

### GET /api/statistiques/semaine

Statistiques de la semaine.

#### Requête
```http
GET /api/statistiques/semaine
```

#### Réponse (200)
```json
{
  "succes": true,
  "statistiques": {
    "total_ventes": 312,
    "par_boisson": {
      "bissap": 180,
      "zoom-koom": 85,
      "tamarin": 47
    },
    "par_jour": {
      "2026-02-01": 42,
      "2026-02-02": 38,
      ...
    }
  }
}
```

---

### GET /api/statistiques/populaire

Retourne la boisson la plus vendue (tous les temps).

#### Requête
```http
GET /api/statistiques/populaire
```

#### Réponse (200)
```json
{
  "succes": true,
  "boisson_populaire": {
    "boisson": "bissap",
    "nombre_ventes": 523
  }
}
```

---

## 📈 Routes - Historiques

### GET /api/historique/niveaux/:boisson

Historique des niveaux d'une boisson sur X jours.

**Utilisé par :** Dashboard (graphiques d'évolution)

#### Requête
```http
GET /api/historique/niveaux/bissap?jours=7
```

#### Paramètres

| Paramètre | Type | Obligatoire | Défaut | Description |
|-----------|------|-------------|--------|-------------|
| boisson | string (URL) | ✅ Oui | - | `bissap`, `zoom-koom`, `tamarin` |
| jours | integer (query) | ❌ Non | 7 | Nombre de jours à récupérer |

#### Réponse (200)
```json
{
  "succes": true,
  "boisson": "bissap",
  "periode_jours": 7,
  "historique": [
    {
      "date_heure": "2026-02-01 08:00:00",
      "niveau": 100
    },
    {
      "date_heure": "2026-02-01 14:00:00",
      "niveau": 95
    },
    {
      "date_heure": "2026-02-01 20:00:00",
      "niveau": 88
    },
    ...
    {
      "date_heure": "2026-02-07 16:00:00",
      "niveau": 70
    }
  ]
}
```

#### Exemples
```bash
# Bissap sur 7 jours
GET /api/historique/niveaux/bissap?jours=7

# Zoom-koom sur 14 jours
GET /api/historique/niveaux/zoom-koom?jours=14

# Tamarin sur 30 jours
GET /api/historique/niveaux/tamarin?jours=30
```

---

### GET /api/historique/temperatures

Historique des températures sur X jours.

**Utilisé par :** Dashboard (graphique température)

#### Requête
```http
GET /api/historique/temperatures?jours=7
```

#### Paramètres

| Paramètre | Type | Obligatoire | Défaut | Description |
|-----------|------|-------------|--------|-------------|
| jours | integer (query) | ❌ Non | 7 | Nombre de jours |

#### Réponse (200)
```json
{
  "succes": true,
  "periode_jours": 7,
  "historique": [
    {
      "date_heure": "2026-02-01 08:00:00",
      "temperature": 8.2
    },
    {
      "date_heure": "2026-02-01 14:00:00",
      "temperature": 9.1
    },
    ...
  ]
}
```

---

## 💡 Exemples d'utilisation

### Exemple 1 : ESP32 envoie une vente

**Code ESP32 (Arduino C++) :**
```cpp
#include <HTTPClient.h>
#include <ArduinoJson.h>

void envoyerVente(String boisson, String mode) {
  HTTPClient http;
  
  // URL du serveur
  String url = "http://192.168.1.100:5000/api/vente";
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  // Créer le JSON
  StaticJsonDocument<200> doc;
  doc["boisson"] = boisson;
  doc["mode"] = mode;
  
  String requestBody;
  serializeJson(doc, requestBody);
  
  // Envoyer la requête POST
  int httpCode = http.POST(requestBody);
  
  if (httpCode == 201) {
    Serial.println("✅ Vente enregistrée");
  } else {
    Serial.println("❌ Erreur : " + String(httpCode));
  }
  
  http.end();
}

// Utilisation
void loop() {
  if (boutonBissapAppuye) {
    envoyerVente("bissap", "bouton");
  }
}
```

---

### Exemple 2 : Dashboard JavaScript récupère l'état

**Code JavaScript :**
```javascript
// Récupérer l'état de la machine toutes les 5 secondes
setInterval(async () => {
  try {
    const response = await fetch('http://localhost:5000/api/etat');
    const data = await response.json();
    
    if (data.succes) {
      // Mettre à jour l'interface
      document.getElementById('temperature').textContent = data.temperature + '°C';
      document.getElementById('niveau-bissap').textContent = data.niveaux.bissap + '%';
      document.getElementById('ventes-jour').textContent = data.ventes_jour;
      
      // Alertes
      if (data.nombre_alertes > 0) {
        document.getElementById('badge-alertes').textContent = data.nombre_alertes;
        document.getElementById('badge-alertes').style.display = 'block';
      }
    } else {
      // Machine hors ligne
      document.getElementById('statut').textContent = '🔴 Hors ligne';
    }
    
  } catch (error) {
    console.error('Erreur réseau:', error);
  }
}, 5000);
```

---

### Exemple 3 : Python récupère les statistiques

**Code Python :**
```python
import requests
import matplotlib.pyplot as plt

# Récupérer les stats
response = requests.get('http://localhost:5000/api/statistiques')
data = response.json()

stats = data['statistiques']['aujourdhui']

# Créer un graphique
boissons = list(stats['par_boisson'].keys())
ventes = list(stats['par_boisson'].values())

plt.bar(boissons, ventes)
plt.title('Ventes du jour par boisson')
plt.xlabel('Boisson')
plt.ylabel('Nombre de ventes')
plt.show()
```

---

## 🔧 Codes d'erreur détaillés

### 400 - Bad Request

**Cas 1 : Champ manquant**
```json
{
  "erreur": "Le champ \"boisson\" est obligatoire"
}
```

**Cas 2 : Valeur invalide**
```json
{
  "erreur": "Boisson invalide. Choix : bissap, zoom-koom, tamarin"
}
```

**Cas 3 : Aucune donnée**
```json
{
  "erreur": "Aucune donnée reçue"
}
```

---

### 404 - Not Found

**Cas 1 : Route inexistante**
```json
{
  "erreur": "Route inexistante",
  "url_demandee": "http://localhost:5000/api/inexistant"
}
```

**Cas 2 : Ressource introuvable**
```json
{
  "succes": false,
  "message": "Aucune mesure enregistrée"
}
```

---

### 500 - Internal Server Error

**Erreur serveur générique**
```json
{
  "erreur": "Erreur interne du serveur",
  "details": "database is locked"
}
```

---

## 📞 Support

Pour toute question sur l'API :

- **Email :** wilfried.kielem@u-naziboni.net
- **Téléphone :** 58 49 84 77
- **Logs :** Consultez `logs/serveur.log` pour le debug

---

## 📝 Changelog

### Version 1.0 (Février 2026)
- ✅ Routes ventes, mesures, alertes
- ✅ Statistiques avancées
- ✅ Historiques sur plusieurs jours
- ✅ Système d'alertes automatiques

### Version future (v2.0)
- 🔜 Authentification API Key
- 🔜 WebSocket pour temps réel
- 🔜 Export CSV/PDF des statistiques
- 🔜 Système de paiement mobile money

---

**Dernière mise à jour :** 7 février 2026