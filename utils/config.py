import socket
import netrc
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if (ip_address == "127.0.1.1"):
    netrc = netrc.netrc()
elif os.getcwd() == "/home/flask-reader/mi-hp":
    netrc = netrc.netrc("/home/flask-reader/netrc")
else:
    netrc = netrc.netrc("/usr/local/lib/mi-hp/.netrc")

weekday = {
    "Montag": "Mo",
    "Dienstag": "Di",
    "Mittwoch": "Mi",
    "Donnerstag": "Do",
    "Freitag": "Fr",
    "Samstag": "Sa",
    "Sonntag": "So",    
}
semester_dict = {
    "ss24": {"name": "Sommersemester 2024"},
    "ws2324": {"name": "Wintersemester 2023/24"},
    "ss23": {"name": "Sommersemester 2023"},
    "ws2223": {"name": "Wintersemester 2022/23"},
    "ss22": {"name": "Sommersemester 2022"},
    "ws2122": {"name": "Wintersemester 2021/22"},
    "ss21": {"name": "Sommersemester 2021"},
    "ws2021": {"name": "Wintersemester 2020/21"},
    "ss20": {"name": "Sommersemester 2020"},
    "ws1920": {"name": "Wintersemester 2019/20"},
    "ss19": {"name": "Sommersemester 2019"},
    "ws1819": {"name": "Wintersemester 2018/19"}
}

semester_dict_old = {
    "ss24": {"name": "Sommersemester 2024"},
    "ws2324": {"name": "Wintersemester 2023/24"},
    "ss23": {"name": "Sommersemester 2023"},
    "ws2223": {"name": "Wintersemester 2022/23"},
    "ss22": {"name": "Sommersemester 2022"},
    "ws2122": {"name": "Wintersemester 2021/22"},
    "ss21": {"name": "Sommersemester 2021"},
    "ws2021": {"name": "Wintersemester 2020/21"},
    "ss20": {"name": "Sommersemester 2020"},
    "ws1920": {"name": "Wintersemester 2019/20"},
    "ss19": {"name": "Sommersemester 2019"},
    "ws1819": {"name": "Wintersemester 2018/19"},
    "ss18": {"name": "Sommersemester 2018"},
    "ws1718": {"name": "Wintersemester 2017/18"},
    "ss17": {"name": "Sommersemester 2017"},
    "ws1617": {"name": "Wintersemester 2016/17"},
    "ss16": {"name": "Sommersemester 2016"},
    "ws1516": {"name": "Wintersemester 2015/16"},
    "ss15": {"name": "Sommersemester 2015"},
    "ws1415": {"name": "Wintersemester 2014/15"},
    "ss14": {"name": "Sommersemester 2014"},
    "ws1314": {"name": "Wintersemester 2013/14"},
    "ss13": {"name": "Sommersemester 2013"},
    "ws1213": {"name": "Wintersemester 2012/13"},
    "ss12": {"name": "Sommersemester 2012"},
    "ws1112": {"name": "Wintersemester 2011/12"},
    "ss11": {"name": "Sommersemester 2011"},
    "ws1011": {"name": "Wintersemester 2010/11"},
    "ss10": {"name": "Sommersemester 2010"},
    "ws0910": {"name": "Wintersemester 2009/10"},
    "ss09": {"name": "Sommersemester 2009"},
    "ws0809": {"name": "Wintersemester 2008/09"},
    "ss08": {"name": "Sommersemester 2008"},
    "ws0708": {"name": "Wintersemester 2007/08"},
    "ss07": {"name": "Sommersemester 2007"},
    "ws0607": {"name": "Wintersemester 2006/07"}
}

for key, value in semester_dict_old.items():
    try:
        app.open_resource('static/pdf/lehrveranstaltungen/'+key+'.pdf')
        semester_dict_old[key]["komm_exists"] = True
    except:
        semester_dict_old[key]["komm_exists"] = False
    try:
        app.open_resource('static/pdf/lehrveranstaltungen/' + key + '_' + lang + '.pdf')
        semester_dict_old[key]["komm_lang_exists"] = True
    except:
        semester_dict_old[key]["komm_lang_exists"] = False

    try:
        app.open_resource('static/pdf/lehrveranstaltungen/'+key+'mh.pdf')
        semester_dict_old[key]["mh_exists"] = True
    except:
        semester_dict_old[key]["mh_exists"] =False

    try:
        app.open_resource('static/pdf/lehrveranstaltungen/' + key + 'mh_' + lang + '.pdf')
        semester_dict_old[key]["mh_lang_exists"] = True
    except:
        semester_dict_old[key]["mh_lang_exists"] =False

    try:
        app.open_resource('static/pdf/lehrveranstaltungen/'+key+'verw.pdf')
        semester_dict_old[key]["verw_exists"] = True
    except:
        semester_dict_old[key]["verw_exists"] =False


calendar_host = "cal.mathematik.privat/davical/caldav.php/"
cal_username, cal_account, cal_password = netrc.authenticators(calendar_host)
sondertermine_lehre_calendar_url = "http://cal.mathematik.privat/davical/caldav.php/pruefungsamt/pramt/"

