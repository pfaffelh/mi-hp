from flask import Flask
import pymongo
import requests
import xmltodict
from datetime import datetime, timedelta
from .config import *
import base64, json
import latex2markdown


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
    vortrag = mongo_db_news["vortrag"]
    vortragsreihe = mongo_db_news["vortragsreihe"]
except:
    pass
    # logger.warning("No connection to Database 1")

# Daten für /nlehre/
def get_events(lang = "de"):
    reihen = []
    events = []
    for vr in list(vortragsreihe.find({"event": False, "sichtbar" : True, "_public" : True}, sort = [("rang", pymongo.ASCENDING)])):
        reihen.append({"kurzname" : vr["kurzname"], "title" : vr[f"title_{lang}"]})

    for vr in list(vortragsreihe.find({"event": True, "sichtbar" : True, "_public" : True}, sort = [("rang", pymongo.ASCENDING)])):
        events.append({"kurzname" : vr["kurzname"], "title" : vr[f"title_{lang}"]})
    print(f"Reihen: {reihen}")
    return reihen, events

def data_for_base(lang="de", dtstring = datetime.now().strftime('%Y%m%d%H%M'), testorpublic = "_public"):
    date_format_no_space = '%Y%m%d%H%M'

    dt = datetime.strptime(dtstring, date_format_no_space)

    data = {}
    if testorpublic == "test":
        data["news"] =  list(news.find({ "home.fuerhome": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }}, sort=[("rang", pymongo.ASCENDING)]))
    else:
        data["news"] =  list(news.find({ "_public": True, "home.fuerhome": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }}, sort=[("rang", pymongo.ASCENDING)]))  
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = True if (item["showlastday"] and dt.date() == item['home']['end'].date()) else False
    # print(data)
    return data

def data_for_newsarchiv(anfang, end, lang="de"):
    data = {}
    data["news"] =  list(news.find({ "_public": True, "home.fuerhome": True, "home.end" : { "$lte" : end, "$gte" : anfang }}, sort=[("home.start", pymongo.DESCENDING)]))
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = False
    # print(data)
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
         #print(tagesplan)
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
        # print(tagesplan)
        
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

####################
## Wochenprogramm ##
####################

def get_start_current_semester():
    if datetime.now().month < 4:
        res = datetime(datetime.now().year-1, 10,1)
    elif 3 < datetime.now().month and datetime.now().month < 10:
        res = datetime(datetime.now().year, 4,1)
    else:
        res = datetime(datetime.now().year, 10,1)
    return res

def get_start_previous_semester(date):
    if date.month == 4:
        res = datetime(date.year-1, 10,1)
    else:
        res = datetime(date.year, 4,1)
    return res

def get_start_next_semester(date):
    if date.month == 4:
        res = datetime(date.year, 10,1)
    else:
        res = datetime(date.year+1, 4,1)
    return res

def get_end_next_semester(date):
    return get_start_next_semester(get_start_next_semester(date))

def get_start_current_month():
    date = datetime.now()
    return datetime(date.year, date.month, 1)

def get_start_next_month(date):
    if date.month < 12:
        res = datetime(date.year, date.month+1,1)
    else:
        res = datetime(date.year+1, 1,1)
    return res

def get_end_next_month(date):
    return get_start_next_month(get_start_next_month(date))

def get_start_previous_month(date):
    if date.month > 1:
        res = datetime(date.year, date.month-1,1)
    else:
        res = datetime(date.year-1, 12, 1)
    return res

def get_monat(n, lang="de"):
    monate_de = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    monate_en = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    monate = monate_de if lang == "de" else monate_en
    return monate[n]


def get_wochenprogramm(anfangdate, enddate, kurzname="alle", lang="de"):
    data = {}
    tage_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tage_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tage = tage_de if lang == "de" else tage_en

    vr = vortragsreihe.find_one({"kurzname" : kurzname, "_public" : True})
    data["reihe"] = vr[f"title_{lang}"]
    data["prefix"] = vr[f"text_{lang}"]
    vo = list(vortrag.find({ "vortragsreihe": { "$elemMatch" : { "$eq" : vr["_id"] }}, "_public" : True, "start" : {"$gte" : anfangdate, "$lte" : enddate }}, sort=[("start", pymongo.ASCENDING)]))
    data["vortrag"] = []
    previousdatum = ""
    for v in vo:
        re = vortragsreihe.find_one({"_id" : { "$in": v["vortragsreihe"], "$ne" : vr["_id"]}, "_public" : True})
        data["vortrag"].append(
            {
                "sprecher" : v["sprecher_en"] if (lang == "en" and v["sprecher"] == "") else v["sprecher"],
                "sprecher_affiliation" : v[f"sprecher_affiliation_{lang}"],
                "ort" : v[f"ort_{lang}"],
                "title" : v[f"title_{lang}"],
                "reihentitle" : "" if re is None else re[f"title_{lang}"],
                "url" : v["url"],
                "lang" : v["lang"],
                "abstract" : latex2markdown.LaTeX2Markdown(v[f"text_{lang}"]).to_markdown(),
                "datum" : v["start"].strftime('%d.%m.%Y'),
                "tag" : tage[v["start"].weekday()],
                "startzeit" : v["start"].strftime('%H:%M'),
                "endzeit" : v["end"].strftime('%H:%M'),
                "kommentar" : v[f"kommentar_{lang}"]
            }
        )
        previousdatum = v["start"]
    return data

def get_event(kurzname, lang = "de"):
    data = {}
    tage_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tage_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tage = tage_de if lang == "de" else tage_en

    vr = vortragsreihe.find_one({"kurzname" : kurzname, "_public" : True})
    data["reihe"] = vr[f"title_{lang}"]
    data["prefix"] = vr[f"text_{lang}"]
    vo = list(vortrag.find({ "vortragsreihe": { "$elemMatch" : { "$eq" : vr["_id"] }}, "_public" : True}, sort=[("start", pymongo.ASCENDING)]))
    data["vortrag"] = []
    previousdatum = ""
    for v in vo:
        data["vortrag"].append(
            {
                "sprecher" : v["sprecher_de"] if (lang == "en" and v["sprecher"] == "") else v["sprecher"],
                "sprecher_affiliation" : v[f"sprecher_affiliation_{lang}"],
                "ort" : v[f"ort_{lang}"],
                "title" : v[f"title_{lang}"],
                "url" : v["url"],
                "lang" : v["lang"],
                "abstract" : latex2markdown.LaTeX2Markdown(v[f"text_{lang}"]).to_markdown(),
                "datum" : v["start"].strftime('%d.%m.%Y') if v["start"] != previousdatum else "",
                "tag" : tage[v["start"].weekday()] if v["start"] != previousdatum else "",
                "startzeit" : v["start"].strftime('%H:%M'),
                "endzeit" : v["end"].strftime('%H:%M'),
                "kommentar" : latex2markdown.LaTeX2Markdown(v[f"kommentar_{lang}"]).to_markdown()
            }
        )
        previousdatum = v["start"]
    return data
    
