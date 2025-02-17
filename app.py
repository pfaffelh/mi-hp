from flask import Flask, jsonify, url_for, render_template, redirect, request, abort
from flask_misaka import Misaka
from ipaddress import ip_network, IPv4Address
import locale, json, os, requests, xmltodict, base64, pymongo, socket
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.background import BackgroundScheduler
from bson import ObjectId
from bs4 import BeautifulSoup
from pybtex.database.input import bibtex

from utils.config import *
from utils.util_logging import logger
# from utils.util_calendar import calendar, get_caldav_calendar_events

import utils.util_faq as faq
import utils.util_person as person
import utils.util_vvz as vvz
import utils.util_news as news
import utils.util_wp as wp

app = Flask(__name__)
Misaka(app, autolink=True, tables=True, math= True, math_explicit = True)

# Die nächsten beiden Funktionen werden benötigt, wenn der Webserver neu aufgesetzt ist, und wir unterscheiden können woher die request kommt.
# Durch diese Funktion werden mit @fortivpn gekennzeichnete Routen nur vom vpn aus erreicht.
def forti_bool_or_localhost(network = '10.23.0.0/16'):
    ip = IPv4Address(request.remote_addr)
# Die nächsten beiden Zeilen sind nach der Umstellung zu ändern.
    return True
#    return ip in ip_network(network) or ip in ip_network('127.0.0.1')

def fortivpn(network = '10.23.0.0/16'):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if forti_bool_or_localhost(network):
                return f(*args, **kwargs)
            else:
                abort(403)
        return wrapper
    return decorator

