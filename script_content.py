import os
import requests
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Définir l'adresse et le port de l'API
api_address = 'api_container'
api_port = 8000

# Définir une liste d'utilisateurs et de phrases
users = [{'username': 'alice', 'password': 'wonderland'}]
phrases = ['life is beautiful', 'that sucks']

# Définir une liste d'endpoints
endpoints = ['v1/sentiment', 'v2/sentiment']

# Initialiser une chaîne de journal vide
log = ""

# Boucler à travers chaque utilisateur, phrase et endpoint
for user in users:
    for phrase in phrases:
        for endpoint in endpoints:
            # Effectuer une requête vers l'endpoint spécifié
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{endpoint}',
                params={'username': user['username'], 'password': user['password'], 'sentence': phrase}
            )

            # Obtenir le score du sentiment
            score = r.json().get('score', 0)

            # Définir le statut du test
            if (phrase == 'life is beautiful' and score > 0) or (phrase == 'that sucks' and score < 0):
                test_status = 'SUCCÈS'
            else:
                test_status = 'ÉCHEC'

            # Ajouter le résultat au journal
            log += f'''
============================
    Test content
============================

Requête effectuée à "/{endpoint}/{phrase}"
| usernam="{user['username']}"
| password="{user['password']}"
| sentence="{phrase}"

==>  {test_status}
'''

# Afficher le journal
print(log)

# Enregistrer le journal dans un fichier si la variable d'environnement LOG est définie à 1

if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a',encoding='utf-8') as file:
        file.write(log)
