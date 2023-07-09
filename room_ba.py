import datetime
import discord
from discord.ext import tasks, commands
from ics import Calendar, Event
import requests
import schedule
import asyncio
# Pour que le bot fonctionne, il faut renseigner votre token ici et l'url de votre fichier .ics (première ligne de la fonction get_the_right_room)
TOKEN = "MTExNzA3NDc0MjEwMTQyNjI2Nw.GztRX8.okIg9igBDFTq1kjHhRQ7gno5DgkL3q3ooTt36A"

intents = discord.Intents.all()
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

#################################################

# Fonction qui permet de lire la bonne partie du fichier .ics en fonction de la commande
def get_the_right_room(commande: str) -> str:

    ics_url = "https://web.isen-ouest.fr/ICS/23_24_CODE_BZH_MICROSOFT_BREST_ALT.ics"
    # sends a GET request to the URL using the requests library. 
    # The response from the server is stored in the response variable. 
    # You can then access the response content using response.content
    response = requests.get(ics_url)
    today = datetime.date.today()

    if commande == "matin":
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == today]
        if events:
            # Il y a deux événements par jour, etrangement, étrangement, le premier [0] est celui de 14h00, le deuxième [1] est celui de 09h00
            event = events[1]
            description = event.description.encode('latin-1').decode('utf-8')
            # Pas envie de récupérer toute la description, on récupère juste la ligne qui nous intéresse
            intervenant = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
            # les fichiers .ics sont encodés en latin-1, on les décode en utf-8 pour pouvoir les afficher
            location = event.location.encode('latin-1').decode('utf-8')
            # On retourne le message à afficher formatté tout joli
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]}"
        else:
            return "Aucun événement trouvé pour cette date le matin."


    elif commande == "aprem":
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == today]
        if events:
            event = events[0]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
            location = event.location.encode('latin-1').decode('utf-8')
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]}"
        else:
            return "Aucun événement trouvé pour cette date l'aprem."
        

    elif commande == "demain":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == tomorrow]
        if events:
            # pour une raison que je ne comprends pas, ici, le seul moyen d'afficher le premier événement de la liste est de prendre le deuxième
            event = events[1]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
            location = event.location.encode('latin-1').decode('utf-8')
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]}"
        else:
            return "Aucun événement trouvé pour demain."
        
    else:
        return "Wut?"

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


def automatique():
    ics_url = "https://web.isen-ouest.fr/ICS/23_24_CODE_BZH_MICROSOFT_BREST_ALT.ics"
    # sends a GET request to the URL using the requests library. 
    # The response from the server is stored in the response variable. 
    # You can then access the response content using response.content
    response = requests.get(ics_url)
    today = datetime.date.today()
    calendar = Calendar(response.text)
    events = [event for event in calendar.events if event.begin.date() == today]
    if events:
        # Il y a deux événements par jour, etrangement, étrangement, le premier [0] est celui de 14h00, le deuxième [1] est celui de 09h00
        event_matin = events[1]
        event_aprem = events[0]
        
        description_matin = event_matin.description.encode('latin-1').decode('utf-8')
        intervenant_matin = ""
        for line in description_matin.splitlines():
            if line.startswith("- Intervenant(s) :"):
                intervenant_matin += line
        location = event_matin.location.encode('latin-1').decode('utf-8')

        description_aprem = event_aprem.description.encode('latin-1').decode('utf-8')
        intervenant_aprem = ""
        for line in description_aprem.splitlines():
            if line.startswith("- Intervenant(s) :"):
                intervenant_aprem += line
        location = event_aprem.location.encode('latin-1').decode('utf-8')

        return f"matin : Salle : {location}Commence à : {event_matin.begin.time()}\n{intervenant_matin[2:]} \b aprem : Salle : {location}Commence à : {event_aprem.begin.time()}\n{intervenant_aprem[2:]} "

    else:
        return "Aucun événement trouvé pour cette date le matin."

#################################################


@bot.event
async def on_ready():
    print('Bot is ready.')
    # Schedule the task to run every day at 8 AM
    schedule.every().day.at('00:01').do(lambda: asyncio.create_task(send_message()))  # Utilisez asyncio.create_task() pour exécuter la coroutine en arrière-plan
    # Run the schedule in the background
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

async def send_message():
    channel = bot.get_channel(1112449155848212640)  # ID du channel room-bot

    if channel:
        await channel.send(automatique())


bot.run(TOKEN)
