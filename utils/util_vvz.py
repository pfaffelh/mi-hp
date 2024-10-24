import pymongo
from datetime import datetime
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

def raum_mit_url(raum_id):
    r = vvz_raum.find_one({ "_id": raum_id})
    g = vvz_gebaeude.find_one({ "_id": r["gebaeude"]})
    gurl = g["url"]
    if gurl == "":
        raum = ", ".join([r["name_de"], g["name_de"]])
    else:
        raum = ", ".join([r['name_de'], f"[{g['name_de']}]({gurl})"])
    res = remove_p(markdown(raum))
    return res

def vorname_name(person_id):
    p = vvz_person.find_one({"_id": person_id})
    return f"{p['vorname']} {p['name']}"

def vorname_name_mit_url(person_id):    
    p = vvz_person.find_one({"_id": person_id})
    if p["url"] != "":
        res = vorname_name(person_id)
        res = f"[{res}]({p['url']})"
    else:
        res = vorname_name(person_id)
        print(res)
    res = remove_p(markdown(res))
    print(res)
    return res

def name_vorname(person_id):
    p = vvz_person.find_one({"_id": person_id})
    return f"{p['name']}, {p['vorname']}"

def name_vorname_mit_url(person_id):
    p = vvz_person.find_one({"_id": person_id})
    res = f"{p['name']}, {p['vorname']}"
    if p["url"] != "":
        res = f"[{res}]({p['url']})"    
    return remove_p(markdown(res))

def name_terminart(terminart_id, lang):
    name = f"name_{lang}"
    ta = vvz_terminart.find_one({"_id": terminart_id})
    return ta[name]

def name(person_id):
    p = vvz_person.find_one({"_id": person_id})
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



# Die Funktion fasst zB Mo, 8-10, HS Rundbau, Albertstr. 21 \n Mi, 8-10, HS Rundbau, Albertstr. 21 \n 
# zusammen in
# Mo, Mi, 8-10, HS Rundbau, Albertstr. 21 \n Mi, 8-10, HS Rundbau, Albertstr. 21
def make_raumzeit(veranstaltung, lang = "de"):    
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
                raum = raum_mit_url(r["_id"])
                # zB Vorlesung: Montag, 8-10 Uhr, HSII, Albertstr. 23a
                if termin['start'] is not None:
                    zeit = f"{str(termin['start'].hour)}{': '+str(termin['start'].minute) if termin['start'].minute > 0 else ''}"
                    if termin['ende'] is not None:
                        zeit = zeit + f"-{str(termin['ende'].hour)}{': '+str(termin['ende'].minute) if termin['ende'].minute > 0 else ''}"
                    zeit = zeit + (" Uhr" if lang == "de" else "h")
                else:
                    zeit = ""
                # zB Mo, 8-10
                tag = weekday[termin['wochentag']]
                # person braucht man, wenn wir dann die Datenbank geupdated haben.
                # person = ", ".join([f"{vvz_person.find_one({"_id": x})["vorname"]} {vvz_person.find_one({"_id": x})["name"]}"for x in termin["person"]])
                kommentar = rf"\newline{termin[f'kommentar_{lang}_html']}" if termin[f'kommentar_{lang}_html'] != "" else ""
                new = [key, tag, zeit, raum, kommentar]
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
    for termin in veranstaltung["einmaliger_termin"]:
        ta = vvz_terminart.find_one({"_id": termin['key']})
        if ta["hp_sichtbar"]:
            ta = ta[f"name_{lang}"]
            # Raum und Gebäude mit Url.
            raeume = list(vvz_raum.find({ "_id": { "$in": termin["raum"]}}))
            raum = ", ".join([raum_mit_url(r["_id"]) for r in raeume])
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
                zeit = f"{str(termin['startzeit'].hour)}{': '+str(termin['startzeit'].minute) if termin['startzeit'].minute > 0 else ''}"
                if termin['endzeit'] is not None:
                    zeit = zeit + f"-{str(termin['endzeit'].hour)}{': '+str(termin['endzeit'].minute) if termin['endzeit'].minute > 0 else ''}"
                zeit = zeit + " Uhr"
            else:
                zeit = ""
            # person braucht man, wenn wir dann die Datenbank geupdated haben.
            # person = ", ".join([f"{vvz_person.find_one({"_id": x})["vorname"]} {vvz_person.find_one({"_id": x})["name"]}"for x in termin["person"]])
            kommentar = rf"{termin[f'kommentar_{lang}_html']}" if termin[f'kommentar_{lang}_html'] != "" else ""
            new = [ta, datum, zeit, raum, kommentar]
            res.append(new)
    res = [f"{x[0]} {(', '.join([z for z in x if z !='' and x.index(z)!=0]))}" for x in res]
    return res

def make_codes(sem_id, veranstaltung_id):
    res = ""
    codekategorie_list = [x["_id"] for x in list(vvz_codekategorie.find({"semester": sem_id, "hp_sichtbar": True}))]
    v = vvz_veranstaltung.find_one({"_id": veranstaltung_id})
    code_list = [vvz_code.find_one({"_id": c, "codekategorie": {"$in": codekategorie_list}}) for c in v["code"]]
    code_list = [x for x in code_list if x is not None]
    if len(code_list)>0:
        res = ", ".join([c["name"] for c in code_list])
    return res

