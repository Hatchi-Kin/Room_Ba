# Room_Ba le gentil bot discord


L'ENT de l'ISEN n'est pas facilement accessible quand on veut rapidement savoir quelle salle a été reservée.
Ce bot permet de lire le fichier .ics (calendrier) hebergé par l'ISEN
et d'afficher quelques infos dont le numéro de salle réservée.

<h2>install</h2>
<h3>linux install </h3>

integré les valeurs d'environement dans le ".env"

        cp .env-exemple .env

installer les dependance python


        pip install -r requirements.txt


<h3>docker install </h3>

integré les valeurs d'environement dans le "docker-compose.yml"


        cp docker-compose.yml-exemple docker-compose.yml

lancer le docker-compose 

        docker-compose up -d


<h2>utilisation dans discord</h2>

utilisé "!id" dans un salon pour que le bot selectionne le salon dans
lequel il postera automatiquement les horaires et numereau de salle 
