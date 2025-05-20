import pymongo
from bson import ObjectId
from datetime import datetime, timedelta
from collections import OrderedDict
from .config import *
from operator import itemgetter
import latex2markdown
from markdown import markdown

from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import xml.etree.ElementTree as etree

def remove_p(html):
    if html.startswith('<p>') and html.endswith('</p>'):
        return html[3:-4] 
    else:
        return html

#from .util_logging import logger

# Connect to MongoDB
try:
    cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    mongo_db_vvz = cluster["vvz"]
    vvz_anforderung = mongo_db_vvz["anforderung"]
    vvz_anforderungkategorie = mongo_db_vvz["anforderungkategorie"]
    vvz_code = mongo_db_vvz["code"]
    vvz_codekategorie = mongo_db_vvz["codekategorie"]
    vvz_gebaeude = mongo_db_vvz["gebaeude"]
    vvz_rubrik = mongo_db_vvz["rubrik"]
    vvz_modul = mongo_db_vvz["modul"]
    vvz_person = mongo_db_vvz["person"]
    vvz_raum = mongo_db_vvz["raum"]
    vvz_semester = mongo_db_vvz["semester"]
    vvz_studiengang = mongo_db_vvz["studiengang"]
    vvz_terminart = mongo_db_vvz["terminart"]
    vvz_veranstaltung = mongo_db_vvz["veranstaltung"]
    vvz_planungveranstaltung = mongo_db_vvz["planungveranstaltung"]
    vvz_planung = mongo_db_vvz["planung"]
except:
    pass
    # logger.warning("No connection to Database 1")

# returns 
# a list of category shortnames (cats_kurzname), 
# a dictionary how to translate them into full names (names_dict), 
# a dict with the shortnames as keys, where each value is a list of triples (id, q, a), which contains the information for each question in each category (qa_pairs). 
# recall that category and qa come with a variable rang: int, which serves to order the categories and qa-pairs. 

def get_showanmeldung(studiengang):
    year = datetime.now().year
    date_format = '%d.%m.'
    res = False
    for b in bewerbungsdaten[studiengang]:
        loc_start = datetime.strptime(b["start"], date_format)
        loc_start = datetime(year, loc_start.month, loc_start.day)
        loc_end = datetime.strptime(b["end"], date_format)
        loc_end = datetime(year, loc_end.month, loc_end.day)
        if loc_start < datetime.now() and datetime.now() < loc_end:
            res = True
    return res

def get_showsemester(shortname, hp_sichtbar = True):
    # Gibt es ein sichtbares Semester mit shortname?
    b = vvz_semester.find_one({"kurzname": shortname, "hp_sichtbar": hp_sichtbar })
    return (b != None)

def get_current_semester_kurzname():
    if datetime.now().month < 4:
        res = f"{datetime.now().year-1}WS"
    elif 3 < datetime.now().month and datetime.now().month < 10:
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
    return f"{'Wintersemester' if b == 'WS' else 'Sommersemester'} {a}{c}"

def semester_name_en(kurzname):
    a = int(kurzname[:4])
    b = kurzname[4:]
    c = f"/{a+1}" if b == "WS" else ""
    return f"{'Winter term' if b == 'WS' else 'Summer term'} {a}{c}"

def get_raum(raum_id, url = True):
    r = vvz_raum.find_one({ "_id": raum_id})
    g = vvz_gebaeude.find_one({ "_id": r["gebaeude"]})
    gurl = g["url"]
    if not url or gurl == "":
        raum = ", ".join([r["name_de"], g["name_de"]])
    else:
        raum = ", ".join([r['name_de'], f"[{g['name_de']}]({gurl})"])
    res = remove_p(markdown(raum))
    return res

def vorname_name(person_id, url = True, lang = "de"):
    p = vvz_person.find_one({"_id": person_id})
    if lang == "en" and p["name_en"] != "":
        res = p["name_en"]
    else:
        res = f"{p['vorname']} {p['name']}"
    if url and p["url"] != "":
        res = f"[{res}]({p['url']})"
    res = remove_p(markdown(res))
    return res

