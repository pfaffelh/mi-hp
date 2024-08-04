from flask import Flask, url_for, render_template, redirect, request
import locale
import json
import os
from bs4 import BeautifulSoup
import requests
from utils.config import *
from utils.util_logging import logger
from utils.util_calendar import calendar, get_caldav_calendar_events

import utils.util_faq as util_faq

import utils.fb as fb
from flask_misaka import Misaka
import socket
from datetime import datetime
import utils.util_vvz as vvz
import utils.util_news as news
import xmltodict
import base64
import pymongo
from bson import ObjectId

app = Flask(__name__)
Misaka(app, autolink=True, tables=True, math= True, math_explicit = True)

# This is such that we can use os-commands in jinja2-templates.
@app.context_processor
def handle_context():
    cur = vvz.get_current_semester_kurzname()
    showanmeldung = {
        "bsc": vvz.get_showanmeldung("bsc"), 
        "msc": vvz.get_showanmeldung("msc"),
        "mscdata": vvz.get_showanmeldung("mscdata")
        }
    return dict(os=os, 
                showanmeldung = showanmeldung, 
                laufendes_semester = cur,
                kommendes_semester = vvz.next_semester_kurzname(cur),
                show_laufendes_semester = vvz.get_showsemester(cur), 
                show_kommendes_semester = vvz.get_showsemester(vvz.next_semester_kurzname(cur)))

# This function is important for changing languages; see base.html. Within a template, we can use its own endpoint, i.e. all parameters it was given. 
# For changing languages, we are then able to only change the lang-parameter.
def url_for_self(**args):
    return url_for(request.endpoint, **dict(request.view_args, **args))

# This is for using the last function within a jinja2 template. 
app.jinja_env.globals['url_for_self'] = url_for_self

# Deutsche Namen für Tage und Monate
locale.setlocale(locale.LC_ALL, "de_DE.UTF8") 

###############
## Home page ##
###############