# This is such that we can use os-commands in jinja2-templates.
@app.context_processor
def handle_context():
    cur = vvz.get_current_semester_kurzname()
    showanmeldung = {
        "bsc": vvz.get_showanmeldung("bsc"), 
        "msc": vvz.get_showanmeldung("msc"),
        "mscdata": vvz.get_showanmeldung("mscdata")
        }
    vpn = forti_bool_or_localhost()
    return dict(datetime =datetime, timedelta=timedelta, vpn=vpn, os=os, 
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

# This should be deleted soon (20.12.2024)
@app.route("/nlehre/screenshotwp/")
def showwp():
    return render_template("screenshottocode.html")

@fortivpn()
@app.route("/nlehre/vpn/wordpress/index")
def wordpress_index():
    response_news = requests.get("https://www.math.uni-freiburg.de/nlehre/api/news/")
    news_data = json.loads(response_news.text)

    response_news = requests.get("https://www.math.uni-freiburg.de/nlehre/api/wochenprogramm/")
    talks_data = json.loads(response_news.text)

    # Render template and pass data
    return render_template(
        template_name_or_list="wordpress/index.html",
        news_data=news_data,
        talks_data=talks_data)

# Ansatz des Personenverzeichnisses etc unter wp
@app.route("/cd2021/<site>/")
@app.route("/cd2021/<site>/<show>/")
def showfakewp(site, show = "", lang = "de"):
    dir = site.split("_")
    lang = list(reversed(dir))[0]
    if dir[0] == "personen":
        if len(dir) == 3:
            abteilung = dir[1]
            data = person.get_person_data(abteilung = abteilung)
        else:
            data = person.get_person_data()
        wp.make_skel(wp.config[site])
    elif dir[0] == "institutstatic":
        return render_template("wp/institut_static.html")
    elif dir[0] == "institut":
        # get data from wochenprogramm, news
        anfang = datetime.now().strftime('%Y%m%d')
        end = (datetime.now() + relativedelta(days = 14)).strftime('%Y%m%d')
        reihen, events = news.get_events(lang)
        data = {}
        data["wochenprogramm"] = news.get_wochenprogramm_full(anfang, end, "alle", lang)
        data["news"] = news.data_for_base(lang)["news"]
        print([item['home'] for item in data["news"]])
        wp.make_skel(wp.config[site])
    elif dir[0] == "newsstatic":
        return render_template("wp/news_static.html")
    elif dir[0] == "news":
        data = news.data_for_base(lang)
        wp.make_skel(wp.config[site])
    elif dir[0] == "personenstochastikstatic":
        return render_template("wp/personenstochastik_static.html")
    elif dir[0] == "pfaffelhuberstatic":
        return render_template("wp/pfaffelhuber_static.html")
    elif dir[0] == "pfaffelhuber":
        parser = bibtex.Parser()
        with app.open_resource("static/bibtex/pfaffelhuber.bib") as f:
            bib_data = parser.parse_file(f)
        data = wp.get_bibdata(f)
        print(data)
        wp.make_skel(wp.config[site])
        
    return render_template(wp.config[site]["template"], data = data, config = wp.config[site], show=show, lang=lang)

# Ansatz der News unter wp
@app.route("/cd2021/<lang>/news/")
def shownewswp(show = "", lang = "de"):
    data = news.data_for_base(lang)
    person.make_skel("https://uni-freiburg.de/lehre/", 
              {"class" : "clearfix"})
    return render_template("wp/news.html", data = data, show=show, lang=lang)


###############
## Home page ##
###############

@app.route("/nlehre/")
@app.route("/nlehre/<lang>/")
@app.route("/nlehre/<lang>/<dtstring>")
@app.route("/nlehre/test/<lang>/")
@app.route("/nlehre/test/<lang>/<dtstring>")
def showbase(lang="de", dtstring = datetime.now().strftime('%Y%m%d%H%M')):
    testorpublic = "test" if "test" in request.path.split("/") else "_public"
    # print(request.endpoint)
    data = news.data_for_base(lang, dtstring, testorpublic)
    filenames = ["index.html"]
    return render_template("home.html", filenames=filenames, data = data, lang=lang)

#def showbase(lang="de"):
#    return redirect(url_for('showlehrveranstaltungen', lang=lang, semester=vvz.get_current_semester_kurzname()))

################################
## Allgemeine Accordion-Seite ##
################################
@app.route("/nlehre/<lang>/page/<kurzname>/")
@app.route("/nlehre/<lang>/page/<kurzname>/<show>")
def showaccordion(lang, kurzname, show =""):
    vpn = False
    data, show, showcat = faq.get_accordion_data(kurzname, lang, show = show)
    return render_template("accordion.html", lang=lang, data = data, showcat = showcat, show=show)

# Here is the vpn version
@app.route("/nlehre/vpn/<lang>/page/<kurzname>/")
@app.route("/nlehre/vpn/<lang>/page/<kurzname>/<show>")
def showvpnaccordion(lang, kurzname, show =""):
    vpn = True
    data, show, showcat = faq.get_accordion_data(kurzname, lang, show = show)
    return render_template("accordion.html", lang=lang, vpn = vpn, data = data, showcat = showcat, show=show)

@app.route("/nlehre/<lang>/lexikon/")
def showlexikon(lang):
    data = faq.get_lexikon_data()
    filenames = ["footer/lexikon.html"]
    return render_template("home.html", filenames = filenames, data = data, lang = lang)



############
## footer ##
############

@app.route("/nlehre/<lang>/bildnachweis/")
def showbildnachweis(lang):
    # Bilder von "News und "Monitor"
    data = news.data_for_bildnachweis(lang)
    filenames = ["footer/bildnachweis.html"]
    return render_template("home.html", filenames = filenames, data = data, lang=lang)

@app.route("/nlehre/<lang>/impressum/")
def showimpressum(lang):
    filenames = ["footer/impressum.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/nlehre/<lang>/datenschutz/")
def showdatenschutz(lang):
    filenames = ["footer/datenschutz.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

@app.route("/nlehre/vpn/<lang>/tools")
def showtools(lang = "de"):
    filenames = ["footer/tools.html"]
    return render_template("home.html", filenames = filenames, lang=lang)

##########################
## Studieninteressierte ## 
##########################

@app.route("/nlehre/studieninformation.html")
@app.route("/nlehre/<lang>/interesse/")
@app.route("/nlehre/<lang>/interesse/<anchor>")
def showinteresse(lang = "de", anchor=""):
    with app.open_resource('static/data/interesse.json') as f:
        data = json.load(f)
    filenames = ["interesse/interesse_prefix.html", "interesse/interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

##########################
## Studienanfänger      ## 
##########################

@app.route("/nlehre/<lang>/anfang/")
@app.route("/nlehre/<lang>/anfang/<anchor>")
def showanfang(lang, anchor=""):
    return redirect(url_for('showaccordion', lang=lang, kurzname = 'studienanfang', show=anchor))

###################
## Weiterbildung ## 
###################
# Soll es diese Seite wirklich geben?

@app.route("/nlehre/<lang>/weiterbildung/")
@app.route("/nlehre/<lang>/weiterbildung/<anchor>")
def showweiterbildung(lang, anchor=""):
    with app.open_resource('static/data/weiterbildung.json') as f:
        data = json.load(f)
    filenames = ["interesse/interesse_content.html"]
    return render_template("home.html", filenames=filenames, data = data, anchor=anchor, lang=lang)

###################
## Studiengaenge ##
###################

@app.route("/nlehre/studiengaenge/index.html") # für Links zur alten Homepage
@app.route("/nlehre/<lang>/studiengaenge/")
@app.route("/nlehre/<lang>/studiengaenge/<anchor>")
def showstudiengaenge(lang = "de", anchor="aktuell"):
    filenames = ["studiengaenge/index.html"]
    return render_template("home.html", filenames = filenames, lang=lang, anchor=anchor)

@app.route("/nlehre/<lang>/studiengaenge/<anchor>")
@app.route("/nlehre/<lang>/studiengaenge/<studiengang>/")
@app.route("/nlehre/<lang>/studiengaenge/<studiengang>/<anchor>")
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
    if studiengang == "med_dual":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'med-dual', show=''))
        # filenames = ["studiengaenge/med_dual/index-2024.html"]
    if studiengang == "promotion":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'promotion', show=''))
    #   filenames = ["studiengaenge/promotion/index.html"]
    return render_template("home.html", filenames=filenames, lang=lang, studiengang=studiengang, anchor=anchor)

