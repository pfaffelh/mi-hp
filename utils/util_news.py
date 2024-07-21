import pymongo
from datetime import datetime
from .config import *

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

