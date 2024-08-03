import socket
import netrc
import os
from datetime import datetime

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
    "ss18": "Sommersemester 2018",
    "ws1718": "Wintersemester 2017/18",
    "ss17": "Sommersemester 2017",
    "ws1617": "Wintersemester 2016/17",
    "ss16": "Sommersemester 2016",
    "ws1516": "Wintersemester 2015/16",
    "ss15": "Sommersemester 2015",
    "ws1415": "Wintersemester 2014/15",
    "ss14": "Sommersemester 2014",
    "ws1314": "Wintersemester 2013/14",
    "ss13": "Sommersemester 2013",
    "ws1213": "Wintersemester 2012/13",
    "ss12": "Sommersemester 2012",
    "ws1112": "Wintersemester 2011/12",
    "ss11": "Sommersemester 2011",
    "ws1011": "Wintersemester 2010/11",
    "ss10": "Sommersemester 2010",
    "ws0910": "Wintersemester 2009/10",
    "ss09": "Sommersemester 2009",
    "ws0809": "Wintersemester 2008/09",
    "ss08": "Sommersemester 2008",
    "ws0708": "Wintersemester 2007/08",
    "ss07": "Sommersemester 2007",
    "ws0607": "Wintersemester 2006/07"
}

calendar_host = "cal.mathematik.privat/davical/caldav.php/"
cal_username, cal_account, cal_password = netrc.authenticators(calendar_host)
sondertermine_lehre_calendar_url = "http://cal.mathematik.privat/davical/caldav.php/pruefungsamt/pramt/"

mensaplan_host = "https://www.swfr.de/"
try:
    mensa_username, mensa_account, mensa_password = netrc.authenticators(mensaplan_host)
except:
    mensa_password = ""
mensaplan_url = mensaplan_host + "apispeiseplan?&type=98&tx_speiseplan_pi1[apiKey]=" + mensa_password + "&&tx_speiseplan_pi1[ort]=620"


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



#    qa_pairs = {}
#    for cat_kurzname in cats_kurzname:
#        y = qa.find({"category": cat_kurzname}, sort=[("rang", pymongo.ASCENDING)])
#        res = []
#        for x in y:
#            a = f"qa_{str(x['_id'])}"
#            d = f"({', '.join(studiengaenge[x['studiengang']])})" if x["studiengang"] != [] else ""
#            b = f"{x['q_de'] if lang == "de" else x["q_en"]} {d}" 
#            c  = (x["a_de"]) if lang == "de" else x["a_en"]
#            res.append((a, b, c))
#        qa_pairs[cat_kurzname] = res
#    return cats_kurzname, names_dict, qa_pairs
