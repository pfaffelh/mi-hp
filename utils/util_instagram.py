import pymongo

# Verbindung zur MongoDB (wie util_news).
#
# Die Streamlit-Editor-App (mi-news, laeuft hinter dem VPN) legt ein gerendertes
# Instagram-Bild kurzzeitig in der Collection insta_bild ab -- unter einem
# unratbaren Zufalls-Token. Diese oeffentliche Route liefert es aus, damit Meta
# es von der URL herunterladen kann (die Graph-API kennt keinen Datei-Upload,
# sondern holt das Bild selbst von einer image_url). Nach dem Posten raeumt
# mi-news den Eintrag wieder auf; ein TTL-Index auf insta_bild faengt Orphans ab.
#
# Warum hier und nicht in mi-news: mi-news ist hinter dem VPN, Meta kaeme von
# aussen nicht dran. mi-hp ist der oeffentliche Server auf www2.
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_news = cluster["news"]
    insta_bild = mongo_db_news["insta_bild"]
except Exception:
    insta_bild = None


def get_insta_bild(token):
    """JPEG-Bytes zu einem Token -- oder None, wenn es den Token nicht gibt."""
    if insta_bild is None:
        return None
    doc = insta_bild.find_one({"token": token})
    if not doc:
        return None
    return doc.get("data")
