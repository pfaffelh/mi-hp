# Repo-Kontext für Claude

Flask-App für die Webseite des Mathematischen Instituts der
Universität Freiburg. Datenquelle ist eine lokale MongoDB; gerendert
wird über Jinja-Templates mit Bootstrap 5.

## Wichtige Pfade

- `app.py` — Routen (kein `if __name__ == "__main__"`, läuft via WSGI
  über `app.wsgi`)
- `utils/util_news.py` — Wochenprogramm-Daten, Datums-Helper, Mail.
  Enthält `_FALLBACK_EN`-Mapping in `getwl()` für Strings, deren
  englischer Titel in der DB fehlt.
- `utils/util_wp.py` — "Fake Wordpress" unter `/cd2021/<site>/`:
  lädt echte WP-Seiten, ersetzt deren Inhaltsblock durch
  `{% block content %}` und legt das Ergebnis als
  `templates/skel*.html` ab. Inhalts-Templates in
  `templates/wp/*.html` extenden diese Skelets.
- `templates/base_wochenprogramm.html` — Haupt-Layout für alles
  unter `/wochenprogramm/...`
- `templates/base_nlehre.html` — Haupt-Layout für alles unter
  `/nlehre/...` (noch nicht migriert, siehe unten)
- `static/css/ufr-theme.css` — UFR-Theme (CSS-Variablen, Header,
  Footer, Buttons, Akkordeon, Modals, Mobile-Bar, News-Cards)
- `static/css/ufr-colors.css` — bestehende Utility-Klassen
- `static/images/ufr-logo-black.svg` — schwarze Variante des
  UFR-Schriftzugs für den weißen Header
- `static/images/ufr-logo-white.svg` — weiße Variante (Footer)
- `static/images/ufr-seal.svg` — extrahiertes Universitätssiegel,
  einfarbig (Hintergrund-Deko im Menü)

## Status branches

- **master** — produktiv. Enthält die Wochenansicht (commit
  `0d1582c`, "Wochenanzeige Mo–So statt Mo–Mo").
- **wp-fake** — UFR-Theme für die Wochenprogramm-Seiten. Komplett
  fertig, noch nicht gemergt. Sollte vor dem Lehre-Umbau gemergt
  werden, damit das CSS für alle nutzbar ist.

## Was auf `wp-fake` umgesetzt ist (alle Wochenprogramm-Seiten)

Vorbild: <https://uni-freiburg.de/math/> und
<https://uni-freiburg.de/forschung/forschungsprofil/sprachen-des-wissens/>.

### `static/css/ufr-theme.css` — vollständiges Theme
- Identity-Farben als CSS-Variablen: `--ufr-blue #34499a`,
  `--ufr-darkblue #000149`, `--ufr-yellow #ffe863`,
  `--ufr-black #2a2a2a` plus 80/60/40/20-Stufen
- `.ufr-header` — **weißer** Top-Block mit großem schwarzen Logo
  links und Icon-Buttons rechts. Padding 25/42/70 px je Breakpoint
- `.ufr-breadcrumb-bar` — weiße Leiste unter dem Header,
  Hierarchie: Universität Freiburg › Fakultät für Mathematik und
  Physik › Mathematisches Institut › Wochenprogramm
- `.ufr-icon-button` — Sprache & Menü oben rechts als gestapelte
  Icon-+-Label-Buttons (schwarz, Hover identity-blue-80)
- `.ufr-offcanvas` — Bootstrap-Offcanvas, dunkelblau, schmal
  (`min(90vw, 480px)`) auf Desktop, vollflächig auf Mobile.
  Mit dezent eingeblendetem Siegel-SVG im Hintergrund
- `.ufr-mobile-bar` — feste untere Action-Bar (<768 px) mit
  Sprache, Vorträge, Institut. Body bekommt
  `padding-bottom: 81px` über `.has-ufr-bottom-bar`
- `.ufr-modal` — Content-Modal (z. B. ehemals Vorträge): blauer
  Header, weißer Body, X-Schließen-Button absolut oben rechts.
  Bleibt für künftige Nutzung im Theme.
- `.ufr-lang-modal` — kompaktes blaues Modal (520 px) für den
  Sprachwechsler
- `.ufr-accordion` + `.ufr-accordion-item` + `.ufr-accordion-header`
  + `.ufr-accordion-chevron` + `.ufr-accordion-body` — vertikales
  Akkordeon mit 3 px schwarzen Linien, großem rotierenden Chevron.
  Variante `.ufr-accordion--nested` für verschachtelte Listen
  (1 px identity-blue-40, kleinerer Chevron, kompakter)
