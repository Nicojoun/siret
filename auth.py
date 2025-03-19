import requests
import base64

# Vos identifiants d'accès
client_id = 'OOzy2in6dIAQXl95Cwm34ZSmaQMa'
client_secret = 'bWnRhjIh0gufNfGIYfjgLrDs1Foa'

# Fonction pour obtenir le token d'accès
def get_token():
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

print(get_token())

# 7yyUr(AU&KwB