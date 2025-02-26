import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from dateutil.relativedelta import relativedelta
import latex2markdown
from markdown import markdown
import utils.util_news as news
from utils.config import *

smtp_user, _, smtp_password = netrc.authenticators("mail.uni-freiburg.de")
empfaenger_email = "pfaffelh@gmail.com"  # Empfänger-E-Mail-Adresse

def send_email(empfaenger_email, betreff, template_html, absender_email, absender_passwort, **data):
    """
    Versendet E-Mails mit einer Jinja2-Vorlage an mehrere Empfänger.
    """
    try:
        with smtplib.SMTP_SSL("mail.uni-freiburg.de", 465) as server:
            server.login(absender_email, absender_passwort)

            with open(template_html, 'r') as f:
                vorlage = Template(f.read())
            # E-Mail-Nachricht erstellen (MIMEMultipart für HTML-Inhalt)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = betreff
            msg['From'] = absender_email
            msg['To'] = empfaenger_email  # Individueller Empfänger

            # Vorlage mit Daten füllen
            print(data)
            print("de")
            html_inhalt = vorlage.render(lang = "de", **data)

            # HTML-Inhalt hinzufügen
            html_part = MIMEText(html_inhalt, 'html')
            msg.attach(html_part)

            server.send_message(msg)
            print(f"E-Mail an {empfaenger_email} erfolgreich versendet!")

    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")


empfaenger_email = "pfaffelh@gmail.com"
template_html = "templates/wochenprogramm/wochenprogrammmail.html"

anfang_date = datetime.now()
anfang = anfang_date.strftime('%Y%m%d')
end_date = datetime.now() + relativedelta(months=3)
end = end_date.strftime('%Y%m%d')

kurzname = "alle"
lang = "de"

data = news.get_wochenprogramm_full(anfang, end, kurzname, lang)
print(data)

betreff = f"Wochenprogramm {anfang_date.strftime('%d.%m')} bis {end_date.strftime('%d.%m')}"
print(betreff)

send_email(empfaenger_email, betreff, template_html, smtp_user, smtp_password, **data)


