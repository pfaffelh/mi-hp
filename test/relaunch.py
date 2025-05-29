import requests
from bs4 import BeautifulSoup

# URL der Seite
url = 'https://uni-freiburg.de/math/'

# Passwort und Feldnamen
password = 'relaunch2024'
password_field_id = 'password_protected_pass'
submit_button_id = 'wp-submit'

# Session-Objekt verwenden, um Cookies zu speichern
session = requests.Session()

# 1. GET-Request, um die Seite zu holen
response = session.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 2. Prüfen, ob das Passwortfeld existiert
password_field = soup.find('input', id=password_field_id)

if password_field:
    print("Passwortgeschützte Seite erkannt. Sende Passwort...")

    # Das Formular hat ein action-Attribut, das wir auslesen sollten
    form = password_field.find_parent('form')
    action = form['action'] if form and form.has_attr('action') else url

    # Optional: hidden fields extrahieren (z.B. für Tokens)
    hidden_fields = form.find_all('input', type='hidden')
    payload = {field['name']: field.get('value', '') for field in hidden_fields if field.has_attr('name')}

    # Passwortfeld ergänzen
    payload[password_field['name']] = password
    payload['Submit'] = 'Weiter'  # Optional, je nach Button-Beschriftung

    # 3. POST-Request mit Passwort
    login_response = session.post(action, data=payload)

    # 4. Nach Login den Inhalt holen
    final_soup = BeautifulSoup(login_response.text, 'html.parser')
    print("Seite nach Login erfolgreich geladen!\n")
    with open("relaunch.html", "w", encoding="utf-8") as file:
        file.write(final_soup.prettify())
else:
    print("Seite ist nicht passwortgeschützt. Inhalt:\n")
    print(soup.prettify()[:1000])  # Ausgabe der ersten 1000 Zeichen


#https://uni-freiburg.de/fdmai/?password-protected=login&redirect_to=https%3A%2F%2Funi-freiburg.de%2Ffdmai
#https://uni-freiburg.de/fdmai/?password-protected=login&redirect_to=https%3A%2F%2Funi-freiburg.de%2Ffdmai%2F