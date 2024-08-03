import pymongo
import utils.config as config
from bson import ObjectId
#from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_faq = cluster["faq"]
    category = mongo_db_faq["category"] 
    qa = mongo_db_faq["qa"]
except:
    logger.warning("No connection to Database 1")


# returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 

def get_faq(lang):
    # Alle Kategorien zeigen außer "unsichtbar"
    cats = list(category.find({"kurzname": {"$ne": "unsichtbar"}}, sort=[("rang", pymongo.ASCENDING)]))
    cats_kurzname = [cat["kurzname"] for cat in cats]
    names_dict = {cat["kurzname"]: (cat["name_de"] if lang == "de" else cat["name_en"]) for cat in cats}
    qa_pairs = {}
    for cat_kurzname in cats_kurzname:
        y = qa.find({"category": cat_kurzname}, sort=[("rang", pymongo.ASCENDING)])
        qa_pairs[cat_kurzname] = [ (f"qa_{str(x['_id'])}", f"{x['q_de'] if lang == 'de' else x['q_en']} " + (f"({', '.join([config.studiengaenge[s] for s in x['studiengang']])})" if x['studiengang'] != [] else ""), (x["a_de"]) if lang == "de" else (x["a_en"])) for x in y]
    return cats_kurzname, names_dict, qa_pairs

def get_cat(qa_id):
    print(qa_id)
    id = qa_id.split("_")[-1]
    print(id)
    x = qa.find_one({"_id" : ObjectId(id)})
    if x:
        res = x["category"]
    else:
        res = ""
    return res

