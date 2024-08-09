### Allgemeines

Dies ist das Repository der [Lehre-Seiten des Mathematischen Instituts der Universität Freiburg](https://www.math.uni-freiburg.de/lehre/). Es handelt sich um eine Flask-App (also python), die mit einer lokalen Datenbank verbunden ist.

#### Aufbau der URLs

Der Aufbau der URLs ist immer `https://ww.math.uni-freiburg.de/lehre/<lang>/unterpunkt/unterseite/anchor`,
wobei `lang == de` oder `lang == en` die Sprache angibt. Die Templates der Unterpunkte

- interesse
- anfang
- studiengaenge
- lehrveranstaltungen
- studiendekanat
- lehrende
- downloads
  sind dabei in den entsprechenden Unterordnern von `template` zu finden. `unterseite` ist meist eine eigene html-Datei, `anchor` meist eine `id` innerhalb der html-Datei.

#### Steuerung eines Requests

Wird die Seite aufgerufen, so steuert `app.py`, was genau passiert. Hier werden auch Routen definiert, die steuern, welche Funktion aufgerufen wird, wenn ein request verarbeitet wird.

#### Angabe von Links

In einer Flask-App kann man interne Links auf zwei verschiedene Arten und Weisen angeben. Entweder wie gewohnt durch Angabe von `<a href="/link/zur/seite">`, alternativ aber auch z.B. mit `<a href="{{ url_for('showdownloads', lang=lang) }}">Downloads</a> `. Hier wird also die Funktion aus `app.py` angegeben, die den Aufruf steuern soll.

#### Statistsche Files

(Das sind etwa verlinkte pdfs, oder Bilder, etc.) Diese sind im Ordner `/static/` zu finden, die Ordnerstruktur ist hoffentlich intuitiv. Hier gibt es den Ordner `/data`, in dem `.json`-Dateien zu finden sind. Die Dateien `anfang.json`, `interesse.json` und `weiterbildung.json` sind die Datengrundlage der Seiten _Studienanfang_, _Studieninteresse_ und _Weiterbildung_ (momentan nicht verlinkt).

#### Verbindung zu einer Datenbank

Die im Footer unter _TOOLS_ verlinkten Apps [mi-faq](http://mi-faq1.mathematik.privat/) (für die Seiten [Studierenden-FAQ](http://www.math.uni-freiburg.de/lehre/de/studiendekanat/faq/) und [Mitarbeiter*innen-FAQ](http://www.math.uni-freiburg.de/lehre/de/lehrende/faq/), aber auch [hier](http://www.math.uni-freiburg.de/lehre/studiendekanat/pruefungsamt/) und [hier](http://www.math.uni-freiburg.de/lehre/de/studiendekanat/studienberatung/)), [mi-vvz](http://mi-vvz1.mathematik.privat/) (für die [Veranstaltungsplanung](http://www.math.uni-freiburg.de/lehre/de/lehrveranstaltungen/)) und [mi-news](http://mi-news1.mathematik.privat/) (für die News [hier](http://www.math.uni-freiburg.de/lehre/) und [hier](http://www.math.uni-freiburg.de/lehre/monitor/)) geben die Möglichkeit, Daten in einer Datenbank zu verändern, die dann hier wieder ausgelesen werden.


#### monitor und news auf /lehre

Der Monitor im EG der EZ1 stellt [diese Seite](http://www.math.uni-freiburg.de/lehre/monitor/) dar. Er enthält News, genau wie die [Startseite](http://www.math.uni-freiburg.de/lehre/). Beide Seiten gibt es auch in Testversionen, nämlich [hier für die deutsche Startseite](http://www.math.uni-freiburg.de/lehre/de/test), [hier für die englische Startseite](http://www.math.uni-freiburg.de/lehre/de/test),und [hier für den Monitor]([hier für die deutsche Startseite](http://www.math.uni-freiburg.de/lehre/monitortest). 


#### TODOs

* mi-news, mi-faq: User eintragen, der eine News oder einen FAQ-Eintrag zuletzt bearbeitet hat.
* mi-vvz: Zukünftige Planung, Deputate?
* mi-hp: Ansicht Lehrveranstaltungen mit row, nicht mit table
+ mi-faq: Bewerbungsphasen für Studiengänge eintragen