def name_vorname(person_id, url = True, lang = "de"):
    p = vvz_person.find_one({"_id": person_id})
    if lang == "en" and p["name_en"].strip() != "":
        res = p["name_en"]
    else:
        res = f"{p['name']}, {p['vorname']}"
    if url and p["url"] != "":
        res = f"[{res}]({p['url']})"    
    return remove_p(markdown(res))

def name_terminart(terminart_id, lang):
    name = f"name_{lang}"
    ta = vvz_terminart.find_one({"_id": terminart_id})
    return ta[name]

def name(person_id, lang = "de"):
    p = vvz_person.find_one({"_id": person_id})
    if lang == "en" and p["name_en"].strip() != "":
        p["name"] = p["name_en"]
    return f"{p['name']}"

def makemodulname(modul_id, lang = "de", alter = True, studiengang = ""):
    otherlang = "de" if "lang" == "en" else "en"
    m = vvz_modul.find_one({"_id": modul_id})
    mname = m[f"name_{lang}"]
    if alter and mname == "":
        mname = m[f"name_{otherlang}"]
    s = ", ".join([x["kurzname"] for x in list(vvz_studiengang.find({"_id": { "$in" : m["studiengang"]}, }))])
    if studiengang == "":
        res = f"{mname} ({s})"
    else:
        res = mname
    return res

def repr_veranstaltung(v_id, lang):
    v = vvz_veranstaltung.find_one({"_id": v_id})
    per = ", ".join([name(p, lang) for p in v["dozent"]]) if v["dozent"] != [] else ""
    per = f"({per})" if per != "" else ""
    return f"{v[f'name_{lang}']} {per}"

def repr_semester(s_id, lang):
    s = vvz_semester.find_one({"_id": s_id})
    return s["kurzname"]

# Die Funktion fasst zB Mo, 8-10, HS Rundbau, Albertstr. 21 \n Mi, 8-10, HS Rundbau, Albertstr. 21 \n 
# zusammen in
# Mo, Mi, 8-10, HS Rundbau, Albertstr. 21 \n Mi, 8-10, HS Rundbau, Albertstr. 21
def make_raumzeit_woechentlich(veranstaltung, lang = "de", url = True):    
    res = []
    for termin in veranstaltung["woechentlicher_termin"]:
        ta = vvz_terminart.find_one({"_id": termin['key']})
        if ta["hp_sichtbar"]:
            ta = ta[f"name_{lang}"]
            if termin['wochentag'] !="":
                # key, raum, zeit, person, kommentar
                key = f"{ta}:" if ta != "" else ""
                # Raum und Gebäude mit Url, zB Hs II.
                r = vvz_raum.find_one({ "_id": termin["raum"]})
                raum = get_raum(r["_id"], url)
                # zB Vorlesung: Montag, 8-10 Uhr, HSII, Albertstr. 23a
                if termin['start'] is not None:
                    zeit = f"{str(termin['start'].hour)}{':'+str(termin['start'].minute) if termin['start'].minute > 0 else ''}"
                    if termin['ende'] is not None:
                        zeit = zeit + f"-{str(termin['ende'].hour)}{':'+str(termin['ende'].minute) if termin['ende'].minute > 0 else ''}"
                    zeit = zeit + (" Uhr" if lang == "de" else "h")
                else:
                    zeit = ""
                # zB Mo, 8-10
                tag = weekday[termin['wochentag']]
                # person braucht man, wenn wir dann die Datenbank geupdated haben.
                # person = ", ".join([f"{vvz_person.find_one({"_id": x})["vorname"]} {vvz_person.find_one({"_id": x})["name"]}"for x in termin["person"]])
                kommentar = rf"{termin[f'kommentar_{lang}_html']}" if termin[f'kommentar_{lang}_html'] != "" else ""
                new = [key, tag, ", ".join([zeit, raum]), kommentar]
                if key in [x[0] for x in res]:
                    new.pop(0)
                    i = [x[0] for x in res].index(key)
                    #print(res[i])
                    if res[i][1] == tag:
                        new.pop(0)
                        if res[i][2] == zeit:
                            new.pop(0)
                    res[i] = (res[i] + new)
                    res[i].reverse()
                    res[i] = list(OrderedDict.fromkeys(res[i]))
                    res[i].reverse()
                else:
                    res.append(new)
    res = [f"{x[0]} {(', '.join([z for z in x if z !='' and x.index(z)!=0]))}" for x in res]
    return res

