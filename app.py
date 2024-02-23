from flask import Flask, url_for, render_template, redirect, request
# import markdown
import locale
import logging
import json
import os
import glob
from bs4 import BeautifulSoup
import requests
from flask import send_file
from flask import make_response

app = Flask(__name__)

locale.setlocale(locale.LC_ALL, "de_DE.UTF8") # Deutsche Namen für Tage und Monate

# Configure the logger
log_file_path = 'hp.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(log_file_path, mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logging.warning('Watch out!')


kommendes = ("ss24", "Sommersemester 2024")
aktuelles = ("ws2324", "Wintersemester 2023/24")
semester = {
    "ss24": "Sommersemester 2024",
    "ws2324": "Wintersemester 2023/24",
    "ss23": "Sommersemester 2023",
    "ws2223": "Wintersemester 2022/23",
    "ss22": "Sommersemester 2023",
    "ws2121": "Wintersemester 2022/23",
    "ss21": "Sommersemester 2023",
    "ws2021": "Wintersemester 2022/23",
    "ss20": "Sommersemester 2023",
    "ws1920": "Wintersemester 2022/23",
    "ss19": "Sommersemester 2023",
    "ws1819": "Wintersemester 2022/23"
}

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

############
## footer ##
############

@app.route("/<lang>/impressum")
def showimpressum(lang):
    filenames = ["footer/impressum.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showimpressum")

@app.route("/<lang>/datenschutz")
def showdatenschutz(lang):
    filenames = ["footer/datenschutz.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showdatenschutz")


#####################
## Studienberatung ##
#####################

@app.route("/<lang>/studienberatung/")
def showstudienberatung(lang):
    filenames = ["studienberatung/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienberatung")

@app.route("/<lang>/studienberatung/schwerpunktgebiete/")
def showstudienberatungschwerpunktgebiete(lang):
    filenames = []
    filenames = ["studienberatung/schwerpunktgebiete.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienberatungschwerpunktgebiete")

@app.route("/<lang>/studienberatung/studienanfang/")
def showstudienberatungstudienanfang(lang):
    filenames = []
    filenames = ["studienberatung/studienanfang.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showstudienberatungstudienanfang")

@app.route("/<lang>/studienberatung/warum_mathematik/")
def showinterestwarum(lang):
    filenames = []
    filenames = ["studienberatung/warum_mathematik.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showinterestwarum")

@app.route("/<lang>/studienberatung/matheinfreiburg/")
def showinterestmatheinfreiburg(lang):
    filenames = []
    filenames = ["studienberatung/mathestudium_in_freiburg.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showinterestmatheinfreiburg")

##########################
## Studieninteressierte ## 
##########################

@app.route("/<lang>/interesse/")
@app.route("/<lang>/interesse/<anchor>")
def showinteresse(lang, anchor="schueler"):
    filenames = ["interesse.html"]
    return render_template("home.html", filenames = filenames, anchor = anchor, lang=lang, site = "showinteresse")

@app.route("/<lang>/studiengaenge/bsc/")
def showbsc(lang):
    filenames = []
    filenames = ["studiengaenge/bsc/index-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showbsc")

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

## Studiengaenge

@app.route("/<lang>/studiengaenge/")
@app.route("/<lang>/studiengaenge/<anchor>")
def showstudiengaenge(lang, anchor="aktuell"):
    filenames = ["studiengaenge/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showstudiengaenge")

