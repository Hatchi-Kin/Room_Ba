# Room_Ba le gentil bot discord

L'ISEN utilise le service WebAurion pour que profs et étudiants aient un accès à leur planning.
Ce c'est pas très pratique à utiliser, en particulier lorsqu'on veut juste rapidement
afficher l'heure et la salle de notre prochain cours.

Ce bot discord écrit en python permet de:
 - lire le fichier .ics (calendrier) hebergé et renseigné par l'ISEN
 - pour afficher quelques infos dont le numéro de salle réservée et l'heure du prochain cours.

Pour utiliser cette version du bot, vous avez besoin:
 - de votre propre bot discord avec un Token 
 - de l'url du fichiers ics qui contient les informations de votre promo
 - d'enregistrer ces infos dans le fichier .env

Pour trouver l'url du fichier ics de votre promo, vous pouvez essayer de vous rendre sur le webaurion 
 -  -> planning des groupes 
 - -> naviguez jusqu'a afficher le planning de votre promo, 
 - -> cliquez sur une des case du calendrier.
 - -> dans l'onglet GROUPES, le texte CODE peut être utilisé à la place des 0000 dans le template
 - "https://web.isen-ouest.fr/0000000000.ics"
