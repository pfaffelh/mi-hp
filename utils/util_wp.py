import requests
from bs4 import BeautifulSoup
from pybtex.database.input import bibtex
from utils.config import *
from utils.util_logging import logger

config = {
    "personen_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_AM_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_D_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_Di_de" : {
        "titel" : "Mitarbeiter der Abteilung für Didaktik der Mathematik",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_ML_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_MSt_de" : {
        "titel" : "",
        "url_skel" : "https://www.math.uni-freiburg.de/cd2021/personenstochastikstatic/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "wp-block-section-is-layout-constrained"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_PA_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "personen_RM_de" : {
        "titel" : "Lehrkörper / Mitarbeiter",
        "url_skel" : "https://uni-freiburg.de/universitaet/portrait/",
        "skel_name" : "skel_person.html",
        "queries" : [{"class" : "clearfix"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/personen.html"
    },
    "institut_de" : {
        "titel" : "Veranstaltungen",
        "url_skel" : "https://www.math.uni-freiburg.de/cd2021/institutstatic/",
        "skel_name" : "skel_institut.html",
        "queries" : [{"string" : "News"}, {"string" : "Veranstaltungen"}],
        "strings" : ["{% block content0%}Content{% endblock %}", "{% block content1%}Content{% endblock %}"], 
        "template" : "wp/institut.html"
    },
    "news_de" : {
        "titel" : "News",
        "url_skel" : "https://www.math.uni-freiburg.de/cd2021/newsstatic/",
        "skel_name" : "skel_news.html",
        "queries" : [{"string" : "News II"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/news.html"
    },
    "pfaffelhuber_de" : {
        "titel" : "",
        "url_skel" : "https://www.math.uni-freiburg.de/cd2021/pfaffelhuberstatic/",
        "skel_name" : "skel_pfaffelhuber.html",
        "queries" : [{"class" : "ufr-accordion-item-body"}],
        "strings" : ["{% block content%}Content{% endblock %}"], 
        "template" : "wp/pershome.html"
    }
}
# change institut_de url_skel to https://math.uni-freiburg.de/cd2021/institutstatic/

def make_skel(site):
    result = requests.get(site["url_skel"])
    doc = BeautifulSoup(result.text, 'lxml')
    for i, query in enumerate(site["queries"]):
        if "string" in query.keys(): 
            content = doc.find(string = query["string"]).find_parent().find_parent()
        else:
            content = doc.find("div", query)
        content.string = site["strings"][i]
    html = doc.prettify("utf-8")
    # Write the skelet
    if (ip_address == "127.0.1.1"):
        fn = "templates/" + site["skel_name"]
    elif os.getcwd() == "/home/flask-reader/mi-hp":
        fn = "/home/flask-reader/mi-hp/templates/" + site["skel_name"]
    else:
        fn = "/usr/local/lib/mi-hp/templates/" + site["skel_name"]
    with open(fn, "wb") as file:
        file.write(html)

from pybtex.database.input import bibtex
from jinja2 import Environment, FileSystemLoader

# BibTeX-Datei einlesen
def get_bibdata(filename):
    parser = bibtex.Parser()
    bib_data = parser.parse_file(filename)

    data = []
    for key, entry in bib_data.entries.items():
        data.append({
            "ID": key,
            "type" : entry.type,
            "author": " and ".join(person.get_part_as_text("last") for person in entry.persons["author"]),
            "title": entry.fields.get("title", "Kein Titel"),
            "journal": entry.fields.get("journal", ""),
            "volume": entry.fields.get("volume", ""),
            "pages": entry.fields.get("pages", ""),
            "year": entry.fields.get("year", ""),
            "note": entry.fields.get("note", ""),
            "url": entry.fields.get("url", ""),
        })
    return data

