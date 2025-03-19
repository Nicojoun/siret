import requests
import pandas as pd
import base64
import urllib.parse

import os

# Vos identifiants d'accès (récupérés depuis les variables d'environnement)
client_id = os.getenv('CLIENT_ID', 'OOzy2in6dIAQXl95Cwm34ZSmaQMa')
client_secret = os.getenv('CLIENT_SECRET', 'bWnRhjIh0gufNfGIYfjgLrDs1Foa')

if client_id == 'default_client_id' or client_secret == 'default_client_secret':
    raise Exception("Veuillez définir les variables d'environnement CLIENT_ID et CLIENT_SECRET.")

# Fonction pour obtenir le token d'accès
def get_token(client_id, client_secret):
    url = 'https://api.insee.fr/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Erreur lors de l'obtention du token : {response.status_code} - {response.text}")

# Fonction pour récupérer le numéro SIRET via l'API SIRENE
def get_siret(name, address, token):
    url = 'https://api.insee.fr/entreprises/sirene/V3.11/siret'
    params = {
        'q': f'denominationUniteLegale:{urllib.parse.quote(name)} AND adresseEtablissement:{urllib.parse.quote(address)}'
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
        print(f"Erreur lors de la récupération du SIRET pour {name} à {address} : {response.status_code} - {response.text}")
    return "erreur"

# Récupération du token
token = get_token(client_id, client_secret)

try:
    # Chargement du fichier de données (test.csv) avec l'encodage correct
    df = pd.read_csv('c:\\Users\\FORMATION6\\Sabathgron\\atypic-lagence\\siret\\siret\\test.csv', encoding='ISO-8859-1')
    
    # Vérification des colonnes requises
    required_columns = ['Nom client (complet)', 'adresse 1']
    for col in required_columns:
        if col not in df.columns:
            raise Exception(f"La colonne requise '{col}' est absente du fichier CSV.")
    
    # Ajouter une colonne avec les numéros SIRET
    df['SIRET'] = df.apply(
        lambda row: get_siret(row['Nom client (complet)'], row['adresse 1'], token)
        if pd.notnull(row['Nom client (complet)']) and pd.notnull(row['adresse 1'])
        else "données manquantes",
        axis=1
    )
    
    # Sauvegarder le fichier mis à jour
    df.to_csv('c:\\Users\\FORMATION6\\Sabathgron\\atypic-lagence\\siret\\siret\\fichier_avec_siret.csv', index=False)

except FileNotFoundError:
    raise Exception("Le fichier test.csv est introuvable.")
except pd.errors.EmptyDataError:
    raise Exception("Le fichier test.csv est vide.")