def make_raumzeit_einmalig(veranstaltung, lang = "de", url = True):    
    res = []
    for termin in veranstaltung["einmaliger_termin"]:
        ta = vvz_terminart.find_one({"_id": termin['key']})
        if ta["hp_sichtbar"]:
            ta = ta[f"name_{lang}"]
            # Raum und Gebäude mit Url.
            raeume = list(vvz_raum.find({ "_id": { "$in": termin["raum"]}}))
            raum = ", ".join([get_raum(r["_id"], url) for r in raeume])
            # zB Vorlesung: Montag, 8-10, HSII, Albertstr. 23a
            if termin['enddatum'] is None:
                termin['enddatum'] = termin['startdatum']
            if termin['startdatum'] is not None:
                startdatum = termin['startdatum'].strftime("%d.%m.")
                if termin['startdatum'] != termin['enddatum']:
                    enddatum = termin['enddatum'].strftime("%d.%m.")
                    datum = " bis ".join([startdatum, enddatum]) if startdatum != enddatum else startdatum
                else:
                    datum = startdatum
            else:
                datum = ""
            if termin['startzeit'] is not None:
                zeit = termin['startzeit'].strftime("%H:%M")
                if termin['endzeit'] is not None:
                    # Bei einmaligen Terminen werden Minuten immer angezeigt.
                    zeit = zeit + "-" + termin['endzeit'].strftime("%H:%M") 
            else:
                zeit = ""
            # person braucht man, wenn wir dann die Datenbank geupdated haben.
            # person = ", ".join([f"{vvz_person.find_one({"_id": x})["vorname"]} {vvz_person.find_one({"_id": x})["name"]}"for x in termin["person"]])
            kommentar = rf"{termin[f'kommentar_{lang}_html']}" if termin[f'kommentar_{lang}_html'] != "" else ""
            new = [ta, datum, zeit, raum, kommentar]
            res.append(new)
    res = [f"{x[0]} {(', '.join([z for z in x if z !='' and x.index(z)!=0]))}" for x in res]
    return res

def make_codes(sem_id, veranstaltung_id, lang):
    res = {}
    codekategorie_list = list(vvz_codekategorie.find({"semester": sem_id, "hp_sichtbar": True}))    
    v = vvz_veranstaltung.find_one({"_id": veranstaltung_id})

    for ck in codekategorie_list:
        code_list = [vvz_code.find_one({"_id": c, "codekategorie": ck["_id"]}) for c in v["code"]]
        code_list = [x for x in code_list if x is not None]
        if len(code_list)>0:
            res[ck[f"name_{lang}"]] = ", ".join([c[f"beschreibung_{lang}"] for c in code_list])
    return res

