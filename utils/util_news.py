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

def getwl(x, field, lang):
    otherlang = "en" if lang == "de" else "de"
    loc = x.get(f"{field}_{lang}", "")
    return loc if loc != "" else x.get(f"{field}_{otherlang}", "")

def get_events(lang = "de"):
    reihen = []
    events = []
    for vr in list(vortragsreihe.find({"event": False, "sichtbar" : True, "_public" : True}, sort = [("rang", pymongo.ASCENDING)])):
        reihen.append({"kurzname" : vr["kurzname"], "title" : getwl(vr, "title", lang)})

    for vr in list(vortragsreihe.find({"event": True, "sichtbar" : True, "_public" : True}, sort = [("rang", pymongo.ASCENDING)])):
        events.append({"kurzname" : vr["kurzname"], "title" : getwl(vr, "title", lang)})
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
            item['home']["title"] = getwl(item['home'], "title", lang)
            item['home']["text"] = getwl(item['home'], "text", lang)
            item['home']["popover_title"] = getwl(item['home'], "popover_title", lang)
            item['home']["popover_text"] = getwl(item['home'], "popover_text", lang)
    for item in data['news']:
        item['today'] = False
    # print(data)
    return data

def data_for_newsarchiv_full(lang, anfang, end):
    anfangdate = datetime.strptime(anfang, '%Y%m%d')
    enddate = datetime.strptime(end, '%Y%m%d')
    data = data_for_newsarchiv(anfangdate, enddate, lang)    
    data["zeitraum"] = f"{get_monat(anfangdate.month, lang)} {anfangdate.year}"
    data["previousanfang"] = get_start_previous_month(anfangdate).strftime('%Y%m%d')
    data["nextend"] = get_end_next_month(anfangdate).strftime('%Y%m%d')
    data["anfang"] = anfang
    data["end"] = end
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
                if len(t["name"]) > 50:
                    name = name[0:49] + "..."
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
    tage = tage_lang(lang)
    vr = vortragsreihe.find_one({"kurzname" : kurzname, "_public" : True})
    data["reihe"] = getwl(vr, "title", lang)
    data["prefix"] = getwl(vr, "text", lang)
    vo = list(vortrag.find({ "vortragsreihe": { "$elemMatch" : { "$eq" : vr["_id"] }}, "_public" : True, "start" : {"$gte" : anfangdate, "$lte" : enddate }}, sort=[("start", pymongo.ASCENDING)]))
    data["vortrag"] = []
    previousdatum = ""
    for v in vo:
        re = vortragsreihe.find_one({"_id" : { "$in": v["vortragsreihe"], "$ne" : vr["_id"]}, "_public" : True})
        data["vortrag"].append(
            {
                "sprecher" : getwl(v, "sprecher", lang),
                "sprecher_affiliation" : getwl(v, "sprecher_affiliation", lang),
                "ort" : getwl(v, "ort", lang),
                "title" : getwl(v, "title", lang),
                "reihentitle" : "" if re is None else getwl(re, "title", lang),
                "url" : v["url"],
                "lang" : v["lang"],
                "abstract" : latex2markdown.LaTeX2Markdown(getwl(v, "text", lang)).to_markdown(),
                "datum" : v["start"].strftime('%d.%m.%Y'),
                "tag" : tage[v["start"].weekday()],
                "startzeit" : v["start"].strftime('%H:%M'),
                "endzeit" : v["end"].strftime('%H:%M'),
                "kommentar" : getwl(v, "kommentar", lang)
            }
        )
        previousdatum = v["start"]
    return data

def get_wochenprogramm_full(anfang, end, kurzname="alle", lang="de"):
    anfangdate = datetime.strptime(anfang, '%Y%m%d')
    enddate = datetime.strptime(end, '%Y%m%d')
    diffmonth = abs(enddate.month - anfangdate.month)
    if diffmonth == 1 or (anfangdate.month == 12 and enddate.month == 1):
        zeitraum = f"{get_monat(anfangdate.month, lang)} {anfangdate.year}"
        previousanfangdate = get_start_previous_month(anfangdate)
        nextenddate = get_end_next_month(anfangdate)
    elif diffmonth == 6:
        sem_de = "Sommersemester" if anfangdate.month == 4 else "Wintersemester"
        sem_en = "Summer term" if anfangdate.month == 4 else "Winter term"
        sem = sem_de if lang == "de" else sem_en
        zeitraum = f"{sem} {anfangdate.year}"
        previousanfangdate = get_start_previous_semester(anfangdate)
        nextenddate = get_end_next_semester(anfangdate)
    else:
        zeitraum = ""
        previousanfangdate = anfangdate
        nextenddate = enddate

    previousanfang = previousanfangdate.strftime('%Y%m%d')
    nextend = nextenddate.strftime('%Y%m%d')

    data = get_wochenprogramm(anfangdate, enddate, kurzname, lang)
    data["anfang"] = anfang
    data["end"] = end
    data["previousanfang"] = previousanfang
    data["nextend"] = nextend
    data["zeitraum"] = zeitraum
    data["anfangcurrentsemester"] = get_start_current_semester().strftime('%Y%m%d')
    data["anfangnextsemester"] = get_start_next_semester(get_start_current_semester()).strftime('%Y%m%d')
    data["anfangcurrentmonth"] = get_start_current_month().strftime('%Y%m%d')
    data["anfangnextmonth"] = get_start_next_month(get_start_current_month()).strftime('%Y%m%d')
    return data