#########################
## Lehrveranstaltungen ##
#########################

@app.route("/nlehre/<lang>/lehrveranstaltungen/")
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
    # print(semester_dict_2)
    for key, value in semester_dict_2.items():
        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'.pdf')
            semester_dict_2[key]["komm_exists"] = True
        except:
            semester_dict_2[key]["komm_exists"] = False
        try:
            app.open_resource('static/pdf/lehrveranstaltungen/' + key + '_' + lang + '.pdf')
            semester_dict_2[key]["komm_lang_exists"] = True
        except:
            semester_dict_2[key]["komm_lang_exists"] = False

        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'mh.pdf')
            semester_dict_2[key]["mh_exists"] = True
        except:
            semester_dict_2[key]["mh_exists"] =False

        try:
            app.open_resource('static/pdf/lehrveranstaltungen/' + key + 'mh_' + lang + '.pdf')
            semester_dict_2[key]["mh_lang_exists"] = True
        except:
            semester_dict_2[key]["mh_lang_exists"] =False

        try:
            app.open_resource('static/pdf/lehrveranstaltungen/'+key+'verw.pdf')
            semester_dict_2[key]["verw_exists"] = True
        except:
            semester_dict_2[key]["verw_exists"] =False

    return render_template("home.html", filenames=filenames, lang=lang, semester_dict=semester_dict_2, semester_dict_old=semester_dict_old)

@app.route("/nlehre/<lang>/lehrveranstaltungen/<semester>/")
@app.route("/nlehre/<lang>/lehrveranstaltungen/<semester>/<studiengang>")
@app.route("/nlehre/<lang>/lehrveranstaltungen/<semester>/<studiengang>/<modul>")
def showlehrveranstaltungen(lang, semester, studiengang = "", modul = ""):
    semesterliste_alt = ["ws0607", "ss07", "ws0708", "ss08", "ws0809", "ss09", "ws0910", "ss10", "ws1011", "ss11", "ws1112", "ss12", "ws1213", "ss13", "ws1314", "ss14", "ws1415", "ss15", "ws1516", "ss16", "ws1617", "ss17", "ws1718", "ss18", "ws1819", "ss19", "ws1920", "ss20", "ws2021", "ss21", "ws2122", "ss22", "ws2223", "ss23", "ws2324", "ss24"]
    if semester in semesterliste_alt:
        filenames = [f"lehrveranstaltungen/{semester}.html"]
        return render_template("home.html", filenames = filenames, lang=lang, semester=semester)
    else:
        data = vvz.get_data(semester, lang, studiengang, modul)
        return render_template("lehrveranstaltungen/vvz.html", lang=lang, data = data, semester=semester, studiengang = studiengang, modul = modul, vpn_nextsemester = False)

