
import datetime
from ics import Calendar
import requests
import os
import streamlit as st
import os
import datetime
import requests
from ics import Calendar, Event
import numpy as np
import pandas as pd

def semaine():
    # joure de la semaine (lundi = 0, dimanche = 6)
    joure_actuel = datetime.datetime.now().weekday()
    #print("jour=",joure_actuel)
    semaine_resultat = []
    i=joure_actuel 
    while i >= 0:
        semaine_resultat.append(i*(-1))
        i=i-1
    i=1
    while i <= 6-joure_actuel:
        semaine_resultat.append(i)
        i=i+1
    print("semaine =" ,semaine_resultat)
    return semaine_resultat

response = requests.get('ICS')
calendar = Calendar(response.text)
jour_semaine=semaine()

# date location horaire horaire_fin description     

def data_planning(jour_n):
    date = datetime.date.today() + datetime.timedelta(days=jour_n)
    events = [event for event in calendar.events if event.begin.date() == date]
    if events:
        events.sort(key=lambda x: x.begin.time())
        journee = []
        for i in events:
            date = i.begin.date().strftime("%d/%m/%Y")
            description = i.description.encode('latin-1').decode('utf-8')   
            location = i.location.encode('latin-1').decode('utf-8') if i.location is not None else ""
            horaire = i.begin.time().strftime("%H:%M")
            horaire_fin = i.end.time().strftime("%H:%M")
            journee.append([date, location, horaire, horaire_fin, description])
        return pd.DataFrame(journee, columns=['date', 'location', 'horaire', 'horaire_fin', 'description'])

df = pd.DataFrame(columns=['date', 'location', 'horaire', 'horaire_fin', 'description'])

for i in range(len(jour_semaine)):
    print(jour_semaine[i])
    df = df._append(data_planning(jour_semaine[i]), ignore_index=True)
    
df.to_csv("./semaine.csv", index=False)
