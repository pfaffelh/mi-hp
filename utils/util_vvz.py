import pymongo
from datetime import datetime

#from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_vvz = cluster["vvz"]
    semester = mongo_db_vvz["semester"] 
except:
    logger.warning("No connection to Database 1")

# returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 

def get_showsemester(shortname):
    # Gibt es ein sichtbares Semester mit shortname?
    b = semester.find_one({"kurzname": shortname, "hp_sichtbar": True })
    return (b != None)

def get_current_semester_kurzname():
    if datetime.now().month < 4:
        res = f"{datetime.now().year-1}WS"
    elif 3 < datetime.now().month and datetime.now().month < 11:
        res = f"{datetime.now().year}SS"
    else:
        res = f"{datetime.now().year}WS"
    return res

def next_semester_kurzname(kurzname):
    a = int(kurzname[:4])
    b = kurzname[4:]
    return f"{a+1}SS" if b == "WS" else f"{a}WS"

def semester_name_de(kurzname):
    a = int(kurzname[:4])
    b = kurzname[4:]
    c = f"/{a+1}" if b == "WS" else ""
    return f"{"Wintersemester" if b == "WS" else "Sommersemester"} {a}{c}"

def semester_name_en(kurzname):
    a = int(kurzname[:4])
    b = kurzname[4:]
    c = f"/{a+1}" if b == "WS" else ""
    return f"{"Winter term" if b == "WS" else "Summer term"} {a}{c}"

def get_data(kurzname):
    data = {}
    return data

