import socket
import netrc
import os

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

home = 'static/data/home.json'
interesse = 'static/data/interesse.json'
studiendekanat = 'static/data/studiendekanat.json'
if (ip_address == "127.0.1.1"):
    netrc = netrc.netrc()
else:
#    home = os.path.abspath("/usr/local/lib/mi-hp/home.json")
#    interesse = os.path.abspath("/usr/local/lib/mi-hp/interesse.json")
#    studiendekanat = os.path.abspath("/usr/local/lib/mi-hp/studiendekanat.json")
    netrc = netrc.netrc("/usr/local/lib/mi-hp/.netrc")

kommendes = ("ss24", "Sommersemester 2024")
aktuelles = ("ws2324", "Wintersemester 2023/24")
semester_dict = {
    "ss24": "Sommersemester 2024",
    "ws2324": "Wintersemester 2023/24",
    "ss23": "Sommersemester 2023",
    "ws2223": "Wintersemester 2022/23",
    "ss22": "Sommersemester 2022",
    "ws2122": "Wintersemester 2021/22",
    "ss21": "Sommersemester 2021",
    "ws2021": "Wintersemester 2020/21",
    "ss20": "Sommersemester 2020",
    "ws1920": "Wintersemester 2019/20",
    "ss19": "Sommersemester 2019",
    "ws1819": "Wintersemester 2018/19"
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