# Falls vpn == True, werden auch nicht sichtbare Semester angezeigt
def get_data(sem_shortname, lang = "de", studiengang = "", modul = "", veranstaltungs_query = {}, vpn = False):
    semester_query = {"kurzname" : sem_shortname}
    if not vpn:
        semester_query["hp_sichtbar"] = True
    sem = vvz_semester.find_one(semester_query)
    sem_id = sem.get("_id", "")

    data = {"vpn" : vpn}

    rubriken = list(vvz_rubrik.find({"semester": sem_id, "hp_sichtbar": True}, sort=[("rang", pymongo.ASCENDING)]))

    codekategorie = list(vvz_codekategorie.find({"semester": sem_id, "hp_sichtbar": True}, sort=[("rang", pymongo.ASCENDING)]))
    codes = list(vvz_code.find({"semester": sem_id, "codekategorie": { "$in" : [c["_id"] for c in codekategorie] }}, sort=[("rang", pymongo.ASCENDING)]))

    data["semester"] = vvz_semester.find_one({"kurzname": sem_shortname})
    data["semester"]["name"] = data["semester"][f"name_{lang}"] 
    data["semester"]["prefix"] = data["semester"][f"prefix_{lang}"] 

    if studiengang != "":
        data["studiengang"] = vvz_studiengang.find_one({"kurzname": studiengang})
        data["studiengang"]["name"] = data["studiengang"][f"name"]
        mod = list(vvz_modul.find({"_id" : { "$in" : data["studiengang"]["modul"] } }, sort = [( f"name_{lang}", pymongo.ASCENDING)]))
        data["studiengang"]["modul"] = [{ "kurzname" : m["kurzname"], "name" : m[f"name_{lang}"] } for m in mod]
        if modul != "":
            data["modul"] = vvz_modul.find_one({"kurzname": modul})
            data["modul"]["name"] = data["modul"][f"name_{lang}"]
    data["rubrik"] = []
    data["code"] = []

    for code in codes:
        if vvz_veranstaltung.find_one({"semester": sem_id, "code" : { "$elemMatch" : { "$eq": code["_id"]}}}):
            code_dict = {}
            code_dict["name"] = code["name"]
            code_dict["beschreibung"] = code[f"beschreibung_{lang}"]
            data["code"].append(code_dict)

    for rubrik in rubriken:
        r_dict = {}
        r_dict["titel"] = rubrik[f"titel_{lang}"]
        r_dict["untertitel"] = rubrik[f"untertitel_{lang}"]
        r_dict["prefix"] = rubrik[f"prefix_{lang}"]
        r_dict["suffix"] = rubrik[f"suffix_{lang}"]
        # print(r_dict["titel"])
        r_dict["veranstaltung"] = []
        
        if studiengang != "":
            s = vvz_studiengang.find_one({"kurzname" : studiengang})
            if modul == "":
                mod_list = list(vvz_modul.find({ "studiengang" : { "$elemMatch" : { "$eq" : s["_id"] }}}))
            else:
                mod_list = list(vvz_modul.find({ "kurzname" : modul}))

            veranstaltungs_query = veranstaltungs_query | {"rubrik": rubrik["_id"], "hp_sichtbar": True, "$or" : [{ "verwendbarkeit_modul" : { "$elemMatch" : { "$eq" : m["_id"] }}} for m in mod_list ]}
            veranstaltungen = list(vvz_veranstaltung.find(veranstaltungs_query, sort=[("rang", pymongo.ASCENDING)]))
        else:
            veranstaltungs_query = veranstaltungs_query | {"rubrik": rubrik["_id"], "hp_sichtbar" : True}
            veranstaltungen = list(vvz_veranstaltung.find(veranstaltungs_query, sort=[("rang", pymongo.ASCENDING)]))
        for veranstaltung in veranstaltungen:
            otherlang = "de" if lang == "en" else "en"
            v_dict = {}
            v_dict["code"] = make_codes(sem_id, veranstaltung["_id"], lang)
            v_dict["titel"] = veranstaltung[f"name_{lang}"] if veranstaltung[f"name_{lang}"] != "" else veranstaltung[f"name_{otherlang}"]
            v_dict["kommentar"] = veranstaltung[f"kommentar_html_{lang}"]
            v_dict["link"] = veranstaltung["url"]
            v_dict["dozent_mit_url"] = ", ".join([vorname_name(x, True, lang) for x in veranstaltung["dozent"]])
            v_dict["dozent"] = ", ".join([vorname_name(x, False, lang) for x in veranstaltung["dozent"]])
            v_dict["allepersonen"] = ", ".join([vorname_name(x, False, lang) for x in veranstaltung["dozent"] + veranstaltung["assistent"]]) # + veranstaltung["organisation"]])
            v_dict["assistent_mit_url"] = ", ".join([vorname_name(x, True, lang) for x in veranstaltung["assistent"]])
            v_dict["assistent"] = ", ".join([vorname_name(x, False, lang) for x in veranstaltung["assistent"]])
            v_dict["organisation_mit_url"] = ", ".join([vorname_name(x, True, lang) for x in veranstaltung["organisation"]])
            v_dict["organisation"] = ", ".join([vorname_name(x, False, lang) for x in veranstaltung["organisation"]])
            # raumzeit ist der Text, der unter der Veranstaltung steht.
            # print(v_dict["titel"])
            v_dict["raumzeit_woechentlich_mit_url"] = make_raumzeit_woechentlich(veranstaltung, lang=lang, url = True)
            v_dict["raumzeit_woechentlich"] = make_raumzeit_woechentlich(veranstaltung, lang=lang, url = False)
            v_dict["raumzeit_einmalig_mit_url"] = make_raumzeit_einmalig(veranstaltung, lang=lang, url = True)
            v_dict["raumzeit_einmalig"] = make_raumzeit_einmalig(veranstaltung, lang=lang, url = False)
            v_dict["inhalt"] = latex2markdown.LaTeX2Markdown(veranstaltung[f"inhalt_{lang}"]).to_markdown()
            v_dict["vorkenntnisse"] = veranstaltung[f"vorkenntnisse_{lang}"]
            if studiengang == "":
                mod_list_reduced = veranstaltung["verwendbarkeit_modul"]
            else:
                mod_list = list(vvz_modul.find({ "studiengang" : { "$elemMatch" : { "$eq" : s["_id"] }}}))
                mod_list_reduced = [m["_id"] for m in mod_list if m["_id"] in veranstaltung["verwendbarkeit_modul"]]
            v_dict["verwendbarkeit"] = "<br>".join([makemodulname(x, lang, True, studiengang)for x in mod_list_reduced])
            r_dict["veranstaltung"].append(v_dict)

        if r_dict["veranstaltung"] != []:
            data["rubrik"].append(r_dict)
    # print(data["rubrik"])
    #print(data)
    return data

