### Allgemeines

Dies ist das Repository der [Lehre-Seiten des Mathematischen Instituts der Universität Freiburg](https://www.math.uni-freiburg.de/lehre/). Es handelt sich um eine Flask-App (also python), die mit einer lokalen Datenbank verbunden ist.

#### Aufbau der URLs

Der Aufbau der URLs ist fast immer `https://www.math.uni-freiburg.de/lehre/<lang>/unterpunkt/unterseite/anchor`, wobei `lang == de` oder `lang == en` die Sprache angibt. Die Templates der Unterpunkte

- interesse
- anfang
- studiengaenge
- lehrveranstaltungen
- studiendekanat
- lehrende
- downloads
  sind dabei in den entsprechenden Unterordnern von `template` zu finden. `unterseite` ist meist eine eigene html-Datei, `anchor` meist eine `id` innerhalb der html-Datei.

Eine Ausnahme sind die Seiten, die mit 
https://www.math.uni-freiburg.de/lehre/vpn/
beginnen. Diese sind nur innerhalb des vpn bzw an Institutsrechnern zugänglich. In diesem Fall bleibt der Aufbau der URL derselbe.

#### Steuerung eines Requests

Wird die Seite aufgerufen, so steuert `app.py`, was genau passiert. Hier werden auch Routen definiert, die steuern, welche Funktion aufgerufen wird, wenn ein request verarbeitet wird.

##### Änderungen an der Seite

Personen, die als Collaborator des Repositories in [github](https://github.com/pfaffelh/mi-hp) eingetragen sind, können das Repository ändern. Hier eine kurze Anleitung, wie man die neue "Lehre"-Seite ändern kann:

Die oben beschrieben muss man verstehen, dass ein `flask`-Skript (ein python-Web-Framework) die ganze Seite steuert. Weiter ist es so, dass einige Inhalte (welche das sind: siehe unten) durch andere Apps befüllt und hier nur noch ausgelesen werden. Anders als bei der restlichen Homepage des Instituts ist die "Lehre-Seite" ein "repository" auf github, das dann zwischen verschiedenen Rechnern synchronisiert wird. Die Version, die auf dem Webserver des Instituts liegt, wird angezeigt. Der Webserver sieht alle paar Minuten nach, ob sein Repository mit dem auf [github](https://github.com/pfaffelh/mi-hp) übereinstimmt. (Etwas genauer: Der Branch "Master" des Repositories wird angezeigt.) Tut es das nicht, synchronisiert er sich. Das bedeutet, dass man das Repository auf github verändern muss, damit Änderungen zum tragen kommen. Hierzu gibt es zwei Möglichkeiten, wie ganz unten beschrieben und erklärt. Die einfachere der beiden ergibt folgenden Arbeitsablauf:

1. Den [vscode-Editor](https://github.dev/pfaffelh/mi-hp) von github öffnen.
2. Änderungen durchführen und speichern.
3. Die Änderungen durch clicken auf das Symbol **unter** 🔎 in der linken Leiste und Eingabe einer ungefähren Beschreibung, woraus die Änderungen bestehen, "committen".
4. Nach ein paar Minuten sollten die Änderungen auf der [Homepage](www.math.uni-freiburg.de/lehre) sichtbar sein.

Folgende Inhalte greifen auf eine Datenbank zu, so dass sie nicht innerhalb dieses Repositories geändert werden können, sondern mittels der entsprechenden App, die für die Änderungen der Datenbank programmiert wurden. Hierbei gibt es Variablen bei der URL, wiefolgt:
* <lang> ist de oder en
* <semester> wird in der Form 2024WS eingegeben. (Andere Formate, etwa ss23, kommen auch vor, aber dann werden die angezeigten Daten nicht aus dem mi-vvz generiert.)
Es geht um folgende Apps bzw Unterseiten:
* Die News der Startseite, sowie die des Monitors, also die Seiten:
  * <lang>/
  * /test/<lang>
  * monitor/
  * monitortest/
  Diese Seiten werden von der App mi-news aus befüllt.
* Alle Details zu Veranstaltungen, also die Seiten
  * `<lang>/lehrveranstaltungen/<semester>/` (das übliche Vorlesungsverzeichnis)
  * `<lang>/lehrveranstaltungen/<semester>/stundenplan/` (dasselbe, aber sortiert nach Zeiten)
  * `/vpn/<lang>/lehrende/<semester>/planung/` (Planung für künftige Semester, nur erreichbar aus dem vpn-Netz)
  Diese Seiten werden von mi-vvz aus befüllt.
* Alle Details von FAQs, also die Seiten:
  * `<lang>>/studiendekanat/faq/` (FAQ für Studierende)
  * `<lang>/lehrende/faq/` (FAQ für Mitarbeiter*innen)
  Diese werden von mi-faq aus befüllt.
* Details zu Sprechstunden im Studiendekanaat, also
  * `<lang>/studiendekanat/` 
  * `<lang>/studiendekanat/pruefungsamt/`
  Diese Seiten werden ebenfalls von mi-faq aus befüllt.
Etwas speziell sind noch die Seiten
* `<lang>/interesse/`
* `<lang>/weiterbildung/`
Diese Daten dieser Seiten sind in `/static/data/interesse.json` und `/static/data/weiterbildung.json` gespeichert (bis auf den Vorspann). 

##### Beschreibung der beiden Möglichkeiten, Inhalte zu ändern
* (Technisch einfacher): Der von github bereitgestellte [Editor](https://github.dev/pfaffelh/mi-hp) zeigt alle Daten des Repositories an. (Etwas genauer hat er noch eine eigene Version des Repositories, deshalb immer zunächst alles "synchronisieren".) Hier kann man Dinge ändern, und speichern. Wenn man fertig ist, muss man das Repository des Editors mit dem auf github synchronisieren. (Oder seine Änderungen 'commit'ten.) Hierzu das Symbol unter der 🔎 in der linken Leiste clicken "Source control"), eine Message ungefähre Nachricht eingeben, woraus die durchgeführte Änderung besteht, und "Commit and Push" drücken. Nach ein paar Minuten synchronisiert sich der Webserver des Instituts, und die Änderungen werden angezeigt.
* (Etwas komplizierter, deshalb nur eine ganz knappe Beschreibung): Um die Änderungen im Master-Branch des Repositories durchzuführen, kann man das Repositorie auch lokal clonen (`git clone https://github.com/pfaffelh/mi-hp`), Änderungen hier durchführen, und von hier aus committen. Der Vorteil dieser Variante besteht darin, dass der zu grunde liegende python-Code dann ebenfalls lokal vorhanden ist, und man diesen (nach `python -m venv venv`, danach `pip install -r requirements.txt` und `flask run --debug`) ebenfalls anzeigen kann. (Im Browser [localhost](127.0.0.1:5000) aufrufen.) Dann sieht man direkt -- ohne commit -- die durchgeführten Änderungen.


#### Angabe von Links auf der Homeapge

In einer Flask-App kann man interne Links auf zwei verschiedene Arten und Weisen angeben. Entweder wie gewohnt durch Angabe von `<a href="/link/zur/seite">`, alternativ aber auch z.B. mit `<a href="{{ url_for('showdownloads', lang=lang) }}">Downloads</a> `. Hier wird also die Funktion aus `app.py` angegeben, die den Aufruf steuern soll.

#### Statistsche Files

(Das sind etwa verlinkte pdfs, oder Bilder, etc.) Diese sind im Ordner `/static/` zu finden, die Ordnerstruktur ist hoffentlich intuitiv. Hier gibt es den Ordner `/data`, in dem `.json`-Dateien zu finden sind. Die Dateien `anfang.json`, `interesse.json` und `weiterbildung.json` sind die Datengrundlage der Seiten _Studienanfang_, _Studieninteresse_ und _Weiterbildung_ (momentan nicht verlinkt).

#### Verbindung zu einer Datenbank

Die im Footer unter _TOOLS_ verlinkten Apps [mi-faq](http://mi-faq1.mathematik.privat/) (für die Seiten [Studierenden-FAQ](http://www.math.uni-freiburg.de/lehre/de/studiendekanat/faq/) und [Mitarbeiter*innen-FAQ](http://www.math.uni-freiburg.de/lehre/de/lehrende/faq/), aber auch [hier](http://www.math.uni-freiburg.de/lehre/studiendekanat/pruefungsamt/) und [hier](http://www.math.uni-freiburg.de/lehre/de/studiendekanat/studienberatung/)), [mi-vvz](http://mi-vvz1.mathematik.privat/) (für die [Veranstaltungsplanung](http://www.math.uni-freiburg.de/lehre/de/lehrveranstaltungen/)) und [mi-news](http://mi-news1.mathematik.privat/) (für die News [hier](http://www.math.uni-freiburg.de/lehre/) und [hier](http://www.math.uni-freiburg.de/lehre/monitor/)) geben die Möglichkeit, Daten in einer Datenbank zu verändern, die dann hier wieder ausgelesen werden.


#### monitor und news auf /lehre

Der Monitor im EG der EZ1 stellt [diese Seite](http://www.math.uni-freiburg.de/lehre/monitor/) dar. Er enthält News, genau wie die [Startseite](http://www.math.uni-freiburg.de/lehre/). Beide Seiten gibt es auch in Testversionen, nämlich [hier für die deutsche Startseite](http://www.math.uni-freiburg.de/lehre/de/test), [hier für die englische Startseite](http://www.math.uni-freiburg.de/lehre/de/test),und [hier für den Monitor]([hier für die deutsche Startseite](http://www.math.uni-freiburg.de/lehre/monitortest). 

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
* <lang>>/studiendekanat/faq/ (FAQ für Studierende)
* <lang>/lehrende/faq/ (FAQ für Mitarbeiter*innen)
generiert. 



## mi-news


#### TODOs

* mi-vvz: Deputate?
* mi-faq: Bewerbungsphasen für Studiengänge eintragen, Eintrag "news" für die Sprechstunden. faq für Studienkoordinatoren anlegen?
* mi-hp: Bildnachweise generieren, interesse und weiterbildung auch in Datenbank faq?
* Allgemein: Interne Seiten in mit-faq eintragen



Vorschläge:

* Würde es Sinn machen, das vvz um Einträge zu Deputaten zu ergänzen? Hier könnte man zB Absprachen (irgendjemand bekommt zB 4 statt 2 SWS eintragen, und mit einer Entshceidungsgrundlage versehen.)
* Würde es Sinn machen, bei den Sprechstunden ein eigenes Feld "Neuigkeiten" zu haben, bei dem man -- mit einem Ablaufdatum versehen -- etwas reinschreiben kann wie "Sprechstunde fällt am xxx aus"?



