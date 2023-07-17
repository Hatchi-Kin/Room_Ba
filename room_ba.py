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
    return f"id du salon update! \n Prochain message automatique a {HEURE} "
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
    info = get_the_comande(id_salon)#restour dans le salon que la comande est effective 
    print("salon id set : ",id_salon)
    last_id_salon['last_id'] = id_salon
    await ctx.send(info)
    await on_ready()

@bot.command(name='semaine', help="Affiche la salle de classe pour ce matin")
async def room_afternoon_command(ctx):
    info = semaine()
    await ctx.send(info)
    
def automatique():
    response = requests.get(ICS_URL)
    today = datetime.date.today()
    filtre_events = []
    tomorrow = datetime.date.today() + datetime.timedelta(days=-2)
    calendar = Calendar(response.text)
    events = [event for event in calendar.events if event.begin.date() == today]
    
    if events:
        # Il y a deux événements par jour, le premier [0] , le deuxième [1] qui ont la posibilité de changer d'ordre
        event_1 = events[0]
        event_2 = events[1]
#####################################################################################
#determiné le matin de l'aprem par une liste de"filtre event"du plus tot au plus tard
#####################################################################################
        for event in events:
            if event.begin.date() == today:
                filtre_events.append(event)
        text_automatique=""
        for i in range (len(filtre_events)):
            text_automatique=text_automatique + f"\n\n {event_affichage(filtre_events[i])}"
        return text_automatique
        #return f"matin :\n {event_affichage(event_matin)}\n\n aprem :\n {event_affichage(event_aprem)}"

   else:
        return "Aucun événement trouvé pour cette date le matin."

def event_affichage(event):
    description = event.description.encode('latin-1').decode('utf-8')
    intervenant = ""
    for line in description.splitlines():
        if line.startswith("- Intervenant(s) :"):
            intervenant += line
    location = event.location.encode('latin-1').decode('utf-8')
    message = f" Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]} "
    return message
#################################################
async def on_ready():
    if not hasattr(bot, 'is_schedule_running'):
        bot.is_schedule_running = True
        schedule.every().day.at(HEURE).do(lambda: asyncio.create_task(send_message()))  #asyncio.create_task() execute la coroutine en arrière-plan
        # Run the schedule in the background
        while True:
            schedule.run_pending()
            await asyncio.sleep(1)

async def send_message():
    last_id = last_id_salon.get('last_id')
    channel = bot.get_channel(int(last_id))  # ID du channel room-bot
    if channel:
        await channel.send(automatique())


def semaine():
    print("tenetative de faire une semaine")
    dt = datetime.now()
    # get day of the week as an integer (Monday = 0, Sunday = 6)
    jour_nombre = dt.weekday()
    for i in range(0,6): #faire afichr la semaine actuelle  
        
    
    
    return jour_semaine
    

print('Bot is ready.')
print('heure prevu',HEURE)
#asyncio.run(on_ready(ID_SALON))

bot.run(TOKEN)
print(f'We have logged in as {bot.user.name}')
