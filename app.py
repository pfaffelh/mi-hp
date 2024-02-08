from flask import Flask, url_for, render_template
# import markdown
import locale
import logging
import json
import os

app = Flask(__name__)


locale.setlocale(locale.LC_ALL, "de_DE.UTF8") # Deutsche Namen für Tage und Monate

# Configure the logger
log_file_path = 'hp.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler(log_file_path, mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# check if the template is available in the correct language
def files_with_lang(filenames, lang):
    lang = lang.replace("/","")
    print(filenames, lang)
    filenames_with_lang = []
    for filename in filenames:
        loc = lang
        # do nothing if the next if is false in order to reduce errors
        if os.path.exists("templates/de/" + filename) or os.path.exists("templates/en/" + filename):
            if os.path.exists("templates/" + lang + "/" + filename):
                loc = loc
            else:
                if loc == "de":
                    loc = "en"
                else:
                    loc = "de"
            filenames_with_lang.append("/" + loc + "/" + filename)
    return filenames_with_lang

@app.route("/<lang>/")
def showbase(lang):
    filenames = ["index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showbase")

@app.route("/<lang>/allgemeines")
def showallgemeines(lang):
    filenames = files_with_lang(["allgemeines"], lang)
    return render_template("home.html", filenames = filenames, lang=lang, site = "showallgemeines")

@app.route("/<lang>/interesse/prospective/")
def showinterestprospective(lang):
    filenames = []
    filenames = ["interesse/prospective.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showinterestprospective")

@app.route("/<lang>/interesse/start/")
def showintereststart(lang):
    filenames = []
    filenames = ["interesse/studienanfang.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showintereststart")

@app.route("/<lang>/interesse/warum_mathematik/")
def showinterestwarum(lang):
    filenames = []
    filenames = ["interesse/warum_mathematik.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showinterestwarum")

@app.route("/<lang>/interesse/matheinfreiburg/")
def showinterestmatheinfreiburg(lang):
    filenames = []
    filenames = ["interesse/mathestudium_in_freiburg.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showinterestmatheinfreiburg")

@app.route("/<lang>/studiengaenge/bsc_m/")
def showbscm(lang):
    filenames = []
    filenames = ["studiengaenge/bsc-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showbscm")

@app.route("/<lang>/studiengaenge/studienverlauf-bsc-2021/")
def showstudienverlaufbsc(lang):
    filenames = []
    filenames = ["studiengaenge/studienverlauf-bsc-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienverlaufbsc")

@app.route("/<lang>/studiengaenge/studienverlauf-msc-2014/")
def showstudienverlaufmsc(lang):
    filenames = []
    filenames = ["studiengaenge/studienverlauf-msc-2014.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienverlaufmsc")

@app.route("/<lang>/studiengaenge/studienverlauf-2hf-b/")
def showstudienverlauf2hfb(lang):
    filenames = ["studiengaenge/studienverlauf-2hfb-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienverlauf2hfb")


@app.route("/<lang>/studiengaenge/2hfb/")
def show2hfb(lang):
    filenames = ["studiengaenge/2hfb-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "show2hfb")

@app.route("/<lang>/studiengaenge/med/")
def showmed(lang):
    filenames = ["studiengaenge/med-2018.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmed")

@app.route("/<lang>/studiengaenge/studienverlauf-med/")
def showstudienverlaufmed(lang):
    filenames = ["studiengaenge/studienverlauf-med-2018.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienverlaufmed")



@app.route("/<lang>/studiengaenge/med_erw/")
def showmederw(lang):
    filenames = ["studiengaenge/med-erweiterung-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmederw")

@app.route("/<lang>/studiengaenge/msc_m/")
def showmsc(lang):
    filenames = ["studiengaenge/msc-2014.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmsc")

@app.route("/<lang>/studiengaenge/msc_data/")
def showmscdata(lang):
    filenames = ["studiengaenge/msc_data_carousel.html", "studiengaenge/msc_data_info.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmscdata")

@app.route("/<lang>/studiengaenge/med_dual/")
def showmeddual(lang):
    filenames = ["studiengaenge/med_dual.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmeddual")

@app.route("/<lang>/studiengaenge/promotion/")
def showpromotion(lang):
    filenames = ["studiengaenge/promotion.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showpromotion")

@app.route("/<lang>/pruefungsamt/")
def showpruefungsamt(lang):
    filenames = ["pruefungsamt/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showpruefungsamt")

@app.route("/<lang>/pruefungsamt/termine/")
def showtermine(lang):
    filenames = ["pruefungsamt/termine.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showtermine")

@app.route("/<lang>/pruefungsamt/pruefungen/")
def showpruefungen(lang):
    filenames = ["pruefungsamt/pruefungen.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showpruefungen")

@app.route("/<lang>/pruefungsamt/abschlussarbeiten/")
def showabschlussarbeiten(lang):
    filenames = ["pruefungsamt/abschlussarbeiten.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showabschlussarbeiten")

@app.route("/<lang>/pruefungsamt/modulhandbuecher/")
def showmodulhandbuecher(lang):
    filenames = ["pruefungsamt/modulhandbuecher.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmodulhandbuecher")

@app.route("/<lang>/studienberatung/")
def showstudienberatung(lang):
    filenames = ["studienberatung.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienberatung")

@app.route("/<lang>/mediathek/")
def showmediathek(lang):
    filenames = ["mediathek.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmediathek")



@app.route("/<lang>/calendar/")
def showcalendar(lang):
    events = [
    {
        "start": '2024-02-14 10:00:00',
        "end": '2024-02-14 11:00:00',
        "title": 'Dualer Master',
        "description": 'Online-Besprechung',
        "responsible": 'Anna Rosen',
        "backgroundColor": '#ccffcc',
        "striped": True, 
    },
    {
        "start": '2024-02-08 13:00:00',
        "end": '2024-02-08 14:00:00',
        "title": 'Tutoratsvergabe',
        "description": 'n!',
        "responsible": 'Studiendekan',
        "backgroundColor": '#ccffcc'
    },    
    ]
    return render_template("calendar.html", events = events, lang=lang, site = "showcalendar")

