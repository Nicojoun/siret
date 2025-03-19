import requests
import urllib.parse

# Fonction pour récupérer le numéro SIRET via l'API SIRENE
def get_siret(name, token):
    url = 'https://api.insee.fr/entreprises/sirene/V3.11/siret'
    # Encodage des paramètres pour gérer les espaces et caractères spéciaux
    name_encoded = urllib.parse.quote(name)
    # Construction de la requête avec uniquement le nom
    params = {
        'q': f'denominationUniteLegale:"{name_encoded}"'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        etablissements = data.get('etablissements', [])
        if etablissements:
            return etablissements[0].get('siret')
    else:
        print(f"Erreur lors de la récupération du SIRET pour '{name}' : {response.status_code} - {response.text}")
    return "erreur"