@app.route("/test/")
@app.route("/test/<lang>/")
@app.route("/test/<lang>/<dtstring>")
@app.route("/")
@app.route("/<lang>/")
@app.route("/<lang>/<dtstring>")
def showbase(lang="de", dtstring = datetime.now().strftime('%Y%m%d%H%M')):
    testorpublic = "_public" if request.endpoint.split(".")[0] == 'monitor' else "test"
    date_format_no_space = '%Y%m%d%H%M'
    dt = datetime.strptime(dtstring, date_format_no_space)

    data = {}
    if testorpublic == "test":
        data["news"] =  list(news.news.find({ "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }},sort=[("rang", pymongo.ASCENDING)]))
    else:
        data["news"] =  list(news.news.find({ "_public": True, "home.start" : { "$lte" : dt }, "home.end" : { "$gte" : dt }}))        
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(news.bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = True if (item["showlastday"] and dt.date() == item['home']['end'].date()) else False

    filenames = ["index.html"]
    return render_template("home.html", filenames=filenames, data = data, lang=lang)


############
## footer ##
############

@app.route("/<lang>/bildnachweis/")
def showbildnachweis(lang):
    with app.open_resource('static/data/bildnachweis.json') as f:
        data = json.load(f)    
    filenames = ["footer/bildnachweis.html"]
    return render_template("home.html", filenames = filenames, data = data, lang=lang)

@app.route("/<lang>/impressum/")
def showimpressum(lang):
    filenames = ["footer/impressum.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/<lang>/datenschutz/")
def showdatenschutz(lang):
    filenames = ["footer/datenschutz.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/<lang>/tools")
def showtools(lang):
    filenames = ["footer/tools.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

##########################
## Studieninteressierte ## 
##########################

@app.route("/<lang>/interesse/")
@app.route("/<lang>/interesse/<anchor>")
def showinteresse(lang, anchor=""):
    with app.open_resource('static/data/interesse.json') as f:
        data = json.load(f)
    filenames = ["studieninteresse/interesse_prefix.html", "studieninteresse/interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

@app.route("/<lang>/weiterbildung/")
@app.route("/<lang>/weiterbildung/<anchor>")
def showweiterbildung(lang, anchor=""):
    with app.open_resource('static/data/weiterbildung.json') as f:
        data = json.load(f)
    filenames = ["studieninteresse/interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

##########################
## Studienanfänger      ## 
##########################

@app.route("/<lang>/anfang/")
@app.route("/<lang>/anfang/<anchor>")
def showanfang(lang, anchor=""):
    filenames = ["studienanfang/studienanfang.html"]
    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

###################
## Studiengaenge ##
###################

@app.route("/<lang>/studiengaenge/")
@app.route("/<lang>/studiengaenge/<anchor>")
def showstudiengaenge(lang, anchor="aktuell"):
    filenames = ["studiengaenge/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor=anchor)

@app.route("/<lang>/studiengaenge/<anchor>")
@app.route("/<lang>/studiengaenge/<studiengang>/")
@app.route("/<lang>/studiengaenge/<studiengang>/<anchor>")
def showstudiengang(lang, studiengang, anchor=""):
    if studiengang == "bsc":
        filenames = ["studiengaenge/bsc/index-2021.html"]
    if studiengang == "msc":
        filenames = ["studiengaenge/msc/index-2014.html"]
    if studiengang == "msc_data":
        filenames = ["studiengaenge/msc_data/index-2024.html"]
    if studiengang == "2hfb":
        filenames = ["studiengaenge/2hfb/index-2021.html"]
    if studiengang == "med":
        # anchor kann sein:
        # kurz, zulassung, dokumente, studienverlauf, modulplan
        filenames = ["studiengaenge/med/index-2018.html"]
    if studiengang == "med_erw":
        filenames = ["studiengaenge/med_erw/index-2021.html"]
    if studiengang == "promotion":
        filenames = ["studiengaenge/promotion/index.html"]
    return render_template("home.html", filenames=filenames, lang=lang, studiengang=studiengang, anchor=anchor)

@app.route("/<lang>/studiengaenge/<studiengang>/news/")
def showstudiengangnews(lang, studiengang):
    if studiengang == "msc_data":
        filenames = ["studiengaenge/msc_data/carousel.html", "studiengaenge/msc_data/news.html"]
    if studiengang == "med_dual":
        filenames = ["studiengaenge/med_dual/index-2024.html"]
    return render_template("home.html", filenames=filenames, lang=lang)

@app.route("/<lang>/studiengaenge/<studiengang>/verlauf/")
def showstudienverlauf(lang, studiengang):
    if studiengang == "bsc":
        filenames = ["studiengaenge/studienverlauf-bsc-2021.html"]
    if studiengang == "bscb":
        filenames = ["studiengaenge/studienverlauf-bsc-2021b.html"]
    if studiengang == "msc":
        filenames = ["studiengaenge/studienverlauf-msc-2014.html"]       
    if studiengang == "2hfb":
        filenames = ["studiengaenge/studienverlauf-2hfb-2021.html"]       
    if studiengang == "med":
        filenames = ["studiengaenge/studienverlauf-med-2018.html"]       
    return render_template("home.html", filenames = filenames, studiengang=studiengang, lang=lang)


#########################
## Lehrveranstaltungen ##
#########################

@app.route("/<lang>/lehrveranstaltungen/")
def showlehrveranstaltungenbase(lang="de"):
    filenames = ["lehrveranstaltungen/index.html"]
    a = [x["kurzname"] for x in list(vvz.vvz_semester.find({"hp_sichtbar": True}))]
    b = ["2024WS"] + [f"20{x}{s}S" for x in range(25,100) for s in ["S", "W"]]
#    b = ["2018WS"] + [f"20{x}{s}S" for x in range(19,100) for s in ["S", "W"]]
    acapb = [x for x in a if x in b]
    acapb.reverse()
    if lang == "de":
        semester_dict_2 = { x : {"name": vvz.semester_name_de(x)} for x in acapb }
    else:
        semester_dict_2 = { x : {"name": vvz.semester_name_en(x)} for x in acapb }
    semester_dict_2.update(semester_dict)

    for key, value in semester_dict_2.items():
        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'.pdf')
            semester_dict_2[key]["komm_exists"] = True
        except:
            semester_dict_2[key]["komm_exists"] = False

        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'mh.pdf')
            semester_dict_2[key]["mh_exists"] = True
        except:
            semester_dict_2[key]["mh_exists"] =False

        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'verw.pdf')
            semester_dict_2[key]["verw_exists"] = True
        except:
            semester_dict_2[key]["verw_exists"] =False

    return render_template("home.html", filenames=filenames, lang=lang, semester_dict=semester_dict_2, semester_dict_old=semester_dict_old)

@app.route("/<lang>/lehrveranstaltungen/<semester>/")
def showlehrveranstaltungen(lang, semester):
    if semester in [f"{s}s{i}{j}" for s in ['s', 'w'] for i in range(3) for j in range(10)]:
        filenames = [f"lehrveranstaltungen/{semester}.html"]
        return render_template("home.html", filenames = filenames, lang=lang, semester=semester)
    else:
        data = vvz.get_data(semester)
        return render_template("lehrveranstaltungen/vvz.html", lang=lang, data = data)


#####################################
## Prüfungsamt und Studienberatung ##
#####################################

#@app.route("/<lang>/studiendekanat/")
#def showstudiendekanatbase(lang):
#    with app.open_resource('static/data/studiendekanat.json') as f:
#        data = json.load(f)    
#    filenames = ["studiendekanat/index.html"]
#    return render_template("home.html", data=data, filenames = filenames, lang=lang)

# which can Werte 'all', 'bsc', '2hfb', 'msc', 'mscdata', 'med', 'mederw', 'meddual' annehmen
# show ist entweder "", oder "all" oder eine id für ein qa-Paar
@app.route("/<lang>/studiendekanat/faq/")
@app.route("/<lang>/studiendekanat/faq/<show>")
def showstufaq(lang, show =""):
    try:
        cat_ids, names_dict, qa_pairs = util_faq.get_stu_faq(lang)
    except:
        logger.warning("No connection to database")
        cat_ids, names_dict, qa_pairs  = ["unsichtbar"], {"unsichtbar": "Unsichtbar"}, {"unsichtbar": []}
    if show == "":
        showcat = ""
    elif show == "all":
        showcat = "all"
    else:
        showcat = util_faq.get_stu_cat(show)
    return render_template("studiendekanat/index.html", lang=lang, cat_ids = cat_ids, names_dict = names_dict, qa_pairs = qa_pairs, showcat = showcat, studiengaenge = studiengaenge, show=show)

@app.route("/<lang>/studiendekanat/")
@app.route("/<lang>/studiendekanat/<unterseite>/")
def showstudiendekanat(lang, unterseite = ""):
    data = {}
    if unterseite == "":
        try:
            cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
            mongo_db_faq = cluster["faq"]
            studiendekanat = mongo_db_faq["studiendekanat"]
        except:
            logger.warning("No connection to Database FAQ")

        data = list(studiendekanat.find({"showstudienberatung" : True}, sort=[("rang", pymongo.ASCENDING)]))
        filenames = ["studiendekanat/studienberatung.html"]
    if unterseite == "pruefungsamt":
        try:
            cluster = pymongo.MongoClient("mongodb://127.0.0.1:27017")
            mongo_db_faq = cluster["faq"]
            studiendekanat = mongo_db_faq["studiendekanat"]
        except:
            logger.warning("No connection to Database FAQ")
        data = list(studiendekanat.find({"showpruefungsamt" : True}, sort=[("rang", pymongo.ASCENDING)]))
        print(data)
        filenames = ["studiendekanat/pruefungsamt.html"]        
    if unterseite == "studienanfang":
        filenames = ["studiendekanat/studienanfang.html"]
    if unterseite == "schwerpunktgebiete":
        filenames = ["studiendekanat/schwerpunktgebiete.html"]
    if unterseite == "warum_mathematik":
        filenames = ["studiendekanat/warum_mathematik.html"]
    if unterseite == "matheinfreiburg":
        filenames = ["studiendekanat/mathestudium_in_freiburg.html"]
    if unterseite == "termine":
        filenames = ["studiendekanat/termine.html"]
    if unterseite == "calendar":
        events = get_caldav_calendar_events(calendar)
        return render_template("studiendekanat/calendar.html", events=events, lang=lang)
    if unterseite == "anmeldung":
        filenames = ["studiendekanat/anmeldung.html"]
    if unterseite == "modulplan":
        filenames = ["studiendekanat/modulplan.html"]
    if unterseite == "termine":
        filenames = ["studiendekanat/termine.html"]
    if unterseite == "modulhandbuecher":
        filenames = ["studiendekanat/modulhandbuecher.html"]    
    if unterseite == "ausland":
        filenames = ["studiendekanat/ausland.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)


#####################################
## Für Lehrende ##
#####################################

# show ist entweder "", oder "all" oder eine id für ein qa-Paar
@app.route("/<lang>/intern/")
@app.route("/<lang>/intern/faq/")
@app.route("/<lang>/intern/faq/<show>")
def showmitfaq(lang, show =""):
    try:
        cat_ids, names_dict, qa_pairs = util_faq.get_mit_faq(lang)
    except:
#        logger.warning("No connection to database")
        cat_ids, names_dict, qa_pairs  = ["unsichtbar"], {"unsichtbar": "Unsichtbar"}, {"unsichtbar": []}
    if show == "":
        showcat = ""
    elif show == "all":
        showcat = "all"
    else:
        showcat = util_faq.get_mit_cat(show)
    return render_template("lehrende/index.html", lang=lang, cat_ids = cat_ids, names_dict = names_dict, qa_pairs = qa_pairs, showcat = showcat, studiengaenge = studiengaenge, show=show)



###############
## Downloads ##
###############

@app.route("/<lang>/downloads/")
@app.route("/<lang>/downloads/<anchor>")
def showdownloads(lang, anchor=""):
    filenames = ["downloads/downloads.html"]
    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

#################
## Monitor EG  ##
#################

def get_mensaplan_text(url, date):
    response = requests.get(url)
    if response.status_code == 200:
        mensaplan_xml = response.text
        mensaplan = xmltodict.parse(mensaplan_xml)
        date_format = '%d.%m.%Y'
        tagesplan = mensaplan["plan"]["ort"]["tagesplan"]
        tagesplan = [t["menue"] for t in tagesplan if t["@datum"] == datetime.now().strftime('%d.%m.%Y')]
        print(tagesplan)
        if tagesplan != []:
            tagesplan = tagesplan[0]
            ausgabe = f"<h2>Mensaplan am {date.strftime('%d.%m.')}</h2>"
            # Abendessen wird nicht ausgegeben
            for t in [t for t in tagesplan if t["@art"][0:10] != "Abendessen"]: 
                art = t["@art"]
                name = t["name"]
                if len(t["name"]) > 60:
                    name = name[0:59] + "..."
                ausgabe = ausgabe + f"<h4>{art}: {name}</h4>"
        else:
            ausgabe = "<h2>Heute ist die Mensa zu!</h2>"
    else: 
        ausgabe = ""
    return ausgabe

@app.route("/monitor/")
@app.route("/monitortest/")
@app.route("/monitor/<dtstring>")
@app.route("/monitortest/<dtstring>")
def showmonitor(dtstring = datetime.now().strftime('%Y%m%d%H%M')):
    # determine if only shown on test
    testorpublic = "_public" if request.endpoint.split(".")[0] == 'monitor' else "test"
    # the date format for <dtstring>
    date_format_no_space = '%Y%m%d%H%M'
    dt = datetime.strptime(dtstring, date_format_no_space)

    data = {}
    # Daten für das Carousel
    if testorpublic == "test":
        data["carouselnews"] = list(news.carouselnews.find({"start" : { "$lte" : dt }, "end" : { "$gte" : dt }}))
    else:
        data["carouselnews"] = list(news.carouselnews.find({"_public" :True, "start" : { "$lte" : dt }, "end" : { "$gte" : dt }}))        

    for item in data["carouselnews"]:
        item["image"] = base64.b64encode(news.bild.find_one({ "_id": item["image_id"]})["data"]).decode()#.encode('base64')
        print((item["image"][0:100]))

    # Daten für die News
    if testorpublic == "test":
        data["news"] =  list(news.news.find({ "monitor.start" : { "$lte" : dt }, "monitor.end" : { "$gte" : dt }}))
    else:
        data["news"] =  list(news.news.find({ "_public": True, "monitor.start" : { "$lte" : dt }, "monitor.end" : { "$gte" : dt }}))        
    for item in data["news"]:
        if item["image"] != []:
            item["image"][0]["data"] = base64.b64encode(news.bild.find_one({ "_id": item["image"][0]["_id"]})["data"]).decode()#.toBase64()#.encode('base64')

    for item in data['news']:
        item['today'] = True if (item["showlastday"] and dt.date() == item['monitor']['end'].date()) else False
 
    return render_template("monitor/monitor_quer.html", data=data, lang="de")

# Wetter vom DWD

#    data['carouselmonitor'].append(
#            {
#            "interval": "7000",
#            "image": "https://morgenwirdes.de/api/v3/minimet.php?plz=79104",
#            "left": "5%",
#            "right": "40%",
#            "bottom": "20%",
#            "text": "",
#            "style": "max-height: 10vw; object-fit: cover",
#            },
#   )

#    data['carouselmonitor'].append(
#            {
#            "interval": "7000",
#            "image": "https://morgenwirdes.de/api/v3/gif6.php?plz=79104&delay=70&type=1&zoomlvl=3&bar=1&map=0&textcol=ffffff&bgcol=8393c9",
#            "left": "5%",
#            "right": "40%",
#            "bottom": "20%",
#            "text": "",
#            "style": "height: 10vw; object-fit: contain",
#            },
#   )

# Mensaplan
#    date = datetime(2024, 6, 24).date()
#    date = dt.date()
#    if dt.hour < 14:
#        text = "" # get_mensaplan_text(mensaplan_url, date)
#        if text != "":
#            data['carouselmonitor'].append(
#                        {
#                        "interval": "15000",
#                        "image": "/static/images/buffet.jpg",
#                        "left": "15%",
#                        "right": "15%",
#                        "bottom": "50%" if text == "<h2>Heute ist die Mensa zu!</h2>" else "2%",
#                        "text": text
#                        }
#                )

#    os.system('textimg -i "$(curl de.wttr.in/Freiburg?1pQ | tail -n 20 -q | head -n 18 -q)" -o static/images/wetter.png')
#    os.system("convert static/images/wetter.png -resize 2000x500 static/images/wetter_cropped.png")
#    data['carouselmonitor'].append(
#            {
#            "interval": "7000",
#            "image": "/static/images/wetter_cropped.png",
#            "left": "5%",
#            "right": "40%",
#            "bottom": "20%",
#            "text": ""
#            },
#    )

