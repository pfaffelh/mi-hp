## Allgemeines

Dies ist das Repository der [Lehre-Seiten des Mathematischen Instituts der Universität Freiburg](https://www.math.uni-freiburg.de/nlehre/). Es handelt sich um eine Flask-App (also python), die mit einer lokalen Datenbank verbunden ist.

## Übersicht aller Seiten:
- Hauptseite "/nlehre/<lang>"
  - zeigt auf 
- interesse "/nlehre/<lang>/interesse/"; Hier kommen die Daten aus
  - /static/data/interesse.json'
    "interesse/interesse_prefix.html", "interesse/interesse_content.html"
- anfang "/nlehre/<lang>/anfang/<anchor>"
  - redirect zu /nlehre/<lang>/page/studienanfang/
  - Hier werden die Daten aus der FAQ-App genommen.
- weiterbildung "/nlehre/<lang>/weiterbildung/<anchor>"
  - momentan nicht verlinkt; Daten kommen aus 'static/data/weiterbildung.json'
    gerenderte Datei ist "interesse/interesse_content.html"
- Studiengaenge "/nlehre/<lang>/studiengaenge/"
  - Daten aus "studiengaenge/index.html"
  - Unterseiten: "/nlehre/<lang>/studiengaenge/<studiengang>/"
    - Daten kommen aus html-Seite (außer med-dual), nämlich
        if studiengang == "bsc": "studiengaenge/bsc/index-2021.html"
        if studiengang == "msc": "studiengaenge/msc/index-2014.html"
        if studiengang == "msc_data": "studiengaenge/msc_data/index-2024.html"
        if studiengang == "2hfb": "studiengaenge/2hfb/index-2021.html"
        if studiengang == "med": "studiengaenge/med/index-2018.html"
        if studiengang == "med_erw": "studiengaenge/med_erw/index-2021.html"
        if studiengang == "med_dual": Hier wird die FAQ-App verwendet, kurzname = 'med-dual'
        if studiengang == "promotion": "studiengaenge/promotion/index.html"
    - **TODO** Auf FAQ-App für alle Studiengänge umsteigen
- lehrveranstaltungen Übersicht "/nlehre/<lang>/lehrveranstaltungen/"
  - Hauptseite aller Lehrveranstaltungen
- lehrveranstaltungen einzelner Semester "/nlehre/<lang>/lehrveranstaltungen/<semester>/", also zB
    Hier werden die Lehrveranstaltungen der Semester angezeigt. Bis incl SS24 sind die Daten als statische Webseiten hinterlegt, etwa unter "/nlehre/<lang>/lehrveranstaltungen/ss24". Die Seite 
    "/nlehre/<lang>/lehrveranstaltungen/2024SS"
    gibt es auch, und sie bezieht Daten aus dem VVZ. Ab WS24 sind nur diese Seiten verlinkt. 
    - Es gibt außerdem Seiten "/nlehre/<lang>/lehrveranstaltungen/<semester>/<studiengang>" und
      "/nlehre/<lang>/lehrveranstaltungen/<semester>/<studiengang>/<modul>",
      die nur das Angebot für die entsprechenden Studiengänge und Module bereitstellen. Diese sind jedoch kaum verlinkt, werden aber automatisch aus dem VVZ generiert.
    - "/nlehre/<lang>/lehrveranstaltungen/<semester>/stundenplan/"
      Hier ist eine Aufschlüsselung der Anzeige nach Zeiten
    - "/nlehre/<lang>/lehrveranstaltungen/<semester>/personenplan/"
      Hier ist eine Aufschlüsselung der Anzeige nach Personen. (Unter tools-depudate gibt es eine ähnliche Ansicht, diese ist ergänzt durch die vereinbarten Deputatsstunden.)
- Prüfungsamt und Studienberatung: 
  - zeigt das studentische FAQ aus mi-FAQ
- studiendekanat "/nlehre/<lang>/studiendekanat/" und Unterseiten
  - Hier sind alle Seite aus dem Untermenü zu "Prüfungsamt und Studienberatung"
  - Die Startseite "Studienberatung" zeigt die Studienberatung, die Daten kommen aus mi-faq "Studiendekanat"
    "studiendekanat/studienberatung.html"
    if unterseite == "pruefungsamt": Daten aus mi-FAQ "showpruefungsamt" muss True sein
    "studiendekanat/pruefungsamt.html"
    if unterseite == "schwerpunktgebiete": "studiendekanat/schwerpunktgebiete.html"
    if unterseite == "warum_mathematik": "studiendekanat/warum_mathematik.html"
    if unterseite == "termine": "studiendekanat/termine.html"
    if unterseite == "calendar": "studiendekanat/calendar.html"
    Ereignisse werden aus dem vvz generiert 
    if unterseite == "anmeldung": "studiendekanat/anmeldung.html"
    if unterseite == "modulplan": "studiendekanat/modulplan.html"
    if unterseite == "pruefungen": "studiendekanat/pruefungen.html"
    if unterseite == "ausland": "studiendekanat/ausland.html"
  - **TODO** Unterseiten warum_mathematik, termine, pruefungen, ausland auf accordion-Seiten umstellen
- lehrende
  - Die Startseite zeigt das Lehrenden-FAQ, die Daten kommen aus mi-faq 
  - unterseite == "zertifikat": accordion-Seite zum Lehrzertifikat
    if unterseite == "calendar": genau wie der Kalender der Studierenden
  - "/nlehre/vpn/<lang>/lehrende/<semester>/planung/"
    Lehrplanung Zukunft aus dem vvz; Zugang nur über vpn
- downloads "/nlehre/<lang>/downloads/"
  - Die Download Seite; "downloads/downloads.html"


- Im Footer der Seite gibt es folgende Elemente:
  - bildnachweis "/nlehre/<lang>/bildnachweis/"
    siehe "footer/bildnachweis.html"; die Daten kommen aus mi-news
  - impressum "/nlehre/<lang>/impressum/"
    siehe "footer/impressum.html"
  - datenschutz "/nlehre/<lang>/datenschutz/"
    siehe "footer/datenschutz.html"
  - tools "/nlehre/vpn/<lang>/tools"
    siehe "footer/tools.html"




## Aufbau der URLs

Der Aufbau der URLs ist fast immer `https://www.math.uni-freiburg.de/nlehre/<lang>/unterpunkt/unterseite/anchor`, wobei `lang == de` oder `lang == en` die Sprache angibt. Die Templates der Unterpunkte

- interesse
- anfang
- studiengaenge
- lehrveranstaltungen
- studiendekanat
- lehrende
- downloads
  sind dabei in den entsprechenden Unterordnern von `template` zu finden. `unterseite` ist meist eine eigene html-Datei, `anchor` meist eine `id` innerhalb der html-Datei.

Eine Ausnahme sind die Seiten, die mit 
`https://www.math.uni-freiburg.de/nlehre/vpn/`
beginnen. Diese sind nur innerhalb des vpn bzw an Institutsrechnern zugänglich. In diesem Fall bleibt der Aufbau der URL derselbe.

## Steuerung eines Requests

Wird die Seite aufgerufen, so steuert `app.py`, was genau passiert. Hier werden auch Routen definiert, die steuern, welche Funktion aufgerufen wird, wenn ein request verarbeitet wird.

### Hier ein paar Beispiele, wie Inhalte angesteuert werden

Das folgende ist in den Templates etwa so zu verwenden: 

<a href="{{ url_for('showstudiendekanat', lang=lang)}}">Studienberatung</a>

* Homepage: `{{ url_for('showbase', lang=lang)}}`
* Studienberatung: `{{ url_for('showstudiendekanat', lang=lang)}}`
* Prüfungsamt: `{{ url_for('showstudiendekanat', unterseite = 'pruefungsamt', lang=lang)}}`
* Prüfungskalender: `{{ url_for('showstudiendekanat', unterseite = 'calendar', lang=lang)}}`
* Termine und Fristen: `{{ url_for('showstudiendekanat', unterseite = 'termine', lang=lang)}}`
* Für Studieninteressierte: `{{ url_for('showinteresse', lang=lang)}}`
* Für Studienanfänger: `{{ url_for('showanfang', lang=lang)}}`
* Alle Studiengänge: `{{ url_for('showstudiengaenge', lang=lang)}}`
* BSc Studiengang: `{{ url_for('showstudiengand', studiengang = 'bsc', lang=lang)}}` (andere sind msc, msc_data, 2hfb, med, med_erw, med_dual, promotion)
* Alle Lehrveranstaltungen: `{{ url_for('showlehrveranstaltungenbase', lang=lang)}}`
* Mitarbeiter-FAQ: `{{ url_for('showmitfaq', lang=lang)}}`
* Lehrzertifikat: `{{ url_for('showlehrende', unterseite = 'zertifikat', lang=lang)}}`
* Prüfungskalender, Lehrenden-Ansicht: `{{ url_for('showlehrende', unterseite = 'calendar', lang=lang)}}`
* Downloads: `{{ url_for('showdownloads', lang=lang)}}`
* Downloads Formulare: `{{ url_for('showdownloads', anchor = pruefungsamt, lang=lang)}}` 
* Downloads Modulhandbücher: `{{ url_for('showdownloads', anchor = studiendokumente, lang=lang)}}` (anchor kann auch sein: lehrende, pruefungsamt, studiendokumente, promotion, gesetz, bericht)


## Änderungen an der Seite

Personen, die als Collaborator des Repositories in [github](https://github.com/pfaffelh/mi-hp) eingetragen sind, können das Repository ändern. Hier eine kurze Anleitung, wie man die neue "Lehre"-Seite ändern kann:

Wie oben beschrieben muss man verstehen, dass ein `flask`-Skript (ein python-Web-Framework) die ganze Seite steuert. Weiter ist es so, dass einige Inhalte (welche das sind: siehe unten) durch andere Apps befüllt und hier nur noch ausgelesen werden. Anders als bei der restlichen Homepage des Instituts ist die "Lehre-Seite" ein "repository" auf github, das dann zwischen verschiedenen Rechnern synchronisiert wird. Die Version, die auf dem Webserver des Instituts liegt, wird angezeigt. (Etwas genauer: Der Branch "Master" des Repositories wird angezeigt.) Der Webserver sieht zu allen ganzen 5 Minuten nach, ob sein Repository mit dem auf [github](https://github.com/pfaffelh/mi-hp) übereinstimmt. Tut es das nicht, synchronisiert er sich. Das bedeutet, dass man das Repository auf github verändern muss, damit Änderungen zum tragen kommen. Hierzu gibt es zwei Möglichkeiten, wie weiter unten beschrieben und erklärt. Die einfachere der beiden ergibt folgenden Arbeitsablauf:

1. Den [vscode-Editor](https://github.dev/pfaffelh/mi-hp) von github öffnen.
2. Änderungen durchführen und speichern.
3. Die Änderungen durch clicken auf das Symbol **unter** 🔎 in der linken Leiste und Eingabe einer ungefähren Beschreibung, woraus die Änderungen bestehen, "committen".
4. Nach ein paar Minuten sollten die Änderungen auf der [Homepage](www.math.uni-freiburg.de/nlehre/) sichtbar sein. (Es sei denn, es ist etwas schiefgegangen.)

Folgende Inhalte greifen auf eine Datenbank zu, so dass sie nicht innerhalb dieses Repositories geändert werden können, sondern mittels der entsprechenden App, die für die Änderungen der Datenbank programmiert wurden. Hierbei gibt es Variablen bei der URL, wiefolgt:
* <lang> ist de oder en
* <semester> wird in der Form 2024WS eingegeben. (Andere Formate, etwa ss23, kommen auch vor, aber dann werden die angezeigten Daten nicht aus dem mi-vvz generiert.)
Es geht um folgende Apps bzw Unterseiten:
* Die News der Startseite, sowie die des Monitors, also:
  * `/nlehre/<lang>/`
  * `/nlehre/api/monitor/` (JSON für die News-App auf dem Monitor)
  Diese Daten werden von der App *mi-news* aus befüllt; siehe [hier](http://mi-news1.mathematik.privat/).
* Alle Details zu Veranstaltungen, also die Seiten
  * `<lang>/lehrveranstaltungen/<semester>/` (das übliche Vorlesungsverzeichnis)
  * `<lang>/lehrveranstaltungen/<semester>/stundenplan/` (dasselbe, aber sortiert nach Zeiten)
  * `/vpn/<lang>/lehrende/<semester>/planung/` (Planung für künftige Semester, nur erreichbar aus dem vpn-Netz)
  Diese Seiten werden von mi-vvz aus befüllt; siehe [hier](http://mi-vvz1.mathematik.privat/).
* Alle Details von FAQs, also die Seiten:
  * `<lang>>/studiendekanat/faq/` (FAQ für Studierende)
  * `<lang>/lehrende/faq/` (FAQ für Mitarbeiter*innen)
  Diese werden von mi-faq aus befüllt.
* Details zu Sprechstunden im Studiendekanaat, also
  * `<lang>/studiendekanat/` 
  * `<lang>/studiendekanat/pruefungsamt/`
  Diese Seiten werden ebenfalls von mi-faq aus befüllt; siehe [hier](http://mi-faq1.mathematik.privat/)
Etwas speziell sind noch die Seiten
* `<lang>/interesse/`
* `<lang>/weiterbildung/`
Diese Daten dieser Seiten sind in `/static/data/interesse.json` und `/static/data/weiterbildung.json` gespeichert (bis auf den Vorspann). 

### Beschreibung der beiden Möglichkeiten, Inhalte zu ändern
* (Technisch einfacher): Der von github bereitgestellte [Editor](https://github.dev/pfaffelh/mi-hp) zeigt alle Daten des Repositories an. (Etwas genauer hat er noch eine eigene Version des Repositories, deshalb immer zunächst alles "synchronisieren".) Hier kann man Dinge ändern, und speichern. Wenn man fertig ist, muss man das Repository des Editors mit dem auf github synchronisieren. (Oder seine Änderungen 'commit'ten.) Hierzu das Symbol unter der 🔎 in der linken Leiste clicken "Source control"), eine Message ungefähre Nachricht eingeben, woraus die durchgeführte Änderung besteht, und "Commit and Push" drücken. Nach ein paar Minuten synchronisiert sich der Webserver des Instituts, und die Änderungen werden angezeigt.
* (Etwas komplizierter, deshalb nur eine ganz knappe Beschreibung): Um die Änderungen im Master-Branch des Repositories durchzuführen, kann man das Repositorie auch lokal clonen (`git clone https://github.com/pfaffelh/mi-hp`), Änderungen hier durchführen, und von hier aus committen. Der Vorteil dieser Variante besteht darin, dass der zu grunde liegende python-Code dann ebenfalls lokal vorhanden ist, und man diesen (nach `python -m venv venv`, danach `pip install -r requirements.txt` und `flask run --debug`) ebenfalls anzeigen kann. (Im Browser [localhost](127.0.0.1:5000) aufrufen.) Dann sieht man direkt -- ohne commit -- die durchgeführten Änderungen.


### Angabe von Links auf der Homeapge

In einer Flask-App kann man interne Links auf zwei verschiedene Arten und Weisen angeben. Entweder wie gewohnt durch Angabe von `<a href="/link/zur/seite">`, alternativ aber auch z.B. mit `<a href="{{ url_for('showdownloads', lang=lang) }}">Downloads</a> `. Hier wird also die Funktion aus `app.py` angegeben, die den Aufruf steuern soll.

### Statistsche Files

(Das sind etwa verlinkte pdfs, oder Bilder, etc.) Diese sind im Ordner `/static/` zu finden, die Ordnerstruktur ist hoffentlich intuitiv. Hier gibt es den Ordner `/data`, in dem `.json`-Dateien zu finden sind. Die Dateien `anfang.json`, `interesse.json` und `weiterbildung.json` sind die Datengrundlage der Seiten _Studieninteresse_ und _Weiterbildung_.

### Verbindung zu einer Datenbank

Die im Footer unter _TOOLS_ verlinkten Apps [mi-faq](http://mi-faq1.mathematik.privat/) (für die Seiten [Studierenden-FAQ](http://www.math.uni-freiburg.de/nlehre/de/studiendekanat/faq/) und [Mitarbeiter*innen-FAQ](http://www.math.uni-freiburg.de/nlehre/de/lehrende/faq/), aber auch [hier](http://www.math.uni-freiburg.de/nlehre/studiendekanat/pruefungsamt/) und [hier](http://www.math.uni-freiburg.de/nlehre/de/studiendekanat/studienberatung/)), [mi-vvz](http://mi-vvz1.mathematik.privat/) (für die [Veranstaltungsplanung](http://www.math.uni-freiburg.de/nlehre/de/lehrveranstaltungen/)) und [mi-news](http://mi-news1.mathematik.privat/) (für die News [hier](http://www.math.uni-freiburg.de/nlehre/) und auf dem Monitor) geben die Möglichkeit, Daten in einer Datenbank zu verändern, die dann hier wieder ausgelesen werden.


### monitor und news auf /nlehre/

Der Monitor im EG der EZ1 zeigt die News-App unter <http://mfs1.mathematik.privat:3000/> (nur im Institutsnetz). Sie holt die News als JSON von `/nlehre/api/monitor/`. Die News stehen auch auf der [Startseite](http://www.math.uni-freiburg.de/nlehre/). Den Stand zu einem bestimmten Zeitpunkt (zB der 1.7.2024 um 10 Uhr) sieht man [hier](http://www.math.uni-freiburg.de/nlehre/de/202407011000) bzw. unter <http://mfs1.mathematik.privat:3000/202407011000>.

Es folgen Beschreibungen der Apps _mi-vvz, _mi-faq_, und _mi-news_. 


## mi-vvz

Diese App dient aller Vorgänge, die mit Lehrplanung (auf Dozentenseite) zu tun hat, insbesondere der Darstellung aller Veranstaltungen. (Die Daten sind nicht mit HisInONE abgeglichen!) Es gibt folgende _Collections_ in der Datenbank, die alle geändert werden können. (Die Hilfe innerhalb jeder App, links unten unter _Dokumentation_, gibt noch mehr Auskunft.)

* Veranstaltung: Dies ist die umfangreichste Collection. Ein Eintrag regelt alles zu einer Veranstaltung, etwa Lehrpersonen, Räume, Termine, Anrechenbarkeit etc.
* Semester: Grunddaten eines Semesters
* Studiengang: Alle Studiengänge, die auf unseren Seiten auftauchen sollen.
* Terminart: zB "Vorlesung", oder "Vorbesprechung".
* Rubrik: Die Rubriken zB "Weiterführende Vorlesung", "Seminar"
* Codekategorie, Code: Jede Veranstaltung kann mit Codes versehen werden, zB "Angebot in englischer Sprache". Jeder Code hat eine Kategorie. Wichtig ist es, dass man Codekategorien (aber keine Codes direkt) auf der homepage ein- und ausblenden kann. In obigem Beispiel ist also "Sprache" die Codekategorie, und alle Codes dieser Kategorie werden angezeigt.
* Dictionary: Ein kleines Lexikon für Fachbegriffe de<->en.
* Anforderung: Eine Sache, die zu erbringen ist, um ECTS-Punkte zu bekommen, zB "Klausur", oder "Anwesenheit" oder so.
* Anforderungkategorie: Entweder PL oder SL oder Kommentar, um die Anforderungen etwas zu gliedern.
* Gebaeude/Raum: Jeder Raum ist in genau einem Gebäude, und Gebäude können URLs für Links haben.
* Modul: Alle Module aller Studiengänge
* Person: Ein Verzeichnis aller Lehrpersonen
* planung/planungsveranstaltung: Dies sind die einzelnen Einträge für die Planung weiterer Semester.


## mi-faq

Hier werden nicht die die Studierenden-, und Mitarbeiter-FAQs verwaltet, sondern auch noch kleinere Inhalte auf der Homepage, insbesondere Sprechstunden von Prüfungsamt und Studienberatung.

Mit dieser App werden unter anderem die FAQs unter
* `<lang>/studiendekanat/faq/` (FAQ für Studierende)
* `<lang>/lehrende/faq/` (FAQ für Mitarbeiter*innen)
generiert. 



## mi-news

Hier werden News verwaltet, inklusive deren Bilder und eventueller Bildrechte. Die App biete einen eingeschränkten Umfang der Bildbearbeitung, etwa die Verringerung der Bildqualität um auf eine kleinere Dateigröße zu kommen.


## Lokales Editieren der Homepage
Will man nicht online auf der github-Seite, sondern lokal die Webpage editieren, so muss man sich etwas mehr mit git auseinandersetzen. Die wichtigsten Befehle sind:
* `git clone <repo>`: Lädt ein Repository erstmals herunter
* `git pull`: Updated ein vorhandenes Repository.
* `git add --all; git commit -m "<message>; git push`: Lädt die lokalen Änderungen auf den github-Server.

Um zu starten, gibt man in einem Terminal in dem Ordner, wo der Ordner mi-hp hin soll, `git clone https://github.com/pfaffelh/mi-hp` ein. (Das repository ist öffentlich, d.h. jeder kann es herunterladen, aber nicht jeder kann es ändern.) Dies lädt alle Dateien herunter. Nach `cd mi-hp` muss man zunächst seine Berechtigung zum Ändern des Repositories hinterlegen. Hierzu sollte das Tool `gh` installiert sein. Mittels `gh auth login` startet man die Hinterlegung der Berechtigung. (Eventuell muss man hier zunächst auf der github-Seite ein login-Token erzeugen, was dann hier das Passwort ist.) Ist dies geschafft, und hat man ein paar Dateien geändert, so ändert man das Repository mit
```
git add --all
git commit -m "<message hier eingeben, was geändert worden ist>"
git push
```
Achtung! Wenn man lokal anfängt zu arbeiten, empfliehlt es sich, zunächst immer ein `git pull` auszuführen, um Änderungen anderer Nutzer auch zu bekommen.

