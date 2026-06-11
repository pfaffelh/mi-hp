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

def get_studiendekenat_data(query, lang = "de"):
    otherlang = "en" if lang == "de" else "de"
    data = list(studiendekanat.find(query, sort=[("rang", pymongo.ASCENDING)]))
    for item in data:
        item["rolle"] = item[f"rolle_{lang}"] if item[f"rolle_{lang}"] != "" else item[f"rolle_{otherlang}"]
        item["raum"] = item[f"raum_{lang}"] if item[f"raum_{lang}"] != "" else item[f"raum_{otherlang}"]
        item["name"] = item[f"name_{lang}"] if item[f"name_{lang}"] != "" else item[f"name_{otherlang}"]
        item["tel"] = item[f"tel_{lang}"] if item[f"tel_{lang}"] != "" else item[f"tel_{otherlang}"]
        item["sprechstunde"] = item[f"sprechstunde_{lang}"] if item[f"sprechstunde_{lang}"] != "" else item[f"sprechstunde_{otherlang}"]
        item["prefix"] = item[f"prefix_{lang}"] if item[f"prefix_{lang}"] != "" else item[f"prefix_{otherlang}"]
        item["text"] = item[f"text_{lang}"] if item[f"text_{lang}"] != "" else item[f"text_{otherlang}"]
        item["news"] = item[f"news_{lang}"] if item[f"news_{lang}"] != "" else item[f"news_{otherlang}"]        
        item["shownews"] = (datetime.now() < item["news_ende"])
    return data

