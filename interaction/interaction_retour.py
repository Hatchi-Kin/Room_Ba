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
        return "comande inconnue utilisé !help pour plus d'info"

def get_the_comande(comande):
    return "menu a faire"