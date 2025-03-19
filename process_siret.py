import pandas as pd
from auth import get_token
from api import get_siret

# Récupération du token
token = get_token()

# Chargement du fichier de données (test.csv) avec l'encodage correct
df = pd.read_csv('c:\\Users\\FORMATION6\\Sabathgron\\atypic-lagence\\siret\\siret\\test.csv', encoding='ISO-8859-1')

# Ajouter une colonne avec les numéros SIRET
df['SIRET'] = df.apply(lambda row: get_siret(row['Nom client (complet)'], row['adresse 1'], token), axis=1)

# Sauvegarder le fichier mis à jour en format CSV
df.to_csv('c:\\Users\\FORMATION6\\Sabathgron\\atypic-lagence\\siret\\siret\\fichier_avec_siret.csv', index=False)