def get_data_stundenplan(sem_shortname, lang="de", vpn = False):
    query = {"kurzname": sem_shortname}
    if not vpn:
        query["hp_sichtbar"] = True
    sem = vvz_semester.find_one(query)
    sem_id = sem.get("_id", "")

    name = f'name_{lang}'
    ver = vvz_veranstaltung.find({"semester" : sem_id})
    data = []
    for v in ver:
        for t in v["woechentlicher_termin"]:
            if t["start"]:
                zeit = f"{str(t['start'].hour)}{': '+str(t['start'].minute) if t['start'].minute > 0 else ''}"
                if t['ende'] is not None:
                    zeit = zeit + f"-{str(t['ende'].hour)}{': '+str(t['ende'].minute) if t['ende'].minute > 0 else ''}"
                zeit = (zeit + " Uhr") if lang == "de" else (zeit + "h")
            else:
                zeit = ""
            if zeit != "":
                url = v["url"]
                if t["wochentag"] in wochentage.keys():
                    data.append({
                        "wochentag": t["wochentag"] if lang=="de" else wochentage[t["wochentag"]],
                        "start": t["start"],
                        "ende": t["ende"],
                        "zeit": zeit,
                        "veranstaltung": v[name],
                        "veranstaltung_mit_link": f"{v[name]}" if url == "" else f"<a href='{url}'>{v[name]}</a>",
                        "dozent": ", ".join([vorname_name(p, True) for p in v["dozent"] + v["organisation"]]),
                        "raum":get_raum(t["raum"], True)
                    })

    wt = wochentage.keys() if lang == "de" else wochentage.values()
    res = {}
    for t in wt:
        data_loc = [d for d in data if d["wochentag"] == t]
        data_loc = sorted(data_loc, key = itemgetter('start', 'ende', 'veranstaltung'))
        
        # Delete entry zeit if it coincides with the previous entry
        zeitprevious = ""
        for d in data_loc:
            z = d["zeit"]
            if d["zeit"] == zeitprevious:
                d["zeit"] = ""
            zeitprevious = z
                        
        res[t] = data_loc
    return res

