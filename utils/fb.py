import requests
from datetime import datetime, timedelta

# date ist das Datum des Spielplans, datetime ist die Uhrzeit, zu der abgerufen wird
# Im laufenden Betrieb ist date = datetime.now().date()
# offset is the difference in seconds between the scheduled time from the api and local time

def get_openligadb_text(url, date, offset):
    date_format = '%Y-%m-%dT%H:%M:%S'

    # A GET request to the API
    response = requests.get(url)

    if response.status_code == 200:
        # Print the response
        matches = response.json()
        matches = [m for m in matches if datetime.strptime(m["matchDateTime"], date_format).date()==date]
        if matches != []:
            ausgabe = f"<h2>Spielplan am {date.strftime('%d.%m.')}</h2>"

            for m in matches:
                t = datetime.strptime(m["matchDateTime"], date_format) + timedelta(0, offset)
                x = f"{t.strftime("%H:%M:")} {m["team1"]["teamName"]}-{m["team2"]["teamName"]}"
                y = ""
                if datetime.now() > t:
                    score1 = max([0] + [i["scoreTeam1"] for i in m["goals"]])
                    score2 = max([0] + [i["scoreTeam2"] for i in m["goals"]])
                    y = f": {score1}:{score2}" + ("" if m["matchIsFinished"] else " <blink>Spiel läuft noch</blink>")
                ausgabe = ausgabe + "<h3>" + x + y + "</h3>"
        else:
            ausgabe = "<h2>Heute keine Spiele!</h2>"
    else: 
        ausgabe = ""

    return ausgabe

