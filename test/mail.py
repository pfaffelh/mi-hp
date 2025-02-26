import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import netrc

netrc = netrc.netrc()

smtp_user, _, smtp_password = netrc.authenticators("mail.uni-freiburg.de")
print("User: " + smtp_user)
print("Password: " + smtp_password)

empfaenger_email = "pfaffelh@gmail.com"  # Empfänger-E-Mail-Adresse

def send_html_email(empfaenger_email, betreff, html_inhalt, absender_email=smtp_user, absender_passwort=smtp_password):
    """
    Versendet eine E-Mail mit HTML-Inhalt über einen SMTP-Server mit SSL-Verbindung.
    """
    try:
        with smtplib.SMTP_SSL("mail.uni-freiburg.de", 465) as server:
            server.login(absender_email, absender_passwort)

            # E-Mail-Nachricht erstellen (MIMEMultipart für HTML-Inhalt)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = betreff
            msg['From'] = absender_email
            msg['To'] = empfaenger_email

            # HTML-Inhalt hinzufügen
            html_part = MIMEText(html_inhalt, 'html')
            msg.attach(html_part)

            server.send_message(msg)
            print("E-Mail mit HTML-Inhalt erfolgreich versendet!")

    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")

# Beispiel-Nutzung
empfaenger_email = "pfaffelh@gmail.com"
betreff = "Test-E-Mail mit HTML 2"
html_inhalt = """
<html>
<body>
    <h1>Hallo Welt!</h1>
    <p>Dies ist eine E-Mail mit <strong>HTML</strong>-Inhalt.</p>
    <a href="https://www.example.com">Klicke hier für weitere Informationen</a>
</body>
</html>
"""

send_html_email(empfaenger_email, betreff, html_inhalt)