- `.ufr-accordion-link` — Inline-Link-Button mit Icon im
  Akkordeon-Body
- `.ufr-news-item` — Flex-Karte für News (Bild fix 240 px,
  max 220 px hoch, `object-fit: contain`; alternierend Bild
  links/rechts via `.is-reversed`; Today-Highlight via `.is-today`;
  Mobile <576 px stackt vertikal)
- `.ufr-footer` — komplette uni-freiburg.de-Struktur:
  zentrierte Linkleiste, Institutsadresse, weißer Trennstrich
  (`h-2 w-32`), UFR-Logo, Universitäts-Anschriften
- Override von Bootstrap `.btn-primary` → weiß mit 3 px schwarzem
  Rahmen, Hover = Unterstreichen, kein Border-Radius

### `templates/base_wochenprogramm.html`
- Weißer Header mit großem schwarzen Logo links, rechts zwei
  Icon-Buttons: **Sprache** (öffnet `#ufrLangModal`) und **Menü**
  (öffnet `#ufrMenu` Offcanvas). Auf Mobile sind beide ausgeblendet
  (Bottom-Bar übernimmt)
- Breadcrumb-Bar (weiß, vier Ebenen tief) direkt darunter
- Offcanvas `#ufrMenu` mit Siegel-SVG-Hintergrund + `{% block navbar %}`
- Modal `#ufrLangModal` mit Globe-Icon-Links Deutsch / English,
  aktive Sprache in Gelb
- `<main id="main-content">` mit Breakpoint-skaliertem Top-Padding
- Mobile-Bar (`<ul class="ufr-mobile-bar">`) mit Sprache, Vorträge,
  Institut
- Footer-HTML komplett im uni-freiburg.de-Stil

### `templates/navbar_wochenprogramm.html`
- Vertikale Liste für das Offcanvas-Menü. Sektionen:
  Alle Vorträge / Vortragsreihen (mit Sub-Items aus `reihen`) /
  Events (mit Sub-Items aus `events`) / News-Archiv / FAQ
- `.ufr-menu-footer` mit Impressum / Datenschutz / Barrierefreiheit
  am Ende

### `templates/wochenprogramm/reihe.html`, `event.html`
- Vorträge und Events als `.ufr-accordion-item`. Geschlossen:
  Reihe + Sprecher:Titel + Datum/Zeit/Ort. Geöffnet: Speaker-
  Headline (verlinkt wenn url), Link-Button, Zeit/Ort, Abstract,
  Kommentar. Modale komplett raus.

### `templates/accordion_wochenprogramm.html` (FAQ)
- Outer-Akkordeon (k1) im großen Stil
- Inner-Akkordeon (k2) mit `.ufr-accordion--nested`
- "Alles ausklappen / einklappen" oben bleibt funktional
  (`?show=all` / `?show=`)
- IDs `{{k2.kurzname}}_q` für scrollIntoView aus base bleiben

### `templates/wochenprogramm/newsarchiv.html`
- Flex-Layout statt Bootstrap-Spalten + Floats. Bilder bleiben
  egal welche DB-Metadaten in einem 240×220-Rahmen.
  `widthmonitor` und `stylemonitor` aus der DB werden ignoriert

## Plan: Lehre-Seiten (`/nlehre/...`) als nächster Schritt

Was ist betroffen? Alles was `base_nlehre.html` extendet:

- `templates/home_nlehre.html` — Startseite Lehre
- `templates/accordion_nlehre.html` — FAQ-artige Akkordeon-Seiten
- `templates/lehrveranstaltungen/vvz.html` (und Varianten:
  `vvz_planung`, `vvz_personenplan`, `vvz_person`,
  `vvz_schwerpunkt`, `vvz_stundenplan`, `vvz_alt`)
- `templates/lehrende/index.html`,
  `templates/lehrende/zertifikat-hochschullehre.html`
- `templates/studiendekanat/index.html`,
  `studiendekanat/calendar_plan.html`,
  `studiendekanat/calendar_pruefungen.html`,
  `studiendekanat/calendarliste.html`

Routes in `app.py` (Section "Home page"): `/nlehre/`,
`/nlehre/<lang>/page/<kurzname>/...`, `/nlehre/<lang>/lexikon/`,
`/nlehre/<lang>/bildnachweis/`, `/nlehre/<lang>/interesse/...`,
`/nlehre/<lang>/anfang/...` und weitere.