@app.route("/nlehre/<lang>/lehrveranstaltungen/<semester>/stundenplan/")
def showlehrveranstaltungenstundenplan(lang, semester):
    data = vvz.get_data_stundenplan(semester, lang)
    return render_template("lehrveranstaltungen/vvz_stundenplan.html", lang=lang, data = data, semester=semester, semester_lang = vvz.semester_name_de(semester), vpn_nextsemester = False)

@app.route("/nlehre/<lang>/lehrveranstaltungen/<semester>/personenplan/")
def showlehrveranstaltungenpersonenplan(lang, semester):
    data = vvz.get_data_personenplan(semester, lang)
    return render_template("lehrveranstaltungen/vvz_personenplan.html", lang=lang, data = data, semester=semester, semester_dict = {}, semester_lang = vvz.semester_name_de(semester), showdeputate = False, vpn_nextsemester = False)

@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/deputate/")
@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/<semester>/deputate/")
def showlehrveranstaltungendeputate(lang, semester = vvz.get_current_semester_kurzname()):
    a = [x["kurzname"] for x in list(vvz.vvz_semester.find({"hp_sichtbar": True}))]
    b = ["2024WS"] + [f"20{x}{s}S" for x in range(25,100) for s in ["S", "W"]]
    acapb = [x for x in a if x in b]
    acapb.reverse()
    semester_dict = { x : {"name": vvz.semester_name_de(x)} for x in acapb }
    data = vvz.get_data_personenplan(semester, lang)
    return render_template("lehrveranstaltungen/vvz_personenplan.html", lang=lang, data = data, semester=semester, semester_dict = semester_dict, semester_lang = vvz.semester_name_de(semester), showdeputate = True, vpn_nextsemester = False)

#################################
## Nächste Semester in Planung ##
#################################

@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/")
@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/<studiengang>")
@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/<studiengang>/<modul>")
def showlehrveranstaltungennextsemester(lang, studiengang = "", modul = ""):
    next_semester = vvz.next_semester_kurzname(vvz.get_current_semester_kurzname())
    if vvz.get_showsemester(next_semester, hp_sichtbar = True):
        filenames = ["message.html"]
        message = f"<h1>Die Daten sind bereits <a href=/nlehre/de/lehrveranstaltungen/{next_semester}>hier</a> veröffentlicht.</h1>"
        return render_template("home.html", filenames = filenames, lang=lang, message = message)
    elif vvz.get_showsemester(next_semester, hp_sichtbar = False):
        data = vvz.get_data(next_semester, lang, studiengang, modul, vpn = True)
        return render_template("lehrveranstaltungen/vvz.html", lang=lang, data = data, semester=next_semester, studiengang = studiengang, modul = modul, vpn_nextsemester = True)
    else:
        filenames = ["message.html"]
        m = "{{ url_for('showlehrveranstaltungen', lang=lang, semester = kommendes_semester) }}"
        message = f"<h1>Es liegen noch keine Daten vor.</h1>"
        return render_template("home.html", filenames = filenames, lang=lang, message = message)

@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/stundenplan/")
def showlehrveranstaltungennextsemesterstundenplan(lang):
    next_semester = vvz.next_semester_kurzname(vvz.get_current_semester_kurzname())
    data = vvz.get_data_stundenplan(next_semester, lang, vpn = True)
    return render_template("lehrveranstaltungen/vvz_stundenplan.html", lang=lang, data = data, semester=next_semester, semester_lang = vvz.semester_name_de(next_semester), vpn_nextsemester = True)

@app.route("/nlehre/vpn/<lang>/lehrveranstaltungen/personenplan/")
def showlehrveranstaltungennextsemesterpersonenplan(lang):
    next_semester = vvz.next_semester_kurzname(vvz.get_current_semester_kurzname())
    data = vvz.get_data_personenplan(next_semester, lang, vpn = True)
    return render_template("lehrveranstaltungen/vvz_personenplan.html", lang=lang, data = data, semester=next_semester, semester_dict = {}, semester_lang = vvz.semester_name_de(next_semester), showdeputate = False, vpn_nextsemester = True)

#####################################
## Prüfungsamt und Studienberatung ##
#####################################

