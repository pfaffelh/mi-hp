import socket
import netrc
import os

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

if (ip_address == "127.0.1.1") or os.getcwd() == "/home/flask-reader/mi-hp":
#    home = 'static/data/home.json'
#    interesse = 'static/data/interesse.json'
#    studiendekanat = 'static/data/studiendekanat.json'
    home = 'home.json'
    interesse = 'interesse.json'
    weiterbildung = 'weiterbildung.json'
    studiendekanat = 'studiendekanat.json'
    bildnachweis = 'bildnachweis.json'
    netrc = netrc.netrc()
else:
    home = os.path.abspath("/usr/local/lib/mi-hp/home.json")
    interesse = os.path.abspath("/usr/local/lib/mi-hp/interesse.json")
    weiterbildung = os.path.abspath("/usr/local/lib/mi-hp/weiterbildung.json")
    studiendekanat = os.path.abspath("/usr/local/lib/mi-hp/studiendekanat.json")
    bildnachweis = os.path.abspath("/usr/local/lib/mi-hp/bildnachweis.json")
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
username, account, password = netrc.authenticators(calendar_host)
sondertermine_lehre_calendar_url = "http://cal.mathematik.privat/davical/caldav.php/pruefungsamt/pramt/"

studiengaenge = {"all": "alle Studiengänge",
                    "bsc": "Bachelor of Science Mathematik",
                    "2hfb": "Zwei-Hauptfächer-Bachelor",
                    "msc": "Master of Science Mathematik",
                    "mscdata": "Master of Science Mathematics in Data and Technology", 
                    "med": "Master of Education Mathematik",
                    "mederw": "Master of Education Mathematik Erweiterungsfach",
                    "meddual": "Masterstudiengang Lehramt Gymnasium – dual"
                    }