### Empfohlenes Vorgehen

1. **wp-fake nach master mergen** (oder cherry-pick), damit das
   Theme `static/css/ufr-theme.css` global nutzbar ist.
2. **Neuen Branch `nlehre-theme` anlegen**.
3. **`base_nlehre.html` parallel zu `base_wochenprogramm.html`
   umbauen.** Großer Teil ist 1:1 kopierbar (Header, Footer,
   Offcanvas, Mobile-Bar, Sprach-Modal). Nur Breadcrumb-Endpunkt
   und das `{% block navbar %}` müssen lehre-spezifisch sein.
4. **`navbar_nlehre.html` neu strukturieren** als vertikale Liste
   im UFR-Stil. Inhalt klären — was sind die top-level Lehre-
   Items? Vorlesungsverzeichnis, Lehrende, Studiendekanat,
   FAQ, …?
5. **`accordion_nlehre.html`** auf `.ufr-accordion` umstellen
   (analog zu `accordion_wochenprogramm.html`).
6. **VVZ-Templates** (`lehrveranstaltungen/vvz*.html`) prüfen —
   das sind oft tabellen- oder listen-basierte Ansichten von
   Veranstaltungsdaten. Hier ggf. Tabellen oder Karten-Layouts
   im UFR-Stil anwenden, ähnlich wie das News-Archiv.
7. **Studiendekanat-Kalender** (`calendar_*`) — falls FullCalendar
   o. ä. genutzt wird, evtl. nur die Drumherum-Optik anpassen.

### Mögliche Stolperfallen

- `base_nlehre.html` hat eigene Inline-Styles (Container-Größen,
  `.btn:focus`, Breakpoint-Spielereien). Beim Umbau ggf. in
  `ufr-theme.css` ziehen oder entfernen.
- Die VVZ-Templates haben oft komplexe Daten-Structures
  (Schwerpunkte, Personenpläne); vor Layout-Änderung kurz das
  Daten-Modell in `utils/util_vvz.py` checken.
- Bestehende Dropdown-Navbars in `navbar_nlehre.html` müssen in
  Offcanvas-Sektionen übersetzt werden.

## Konventionen

- Commit-Messages auf Deutsch, knapp; Co-Authored-By-Footer mit
  `Claude Opus 4.7 (1M context)`.
- Keine Push-/Merge-Aktionen ohne explizite Freigabe.
- Branches werden nach explizitem Wunsch gelöscht.
- VPN-Variante: `vpn = True` setzt im Footer/Menü zusätzliche
  Tools-Links frei.
- Bei Übersetzungslücken bevorzugt `_FALLBACK_EN` in
  `utils/util_news.py::getwl` ergänzen, statt im Template
  hartzucodieren.

## Jinja-Smoke-Test (ohne MongoDB)

```bash
python3 -c "
import sys
sys.path.insert(0, '/home/pfaffelh/Code/mi/mi-hp')
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('/home/pfaffelh/Code/mi/mi-hp/templates'))
env.filters['markdown'] = lambda x: x
env.filters['safe'] = lambda x: x
env.globals['url_for'] = lambda *a, **kw: '#'
env.globals['url_for_self'] = lambda **kw: '#'
for name in ['base_wochenprogramm.html', 'navbar_wochenprogramm.html',
             'accordion_wochenprogramm.html', 'wochenprogramm/reihe.html',
             'wochenprogramm/event.html', 'wochenprogramm/newsarchiv.html',
             'home_news.html',
             'base_nlehre.html', 'navbar_nlehre.html',
             'accordion_nlehre.html']:
    try:
        env.get_template(name)
        print(f'OK: {name}')
    except Exception as e:
        print(f'FAIL: {name}: {e}')
"
```

## Wochenansicht (bereits in `master` gemergt)

In `utils/util_news.py::get_wochenprogramm_full` wird ein 7-Tage-
Range (Mo→Mo) erkannt; setzt `data["zeitraum"]` als z. B.
`9.3.-15.3.2026` (DE) bzw. `March 9-15, 2026` (EN), Datum
inklusive Mo–So. Verfügbare Felder:
`data["anfangcurrentweek"]` / `data["anfangnextweek"]`. In
`reihe.html` gibt es einen Button "Wochenansicht" / "Weekly view".
