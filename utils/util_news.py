from flask import Flask
import pymongo
import requests
import xmltodict
from datetime import datetime, timedelta
from .config import *
import base64, json


app = Flask(__name__)

#from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_news = cluster["news"]
    mensaplan = mongo_db_news["mensaplan"]
    bild = mongo_db_news["bild"]
    carouselnews = mongo_db_news["carouselnews"]
    news = mongo_db_news["news"]
except:
    pass
    # logger.warning("No connection to Database 1")

# Daten für /nlehre/

def data_for_base(lang="de", dtstring = datetime.now().strftime('%Y%m%d%H%M'), testorpublic = "_public"):
    date_format_no_space = '%Y%m%d%H%M'

    dt = datetime.strptime(dtstring, date_format_no_space)

    data = {}
    if testorpublic == "test":
        data["news"] =  list(news.find({ "home.fuerhome": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }},sort=[("rang", pymongo.ASCENDING)]))
    else:
        data["news"] =  list(news.find({ "_public": True, "home.fuerhome": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }}))        
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = True if (item["showlastday"] and dt.date() == item['home']['end'].date()) else False
    print(data)
    return data

def data_for_bildnachweis(lang="de"):
    data_news = []
    dcarouselnews = list(carouselnews.find({"_public" :True, "start" : { "$lte" : datetime.now() }, "end" : { "$gte" : datetime.now() }}))        
    for item in dcarouselnews:
        b = bild.find_one({ "_id": item["image_id"]})
        data_news.append({"bild" : base64.b64encode(b["thumbnail"]).decode(), 
                          "mime": b["mime"], 
                          "bildnachweis" : b["bildnachweis"]
                          })
    dnews = list(news.find({ "_public": True, "$or" : [{"monitor.fuermonitor": True, "monitor.start" : { "$lte" : datetime.now() }, "monitor.end" : { "$gte" : datetime.now() }}, {"home.fuerhome": True, "home.start" : { "$lte" : datetime.now() }, "home.end" : { "$gte" : datetime.now() }}]}))        
    for item in dnews:
        if item["image"] != []:
            b = bild.find_one({ "_id": item["image"][0]["_id"]})
            data_news.append({"bild" : base64.b64encode(b["thumbnail"]).decode(), 
                            "mime": b["mime"], 
                            "bildnachweis" : b["bildnachweis"]
                            })
    # Bilder von "Studieninteressierte"
    # Das ist die Liste von Dateinamen der Bilder
    interesse_filenames = []
    with app.open_resource('../static/data/interesse.json') as f:
        data_interesse = json.load(f)
    for c in data_interesse["content"]:
        interesse_filenames = interesse_filenames + [a["image"].split("/")[-1] for a in c["cards"] if a["image"] != ""]
    data_interesse = []
    for filename in interesse_filenames:
        b = bild.find_one({ "filename": filename}) 
        if b:
            data_interesse.append({"bild" : base64.b64encode(b["thumbnail"]).decode(), 
                                   "mime": b["mime"], 
                                   "bildnachweis" : b["bildnachweis"]
                                   })

    data = [{ "titel" : "News und Monitor" if lang == "de" else "News and monitor",
              "data" : data_news
                            },
            { "titel" : "Für Studieninteressierte" if lang == "de" else "Study with us",
              "data" : data_interesse
            }
    ]
    return data

def get_mensaplan_text(url, date):
    response = requests.get(url)
    if response.status_code == 200:
        mensaplan_xml = response.text
        mensaplan = xmltodict.parse(mensaplan_xml)
        date_format = '%d.%m.%Y'
        tagesplan = mensaplan["plan"]["ort"]["tagesplan"]
        tagesplan = [t["menue"] for t in tagesplan if t["@datum"] == datetime.now().strftime('%d.%m.%Y')]
        print(tagesplan)
        if tagesplan != []:
            tagesplan = tagesplan[0]
            ausgabe = f"<h2>Mensaplan am {date.strftime('%d.%m.')}</h2>"
            # Abendessen wird nicht ausgegeben
            for t in [t for t in tagesplan if t["@art"][0:10] != "Abendessen"]: 
                art = t["@art"]
                name = t["name"]
                if len(t["name"]) > 60:
                    name = name[0:59] + "..."
                ausgabe = ausgabe + f"<h4>{art}: {name}</h4>"
        else:
            ausgabe = "<h2>Heute ist die Mensa zu!</h2>"
    else: 
        ausgabe = ""
    return ausgabe

def writetonews_mensaplan_text(url = mensaplan_url):
    response = requests.get(url)
    if response.status_code == 200:
        mensaplan_xml = response.text
        mensaplan = xmltodict.parse(mensaplan_xml)
        date_format = '%d.%m.%Y'
        tagesplan = mensaplan["plan"]["ort"]["tagesplan"]
        print(tagesplan)
        
        for t in tagesplan:
            if carouselnews.find_one({"kommentar" : "Mensaplan", "start" : datetime.strptime(t["@datum"], date_format) }):
                pass
            else:
                menue = t["menue"]
                ausgabe = f"<h2>Mensaplan am {t['@datum']}</h2>"    
                for m in [m for m in menue if m["@art"][0:10] != "Abendessen"]: 
                    art = m["@art"]
                    name = m["name"]
                    if len(m["name"]) > 60:
                        name = name[0:59] + "..."
                    ausgabe = ausgabe + f"<h4>{art}: {name}</h4>"
                carouselnews.insert_one({
                    "_public" : True,
                    "start" : datetime.strptime(t["@datum"], date_format),
                    "end" : datetime.strptime(t["@datum"], date_format) + timedelta(hours=14),
                    "interval" : 4000, 
                    "left" : 15,
                    "right" : 15,
                    "bottom" : 2,
                    "text" : ausgabe,
                    "bearbeitet" : f"Automatisch generiert am {datetime.now().strftime('%d.%m.%Y um %H:%M:%S.')}",
                    "kommentar" : "Mensaplan",
                    "rang": max([x["rang"] for x in list(carouselnews.find())])+1,
                    "image_id" : bild.find_one({"titel" : "Mensa Rempartstraße"})["_id"]
                })                                     

#def get_wettervorhersage():
#    url = "https://de.wttr.in/Freiburg?1pQ"
#    response = requests.get(url)
#    if response.status_code == 200:
#        wettervorhersage_text = response.text[2:-210]

