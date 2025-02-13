import pymongo
from datetime import datetime, timedelta
from collections import OrderedDict
from operator import itemgetter
from markdown import markdown
from ldap3 import Server, Connection, ALL, SUBTREE
import json
from bs4 import BeautifulSoup
import requests
from utils.config import *

def remove_p(html):
    if html.startswith('<p>') and html.endswith('</p>'):
        return html[3:-4] 
    else:
        return html

def get_person_data(abteilung = ""):
    try:
        # URL des öffentlichen LDAP-Servers
        ldap_server = 'ldap://home.mathematik.uni-freiburg.de'  # Beispiel für einen öffentlichen LDAP-Server

        # LDAP-Baum und Suchbasis
        search_base = 'ou=People,dc=home,dc=mathematik,dc=uni-freiburg,dc=de'  # Der Startpunkt für die LDAP-Suche
        if abteilung != "":
            search_base = f"ou={abteilung}," + search_base

        search_filter = '(objectClass=*)'  # Beispielhafter Filter, um alle Personenobjekte zu suchen

        # Verbindung zum LDAP-Server ohne Authentifizierung herstellen (anonyme Bindung)
        server = Server(ldap_server, get_info=ALL)
        conn = Connection(server, auto_bind=True)  # Keine Anmeldeinformationen erforderlich
        attributes = ['cn', 'sn', 'mail', 'labeledURI', 'givenName', 'objectClass', 'eduPersonPrimaryAffiliation', 'street', 'telephoneNumber', 'roomNumber', 'personalTitle'] 

        # Suche im LDAP-Baum durchführen
        conn.search(search_base, search_filter, search_scope=SUBTREE, attributes=attributes)

        # Liste für die Ergebnisse
        res = []

        # Ergebnisse in eine Liste von Dictionaries umwandeln
        for entry in conn.entries:
            entry_dict = {attr: entry[attr].value for attr in attributes if attr in entry}
            res.append(entry_dict)

        # Verbindung beenden
        conn.unbind()

    except:
        print(ip_address)
        if (ip_address == "127.0.1.1"):
            fn = "static/data/ldap.json"
        elif os.getcwd() == "/home/flask-reader/mi-hp":
            fn = "/home/flask-reader/mi-hp/static/data/ldap.json"
        else:
            fn = "/usr/local/lib/mi-hp/static/data/ldap.json"
        with open(fn , 'r') as file:
            res = json.load(file)

    trans = {
        "secretary" : "Sekretariate",
        "faculty" : "Professorinnen und Professoren",
        "retired" : "Emeritierte und pensionierte Professoren",
        "staff" : "Wissenschaftlicher Dienst",
        "employee" : "Administration und Technik"
    }
    res = [item for item in res if item["eduPersonPrimaryAffiliation"] in trans.keys()]
    print(res)   
#    res = dict(sorted(res, key=lambda x: (x["eduPersonPrimaryAffiliation"], x["cn"])))
        
    data = []
    for key, value in trans.items():
        data.append({
            "kurzname" : key,
            "name" : value,
            "person" : sorted([x for x in res if x["eduPersonPrimaryAffiliation"] == key ], key = lambda x: x['sn'][0])
        })
    print(data)
    return data

if __name__ == "__main__":
    get_person_data()

# id is a dict, e.g. {"class" : "clearfix"}
def make_skel(url, id, string = "{% block content%}Content{% endblock %}"):
    print(url)
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'lxml')

    content = doc.find('div', id)
    content.string = string
    html = doc.prettify("utf-8")
    # Write the skelet
    if (ip_address == "127.0.1.1"):
        fn = "templates/skel.html"
    elif os.getcwd() == "/home/flask-reader/mi-hp":
        fn = "/home/flask-reader/mi-hp/templates/skel.html"
    else:
        fn = "/usr/local/lib/mi-hp/templates/skel.html"
    with open(fn, "wb") as file:
        file.write(html)
