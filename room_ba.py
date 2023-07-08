import datetime
import discord
from discord.ext import tasks, commands
from ics import Calendar, Event
import requests

# Pour que le bot fonctionne, il faut renseigner votre token discord ici 
# et l'url de votre fichier .ics (première ligne de la fonction get_the_right_room)
TOKEN = "DISCORD TOKEN HERE"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

#################################################

# Fonction qui permet de lire la bonne partie du fichier .ics en fonction de la commande
def get_the_right_room(commande: str) -> str:

    ics_url = "URL TO YOUR .ICS HERE"
    # sends a GET request to the URL using the requests library. 
    # The response from the server is stored in the response variable. 
    # You can then access the response content using response.content
    response = requests.get(ics_url)
    today = datetime.date.today()

    if commande == "matin":
        calendar = Calendar(response.text)
        # les fichiers .ics sont des enchainements d'événements, on parcourt donc tous les événements du fichier
        # et on ne garde que ceux qui ont lieu aujourd'hui
        events = [event for event in calendar.events if event.begin.date() == today]
        if events:
            # Il y a deux événements par jours, un pour la matinée et un pour l'après-midi
            # le premier [0] est celui de 09h00, le deuxième [1] est celui de 14h00
            event = events[0]
            # les fichiers .ics sont encodés en latin-1, on les décode en utf-8 pour pouvoir les afficher
            description = event.description.encode('latin-1').decode('utf-8')
            # Pas envie de récupérer toute la description, on récupère juste les lignes qui nous intéressent.
            # les fichiers .ics sont encodés en latin-1, on les décode en utf-8 pour pouvoir les afficher
            location = event.location.encode('latin-1').decode('utf-8')
            # strftime permet de formater la date et l'heure pour ne pas afficher les secondes
            horaire = event.begin.time().strftime("%H:%M")
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


    elif commande == "aprem":
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == today]
        if events:
            event = events[1]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            descript = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
                if line.startswith("- Description :"):
                    descript += line
            location = event.location.encode('latin-1').decode('utf-8')
            horaire = event.begin.time().strftime("%H:%M")
            return f"Salle : {location}Commence à : {horaire}\n{intervenant[2:]}\n{descript[2:]}"
        else:
            return "Aucun événement trouvé pour cette date."
        

    elif commande == "demain":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == tomorrow]
        if events:
            event = events[0]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            descript = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
                if line.startswith("- Description :"):
                    descript += line
            location = event.location.encode('latin-1').decode('utf-8')
            horaire = event.begin.time().strftime("%H:%M")
            return f"Salle : {location}Commence à : {horaire}\n{intervenant[2:]}\n{descript[2:]}"
        else:
            return "Aucun événement trouvé pour cette date."
        
    else:
        return "Want some help? Type !help :) "

#################################################

# Action à effectuer pour la commande !matin
@bot.command(name='matin', help="Affiche la salle de classe pour ce matin")
async def room_morning_command(ctx):    
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

bot.run(TOKEN)
