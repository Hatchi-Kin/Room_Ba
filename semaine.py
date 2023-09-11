
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
    semaine_resultat = [[],[]]
    liste_joure=["lundi","mardi","mercredi","jeudi","vendredi","samedi","dimanche"]
    y=0
    i=joure_actuel 
    while i >= 0:
        semaine_resultat[0].append(i*(-1))
        semaine_resultat[1].append(liste_joure[y])
        i=i-1
        y=y+1
    i=1
    while i <= 6-joure_actuel:
        semaine_resultat[0].append(i)
        semaine_resultat[1].append(liste_joure[y])
        i=i+1
        y=y+1
    
    print("semaine =" ,semaine_resultat)
    return semaine_resultat
rep=st.text_input('le input')

def data_planning(jour_n,jour_string):
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
            journee.append([jour_string,date, location, horaire, horaire_fin, description])
        return pd.DataFrame(journee, columns=['jour','date', 'location', 'horaire', 'horaire_fin', 'description'])
df = pd.DataFrame(columns=['jour','date', 'location', 'horaire', 'horaire_fin', 'description'])

@st.cache_data 
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

if rep:
    response = requests.get(rep)
    calendar = Calendar(response.text)
    jour_semaine=semaine()
    for i in range(len(jour_semaine[0])):
        print(f"jour{jour_semaine[0][i]}:{jour_semaine[1][i]} ")
        print(f"nombre de jour{len(jour_semaine)}")
        df = df._append(data_planning(jour_semaine[0][i],jour_semaine[1][i]), ignore_index=True)
        
    df.to_csv("./semaine.csv", index=False)
    st.dataframe(df)
    
    csv = convert_df(df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='semaine.csv',
        mime='text/csv',
    )