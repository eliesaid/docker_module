import os
import requests

import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# Définir l'adresse et le port de l'API
api_address = 'api_container'
api_port = 8000

# Définir une liste d'utilisateurs et de mots de passe
users = [
    {'username': 'alice', 'password': 'wonderland'},
    {'username': 'bob', 'password': 'builder'},
    {'username':'clementine','password':"mandarine"}
]

# Initialiser une chaîne de journal vide
log = ""
# Boucler à travers chaque utilisateur
for user in users:
    # Effectuer une requête vers l'endpoint "/permissions"
    r = requests.get(
        url=f'http://{api_address}:{api_port}/permissions',
        params=user
    )

    # Définir le code d'état attendu
    expected_status_code = 200

    # Obtenir le code d'état réel
    actual_status_code = r.status_code

    # Vérifier si la requête a réussi
    if actual_status_code == expected_status_code:
        test_status = 'SUCCÈS'
    else:
        test_status = 'ÉCHEC'

    # Ajouter le résultat au journal
    
    log += f'''
============================
    Test authentication
============================

request done at "/permissions"
| username="{user['username']}"
| password="{user['password']}"

Résultat attendu = {expected_status_code}
Résultat réel = {actual_status_code}

==>  {test_status}
'''

# Afficher le journal
print(log)

# Enregistrer le journal dans un fichier si la variable d'environnement LOG est définie à 1

if os.environ.get('LOG') == '1':
    with open('api_test.log', 'a',encoding='utf-8') as file:
        file.write(log)
