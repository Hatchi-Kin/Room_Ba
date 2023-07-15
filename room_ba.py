import os
import datetime
import requests
import discord
from discord.ext import tasks, commands
from ics import Calendar, Event
from dotenv import load_dotenv

#################################################

load_dotenv()
# Pour que le bot fonctionne, il faut renseigner votre token discord dans le fichier .env
# de même pour l'url de votre fichier .ics (les valeurs sont à remplacer SANS guillemets dans le .env mais AVEC dans le .py)
TOKEN = os.getenv('DISCORD_TOKEN')
ICS_URL = os.getenv('ICS_URL')
intents = discord.Intents.all()
# On déclare le bot avec le préfixe de commande qui servera à l'appeler dans le chat discord
bot = commands.Bot(command_prefix='!', intents=intents)

#################################################

# Fonction qui permet de lire la bonne partie du fichier .ics en fonction de la commande
def get_the_right_room(commande: str) -> str:

    # Envoie une requête GET à l'URL en utilisant la bibliothèque requests.
    # La réponse du serveur est stockée dans la variable response.
    # On peut utiliser response.text pour avoir le contenu de la réponse en string
    global ICS_URL
    response = requests.get(ICS_URL)
    calendar = Calendar(response.text)

    # On déclare les variables date et matin_aprem en fonction de la commande pour pouvoir les utiliser plus tard
    if commande == "matin":
        # date servira à comparer la date de début de l'événement avec la date du jour quand on parcourra le fichier .ics
        date = datetime.date.today()
        # matin_aprem servira à récupérer le bon événement dans la liste des événements du jour
        matin_aprem = 0
    elif commande == "aprem":
        date = datetime.date.today()
        matin_aprem = 1
    elif commande == "demain":
        date = datetime.date.today() + datetime.timedelta(days=1)
        matin_aprem = 0

    # les fichiers .ics sont des enchainements d'événements, on parcourt donc tous les événements du fichier
    # et on stocke dans la variable events une liste de tous les événements qui ont lieu à la date définie plus haut    
    events = [event for event in calendar.events if event.begin.date() == date]

    if events:
        # La liste events n'est pas triée toujours dans le même ordre, 
        # On a donc besoin de la trier pour pouvoir faire confiance aux index et récupérer le bon événement
        # .sort() modifie la liste events sur place dans l'odre croissant des heures de début des événements
        events.sort(key=lambda x: x.begin.time())
        # Il y a deux événements par jours, un pour la matinée et un pour l'après-midi
        # le premier [0] est celui de 09h00, le deuxième [1] est celui de 14h00
        # On récupère donc le bon événement en fonction de la commande
        event = events[matin_aprem]
        # les fichiers .ics sont encodés en latin-1, on les décode en utf-8 pour pouvoir les afficher
        description = event.description.encode('latin-1').decode('utf-8')
        location = event.location.encode('latin-1').decode('utf-8')
        # strftime permet de formater la date et l'heure pour ne pas afficher les secondes
        horaire = event.begin.time().strftime("%H:%M")
        # Pas envie de récupérer toute les lignes présentes dans description, on récupère juste les lignes qui nous intéressent.
        # On initialise les variables intervenant et descript pour pouvoir les remplir avec les bonnes lignes
        intervenant = ""
        descript = ""
        for line in description.splitlines():
            if line.startswith("- Intervenant(s) :"):
                intervenant += line
            if line.startswith("- Description :"):
                descript += line

        # On retourne le message à afficher formatté tout joli
        # [2:] permet de supprimer les deux premiers caractères (sur le fichier .ics, il y a un tiret et un espace avant le texte)
        return f"Salle : {location}Commence à : {horaire}\n{intervenant[2:]}\n{descript[2:]}"       
    else:
        return "Aucun événement trouvé pour cette date."
    
#################################################

# Fonctions exécutées quand le bot est appelé par une commande.
# une commande est un message qui commence par le préfixe défini plus haut et qui est suivi du nom de la commande 
@bot.command(name='matin', help="Affiche la salle de classe pour ce matin")
async def room_morning_command(ctx):
    # ctx est le contexte de la commande, il contient des informations sur l'auteur de la commande, le channel, etc.
    # On utilise ctx.send pour envoyer un message dans le channel où la commande a été envoyée
    info = get_the_right_room("matin")
    await ctx.send(info)

@bot.command(name='aprem', help="Affiche la salle de classe pour cet après-midi")
async def room_afternoon_command(ctx):
    info = get_the_right_room("aprem")
    await ctx.send(info)

@bot.command(name='demain', help="Affiche la salle de classe pour le lendemain")
async def room_tomorrow_command(ctx):    
    info = get_the_right_room("demain")
    await ctx.send(info)

#################################################

if __name__ == "__main__":
    bot.run(TOKEN)
