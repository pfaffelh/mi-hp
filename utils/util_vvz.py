import pymongo
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



