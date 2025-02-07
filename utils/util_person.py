import pymongo
from datetime import datetime, timedelta
from collections import OrderedDict
from operator import itemgetter
from markdown import markdown
from ldap3 import Server, Connection, ALL, SUBTREE
import json
from bs4 import BeautifulSoup
import requests

try:
    ldap_server = 'ldap://home.mathematik.uni-freiburg.de'  # Beispiel für einen öffentlichen LDAP-Server

    # LDAP-Baum und Suchbasis
    search_base = 'ou=People,dc=home,dc=mathematik,dc=uni-freiburg,dc=de'  # Der Startpunkt für die LDAP-Suche
    search_filter = '(objectClass=*)'  # Beispielhafter Filter, um alle Personenobjekte zu suchen

    # Verbindung zum LDAP-Server ohne Authentifizierung herstellen (anonyme Bindung)
    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, auto_bind=True)  # Keine Anmeldeinformationen erforderlich
    attributes = ['cn', 'sn', 'mail', 'labeledURI', 'givenName', 'objectClass', 'eduPersonPrimaryAffiliation', 'street', 'telephoneNumber', 'roomNumber', 'personalTitle'] 
except:
    print("No connection to LDAP server")

def remove_p(html):
    if html.startswith('<p>') and html.endswith('</p>'):
        return html[3:-4] 
    else:
        return html

def get_person_data():
    # Suche im LDAP-Baum durchführen
    try:
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
        with open("static/data/ldap.json", 'r') as file:
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
    result = requests.get(url, verify=False)
    doc = BeautifulSoup(result.text, 'lxml')

    content = doc.find('div', id)
    content.string = string
    html = doc.prettify("utf-8")
    # Write the skelet
    with open("/nlehre/templates/skel.html", "wb") as file:
        file.write(html)
