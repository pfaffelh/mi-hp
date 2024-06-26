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
from flask_misaka import markdown
from flask_misaka import Misaka
import json
import socket
from datetime import datetime

app = Flask(__name__)
Misaka(app)

# This is such that we can use os-commands in jinja2-templates.
@app.context_processor
def handle_context():
    return dict(os=os)

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
    data = json.load(open(home))
    filenames = ["index.html"]
    return render_template("home.html", filenames=filenames, data = data, lang=lang)

############
## footer ##
############

@app.route("/<lang>/bildnachweis/")
def showbildnachweis(lang):
    data = json.load(open(os.path.abspath(bildnachweis)))
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

##########################
## Studieninteressierte ## 
##########################

@app.route("/<lang>/interesse/")
@app.route("/<lang>/interesse/<anchor>")
def showinteresse(lang, anchor=""):
#    filenames = ["interesse.html"]
    data = json.load(open(interesse))
    filenames = ["interesse_prefix.html", "interesse_content.html"]
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
    return render_template("home.html", filenames=filenames, lang=lang, semester_dict=semester_dict, semester_dict_old=semester_dict_old)

@app.route("/<lang>/lehrveranstaltungen/<semester>/")
def showlehrveranstaltungen(lang, semester):
    filenames = [f"lehrveranstaltungen/{semester}.html"]    
    return render_template("home.html", filenames = filenames, lang=lang, semester=semester)

@app.route("/<lang>/lehrveranstaltungen/pdf/<semester>/")
def sendlehrveranstaltungen(semester, lang="de"):
    response = None
    path = os.path.relpath(f"mi-hp/templates/lehrveranstaltungen/pdf/{semester}.pdf")    
    path = os.path.abspath(path)
    print(path)
    print(os.path.exists(path))
    if os.path.exists(path):        
        response = send_file(path)
        print(path)
        return response
    return make_response("not found", 404)

# Ergänzungen zu den Modulhandbüchern
@app.route("/<lang>/lehrveranstaltungen/pdf/mh/<semester>/")
def sendlehrveranstaltungen_mh(semester, lang="de"):
    response = None
    path = os.path.relpath(f"mi-hp/templates/lehrveranstaltungen/pdf/{semester}mh.pdf")    
    path = os.path.abspath(path)
    print(path)
    print(os.path.exists(path))
    if os.path.exists(path):        
        response = send_file(path)
        print(path)
        return response
    return make_response("not found", 404)

# Verwendbarkeitstabellen
@app.route("/<lang>/lehrveranstaltungen/pdf/verw/<semester>/")
def sendlehrveranstaltungen_verw(semester, lang="de"):
    response = None
    path = os.path.relpath(f"mi-hp/templates/lehrveranstaltungen/pdf/{semester}verw.pdf")    
    path = os.path.abspath(path)
    print(path)
    print(os.path.exists(path))
    if os.path.exists(path):        
        response = send_file(path)
        print(path)
        return response
    return make_response("not found", 404)

@app.route("/<lang>/lehrveranstaltungen/aktuelles/")
def showlehrveranstaltungenaktuelles(lang):
    return redirect(url_for('showlehrveranstaltungen', lang=lang, semester=aktuelles[0]))

@app.route("/<lang>/lehrveranstaltungen/kommendes/")
def showlehrveranstaltungenkommendes(lang):
    return redirect(url_for('showlehrveranstaltungen', lang=lang, semester=kommendes[0]))


#####################################
## Prüfungsamt und Studienberatung ##
#####################################

@app.route("/<lang>/studiendekanat/")
def showstudiendekanatbase(lang):
    data = json.load(open(studiendekanat))
    filenames = ["studiendekanat/index.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)

@app.route("/<lang>/studienberatung/")
def showstudienberatungbase(lang):
    data = json.load(open(studiendekanat))
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
    data = json.load(open(studiendekanat))
    filenames = ["studiendekanat/pruefungsamt.html"]
    return render_template("home.html", data=data, filenames = filenames, lang=lang)


@app.route("/<lang>/pruefungsamt/<unterseite>")
def showpruefungsamt(lang, unterseite):
    if unterseite == "calendar":
        events = get_caldav_calendar_events(calendar)
        return render_template("pruefungsamt/calendar.html", events=events, lang=lang)
    if unterseite == "anmeldung":
        filenames = ["studiendekanat/anmeldung.html"]
    if unterseite == "termine":
        filenames = ["pruefungsamt/termine.html"]
    if unterseite == "modulhandbuecher":
        filenames = ["pruefungsamt/modulhandbuecher.html"]    
    if unterseite == "ausland":
        filenames = ["pruefungsamt/modulhandbuecher.html"]    
#    filenames = []
    return render_template("home.html", filenames=filenames, lang=lang)

#########
## faq ##
#########

# which can Werte 'all', 'bsc', '2hfb', 'msc', 'mscdata', 'med', 'mederw', 'meddual' annehmen
# show ist entweder "", oder "alleantworten", oder der kurzname für eine category im FAQ
@app.route("/<lang>/faq/")
@app.route("/<lang>/faq/<which>/")
@app.route("/<lang>/faq/<which>/<show>/")
def showfaq(lang, which = "all", show = ""):
    try:
        cats_kurzname, names_dict, qa_pairs = get_faq(lang)
    except:
#        logger.warning("No connection to database")
        cats_kurzname, names_dict, qa_pairs  = ["unsichtbar"], {"unsichtbar": "Unsichtbar"}, {"unsichtbar": []}

    return render_template("faq.html", lang=lang, cats_kurzname = cats_kurzname, names_dict = names_dict, qa_pairs = qa_pairs, which=which, show = show, studiengaenge = studiengaenge)

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
#   data = json.load(open(os.path.abspath("/usr/local/lib/mi-hp/home.json")))
#   with app.open_resource('/static/data/home.json') as f:
#        data = json.load(f)

    data = json.load(open(os.path.abspath(home)))
    data['carouselmonitor'] = [item for item in data['carouselmonitor'] if item['show']]
    data['news'] = [item for item in data['news'] if item['showmonitor']]
    filenames = ["monitor.html"]
    return render_template("monitor.html", data=data, filenames = filenames, lang="de")

def get_semester(date):
    # In 2024, the next line gives 24
    y = datetime.now().year-2000
    m = datetime.now().month
    if m <= 3:
        current_semester = f"ws{y-1}{y}"
        upcoming_semester = f"ss{y}"
    elif m <= 9:
        current_semester = f"ss{y}"
        upcoming_semester = f"ws{y}{y+1}"
    else:
        current_semester = f"ws{y}{y+1}"
        upcoming_semester = f"ss{y+1}"
    return current_semester, upcoming_semester

