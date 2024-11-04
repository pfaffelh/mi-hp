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

def get_accordion_data(kurzname, lang, show = ""):
    bearbeitet = f"bearbeitet_{lang}"
    titel = f"titel_{lang}"
    prefix = f"prefix_{lang}"
    suffix = f"suffix_{lang}"

    try:
        x = knoten.find_one({"kurzname" : kurzname, "sichtbar" : True})
        print(x)
        data = { "kurzname" : x["kurzname"], "sichtbar" : x["sichtbar"], "titel" : x[titel], "titel_html" : x["titel_html"], "prefix" : x[prefix], "prefix_html" : x["prefix_html"], "suffix" : x[suffix], "suffix_html" : x["suffix_html"], "bearbeitet" : x[bearbeitet], "kinder" : []}
        for k1 in x["kinder"]:
            y = knoten.find_one({"_id" : k1})
            if y["sichtbar"]:
                data["kinder"].append(
                    { "kurzname" : y["kurzname"], "sichtbar" : y["sichtbar"], "titel" : y[titel], "titel_html" : y["titel_html"], "prefix" : y[prefix], "prefix_html" : y["prefix_html"], "suffix" : y[suffix], "suffix_html" : y["suffix_html"], "bearbeitet" : y[bearbeitet],"kinder" : []}
                )
                for k2 in y["kinder"]:
                    z = knoten.find_one({"_id" : k2})
                    if z["sichtbar"]:
                        data["kinder"][-1]["kinder"].append(
                        { "kurzname" : z["kurzname"], "parent_kurzname" : y["kurzname"], "sichtbar" : z["sichtbar"], "titel" : z[titel], "titel_html" : z["titel_html"], "prefix" : z[prefix], "prefix_html" : z["prefix_html"], "suffix" : z[suffix],  "suffix_html" : z["suffix_html"], "bearbeitet" : z[bearbeitet],"kinder" : []}              
                        )
    except:
        logger.warning("No connection to database")
        data = { "kurzname" : kurzname, "sichtbar" : True, "titel" : "", "titel_html" : False, "prefix" : "", "prefix_html" : False, "suffix" : "", "suffix_html" : False, "bearbeitet" : "", "kinder" : []}
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