# Falls vpn == True, werden auch nicht sichtbare Semester angezeigt
def get_data(sem_shortname, lang = "de", studiengang = "", modul = "", vpn = False):
    sem_id = vvz_semester.find_one({"kurzname": sem_shortname})["_id"]
    if vpn:
        rubriken = list(vvz_rubrik.find({"semester": sem_id}, sort=[("rang", pymongo.ASCENDING)]))
    else:
        rubriken = list(vvz_rubrik.find({"semester": sem_id, "hp_sichtbar": True}, sort=[("rang", pymongo.ASCENDING)]))
            
    rubriken = list(vvz_rubrik.find({"semester": sem_id, "hp_sichtbar": True}, sort=[("rang", pymongo.ASCENDING)]))

    codekategorie = list(vvz_codekategorie.find({"semester": sem_id, "hp_sichtbar": True}, sort=[("rang", pymongo.ASCENDING)]))
    codes = list(vvz_code.find({"semester": sem_id, "codekategorie": { "$in" : [c["_id"] for c in codekategorie] }}, sort=[("rang", pymongo.ASCENDING)]))
    #print(codes)

    data = {}
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

            query = {"rubrik": rubrik["_id"], "$or" : [{ "verwendbarkeit_modul" : { "$elemMatch" : { "$eq" : m["_id"] }}} for m in mod_list ]}
            if vpn == False:
                query["hp_sichtbar"] = True
            veranstaltungen = list(vvz_veranstaltung.find(query, sort=[("rang", pymongo.ASCENDING)]))
        else:
            if vpn:
                veranstaltungen = list(vvz_veranstaltung.find({"rubrik": rubrik["_id"]}, sort=[("rang", pymongo.ASCENDING)]))                
            else:
                veranstaltungen = list(vvz_veranstaltung.find({"rubrik": rubrik["_id"], "hp_sichtbar" : True}, sort=[("rang", pymongo.ASCENDING)]))
        for veranstaltung in veranstaltungen:
            v_dict = {}
            v_dict["code"] = make_codes(sem_id, veranstaltung["_id"])            
            v_dict["titel"] = veranstaltung[f"name_{lang}"]
            v_dict["kommentar"] = veranstaltung[f"kommentar_html_{lang}"]
            v_dict["link"] = veranstaltung["url"]
            v_dict["dozent"] = ", ".join([vorname_name_mit_url(x) for x in veranstaltung["dozent"]])
            v_dict["assistent"] = ", ".join([vorname_name_mit_url(x) for x in veranstaltung["assistent"]])
            v_dict["organisation"] = ", ".join([vorname_name_mit_url(x) for x in veranstaltung["organisation"]])
            # raumzeit ist der Text, der unter der Veranstaltung steht.
            # print(v_dict["titel"])
            v_dict["raumzeit"] = make_raumzeit(veranstaltung, lang=lang)
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

def get_data_stundenplan(sem_shortname, lang="de"):
    name = f'name_{lang}'
    sem_id = vvz_semester.find_one({"kurzname": sem_shortname})["_id"]
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
                zeit == ""
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
                        "dozent": ", ".join([vorname_name_mit_url(p) for p in v["dozent"]]),
                        "raum":raum_mit_url(t["raum"])
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
                zeit = f"{str(t['startzeit'].hour)}{': '+ str(t['startzeit'].minute) if t['startzeit'].minute > 0 else ''}"
                if t['endzeit'] is not None:
                    zeit = zeit + f"-{str(t['endzeit'].hour)}{': '+str(t['endzeit'].minute) if t['endzeit'].minute > 0 else ''}"
                zeit = zeit + " Uhr"
            else:
                zeit = ""
            termine.append(": ".join([x for x in [ta, ", ".join([x for x in [datum, zeit] if x != ""])] if x != ""]))
    res = (f"<strong>{v[name]}</strong>" if url == "" else f"<strong><a href='{url}'>{v[name]}</a></strong>")
    if termine != []:
        res = res + "<br>" + "; ".join(termine)
    return res

def get_data_personenplan(sem_shortname, lang="de"):
    sem_id = vvz_semester.find_one({"kurzname": sem_shortname})["_id"]
    ver = vvz_veranstaltung.find({"semester" : sem_id})

    data = []
    for v in ver:
        nt = name_termine(v["_id"], lang)
        for p in v["dozent"]:
            data.append({
                "person": f"{name_vorname(p)}",
                "person_mit_url": f"{name_vorname_mit_url(p)}",
                "veranstaltung": nt,
                "rolle": "Dozent*in",
                "sws": [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                })
        for p in v["assistent"]:
            data.append({
                "person": f"{name_vorname(p)}",
                "person_mit_url": f"{name_vorname_mit_url(p)}",
                "veranstaltung": nt,
                "rolle": "Assistent*in",
                "sws": [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                })
            
        for p in v["organisation"]:
            data.append({
                "person": f"{name_vorname(p)}",
                "person_mit_url": f"{name_vorname_mit_url(p)}",
                "veranstaltung": nt,
                "rolle": "Organisation",
                "sws": [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                })

        for t in v["woechentlicher_termin"]:
            for p in t["person"]:
                data.append({
                    "person": f"{name_vorname(p)}",
                    "person_mit_url": f"{name_vorname_mit_url(p)}",
                    "veranstaltung": nt,
                    "rolle": name_terminart(t["key"], lang),
                    "sws": [d["sws"] for d in v["deputat"] if d["person"] == p][0]
                    })
        for t in v["einmaliger_termin"]:
            for p in t["person"]:
                data.append({
                    "person": f"{name_vorname(p)}",
                    "person_mit_url": f"{name_vorname_mit_url(p)}",
                    "veranstaltung": nt,
                    "rolle": name_terminart(t["key"], lang),
                    "sws": [d["sws"] for d in v["deputat"] if d["person"] == p][0]
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

