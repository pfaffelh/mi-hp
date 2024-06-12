from flask import Flask, url_for, render_template, redirect, request
# import markdown
import locale
import json
import os
import glob
from bs4 import BeautifulSoup
import requests
from flask import send_file
from flask import make_response
from utils.config import *
#from utils.util_logging import logger
from utils.util_calendar import calendar, get_caldav_calendar_events
from utils.util_faq import get_faq
import utils.fb as fb
from flask_misaka import markdown
from flask_misaka import Misaka
import socket
from datetime import datetime
import utils.util_vvz as vvz
from urllib.request import urlopen 

app = Flask(__name__)
Misaka(app, autolink=True, tables=True)

# This is such that we can use os-commands in jinja2-templates.
@app.context_processor
def handle_context():
    cur = vvz.get_current_semester_kurzname()
    return dict(os=os, 
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

@app.route("/")
@app.route("/<lang>/")
def showbase(lang="de"):
    date_format = '%d.%m.%Y %H:%M'
    with app.open_resource('static/data/home.json') as f:
        data = json.load(f)    
    data['news'] = [item for item in data['news'] if datetime.strptime(item['showhomestart'], date_format) < datetime.now() and datetime.now() < datetime.strptime(item['showhomeend'], date_format)]
    for item in data['news']:
        item['color'] = "bg-ufr-yellow" if datetime.now().date() == datetime.strptime(item['showhomeend'], date_format).date() else "" 
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
    filenames = ["interesse_prefix.html", "interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

@app.route("/<lang>/weiterbildung/")
@app.route("/<lang>/weiterbildung/<anchor>")
def showweiterbildung(lang, anchor=""):
    with app.open_resource('static/data/weiterbildung.json') as f:
        data = json.load(f)
    filenames = ["interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

##########################
## Studienanfänger      ## 
##########################

@app.route("/<lang>/anfang/")
@app.route("/<lang>/anfang/<anchor>")
def showanfang(lang, anchor=""):
    filenames = ["studienanfang.html"]
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
def showstudiengang(lang, studiengang, anchor="kurzbeschreibung"):
    if studiengang == "bsc":
        filenames = ["studiengaenge/bsc/index-2021.html"]
    if studiengang == "msc":
        filenames = ["studiengaenge/msc/index-2014.html"]
    if studiengang == "msc_data":
        filenames = ["studiengaenge/msc_data/index-2024.html"]
    if studiengang == "2hfb":
        filenames = ["studiengaenge/2hfb/index-2021.html"]
    if studiengang == "med":
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
            semester_dict_2[key]["komm_exists"] =False

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
    if semester in [f"{s}s{i}{j}" for s in ["s", "w"] for i in range(3) for j in range(10)]:
        filenames = [f"lehrveranstaltungen/{semester}.html"]
        return render_template("home.html", filenames = filenames, lang=lang, semester=semester)
    else:
        data = vvz.get_data(semester)
        return render_template("lehrveranstaltungen/vvz.html", lang=lang, data = data)


#####################################
## Prüfungsamt und Studienberatung ##
#####################################

@app.route("/<lang>/studiendekanat/")
def showstudiendekanatbase(lang):
    with app.open_resource('static/data/studiendekanat.json') as f:
        data = json.load(f)    
    filenames = ["studiendekanat/index.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)

@app.route("/<lang>/studienberatung/")
def showstudienberatungbase(lang):
    with app.open_resource('static/data/studiendekanat.json') as f:
        data = json.load(f)    
    filenames = ["studiendekanat/studienberatung.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)

@app.route("/<lang>/studienberatung/<unterseite>/")
def showstudienberatung(lang, unterseite):
    if unterseite == "studienanfang":
        filenames = ["studienberatung/studienanfang.html"]
    if unterseite == "schwerpunktgebiete":
        filenames = ["studienberatung/schwerpunktgebiete.html"]
    if unterseite == "warum_mathematik":
        filenames = ["studienberatung/warum_mathematik.html"]
    if unterseite == "matheinfreiburg":
        filenames = ["studienberatung/mathestudium_in_freiburg.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/<lang>/pruefungsamt/")
def showpruefungsamtbase(lang):
    with app.open_resource('static/data/studiendekanat.json') as f:
        data = json.load(f)    
    filenames = ["studiendekanat/pruefungsamt.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)

@app.route("/<lang>/pruefungsamt/<unterseite>")
@app.route("/<lang>/pruefungsamt/<unterseite>/<anchor>")
def showpruefungsamt(lang, unterseite, anchor=""):
    if unterseite == "calendar":
        events = get_caldav_calendar_events(calendar)
        return render_template("pruefungsamt/calendar.html", events=events, lang=lang)
    if unterseite == "anmeldung":
        filenames = ["studiendekanat/anmeldung.html"]
    if unterseite == "modulplan":
        filenames = ["studiendekanat/modulplan.html"]
    if unterseite == "belegung":
        filenames = ["studiendekanat/belegung.html"]
    if unterseite == "termine":
        filenames = ["pruefungsamt/termine.html"]
    if unterseite == "modulhandbuecher":
        filenames = ["pruefungsamt/modulhandbuecher.html"]    
    if unterseite == "ausland":
        filenames = ["pruefungsamt/modulhandbuecher.html"]    
#    filenames = []
    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

#########
## faq ##
#########

# which can Werte 'all', 'bsc', '2hfb', 'msc', 'mscdata', 'med', 'mederw', 'meddual' annehmen
# show ist entweder "", oder "alleantworten", oder der kurzname für eine category im FAQ
# anchor ist entweder "", oder eine id für ein qa-Paar
@app.route("/<lang>/faq/")
@app.route("/<lang>/faq/<which>/")
@app.route("/<lang>/faq/<which>/<show>/<anchor>/")
def showfaq(lang, which = "all", show = "", anchor =""):
    try:
        cats_kurzname, names_dict, qa_pairs = get_faq(lang)
    except:
#        logger.warning("No connection to database")
        cats_kurzname, names_dict, qa_pairs  = ["unsichtbar"], {"unsichtbar": "Unsichtbar"}, {"unsichtbar": []}

    return render_template("faq.html", lang=lang, cats_kurzname = cats_kurzname, names_dict = names_dict, qa_pairs = qa_pairs, which=which, show = show, studiengaenge = studiengaenge, anchor=anchor)

###############
## Downloads ##
###############

@app.route("/<lang>/downloads/")
@app.route("/<lang>/downloads/<anchor>")
def showdownloads(lang, anchor=""):
    filenames = ["downloads.html"]
    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

#################
## Monitor EG  ##
#################

@app.route("/monitor/")
def showmonitor():

    with app.open_resource('static/data/home.json') as f:
        data = json.load(f)    
    date_format = '%d.%m.%Y %H:%M'
    data['carouselmonitor'] = [item for item in data['carouselmonitor'] if datetime.strptime(item['showstart'], date_format) < datetime.now() and datetime.now() < datetime.strptime(item['showend'], date_format)]

    # Fußball EM 2024
    if datetime(2024,6,14) < datetime.now() and datetime.now() < datetime(2024,7,15):
        url = "https://api.openligadb.de/getmatchdata/em/2024/"
        date = datetime.now().date()
#        date = datetime(2024, 6, 29).date()
        data['carouselmonitor'].append(
                {
                "interval": "7000",
                "image": "/static/images/fussball.jpeg",
                "left": "5%",
                "right": "40%",
                "bottom": "20%",
                "text": fb.get_openligadb_text(url, date, 0)
                },
        )

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

    data['news'] = [item for item in data['news'] if datetime.strptime(item['showmonitorstart'], date_format) < datetime.now() and datetime.now() < datetime.strptime(item['showmonitorend'], date_format)]
    for item in data['news']:
        item['today'] = True if datetime.now().date() == datetime.strptime(item['showmonitorend'], date_format).date() else False
    filenames = ["monitor_quer.html"]
    return render_template("monitor_quer.html", data=data, filenames = filenames, lang="de")