def name_termine(ver_id, lang="de"):
    name = f'name_{lang}'
    v = vvz_veranstaltung.find_one({"_id" : ver_id})
    url = v["url"]
    
    termine = []
    for t in v["woechentlicher_termin"]:
        if t["start"]:
            zeit = f"{str(t['start'].hour)}{': '+str(t['start'].minute) if t['start'].minute > 0 else ''}"
            if t['ende'] is not None:
                zeit = zeit + f"-{str(t['ende'].hour)}{': '+str(t['ende'].minute) if t['ende'].minute > 0 else ''}"
            zeit = (zeit + " Uhr") if lang == "de" else (zeit + "h")
        else:
            zeit = ""
        if zeit != "":
            termine.append((t["wochentag"] if lang=="de" else wochentage[t["wochentag"]]) + ", " + zeit)
            
    for t in v["einmaliger_termin"]:
        ta = vvz_terminart.find_one({"_id": t['key']})
        if ta["hp_sichtbar"]:
            ta = ta[f"name_{lang}"]
            if t['enddatum'] is None:
                t['enddatum'] = t['startdatum']
            if t['startdatum'] is not None:
                startdatum = t['startdatum'].strftime("%d.%m.")
                if t['startdatum'] != t['enddatum']:
                    enddatum = t['enddatum'].strftime("%d.%m.")
                    datum = " bis ".join([startdatum, enddatum]) if startdatum != enddatum else startdatum
                else:
                    datum = startdatum
            else:
                datum = ""
            if t['startzeit'] is not None:
                zeit = t['startzeit'].strftime("%H:%M")
                if t['endzeit'] is not None:
                    zeit = zeit + "-" + t['endzeit'].strftime("%H:%M")
            else:
                zeit = ""
            termine.append(": ".join([x for x in [ta, ", ".join([x for x in [datum, zeit] if x != ""])] if x != ""]))
    res = (f"<strong>{v[name]}</strong>" if url == "" else f"<strong><a href='{url}'>{v[name]}</a></strong>")
    if termine != []:
        res = res + "<br>" + "; ".join(termine)
    return res

def get_current_personen(lang = "de"):
    s = vvz_semester.find_one({"hp_sichtbar" : True}, sort=[("rang", pymongo.DESCENDING)])
    personen = list(vvz_person.find({"semester" : { "$elemMatch" : { "$eq" : s["_id"]}}}))
    for p in personen:
        p["name_nolang"] = p["name"] if (lang == "de" or p["name_en"] == "") else p["name_en"]
    per = sorted(personen, key=lambda d: (d["name_nolang"], d["vorname"]))
    data = [{"_id" : str(p["_id"]), "name" : vorname_name(p["_id"], url = False, lang = lang), "url" : p["url"]} for p in per]
    return data

# Wenn id == "all", werden alle Daten der Semester ausgelesen. Wenn id == "", werden keine Daten zurückgegeben. Andernfalls ist es die id einer Lehrperson im vvz.
def get_data_person(id, lang = "de"):
    if str(id) == "":
        data = []
    else:
        if id != "all":
            id = ObjectId(id)
            query = {"$or" : [{"dozent" : { "$elemMatch" : { "$eq" : id}}}, {"assistent" : { "$elemMatch" : { "$eq" : id }}}]}
        else:
            query = {}

        name = f"name_{lang}"
        # Hier wird das Semester festgelegt, ab wann die Anzeige stattfindet.
        startsemester = vvz_semester.find_one({"kurzname" : "2018WS", "hp_sichtbar" : True})
        semester = list(vvz_semester.find({"hp_sichtbar" : True, "rang" : { "$gte" : startsemester["rang"]}}, sort=[("rang", pymongo.DESCENDING)]))

        data = []
        for s in semester:
            sem_data = get_data(s["kurzname"], lang, "", "", query)
            data.append(sem_data)
    return data

