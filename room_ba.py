import datetime
import discord
from discord.ext import tasks, commands
from ics import Calendar, Event
import asyncio
import requests

TOKEN = "YOUR TOKEN HERE"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

#################################################

def get_the_right_room(commande):
    ics_url = "URL TO YOUR .ICS HERE"
    response = requests.get(ics_url)
    today = datetime.date.today()

    if commande == "matin":
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
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant}"
        else:
            return "Aucun événement trouvé pour cette date."

    elif commande == "aprem":
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == today]
        if events:
            event = events[1]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
            location = event.location.encode('latin-1').decode('utf-8')
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant}"
        else:
            return "Aucun événement trouvé pour cette date."
        
    elif commande == "demain":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == tomorrow]
        if events:
            event = events[1]
            description = event.description.encode('latin-1').decode('utf-8')
            intervenant = ""
            for line in description.splitlines():
                if line.startswith("- Intervenant(s) :"):
                    intervenant += line
            location = event.location.encode('latin-1').decode('utf-8')
            return f"Salle : {location}Commence à : {event.begin.time()}\n{intervenant}"
        else:
            return "Aucun événement trouvé pour cette date."
        
    else:
        return "Aucun événement trouvé pour cette date."

#################################################

@bot.command(name='matin', help="Affiche la salle de classe pour ce matin")
async def room_command(ctx):    
    info = get_the_right_room("matin")
    await ctx.send(info)


@bot.command(name='aprem', help="Affiche la salle de classe pour cet après-midi")
async def room_command(ctx):
    info = get_the_right_room("aprem")
    await ctx.send(info)


@bot.command(name='demain', help="Affiche la salle de classe pour le lendemain")
async def room_tomorrow_command(ctx):    
    info = get_the_right_room("demain")
    await ctx.send(info)

#################################################

bot.run(TOKEN)
