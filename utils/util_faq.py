import pymongo
import utils.config as config
from bson import ObjectId
from .util_logging import logger
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils.config import *

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_faq = cluster["faq"]
    knoten = mongo_db_faq["knoten"]
    studiendekanat = mongo_db_faq["studiendekanat"]
    dictionary = mongo_db_faq["dictionary"]
    kalender = mongo_db_faq["kalender"]
    prozesspaket = mongo_db_faq["prozesspaket"]
    prozess = mongo_db_faq["prozess"]
    aufgabe = mongo_db_faq["aufgabe"]
    mongo_db_users = cluster["user"]
    users = mongo_db_users["user"]
    group = mongo_db_users["group"]    
    mongo_db_faq = cluster["faq"]
    studiendekanat = mongo_db_faq["studiendekanat"]
            
except:
    logger.warning("No connection to Database!")

def get_studiendekenat_data(query):
    data = list(studiendekanat.find(query, sort=[("rang", pymongo.ASCENDING)]))
    for item in data:
        item["shownews"] = (datetime.now() < item["news_ende"])
    return data

# Here, x is a dict with fields x[f"{field_prefix}_de"] and x[f"{field_prefix}_en"]. The goal is to read x[f"{field_prefix}_{lang}"] if this data is available, otherwise use the other language.
def get(x, field_prefix, lang, alt = ""):
    otherlang = "de" if lang == "en" else "en"
    if x.get(f"{field_prefix}_de") is None: # field is not acailable, return alt
        res = alt
    else:
        res = x[f"{field_prefix}_{lang}"] if x[f"{field_prefix}_{lang}"] != "" else x[f"{field_prefix}_{otherlang}"]
    return res

# get_accordion_data returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 
def get_accordion_data(kurzname, lang, show = ""):
    fields = ["kurzname", "sichtbar", "prefix_html", "suffix_html"] # no language in these fields
    field_prefixes = ["titel", "prefix", "suffix", "bearbeitet"] # these fields exists with _de and _en
    quicklink_prefixes = ["title", "url"] # there are title_de and title_en, and url_de and url_en

    try:
        x = knoten.find_one({"kurzname" : kurzname, "sichtbar" : True})
        loc = { field: x[field] for field in fields}
        loc["quicklinks"] = [{quicklink_prefix : get(q, quicklink_prefix, lang) for quicklink_prefix in quicklink_prefixes} for q in x["quicklinks"]]
        loc["kinder"] = []
        for field_prefix in field_prefixes:
            loc[field_prefix] = get(x, field_prefix, lang)
        data = loc
        for k1 in x["kinder"]:
            y = knoten.find_one({"_id" : k1})
            loc = {}
            if y["sichtbar"]:
                loc = { field: y[field] for field in fields}
                loc["quicklinks"] = [{quicklink_prefix : get(q, quicklink_prefix, lang) for quicklink_prefix in quicklink_prefixes} for q in y["quicklinks"]]
                loc["kinder"] = []
                for field_prefix in field_prefixes:
                    loc[field_prefix] = get(y, field_prefix, lang)
                data["kinder"].append(loc)
                for k2 in y["kinder"]:
                    z = knoten.find_one({"_id" : k2})
                    if z["sichtbar"]:
                        loc = { field: z[field] for field in fields}
                        loc["quicklinks"] = [{quicklink_prefix : get(q, quicklink_prefix, lang) for quicklink_prefix in quicklink_prefixes} for q in z["quicklinks"]]
                        loc["kinder"] = []
                        for field_prefix in field_prefixes:
                            loc[field_prefix] = get(z, field_prefix, lang)
                        data["kinder"][-1]["kinder"].append(loc)                        
                        
    except:
        logger.warning("No connection to database")
        data = { "kurzname" : kurzname, "sichtbar" : True, "titel" : "", "titel_html" : False, "prefix" : "", "prefix_html" : False, "quicklinks" : [], "suffix" : "", "suffix_html" : False, "bearbeitet" : "", "kinder" : []}
    if show == "":
        showcat = ""
    elif show == "all":
        showcat = "all"
    else:
        k = knoten.find_one({"kurzname" : show, "sichtbar" : True})
        p = knoten.find_one({"kinder" : { "$elemMatch" : { "$eq": k["_id"]}}})
        if p == knoten.find_one({"kurzname" : kurzname}):
            showcat = show
        else:
            showcat = p["kurzname"]
    return data, show, showcat

def get_lexikon_data(lang = "de"):
    return list(dictionary.find({}, sort=[("de", pymongo.ASCENDING)]))
        
# Hier werden alle Termine ausgegeben, die nach anzeige_start liegen
def get_calendar_data(anzeige_start):
    gr = group.find_one({"name" : "faq"})
    # kalender und aufgaben, die nur Termine sind: 
    # aus kalender
    events = []
    termine_prpa = list(kalender.find({"datum" : { "$gte" : anzeige_start}}))
    for t in termine_prpa:
        col = next((c["color"] for c in calendars if c["kurzname"] == "semesterplan"), "#FFFFFF")
        allDay = True if t["datum"].time() == datetime.min.time() else False
        events.append({
            "color" : col,
            "textcolor" : get_contrasting_text_color(col),
            "start": t["datum"].strftime('%Y-%m-%d') if allDay else t["datum"].isoformat(),
            "end": t["datum"].isoformat(),
            "allDay": allDay,
            "title": t["name"],
            "extendedProps" : {
                "description1" : format_termin(t),
                "description2" : "",
                "ort" : "",
                "googleTime" : formatDateForGoogle(t["datum"], t["datum"], allDay),
                "icsTime" : formatDateForIcs(t["datum"], t["datum"], allDay),
            },
            "groupId" : "semesterplan"
        })
    # aus aufgabe
    termine_auf = list(aufgabe.find({"ankerdatum" : { "$in" : [t["_id"] for t in termine_prpa]}}))
    gr = group.find_one({"name" : "faq"})
    faq_users = list(users.find({"groups" : { "$elemMatch" : { "$eq" : gr["_id"]}}}, sort = [("name", pymongo.ASCENDING)])) 
    for t in termine_auf:
        col = next((c["color"] for c in calendars if c["kurzname"] == "studiendekanat"), "#FFFFFF")
        anfang = kalender.find_one({"_id" : t["ankerdatum"]})["datum"] + relativedelta(days = t["start"])
        ende = kalender.find_one({"_id" : t["ankerdatum"]})["datum"] + relativedelta(days = t["ende"])
        allDay = True if anfang.time() == datetime.min.time() else False

        events.append({
            "color" : col,
            "textcolor" : get_contrasting_text_color(col),
            "start": anfang.strftime('%Y-%m-%d') if allDay else anfang.isoformat(),
            "end": ende.isoformat(),
            "allDay": allDay,
            "title": t["name"],
            "extendedProps" : {
                "description" : "",
                "googleTime" : formatDateForGoogle(anfang, ende, allDay),
                "icsTime" : formatDateForIcs(anfang, ende, allDay),
            },
            "groupId" : "studiendekanat"
        })

    return events