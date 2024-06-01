#!/bin/bash

# commnade pour construire les images:

# image my_authentication:latest

docker image build . -t my_authentication:latest -f Dockerfile_authentication

# image my_authorization:latest

docker image build . -t my_authorization:latest -f Dockerfile_perm

# image my_content:latest

docker image build . -t my_content:latest -f Dockerfile_content


# lancer le docker-compose

docker-compose up

# Voici les commandes utilisés pour faire des tests individuellement

# Aprésa avoir crée une image my_auth, je reste sur le dossier, et je crée un fichier vide appelé api_test.log

# je crée un volume appelé mon_volume

docker volume create --name mon_volume

# Je copie api_test.log dans mon volume

sudo mv ~/api_test.log /var/lib/docker/volumes/my_volume/_data/api_test.log

# je lance la commande qui appelle le container de test sur mon container de l'api

# je rappelle que le container de l'api est lancé en exposant son port 8000:800 et sur network=my_network

docker container run --rm --network my_network -p 8000:8000 --name api_container  datascientest/fastapi:1.0.0

 # je lance mes containers de tests avec les commandes suivantes

 # Authentication:

docker run -it --rm -e 'LOG'='1' --network my_network\
  --name my_authentication_test\
  --mount type=volume,src=mon_volume,dst=/home/my_folder my_authentication:latest bash

 # Authorization:

 docker run -it --rm -e 'LOG'='1' --network my_network\
  --name my_authorization_test\
  --mount type=volume,src=mon_volume,dst=/home/my_folder my_authorization:latest bash

  # content:

docker run -it --rm -e 'LOG'='1' --network my_network\
  --name my_content_test\
  --mount type=volume,src=mon_volume,dst=/home/my_folder my_content:latest bash



# Une fois dans le container, je vérifie le contenu

ls /home/my_folder

cat /home/my_folder/api_test.log

# Je peux donc copier le contenu dans un fichier appelé log.txt

# pour cela , je reste sur le dossier local, et j'execute la commande suivante pour chaque container

docker cp my_authentication_test:/home/my_folder/api_test.log log.txt

docker cp my_authorization_test:/home/my_folder/api_test.log log.txt

docker cp my_content_test:/home/my_folder/api_test.log log.txt