# Here, x is a dict with fields x[f"{field_prefix}_de"] and x[f"{field_prefix}_en"]. The goal is to read x[f"{field_prefix}_{lang}"] if this data is available, otherwise use the other language.
def get(x, field_prefix, lang, alt = ""):
    otherlang = "de" if lang == "en" else "en"
    if x.get(f"{field_prefix}_de") is None: # field is not abailable, return alt
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
        loc["url"] = f"/nlehre/{lang}/page/{x['kurzname']}"
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
                loc["url"] = f"/nlehre/{lang}/page/{x['kurzname']}/{y['kurzname']}"
                for field_prefix in field_prefixes:
                    loc[field_prefix] = get(y, field_prefix, lang)
                data["kinder"].append(loc)
                for k2 in y["kinder"]:
                    z = knoten.find_one({"_id" : k2})
                    if z["sichtbar"]:
                        loc = { field: z[field] for field in fields}
                        loc["quicklinks"] = [{quicklink_prefix : get(q, quicklink_prefix, lang) for quicklink_prefix in quicklink_prefixes} for q in z["quicklinks"]]
                        loc["kinder"] = []
                        loc["url"] = f"/nlehre/{lang}/page/{x['kurzname']}/{z['kurzname']}"
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
    termine_prpa = list(kalender.find({"datum" : { "$gte" : anzeige_start}, "sichtbar" : True}))
    for t in termine_prpa:
        col = next((c["color"] for c in calendars if c["kurzname"] == "semesterplan"), "#FFFFFF")
        allDay = True if t["datum"].time() == datetime.min.time() else False
        events.append({
            "uid": f"{t['_id']}@math.uni-freiburg.de",
            "color" : col,
            "textcolor" : get_contrasting_text_color(col),
            "start": t["datum"].strftime('%Y-%m-%d') if allDay else t["datum"].isoformat(),
            "end": (t["datum"] + relativedelta(minutes = t["dauer"])).isoformat(),
            "allDay": allDay,
            "title": t["name"],
            "extendedProps" : {
                "description1" : format_termin(t),
                "description2" : "",
                "ort" : "",
                "googleTime" : formatDateForGoogle(t["datum"], t["datum"] + relativedelta(minutes = t["dauer"]), allDay),
                "icsTime" : formatDateForIcs(t["datum"], t["datum"] + relativedelta(minutes = t["dauer"]), allDay),
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
            "uid": f"{t['_id']}@math.uni-freiburg.de",
            "color" : col,
            "textcolor" : get_contrasting_text_color(col),
            "start": anfang.strftime('%Y-%m-%d') if allDay else anfang.isoformat(),
            "end": ende.isoformat(),
            "allDay": allDay,
            "title": t["name"],
            "extendedProps" : {
                "description1" : "",
                "description2" : "",
                "ort" : "",
                "googleTime" : formatDateForGoogle(anfang, ende, allDay),
                "icsTime" : formatDateForIcs(anfang, ende, allDay),
            },
            "groupId" : "studiendekanat"
        })

    return events

# ----------------------------------------------------------------------------
# ICS-Abo-Feed pro Verantwortlicher
# ----------------------------------------------------------------------------
# Liefert einen abonnierbaren Kalender (text/calendar) mit allen Aufgaben, für
# die die übergebene RZ-Kennung verantwortlich ist. Datums- und allDay-Logik
# spiegeln get_calendar_data(); formatDateForIcs() kommt aus utils.config.

def _ics_escape(text):
    # RFC5545 3.3.11: Sonderzeichen in TEXT-Werten maskieren.
    return (text or "").replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def _ics_fold(line):
    # RFC5545 3.1: Zeilen > 75 Oktette werden mit CRLF + Space gefaltet.
    encoded = line.encode("utf-8")
    if len(encoded) <= 75:
        return line
    parts = []
    while len(encoded) > 75:
        cut = 75
        while (encoded[cut] & 0xC0) == 0x80:  # nicht mitten in einem Mehrbyte-Zeichen schneiden
            cut -= 1
        parts.append(encoded[:cut].decode("utf-8"))
        encoded = encoded[cut:]
    parts.append(encoded.decode("utf-8"))
    return "\r\n ".join(parts)

def get_planer_ics(rz):
    """ICS-String aller Aufgaben, für die `rz` verantwortlich ist.
    Gibt None zurück, wenn die RZ-Kennung keinem User entspricht."""
    user = users.find_one({"rz": rz})
    if user is None:
        return None
    full_name = f"{user.get('vorname', '')} {user.get('name', '')}".strip() or rz

    auf = list(aufgabe.find({"verantwortlicher": rz}))

    # kleine Lookup-Caches gegen N+1 (Anker-Kalender, Prozess, Semester)
    kal_cache, proz_cache, sem_cache = {}, {}, {}
    def _kal(_id):
        if _id not in kal_cache:
            kal_cache[_id] = kalender.find_one({"_id": _id})
        return kal_cache[_id]
    def _proz(_id):
        if _id not in proz_cache:
            proz_cache[_id] = prozess.find_one({"_id": _id})
        return proz_cache[_id]
    def _sem(_id):
        if _id not in sem_cache:
            sem_cache[_id] = mongo_db_faq["semester"].find_one({"_id": _id})
        return sem_cache[_id]

    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Mathematisches Institut Freiburg//Planer//DE",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Planer – {_ics_escape(full_name)}",
        f"NAME:Planer – {_ics_escape(full_name)}",
        "X-WR-TIMEZONE:Europe/Berlin",
        "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
        "X-PUBLISHED-TTL:PT12H",
        # VTIMEZONE-Definition für die von formatDateForIcs referenzierte TZID
        # (RFC5545: nicht-globale TZID muss im Kalender definiert sein).
        "BEGIN:VTIMEZONE",
        "TZID:Europe/Berlin",
        "X-LIC-LOCATION:Europe/Berlin",
        "BEGIN:DAYLIGHT",
        "TZOFFSETFROM:+0100",
        "TZOFFSETTO:+0200",
        "TZNAME:CEST",
        "DTSTART:19700329T020000",
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU",
        "END:DAYLIGHT",
        "BEGIN:STANDARD",
        "TZOFFSETFROM:+0200",
        "TZOFFSETTO:+0100",
        "TZNAME:CET",
        "DTSTART:19701025T030000",
        "RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU",
        "END:STANDARD",
        "END:VTIMEZONE",
    ]
    for t in auf:
        ka = _kal(t.get("ankerdatum"))
        if ka is None:
            continue
        anfang = ka["datum"] + relativedelta(days=t["start"])
        ende = ka["datum"] + relativedelta(days=t["ende"])
        allDay = anfang.time() == datetime.min.time()

        pr = _proz(t.get("parent"))
        sem = _sem(pr["parent"]) if pr else None
        kontext = " · ".join(x for x in [sem["name"] if sem else "", pr["name"] if pr else ""] if x)
        status_bits = []
        if t.get("bestätigt"):
            status_bits.append("bestätigt")
        if t.get("angefangen"):
            status_bits.append("begonnen")
        if t.get("erledigt"):
            status_bits.append("erledigt")
        desc_parts = [kontext, t.get("kommentar", "")]
        if status_bits:
            desc_parts.append("Status: " + ", ".join(status_bits))
        description = "\\n".join(_ics_escape(p) for p in desc_parts if p)

        event = [
            "BEGIN:VEVENT",
            f"UID:{t['_id']}@math.uni-freiburg.de",
            f"DTSTAMP:{dtstamp}",
        ]
        event += formatDateForIcs(anfang, ende, allDay).split("\n")
        event.append(f"SUMMARY:{_ics_escape(t.get('name', ''))}")
        if description:
            event.append(f"DESCRIPTION:{description}")
        event.append("STATUS:" + ("CONFIRMED" if t.get("bestätigt") else "TENTATIVE"))
        event.append("END:VEVENT")
        lines += event

    lines.append("END:VCALENDAR")
    return "\r\n".join(_ics_fold(l) for l in lines) + "\r\n"