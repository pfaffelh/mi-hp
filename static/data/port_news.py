import json
from datetime import datetime

date_format = '%d.%m.%Y %H:%M'

with open('home.json') as f:
    data = json.load(f)    

carouselnews = data["carouselmonitor"]
data["carouselnews"] = []

for n in carouselnews:
    data["carouselnews"].append(
        {
            "test": True,
            "public": True, 
            "start": datetime.strptime(n["showstart"], date_format),
            "end": datetime.strptime(n["showend"], date_format),
            "interval": n["interval"],
            "image": n["image"],
            "left": n["left"],
            "right": n["right"],
            "bottom": n["bottom"],
            "text": n["text"]
        }
    )



news = data["news"]
data["news"] = []

for n in news:
    print(n)
    data["news"].append(
        {
        "link": n["link"],
        "image": [{
            "file": n["image"],
            "stylehome": n["style"],
            "stylemonitor": n["style"],
            "widthmonitor": 4
        }] if n["image"] != "" else [],
        "home": {
            "test": True, 
            "public": True,
            "atchiv": True,
            "showlastday": True,
            "start": datetime.strptime(n["showhomestart"], date_format),
            "end": datetime.strptime(n["showhomeend"], date_format),
            "title_de": n["title_de"],
            "title_en": n["title_en"],
            "text_de": n["text_de"],
            "text_en": n["text_en"],
            "popover_title_de": n["popover_title_de"],
            "popover_title_en": n["popover_title_en"],
            "popover_text_de": n["popover_text_de"],
            "popover_text_en": n["popover_text_en"],
        },
        "monitor": {
            "test": True, 
            "public": True,
            "showlastday": True,
            "start": datetime.strptime(n["showmonitorstart"], date_format),
            "end": datetime.strptime(n["showmonitorend"], date_format),
            "title": n["title_de"],
            "text": n["text_de"]
        }
    })

with open('home2.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False)    


# Write to database:
# Collections are: 
# Mensaplan
# Images: File, Titel, Bildnachweis, 
# Carouselnews: test, public, showstart, showend, interval, image, left (in %), right (in %), bottom (in %), text
# News: wie oben