def get_event(kurzname, lang = "de"):
    data = {}
    tage = tage_lang(lang)

    vr = vortragsreihe.find_one({"kurzname" : kurzname, "_public" : True})
    data["reihe"] = getwl(vr, "title", lang)
    data["prefix"] = getwl(vr, "text", lang)
    vo = list(vortrag.find({ "vortragsreihe": { "$elemMatch" : { "$eq" : vr["_id"] }}, "_public" : True}, sort=[("start", pymongo.ASCENDING)]))
    data["vortrag"] = []
    previousdatum = ""
    for v in vo:
        data["vortrag"].append(
            {
                "sprecher" : getwl(v, "sprecher", lang),
                "sprecher_affiliation" : getwl(v, "sprecher_affiliation", lang),
                "ort" : getwl(v, "ort", lang),
                "title" : getwl(v, "title", lang),
                "url" : v["url"],
                "lang" : v["lang"],
                "abstract" : latex2markdown.LaTeX2Markdown(getwl(v, "text", lang)).to_markdown(),
                "datum" : v["start"].strftime('%d.%m.%Y') if v["start"] != previousdatum else "",
                "tag" : tage[v["start"].weekday()] if v["start"] != previousdatum else "",
                "startzeit" : v["start"].strftime('%H:%M'),
                "endzeit" : v["end"].strftime('%H:%M'),
                "kommentar" : latex2markdown.LaTeX2Markdown(getwl(v, "kommentar", lang)).to_markdown()
            }
        )
        previousdatum = v["start"]
    return data
    
def get_monitordata(dtstring, testorpublic):
    # the date format for <dtstring>
    date_format_no_space = '%Y%m%d%H%M'
    dt = datetime.strptime(dtstring, date_format_no_space)

    data = {}
    # Daten für das Carousel
    if testorpublic == "test":
        data["carouselnews"] = list(carouselnews.find({"start" : { "$lte" : dt }, "end" : { "$gte" : dt }},sort=[("rang", pymongo.ASCENDING)]))
    else:
        data["carouselnews"] = list(carouselnews.find({"_public" :True, "start" : { "$lte" : dt }, "end" : { "$gte" : dt }},sort=[("rang", pymongo.ASCENDING)]))  

    for item in data["carouselnews"]:
        item["image"] = base64.b64encode(bild.find_one({ "_id": item["image_id"]})["data"]).decode()#.encode('base64')

    # Daten für die News
    query = { "monitor.fuermonitor": True, 
             "monitor.start" : { "$lte" : dt }, 
             "monitor.end" : { "$gte" : dt }}
    if testorpublic == "test":
        data["news"] = list(news.find(query ,sort=[("rang", pymongo.ASCENDING)]))
    else:
        query["_public"] = True
        data["news"] = list(news.find(query, sort=[("rang", pymongo.ASCENDING)]))  
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = True if (item["showlastday"] and dt.date() == item['monitor']['end'].date()) else False
    return data


def get_api_news():    
    dt = datetime.now()
    new =  list(news.find({ "_public": True, "home.fuerhome": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }}, sort=[("rang", pymongo.ASCENDING)]))  
    news_reduced = []
    for n in new:
        news_reduced.append({"title_de" : n["home"]["title_de"],
                             "title_en" : n["home"]["title_en"],
                             "text_de" : n["home"]["text_de"],
                             "text_en" : n["home"]["text_en"],
                             "link" : n["link"]
                             })
    return news_reduced


def get_api_wochenprogramm(anfang, ende):
    anfang = datetime.strptime(anfang, "%Y%m%d")
    ende = datetime.strptime(ende, "%Y%m%d")

    vortraege =  list(vortrag.find({ "_public": True, "start" : { "$gte" : anfang }, "end" : { "$lte" : ende }}, sort=[("start", pymongo.ASCENDING)]))
    vortraege_reduced = []
    leer = vortragsreihe.find_one({"kurzname" : "alle"})
    tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    for v in vortraege:
        reihe = list(vortragsreihe.find({"_id" : { "$in" : v["vortragsreihe"]}}))
        reihenkurzname = [item["kurzname"] for item in reihe if item != leer]
        reihe = [item["title_de"] for item in reihe if item != leer]
        reihenkurzname = "" if reihe == [] else reihenkurzname[0]
        reihe = "" if reihe == [] else reihe[0]
        vortraege_reduced.append(
            {
                "reihenkurzname" : reihenkurzname,
                "vortragsreihe" : reihe,
                "sprecher" : getwl(v, "sprecher", "de"),
                "sprecher_affiliation" : getwl(v, "sprecher_affiliation", "de"),
                "titel" : getwl(v, "title", "de"),
                "abstract" : getwl(v, "text", "de"),
                "ort" : getwl(v, "ort", "de"),
                "url" : v["url"],
                "datum" : v["start"].strftime('%d.%m.%Y'),
                "tag" : tage[v["start"].weekday()],
                "startzeit" : v["start"].strftime('%H:%M'),
                "endzeit" : v["end"].strftime('%H:%M'),
                "kommentar" : getwl(v, "kommentar", "de")
            })
    return vortraege_reduced

