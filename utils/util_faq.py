import pymongo
import utils.config as config
from bson import ObjectId
from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_faq = cluster["faq"]
    studiengang = mongo_db_faq["studiengang"]
    stu_category = mongo_db_faq["stu_category"]
    stu_qa = mongo_db_faq["stu_qa"]
    mit_category = mongo_db_faq["mit_category"]
    mit_qa = mongo_db_faq["mit_qa"]
    studiendekanat = mongo_db_faq["studiendekanat"]
    
except:
    logger.warning("No connection to Database 1")


# returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 

def get_stu_faq(lang):
    # Alle Kategorien zeigen außer "unsichtbar"
    cats = list(stu_category.find({"kurzname": {"$ne": "unsichtbar"}}, sort=[("rang", pymongo.ASCENDING)]))
    q = f"q_{lang}"
    a = f"a_{lang}"
    name = f"name_{lang}"

    cat_ids = [f"stu_kat_{cat['_id']}" for cat in cats]
    names_dict = {f"stu_kat_{cat['_id']}": cat[name] for cat in cats}
    qa_pairs = {}
    for cat in cats:
        y = list(stu_qa.find({"category": cat["_id"]}, sort=[("rang", pymongo.ASCENDING)]))
        qa_pairs[f"stu_kat_{cat['_id']}"] = [ (f"qa_{str(x['_id'])}", x[q]  + (f" ({', '.join([s[name] for s in list(studiengang.find({'_id': { '$in' : x['studiengang']}}))])})" if x['studiengang'] != [] else "") , x[a]) for x in y]
        #print(qa_pairs[cat_id])
    return cat_ids, names_dict, qa_pairs

def get_mit_faq(lang):
    # Alle Kategorien zeigen außer "unsichtbar"
    cats = list(mit_category.find({"kurzname": {"$ne": "unsichtbar"}}, sort=[("rang", pymongo.ASCENDING)]))
    q = f"q_{lang}"
    a = f"a_{lang}"
    name = f"name_{lang}"

    cat_ids = [f"mit_kat_{cat['_id']}" for cat in cats]
    names_dict = {f"mit_kat_{cat['_id']}": cat[name] for cat in cats}
    qa_pairs = {}
    for cat in cats:
        y = list(mit_qa.find({"category": cat["_id"]}, sort=[("rang", pymongo.ASCENDING)]))
        qa_pairs[f"mit_kat_{cat['_id']}"] = [ (f"qa_{str(x['_id'])}", x[q] , x[a]) for x in y]
    return cat_ids, names_dict, qa_pairs

def get_stu_cat(qa_id):
    id = qa_id.split("_")[-1]
    x = stu_qa.find_one({"_id" : ObjectId(id)})
    if x:
        res = f"stu_kat_{x['category']}"
    else:
        res = ""
    return res

def get_mit_cat(qa_id):
    id = qa_id.split("_")[-1]
    x = mit_qa.find_one({"_id" : ObjectId(id)})
    if x:
        res = f"mit_kat_{x['category']}"
    else:
        res = ""
    return res

