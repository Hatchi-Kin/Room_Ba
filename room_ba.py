import datetime
import discord
from discord.ext import tasks, commands
from ics import Calendar, Event
import requests
import schedule
import asyncio
from dotenv import load_dotenv
import os
import asyncio

load_dotenv() #load la rariable TOKEN et ICS_URL
TOKEN = os.getenv('TOKEN')
ICS_URL = os.getenv('ICS_URL')
ID_SALON = os.getenv('ID_SALON')
HEURE = os.getenv('HEURE')

intents = discord.Intents.all()
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)
last_id_salon = {} #dicsionaire pour le salon automatique   
 

#################################################

def get_the_right_room(commande: str) -> str:
    response = requests.get(ICS_URL)
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

def get_the_comande(id):
    return "id du salon update: ",id
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
    
@bot.command(name='id', help="Affiche la salle de classe pour le lendemain")
async def command(ctx):    
    id_salon = ctx.channel.id
    info = get_the_comande(id_salon)
    print("salon id set : ",id_salon)
    last_id_salon['last_id'] = id_salon

    await ctx.send(info)
    await on_ready(id_salon)

def automatique():
    response = requests.get(ICS_URL)
    today = datetime.date.today()
    
    filtre_events = []
    
    calendar = Calendar(response.text)
    events = [event for event in calendar.events if event.begin.date() == today]
    if events:
        # Il y a deux événements par jour, le premier [0] , le deuxième [1] 
        event_matin = events[0]
        event_aprem = events[1]
        
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
        
#####################################################################################
#determiné le matin de l'aprem par une liste de"filtre event"du plus tot au plus tard
#####################################################################################
        for event in events:
            if event.begin.date() == today:
                filtre_events.append(event)
                
        filtre_events.sort(key=lambda event: event.begin.time())
        if filtre_events:
            horaire_matin = filtre_events[0].begin.time()
            horaire_aprem = filtre_events[1].begin.time()
        else:
            return "format de date non valide ou inexistant"

        return f"matin : Salle : {location}Commence à : {event_matin.begin.time()}\n{intervenant_matin[2:]} \n\n aprem : Salle : {location}Commence à : {event_aprem.begin.time()}\n{intervenant_aprem[2:]} \n \n horaire matin:{horaire_matin} -- horaire aprem:{horaire_aprem}"

    else:
        return "Aucun événement trouvé pour cette date le matin."

#################################################

async def on_ready(id_salon):
    print(f'We have logged in as {bot.user.name}')
    if not hasattr(bot, 'is_schedule_running'):
        bot.is_schedule_running = True
        schedule.every().day.at(HEURE).do(lambda: asyncio.create_task(send_message(id_salon)))  #asyncio.create_task() execute la coroutine en arrière-plan
        # Run the schedule in the background
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

async def send_message(id_salon):
    last_id = last_id_salon.get('last_id')
    channel = bot.get_channel(int(last_id))  # ID du channel room-bot
    if channel:
        await channel.send(automatique())
print('Bot is ready.')
print('heure prevu',HEURE)
#asyncio.run(on_ready(ID_SALON))
bot.run(TOKEN)