def get_data_personenplan(sem_shortname, lang="de", vpn = False):
    query = {"kurzname": sem_shortname}
    if not vpn:
        query["hp_sichtbar"] = True
    sem = vvz_semester.find_one(query)
    sem_id = sem["_id"] if sem else ""
    ver = vvz_veranstaltung.find({"semester" : sem_id})

    data = []
    for v in ver:
        nt = name_termine(v["_id"], lang)
        for p in v["dozent"] + v["assistent"] + v["organisation"]:
            rolle = "Dozent*in" if p in v["dozent"] else ("Assistent*in" if p in v["assistent"] else "Organisation")
            try :
                sws = [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                kommentar = [d["kommentar"] for d in v["deputat"] if d["person"] == p][0]
            except:
                sws = 0
                kommentar = ""
            data.append({
                "person": f"{name_vorname(p, False, lang)}",
                "person_mit_url": f"{name_vorname(p, True, lang)}",
                "veranstaltung": nt,
                "rolle": rolle,
                "sws": sws,
                "kommentar": kommentar
                })

        for t in v["woechentlicher_termin"] + v["einmaliger_termin"]:
            for p in t["person"]:
                try :
                    sws = [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                    kommentar = [d["kommentar"] for d in v["deputat"] if d["person"] == p][0]
                except:
                    sws = 0
                    kommentar = ""
                data.append({
                    "person": f"{name_vorname(p, False, lang)}",
                    "person_mit_url": f"{name_vorname(p, True, lang)}",
                    "veranstaltung": nt,
                    "rolle": name_terminart(t["key"], lang),
                    "sws": sws,
                    "kommentar" : kommentar
                    })

    data = sorted(data, key = itemgetter('person', 'veranstaltung'))
    personprevious = ""
    for d in data:
        z = d["person_mit_url"]
        if d["person_mit_url"] == personprevious:
            d["person_mit_url"] = ""
        personprevious = z
    return data

def nextsemester(sem_shortname):
    if sem_shortname[4:6] == "WS":
        res = f"{int(sem_shortname[0:4])+1}SS"
    else:
        res = f"{int(sem_shortname[0:4])}WS"
    return res

def is_WS(sem_shortname):
    return sem_shortname[4:6] == "WS"

def get_data_planung(sem_shortname, lang="de"):
    sems = [nextsemester(sem_shortname)]
    for i in range(5):
        sems.append(nextsemester(sems[-1]))
        
    planungveranstaltung = list(vvz_planungveranstaltung.find({}, sort=[("rang", pymongo.ASCENDING)]))
    planung = list(vvz_planung.find({"sem" : { "$in" : sems }}))
        
    data = []
    for pv in planungveranstaltung:
        loc1 = {key: "-" for key in sems}
        loc2 = loc3 = {}
        for s in sems:
            if pv["regel"] == "Jedes Semester" or (is_WS(s) and pv["regel"] == "Jedes Wintersemester") or (not is_WS(s) and pv["regel"] == "Jedes Sommersemester"):
                loc2[s] = "offen"                
        for p in planung: #[p in planung if p["veranstaltung"] == pv] :
            if p["veranstaltung"] == pv["_id"]:
                loc3[p["sem"]] = ", ".join([name(x) for x in p["dozent"]] + ([p["kommentar"]] if p["kommentar"] != "" else []))
        data.append({"name" : pv["name"], "sws" : pv["sws"] } | loc1 | loc2 | loc3)
    # print(data)
    return sems, data

# Hier werden alle Termine ausgegeben, die nach anzeige_start liegen
def get_calendar_data(anzeige_start, lang = "de"):
    ter_list = [ta["_id"] for ta in list(vvz_terminart.find({"cal_sichtbar" : True}))]
    ver = list(vvz_veranstaltung.find({"einmaliger_termin" : { "$elemMatch" : {  "key" : { "$in" : ter_list},"startdatum" : { "$gte" : anzeige_start}}}}))
    all = []

    for v in ver:
        for t in v["einmaliger_termin"]:
            if t["startdatum"] is not None and t["startdatum"] >= anzeige_start and t["key"] in ter_list:
                if t["enddatum"] is None:
                    t["enddatum"] = t["startdatum"]
                te = f"{name_terminart(t['key'], lang)}"
                te = te + ": " if te != "" else ""
                title = f"{te} {repr_veranstaltung(v['_id'], lang)} {t[f'kommentar_{lang}_html']}, {repr_semester(v['semester'], lang)}"
                if t["startzeit"] and (t["startzeit"].hour != 0 or t["startzeit"].minute != 0): 
                    start = datetime.combine(t["startdatum"].date(), t["startzeit"].time())
                    allDay = 'false'
                    title_lang = f"{start.strftime("%H:%M")} :{title}"
                else:
                    start = t["startdatum"]
                    allDay = 'true'
                    title_lang = title
                if t["endzeit"] : 
                    ende = datetime.combine(t["enddatum"].date(), t["endzeit"].time())
                else:
                    ende = t["enddatum"]
                col = next((c["color"] for c in calendars if c["kurzname"] == "pruefungen"), "#FFFFFF")

                all.append({
                    "color" : col,
                    "textcolor" : get_contrasting_text_color(col),
                    "start": start.strftime("%Y-%m-%d %H:%M:00"),
                    "end": ende.strftime("%Y-%m-%d %H:%M:00"),
                    "startzeit": start.strftime("%H:%M"),
                    "endezeit": ende.strftime("%H:%M"),
                    "allDay": allDay,
                    "title": title,
                    "extendedProps" : {
                        "description" : title_lang
                    },
                    "groupId" : "pruefungen"
                })
    return all