# TEST: Neue Accordions

@app.route("/nlehre/vpn/<lang>/studiendekanat/pruefungsregeln/")
@app.route("/nlehre/vpn/<lang>/studiendekanat/pruefungsregeln/<show>")
def show_pruefungen(lang, show =""):
    return redirect(url_for('showaccordion', lang=lang, kurzname =
    'pruefungen-begriffe-regeln', show=show))

# Neue Accordions Ende

@app.route("/nlehre/<lang>/studiendekanat/faq/")
@app.route("/nlehre/<lang>/studiendekanat/faq/<show>")
def showstufaq(lang, show =""):
    return redirect(url_for('showaccordion', lang=lang, kurzname = 'faqstud', show=show))

@app.route("/nlehre/<lang>/studiendekanat/")
@app.route("/nlehre/<lang>/studiendekanat/<unterseite>/")
@app.route("/nlehre/<lang>/studiendekanat/<unterseite>/<show>")
def showstudiendekanat(lang, unterseite = "", show = ""):
    data = {}
    filenames = []
    if unterseite == "":
        data = faq.get_studiendekenat_data({"showstudienberatung" : True})
        filenames = ["studiendekanat/studienberatung.html"]
    if unterseite == "pruefungsamt":
        data = faq.get_studiendekenat_data({"showpruefungsamt" : True})
        filenames = ["studiendekanat/pruefungsamt.html"]        
    if unterseite == "schwerpunktgebiete":
        filenames = ["studiendekanat/schwerpunktgebiete.html"]
    if unterseite == "warum_mathematik":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'warum-mathematik', show=show))
        # filenames = ["studiendekanat/warum_mathematik.html"]
    if unterseite == "termine":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'pruefungstermine', show=show))
        # filenames = ["studiendekanat/termine.html"]
    if unterseite == "calendar":
        events = vvz.get_calendar_data(datetime.now() + timedelta(days = -365), lang)
        return render_template("studiendekanat/calendar.html", events=events, lang=lang, lehrende = False)
    if unterseite == "anmeldung":
        filenames = ["studiendekanat/anmeldung.html"]
    if unterseite == "modulplan":
        filenames = ["studiendekanat/modulplan.html"]
    if unterseite == "pruefungen":
        filenames = ["studiendekanat/pruefungen.html"]
    if unterseite == "ausland":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'ausland', show=show))
    return render_template("home.html", data=data, filenames = filenames, lang=lang)


##################
## Für Lehrende ##
##################

# show ist entweder "", oder "all" oder eine id für ein qa-Paar
@app.route("/nlehre/<lang>/lehrende/")
@app.route("/nlehre/<lang>/lehrende/faq/")
@app.route("/nlehre/<lang>/lehrende/faq/<show>")
def showmitfaq(lang, show =""):
    return redirect(url_for('showaccordion', lang=lang, kurzname = 'faqmit', show=show))

@app.route("/nlehre/<lang>/lehrende/<unterseite>")
@app.route("/nlehre/<lang>/lehrende/<unterseite>/<anchor>")
def showlehrende(lang, unterseite ="", anchor = ""):
    filenames = []
    if unterseite == "zertifikat":
        return redirect(url_for('showaccordion', lang=lang, kurzname = 'zertifikat', show=anchor))
    if unterseite == "calendar":
        events = vvz.get_calendar_data(datetime.now() + timedelta(days = -360), lang)
        return render_template("studiendekanat/calendar.html", events=events, lang=lang, lehrende = True)
        
    return render_template("home.html", filenames = filenames, anchor = anchor, lang=lang)

@fortivpn()
@app.route("/nlehre/vpn/<lang>/lehrende/<unterseite>")
@app.route("/nlehre/vpn/<lang>/lehrende/<unterseite>/<anchor>")
def showlehrendevpn(lang, unterseite ="", anchor = ""):
    filenames = []
    return render_template("home.html", filenames = filenames, anchor = anchor, lang=lang)

@app.route("/nlehre/vpn/<lang>/lehrende/<semester>/planung/")
def showlehrveranstaltungenplanung(lang, semester):
    sems, data = vvz.get_data_planung(semester)
    return render_template("lehrveranstaltungen/vvz_planung.html", lang=lang, data = data, semester=semester, sems=sems)


###############
## Downloads ##
###############

