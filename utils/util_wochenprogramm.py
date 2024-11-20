from flask import Flask
import pymongo
import requests
import xmltodict
from datetime import datetime, timedelta
from .config import *
import base64, json


app = Flask(__name__)

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_news = cluster["news"]
    vortrag = mongo_db_news["vortrag"]
    vortragsreihe = mongo_db_news["vortragsreihe"]
except:
    pass
    # logger.warning("No connection to Database 1")

# Daten für /nlehre/

def get_wochenprogramm(kurzname="alle", daysinpast = 365):
    data = {}
    vr = vortragsreihe.find_one({"kurzname" : kurzname, "_public" : True})
    data["reihe"] = vr
    data["vortrag"] =  list(vortrag.find({ "vortragsreihe": { "$elemMatch" : { "$eq" : vr["_id"] }}, "_public" : True, "start" : {"$gte" : datetime.now() + timedelta(days = - daysinpast)}}), sort=[("rang", pymongo.ASCENDING)])
    return data

def get_event(kurzname="alle"):
    data = get_wochenprogramm(kurzname, daysinpast = 100000)
    

