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
def get_the_comande(id):
    return f"id du salon update! \n Prochain message automatique a {HEURE} "
#################################################

    
@bot.command(name='id', help="Affiche la salle de classe pour le lendemain")
async def command(ctx):    
    id_salon = ctx.channel.id
    info = get_the_comande(id_salon)#restour dans le salon que la comande est effective 
    print("salon id set : ",id_salon)
    last_id_salon['last_id'] = id_salon
    await ctx.send(info)
    await on_ready()

def automatique():
    response = requests.get(ICS_URL)
    today = datetime.date.today()
    filtre_events = []
    tomorrow = datetime.date.today() + datetime.timedelta(days=-2)
    calendar = Calendar(response.text)
    events = [event for event in calendar.events if event.begin.date() == today]
    
    if events:
###########################################################################################
#determiné le matin de l'aprem par une liste de"filtre_events"du plus tot au plus tard
###########################################################################################
        for event in events:
            if event.begin.date() == today:
                filtre_events.append(event)
        filtre_events.sort(key=lambda item: item.begin.time())
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


print('Bot is ready.')
print('heure prevu',HEURE)
#asyncio.run(on_ready(ID_SALON))

bot.run(TOKEN)
print(f'We have logged in as {bot.user.name}')
