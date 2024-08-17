from flask import Flask
import pymongo
from datetime import datetime
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