# Mensaplan für Monitor
mensaplan_host = "https://www.swfr.de/"
try:
    mensa_username, mensa_account, mensa_password = netrc.authenticators(mensaplan_host)
except:
    mensa_password = ""
mensaplan_url = mensaplan_host + "apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]=" + mensa_password + "&&tx_speiseplan_pi1[ort]=620"

# Mailversand
smtp_user, _, smtp_password = netrc.authenticators("mail.uni-freiburg.de")
empfaenger_email = "mathkoll@math.uni-freiburg.de" # Empfänger-E-Mail-Adresse für das Wocheprogramm
#empfaenger_email = "p.p@stochastik.uni-freiburg.de"  
mail_template = "../static/mail/wochenprogrammmail.html"
anfang_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(days=1)
anfang = anfang_date.strftime('%Y%m%d')
end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + relativedelta(days=7)
end = end_date.strftime('%Y%m%d')
kurzname = "alle"
lang = "de"
betreff = f"Wochenprogramm {anfang_date.strftime('%-d.%-m')} bis {end_date.strftime('%-d.%-m')}"

studiengaenge = {"all": "alle Studiengänge",
                    "bsc": "Bachelor of Science Mathematik",
                    "2hfb": "Zwei-Hauptfächer-Bachelor",
                    "msc": "Master of Science Mathematik",
                    "mscdata": "Master of Science Mathematics in Data and Technology", 
                    "med": "Master of Education Mathematik",
                    "mederw": "Master of Education Mathematik Erweiterungsfach",
                    "meddual": "Masterstudiengang Lehramt Gymnasium – dual"
                    }

bewerbungsdaten = {
    "bsc": [{"start": "01.08.", "end": "30.10."}],
    "msc": [{"start": "01.06.", "end": "15.09."}, {"start": "01.02.", "end": "15.03."}],
    "mscdata": [{"start": "01.06.", "end": "15.09."}]
}

wochentage = {
    "Montag": "Monday",
    "Dienstag": "Tuesday",
    "Mittwoch": "Wednesday",
    "Donnerstag": "Thursday",
    "Freitag": "Friday",
    "Samstag": "Saturday",
    "Sonntag": "Sunday"
}

tage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

def tage_lang(lang):
    tage_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    tage_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return tage_de if lang == "de" else tage_en


calendars = [
    { "kurzname" : "wochenprogramm",
      "name_de" : "Wochenprogramm",
      "name_en" : "Talks",
      "color" : "#2ca02c",
    },
    { "kurzname" : "studiendekanat",
      "name_de" : "Studiendekanat",
      "name_en" : "Program coordination",
      "color": "#ff7f0e",
    },
    { "kurzname" : "semesterplan",
      "name_de" : "Semesterplan",
      "name_en" : "Semester schedule",
      "color" : "#1f77b4",
    },
    { "kurzname" : "pruefungen",
      "name_de" : "Prüfungen",
      "name_en" : "Exams",
      "color" : "#9467bd"
    },
    { "kurzname" : "promotion",
      "name_de" : "Disputationen",
      "name_en" : "PhD exams",
      "color" : "#bcbd22"
    },
]

def get_contrasting_text_color(hex_color):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    # Convert hex to RGB
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    # Calculate luminance (per W3C)
    luminance = (0.299 * r + 0.587 * g + 0.114 * b)
    # Return white for dark backgrounds, black for light backgrounds
    return '#ffffff' if luminance < 128 else '#000000'

def format_termin(t):
    if t["datum"].time() == datetime.min.time():
        res = t["name"]
    else:
        res = f"{t['datum'].strftime('%H:%M')}: {t['name']}"
    return res    

from datetime import datetime, timedelta

def formatDateForGoogle(start, end, allDay):
    if not isinstance(end, datetime):
        end = datetime.combine(end, datetime.min.time())
    if allDay:
        start_str = start.strftime('%Y%m%d')
        # Google erwartet das Enddatum exklusiv → +1 Tag
        end = end if start <= end else start
        end_str = (end + timedelta(days=1)).strftime('%Y%m%d')
        end_str = end.strftime('%Y%m%d')
    else:
        # Ohne Zeitzone (lokal)
        start_str = start.strftime('%Y%m%dT%H%M%S')
        end_str = end.strftime('%Y%m%dT%H%M%S')
    
    return f"{start_str}/{end_str}"

def formatDateForIcs(start, end, allDay):
    if not isinstance(end, datetime):
        end = datetime.combine(end, datetime.min.time())
    if allDay:
        start_str = start.strftime('%Y%m%d')
        # ics erwartet das Enddatum exklusiv → +1 Tag
        end = end if start <= end else start
        end_str = (end + timedelta(days=1)).strftime('%Y%m%d')
        # end_str = end.strftime('%Y%m%d')
        res = f"DTSTART;VALUE=DATE:{start_str}\nDTEND;VALUE=DATE:{end_str}"
    else:
        # Ohne Zeitzone (lokal)
        start_str = start.strftime('%Y%m%dT%H%M%S')
        end_str = end.strftime('%Y%m%dT%H%M%S')
        res = f"DTSTART:{start_str}\nDTEND:{end_str}"
    
    return res

