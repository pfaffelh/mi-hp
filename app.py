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
from utils.util_logging import logger
# from utils.util_calendar import calendar, get_caldav_calendar_events
from utils.util_faq import get_faq
from flask_misaka import markdown
from flask_misaka import Misaka

app = Flask(__name__)
Misaka(app)

# This function is important for changing languages; see base.html. Within a template, we can use its own endpoint, i.e. all parameters it was given. 
# For changin languages, we are then able to only change the lang-parameter.
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
    filenames = ["index.html"]
    return render_template("home.html", filenames=filenames, lang=lang)

############
## footer ##
############

@app.route("/<lang>/impressum/")
def showimpressum(lang):
    filenames = ["footer/impressum.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/<lang>/datenschutz/")
def showdatenschutz(lang):
    filenames = ["footer/datenschutz.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

###################
## Studiengaenge ##
###################

@app.route("/<lang>/studiengaenge/")
@app.route("/<lang>/studiengaenge/<anchor>")
def showstudiengaenge(lang, anchor="aktuell"):
    filenames = ["studiengaenge/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor=anchor)
navbar=True
@app.route("/<lang>/studiengaenge/<studiengang>/")
@app.route("/<lang>/studiengaenge/<studiengang>/<anchor>")
def showstudiengang(lang, studiengang, anchor="kurzbeschreibung"):
    if studiengang == "bsc":
        filenames = ["studiengaenge/bsc/index-2021.html"]
    if studiengang == "msc":
        filenames = ["studiengaenge/msc/index-2014.html"]
    if studiengang == "msc_data":
#        navbar = False
        filenames = ["studiengaenge/msc_data/index-2024.html"]
    if studiengang == "2hfb":
        filenames = ["studiengaenge/2hfb/index-2021.html"]
    if studiengang == "med":
        filenames = ["studiengaenge/med/index-2018.html"]
    if studiengang == "med_erw":
        filenames = ["studiengaenge/med_erw/index-2021.html"]
    if studiengang == "promotion":
        filenames = ["studiengaenge/promotion/index.html"]
    return render_template("home.html", filenames=filenames, lang=lang, studiengang=studiengang, anchor=anchor)#, navbar = navbar)

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

#####################
## Studienberatung ##
#####################

@app.route("/<lang>/studienberatung/")
def showstudienberatungbase(lang):
    filenames = ["studienberatung/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

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

##########################
## Studieninteressierte ## 
##########################

@app.route("/<lang>/interesse/")
@app.route("/<lang>/interesse/<anchor>")
def showinteresse(lang, anchor="schueler"):
    filenames = ["interesse.html"]
    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

#################
## Prüfungsamt ##
#################

@app.route("/<lang>/pruefungsamt/")
def showpruefungsamtbase(lang):
    filenames = ["pruefungsamt/index.html"]
    return render_template("home.html", filenames=filenames, lang=lang)

@app.route("/<lang>/pruefungsamt/<unterseite>")
def showpruefungsamt(lang, unterseite):
    if unterseite == "calendar":
        events = "" # get_caldav_calendar_events(calendar)
        return render_template("pruefungsamt/calendar.html", events=events, lang=lang)
    if unterseite == "termine":
        filenames = ["pruefungsamt/index.html"]
    if unterseite == "formulare":
        filenames = ["pruefungsamt/formulare.html"]
    if unterseite == "modulhandbuecher":
        filenames = ["pruefungsamt/modulhandbuecher.html"]    
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
        logger.warning("No connection to database")
        cats_kurzname, names_dict, qa_pairs  = ["unsichtbar"], {"unsichtbar": "Unsichtbar"}, {"unsichtbar": []}

    return render_template("faq.html", lang=lang, cats_kurzname = cats_kurzname, names_dict = names_dict, qa_pairs = qa_pairs, which=which, show = show, studiengaenge = studiengaenge)

#########################
## Lehrveranstaltungen ##
#########################

@app.route("/<lang>/lehrveranstaltungen/")
def showlehrveranstaltungenbase(lang="de"):
    filenames = ["lehrveranstaltungen/index.html"]
    return render_template("home.html", filenames=filenames, lang=lang, semester_dict=semester_dict)

@app.route("/<lang>/lehrveranstaltungen/<semester>/")
def showlehrveranstaltungen(lang, semester):
    print(semester)
    url = f"https://www.math.uni-freiburg.de/lehre/v/{semester}.html"
    result = requests.get(url, verify=False)
    soup = BeautifulSoup(result.text, 'lxml')
    content = soup.find('div', id="inhalt")
    content['class'] = "container"
    filenames = [f"lehrveranstaltungen/{semester}.html"]    
    with open("mi-hp/templates/"+filenames[0], "w") as file:
        file.write(content.prettify())
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

###############
## Mediathek ##
###############

@app.route("/<lang>/mediathek/")
def showmediathek(lang):
    filenames = ["mediathek.html"]
    return render_template("home.html", filenames=filenames, lang=lang)