# show kann sein: lehrende, pruefungsamt, studiendokumente, promotion, gesetz, bericht
@app.route("/nlehre/<lang>/downloads/")
@app.route("/nlehre/<lang>/downloads/<show>")
def showdownloads(lang, show=""):
    return redirect(url_for('showaccordion', lang=lang, kurzname =
        'downloads', show=show))
#    filenames = ["downloads/downloads.html"]
#    return render_template("home.html", filenames=filenames, anchor=anchor, lang=lang)

####################
## Wochenprogramm ##
####################

@app.route("/wochenprogramm/")
@app.route("/wochenprogramm/<lang>/")
@app.route("/wochenprogramm/<lang>/vortragsreihe/")
@app.route("/wochenprogramm/<lang>/vortragsreihe/<kurzname>/")
@app.route("/wochenprogramm/<lang>/vortragsreihe/<kurzname>/<anfang>/<end>")
def showvortragsreihe(lang="de", kurzname="alle", anfang = datetime(datetime.now().year, datetime.now().month, 1).strftime('%Y%m%d'), end = (datetime(datetime.now().year, datetime.now().month, 1) + relativedelta(months=1)).strftime('%Y%m%d')):
    reihen, events = news.get_events(lang)
    data = news.get_wochenprogramm_full(anfang, end, kurzname, lang)
    return render_template("wochenprogramm/reihe.html", reihen = reihen, events = events, kurzname = kurzname, lang=lang, data = data)

@app.route("/wochenprogramm/<lang>/event/<kurzname>/")
def showevent(lang, kurzname="alle"):
    reihen, events = news.get_events(lang)
    data = news.get_event(kurzname, lang)
    return render_template("wochenprogramm/event.html", reihen = reihen, events = events, kurzname = kurzname, lang=lang, data = data)

@app.route("/wochenprogramm/<lang>/newsarchiv/")
@app.route("/wochenprogramm/<lang>/newsarchiv/<anfang>/<end>/")
def shownews(lang = "de", anfang = datetime(datetime.now().year, datetime.now().month, 1).strftime('%Y%m%d'), end = (datetime(datetime.now().year, datetime.now().month, 1) + relativedelta(months=1)).strftime('%Y%m%d')):
    reihen, events = news.get_events(lang)
    data = news.data_for_newsarchiv_full(lang, anfang, end)
    filenames = ["wochenprogramm/newsarchiv.html"]
    return render_template("home_news.html", filenames=filenames, reihen = reihen, events = events, data = data, lang=lang)

#################
## Monitor EG  ##
#################

@app.route("/nlehre/monitortest/")
@app.route("/nlehre/monitortest/<dtstring>")
@app.route("/nlehre/monitor/")
@app.route("/nlehre/monitor/<dtstring>")
def showmonitor(dtstring = datetime.now().strftime('%Y%m%d%H%M')):
    # determine if only shown on test
    testorpublic = "test" if "monitortest" in request.path.split("/") else "_public" 
    data = news.get_monitordata(dtstring, testorpublic)
    return render_template("monitor/monitor_quer.html", data=data, lang="de")

###########
## api's ##
###########

@app.route("/nlehre/api/news/")
def get_news():
    news_reduced = news.get_api_news()
    return jsonify(news_reduced)

@app.route("/nlehre/api/wochenprogramm/")
@app.route("/nlehre/api/wochenprogramm/<anfang>/<ende>/")
# Default ist: anfang ist Anfang dieser Woche, ende ist Ende dieser Woche
def get_vortraege(anfang = (datetime.now() - timedelta(days=datetime.now().weekday())).strftime('%Y%m%d'), ende = (datetime.now() + timedelta(days=7-datetime.now().weekday())).strftime('%Y%m%d')):
    wochenprogramm_reduced = news.get_api_wochenprogramm(anfang, ende)
    return jsonify(wochenprogramm_reduced)


# This function reads the Mensaplan everyday and puts the result into the mongodb
scheduler = BackgroundScheduler(timezone="Europe/Rome")
# Runs from Monday to Sunday at 05:30 
scheduler.add_job(
    func=news.writetonews_mensaplan_text,
    trigger="cron",
    max_instances=1,
    day_of_week='mon-sun',
    hour=5,
    minute=30
)
scheduler.start()

