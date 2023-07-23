
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

def afichage_semaine(semaine_resultat):
    
    response = requests.get('ICS URL')
    for element in semaine_resultat:
        print("\njour",element)
        filtre_events = []
        date_jour = datetime.date.today() + datetime.timedelta(days=element)

        calendar = Calendar(response.text)
        events = [event for event in calendar.events if event.begin.date() == date_jour]
        if events:
            for event in events:
                if event.begin.date() == date_jour:
                    filtre_events.append(event)
            filtre_events.sort(key=lambda item: item.begin.time())
            text_automatique=""
            for i in range (0,len(filtre_events)):
                text_automatique=text_automatique + f"\n\n {event_affichage(filtre_events[i])}"
                
            #return f"matin :\n {event_affichage(event_matin)}\n\n aprem :\n {event_affichage(event_aprem)}"
        else:
            print("Aucun événement trouvé pour cette date")

def event_affichage(event):
    description = event.description.encode('latin-1').decode('utf-8')
    intervenant = ""
    for line in description.splitlines():
        if line.startswith("- Intervenant(s) :"):
            intervenant += line
    location = event.location.encode('latin-1').decode('utf-8')
    message = f" Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]} "
    if message == "":
        message = "rien de prevu"
    #print(message)



#afichage_semaine(semaine())


#date_jour = datetime.date.today() + datetime.timedelta(days=element)

response = requests.get('ICS URL')
calendar = Calendar(response.text)

def planning(date):
    events = [event for event in calendar.events if event.begin.date() == date]
    if events:
        events.sort(key=lambda x: x.begin.time())
        for i in events:
            print(f"events ======{events}")
            date = i.begin.date().strftime("%d/%m/%Y")
            description = i.description.encode('latin-1').decode('utf-8')   
            location = i.location.encode('latin-1').decode('utf-8')
            horaire = i.begin.time().strftime("%H:%M")
            horaire_fin = i.end.time().strftime("%H:%M")
            st.write(f"Date: {date}")
            st.write(f"Salle: {location[:-1]}")
            st.write(f"Commence à {horaire} et fini à {horaire_fin}")
            st.write(description)
            st.write("\n")
            st.write("\n")
    else:
        st.write("Aucun événement trouvé pour cette date")


col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
jour_semaine=semaine()
for i in range (len(jour_semaine)):
    with col1:
        date = datetime.date.today() + datetime.timedelta(days=jour_semaine[i])
        planning(date)