@app.route("/<lang>/studiengaenge/2hfb/")
@app.route("/<lang>/studiengaenge/2hfb/<anchor>")
def show2hfb(lang, anchor="kurzbeschreibung"):
    filenames = ["studiengaenge/2hfb/index-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "show2hfb")
@app.route("/<lang>/studiengaenge/med/")
@app.route("/<lang>/studiengaenge/med/<anchor>")
def showmed(lang, anchor="kurzbeschreibung"):
    filenames = ["studiengaenge/med/index-2018.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showmed")

@app.route("/<lang>/studiengaenge/med_erw/")
@app.route("/<lang>/studiengaenge/med_erw/<anchor>")
def showmederw(lang, anchor="kurzbeschreibung"):
    filenames = ["studiengaenge/med_erw/index-2021.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showmederw")

@app.route("/<lang>/studiengaenge/msc/")
@app.route("/<lang>/studiengaenge/msc/<anchor>")
def showmsc(lang, anchor = "kurzbeschreibung"):
    filenames = ["studiengaenge/msc/index-2014.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showmsc")

@app.route("/<lang>/studiengaenge/msc_data/")
@app.route("/<lang>/studiengaenge/msc_data/<anchor>")
def showmscdata(lang, anchor = "kurzbeschreibung"):
#    filenames = ["studiengaenge/msc_data_carousel.html","studiengaenge/mscdata-2024.html"]
    filenames = ["studiengaenge/msc_data/index-2024.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showmscdata")

@app.route("/<lang>/studiengaenge/msc_data/news/")
def showmscdatanews(lang):
    filenames = ["studiengaenge/msc_data/carousel.html", "studiengaenge/msc_data/news.html"]
    return render_template("home.html", filenames = filenames, lang=lang, site = "showmscdatanews")

@app.route("/<lang>/studiengaenge/med_dual/")
@app.route("/<lang>/studiengaenge/med_dual/<anchor>")
def showmeddual(lang, anchor="kurzbeschreibung"):
    filenames = ["studiengaenge/med_dual/index-2024.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showmeddual")

@app.route("/<lang>/studiengaenge/promotion/")
@app.route("/<lang>/studiengaenge/promotion/<anchor>")
def showpromotion(lang, anchor="kurzbeschreibung"):
    filenames = ["studiengaenge/promotion/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor = anchor, site = "showpromotion")

#################
## Prüfungsamt ##
#################

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


#########
## faq ##
#########



# which can Werte 'all', 'bsc', '2hfb', 'msc', 'mscdata', 'med', 'mederw', 'meddual' annehmen
# show ist entweder "" oder "alleantworten"
@app.route("/<lang>/faq/")
@app.route("/<lang>/faq/<which>/")
@app.route("/<lang>/faq/<which>/<show>/")
def showfaq(lang, which = "all", show = ""):
    studiengaenge = {"all": "alle Studiengänge",
                     "bsc": "Bachelor of Science Mathematik",
                     "2hfb": "Zwei-Hauptfächer-Bachelor",
                     "msc": "Master of Science Mathematik",
                     "mscdata": "Master of Science Mathematics in Data and Technology", 
                     "med": "Master of Education Mathematik",
                     "mederw": "Master of Education Mathematik Erweiterungsfach",
                     "meddual": "Masterstudiengang Lehramt Gymnasium – dual"
                     }
    def getid(item):
        return item.replace("faq/","").replace(".html","").replace("/", "_")
    faq_tags = {"allgemeines": "Allgemeines",
            "verwendung": "Belegung und Verwendung von Veranstaltungen",
            "pruefungen": "Prüfungen und deren Anmeldungen",
             "abschlussarbeit": "Abschlussarbeit", 
             "sonstiges": "Sonstiges"
             }
    faq_dicts = {}
    for tag in faq_tags.keys():
        faq_dicts[tag] = {}
        faq_items = glob.glob("mi-hp/templates/faq/" + tag + "/faq*.html")
        logging.warning(faq_items)
        faq_items = [item.replace("mi-hp/templates/", "") for item in faq_items]
        faq_items.sort()
        for item in faq_items:
            faq_dicts[tag][getid(item)] = item
    showtag = show.split("_")[0]    
    return render_template("faq.html", lang=lang, faq_tags=faq_tags, faq_dicts=faq_dicts, which=which, getid = getid, show = show, showtag = showtag, studiengaenge = studiengaenge, site = "showfaq")

#########################
## Lehrveranstaltungen ##
#########################

@app.route("/<lang>/lehrveranstaltungen/")
def showlehrveranstaltungenbase(lang):
    filenames = ["lehrveranstaltungen/index.html"]    
    return render_template("home.html", filenames = filenames, lang=lang, semester = semester, site = "showlehrveranstaltungenbase")

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
    return render_template("home.html", filenames = filenames, lang=lang, semester=semester, site = "showlehrveranstaltungen")

@app.route("/<lang>/lehrveranstaltungen/aktuelles/")
def showlehrveranstaltungenaktuelles(lang):
    return redirect(url_for('showlehrveranstaltungen', lang=lang, semester = aktuelles[0]))

@app.route("/<lang>/lehrveranstaltungen/kommendes/")
def showlehrveranstaltungenkommendes(lang):
    return redirect(url_for('showlehrveranstaltungen', lang=lang, semester = kommendes[0]))


###############
## Mediathek ##
###############


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

