# Repo-Kontext für Claude

Flask-App für die Webseite des Mathematischen Instituts der
Universität Freiburg. Datenquelle ist eine lokale MongoDB; gerendert
wird über Jinja-Templates mit Bootstrap 5.

## Wichtige Pfade

- `app.py` — Routen (kein `if __name__ == "__main__"`, läuft via WSGI
  über `app.wsgi`)
- `utils/util_news.py` — Wochenprogramm-Daten, Datums-Helper, Mail
- `utils/util_wp.py` — "Fake Wordpress" unter `/cd2021/<site>/`:
  lädt echte WP-Seiten, ersetzt deren Inhaltsblock durch
  `{% block content %}` und legt das Ergebnis als
  `templates/skel*.html` ab. Die dynamischen Inhalts-Templates
  (`templates/wp/*.html`) extenden dann diese Skelets.
- `templates/base_wochenprogramm.html` — Haupt-Layout für alles
  unter `/wochenprogramm/...` (Header, Offcanvas-Menü, Footer)
- `templates/wochenprogramm/` — Inhalts-Templates (`reihe.html`,
  `event.html`, `newsarchiv.html`, `calendar.ics`)
- `static/css/ufr-theme.css` — UFR-Theme (siehe unten)
- `static/css/ufr-colors.css` — vorhandene Utility-Klassen für
  UFR-Farben
- `static/images/ufr-seal.svg` — extrahiertes Universitätssiegel,
  einfarbig (Hintergrund-Deko im Menü)

## Aktiver Branch: `wp-fake`

Aktuelles Ziel: das Wochenprogramm-Layout an das Design von
**uni-freiburg.de/math** angleichen (Tailwind-basiert; wir benutzen
weiter Bootstrap 5 + eigene CSS-Variablen).

## Was schon umgesetzt ist (in `wp-fake`)

### `static/css/ufr-theme.css`
- Identity-Farben als CSS-Variablen: `--ufr-blue #34499a`,
  `--ufr-darkblue #000149`, `--ufr-yellow #ffe863`,
  `--ufr-black #2a2a2a` plus 80/60/40/20-Stufen.
- `.ufr-header` (blauer Top-Block, Padding skaliert mit
  Breakpoints 0/768/1200 px).
- `.ufr-breadcrumb-bar` — weiße Leiste **unter** dem blauen Header
  mit Breadcrumb. Keine Trennlinie unten.
- `.ufr-icon-button` — Header-Buttons als gestapelte Icon-+-Label-
  Variante, transparent, weiß, Hover = `--ufr-yellow-40`.
- `.ufr-offcanvas` — Bootstrap-Offcanvas, dunkelblauer Grund.
  Auf Desktop schmal (`min(90vw, 480px)`), auf Mobile Vollbild.
  `.ufr-menu-list` als vertikale Liste mit Trennlinien;
  `.ufr-menu-section-title` als gelber Großbuchstaben-Label;
  `.ufr-menu-sub` für Untermenüs.
  `.ufr-menu-seal` zeigt das Siegel-SVG dezent (Opacity 0.12) im
  Hintergrund rechts.
  `.ufr-menu-footer` mit Impressum / Datenschutz / Barrierefreiheit
  am Ende.
- `.ufr-mobile-bar` — feste untere Action-Bar (nur <768 px) mit
  Sprache, Vorträge, Institut. Body bekommt `padding-bottom: 81px`.
- `.ufr-modal` — generisches Content-Modal: blaue Header-Leiste,
  weißer Body, X-Schließen-Button (weiß gefiltert) absolute oben
  rechts im Header. Wird in `reihe.html` / `event.html` benutzt.
- `.ufr-lang-modal` — kompaktes blaues Modal (520 px), nur für den
  Sprachwechsler.
- `.ufr-footer` mit kompletter uni-freiburg-Struktur:
  zentrierte Linkleiste, Institutsadresse, weißer Trennstrich
  (h-2 w-32), UFR-Logo, Universitäts-Anschriften.
- Override von Bootstrap `.btn-primary` → weiß mit 3 px schwarzem
  Rahmen, Hover = Unterstreichen, kein Border-Radius.
  Damit übernehmen alte Templates den neuen Look ohne Anpassung.
- Override von `.lecture-module-button` analog mit gelblichem Hover.

### `templates/base_wochenprogramm.html`
- Blauer Header oben mit UFR-Logo links, rechts zwei
  Icon-Buttons: **Sprache** (öffnet `#ufrLangModal`) und **Menü**
  (öffnet `#ufrMenu` Offcanvas). Auf Mobile sind beide ausgeblendet
  (Bottom-Bar übernimmt).
- Breadcrumb-Bar (weiß) direkt darunter.
- Offcanvas `#ufrMenu` mit Siegel-SVG-Hintergrund + `{% block navbar %}`.
- Modal `#ufrLangModal` mit Globe-Icon-Links Deutsch / English,
  aktive Sprache in Gelb.
- `<main id="main-content">` mit Breakpoint-skaliertem Top-Padding.
- Mobile-Bar (`<ul class="ufr-mobile-bar">`) mit Sprache, Vorträge,
  Institut.
- Footer-HTML komplett ersetzt (siehe oben).

### `templates/navbar_wochenprogramm.html`
- Vertikale Liste für das Offcanvas-Menü. Sektionen:
  Alle Vorträge / Vortragsreihen (mit Sub-Items aus `reihen`) /
  Events (mit Sub-Items aus `events`) / News-Archiv / FAQ.
- `.ufr-menu-footer` mit Impressum / Datenschutz / Barrierefreiheit
  am Ende.

### `templates/wochenprogramm/reihe.html`, `event.html`
- Vortrags-Modale verwenden jetzt `.ufr-modal`-Klasse:
  X-Schließen-Button im blauen Header oben rechts; der frühere
  `btn btn-secondary` "Schließen" / "Close" am Ende ist entfernt.

## Vorher-Stand (master)

Der `master`-Branch hat das frühere Bootstrap-Design mit horizontaler
Navbar (`bg-ufr-darkblue`, dropdown-basiert). Die gerade
beschriebenen Änderungen liegen alle auf `wp-fake` und sind noch
nicht gemergt.

## Wochenansicht (bereits in `master` gemergt)

In `utils/util_news.py::get_wochenprogramm_full` wird ein 7-Tage-Range
(Mo→Mo) erkannt; setzt `data["zeitraum"]` als
`9.3.-15.3.2026` (DE) bzw. `March 9-15, 2026` (EN), Datum
inklusive Mo-So. `data["anfangcurrentweek"]` /
`data["anfangnextweek"]` sind verfügbar; in `reihe.html` gibt es
einen Button "Wochenansicht" / "Weekly view".

## Jinja-Smoke-Test

Schnell-Validierung aller Templates ohne MongoDB:

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
             'wochenprogramm/event.html', 'home_news.html']:
    try:
        env.get_template(name)
        print(f'OK: {name}')
    except Exception as e:
        print(f'FAIL: {name}: {e}')
"
```

## Konventionen

- Commit-Messages auf Deutsch, knapp; Co-Authored-By-Footer mit
  `Claude Opus 4.7 (1M context)`.
- Keine Push-/Merge-Aktionen ohne explizite Freigabe.
- Branches werden nach explizitem Wunsch des Users gelöscht.
- VPN-Variante: `vpn = True` setzt im Footer/Menü zusätzliche
  Tools-Links frei.
