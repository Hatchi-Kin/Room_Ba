from streamlit_calendar import calendar
import streamlit as st
import streamlit as st

from fpdf import FPDF

import base64









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


response = requests.get("url de l'ics")
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










# Sidebar pour la colonne du haut
st.sidebar.write("Agenda")

# Affichage des jours de la semaine
days = ["lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
columns = st.columns(len(days))
for i, day in enumerate(days):
    columns[i].write(day)

data = {
    "lundi": [],
    "mardi": [],
    "mercredi": [],
    "jeudi": [],
    "vendredi": [],
    "samedi": [],
    "dimanche": [],
    # ... Add data for other days of the week
}

data_combined = {}
for day in data.keys():
    data_combined[day] = df[df['jour'] == day].to_dict('records')

# Print the combined data dictionary
print(data_combined)

# Iterate over each day in the data_combined dictionary
for day, events in data_combined.items():
    # Display the day as a header
    st.header(day.capitalize())
    
    # Display each event for the day
    for event in events:
        st.subheader(event["date"])
        st.write("Location:", event["location"])
        st.write("Time:", event["horaire"], "-", event["horaire_fin"])
        st.write("Description:", event["description"])
        
    # Add a separator between days
    st.markdown("---")

data = data_combined
# Créez un nouveau fichier PDF
from fpdf import FPDF

def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica', '', 12)
    # Iterate over each day in the data_combined dictionary
    for day, events in data_combined.items():
        pdf.cell(0, 10, day.capitalize(), ln=True)
        for event in events:
            pdf.cell(0, 10, f"Date: {event['date']}", ln=True)
            pdf.cell(0, 10, f"Location: {event['location']}", ln=True)
            pdf.cell(0, 10, f"Time: {event['horaire']} - {event['horaire_fin']}", ln=True)
            pdf.cell(0, 10, f"Description: {event['description']}", ln=True)

    # Save the PDF file
    pdf.output("weekly_agenda.pdf")
    
    st.download_button(
        "Download Report",
        data=pdf.output(dest='S').encode('latin-1'),
        file_name="agenda_semaine.pdf",
    )

# Save the PDF file
#pdf.output("agenda_semaine.pdf")
generate_pdf()


# Chemin d'accès complet au fichier PDF existant
chemin_fichier = b"/agenda_semaine.pdf"

