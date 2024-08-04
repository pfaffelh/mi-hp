from bs4 import BeautifulSoup
import requests
import os

# import studiengaenge
files = [
    #{
    #    "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/bsc-2021.html",
    #    "target": "templates/studiendekanat/belegung_bsc.html"
    #},
    #{
    #    "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/2hfb-2021.html",
    #    "target": "templates/studiendekanat/belegung_2hfb.html"
    #},
    #{
    #    "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/msc-2014.html",
    #    "target": "templates/studiendekanat/belegung_msc.html"
    #},
    #{
    #    "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-2018.html",
    #    "target": "templates/studiendekanat/belegung_med.html"
    #},
#     {
#         "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-erweiterung-2021.html",
#         "target": "templates/studiendekanat/belegung_mederwbf.html"
#     },
]

for file in files:
    print(file["source"])
    result = requests.get(file["source"], verify=False)
    soup = BeautifulSoup(result.text, 'lxml')
    content = soup.find('div', id="pruefungen_meb")
    content['class'] = "container"

    with open(file["target"], "w") as file:
        file.write(content.prettify())

