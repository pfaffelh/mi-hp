import pymongo
import utils.config as config
from bson import ObjectId
from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_faq = cluster["faq"]
    knoten = mongo_db_faq["knoten"]
    studiendekanat = mongo_db_faq["studiendekanat"]
    
except:
    logger.warning("No connection to Database FAQ")

# returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 

def get_accordion_data(kurzname, lang):
    bearbeitet = f"bearbeitet_{lang}"
    titel = f"titel_{lang}"
    prefix = f"prefix_{lang}"
    suffix = f"suffix_{lang}"

    x = knoten.find_one({"kurzname" : kurzname})
    # Alle Kategorien zeigen außer "unsichtbar"

    res = { "kurzname" : x["kurzname"], "titel" : x[titel], "prefix" : x[prefix], "suffix" : x[suffix], "bearbeitet" : x[bearbeitet], "kinder" : []}
    for k1 in x["kinder"]:
        y = knoten.find_one({"_id" : k1})
        res["kinder"].append(
            { "kurzname" : y["kurzname"], "titel" : y[titel], "prefix" : y[prefix], "suffix" : y[suffix],  "bearbeitet" : y[bearbeitet],"kinder" : []}
        )
        for k2 in y["kinder"]:
            z = knoten.find_one({"_id" : k2})
            res["kinder"][-1]["kinder"].append(
            { "kurzname" : x["kurzname"], "parent_kurzname" : y["kurzname"], "titel" : z[titel], "prefix" : z[prefix], "suffix" : z[suffix],  "bearbeitet" : z[bearbeitet],"kinder" : []}              
            )
    return res

