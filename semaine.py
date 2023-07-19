
import datetime
from ics import Calendar
import requests

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
    
    response = requests.get('https://web.isen-ouest.fr/ICS/23_24_CODE_BZH_MICROSOFT_BREST_ALT.ics')
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
            return "Aucun événement trouvé pour cette date le matin."

def event_affichage(event):
    description = event.description.encode('latin-1').decode('utf-8')
    intervenant = ""
    for line in description.splitlines():
        if line.startswith("- Intervenant(s) :"):
            intervenant += line
    location = event.location.encode('latin-1').decode('utf-8')
    message = f" Salle : {location}Commence à : {event.begin.time()}\n{intervenant[2:]} "
    print(message)



afichage_semaine(semaine())


#date_jour = datetime.date.today() + datetime.timedelta(days=element)
