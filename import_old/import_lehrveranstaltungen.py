from bs4 import BeautifulSoup
import requests

semesters = ["ws0607", "ss07", "ws0708", "ss08", "ws0809", "ss09", "ws0910", "ss10", "ws1011", "ss11", "ws1112", "ss12", "ws1213", "ss13", "ws1314", "ss14", "ws1415", "ss15", "ws1516", "ss16", "ws1617", "ss17", "ws1718", "ss18", "ws1819", "ss19", "ws1920", "ss20", "ws2021", "ss21", "ws2122", "ss22", "ws2223", "ss23", "ws2324", "ss24", "ws2425"]

for semester in semesters:
    print(semester)
    url = f"https://www.math.uni-freiburg.de/lehre/v/{semester}.html"
    print(url)
    result = requests.get(url, verify=False)
    soup = BeautifulSoup(result.text, 'lxml')
    content = soup.find('div', id="inhalt")
    print(content)
    content['class'] = "container"
    filenames = [f"lehrveranstaltungen/{semester}.html"]    
    with open("templates/"+filenames[0], "w") as file:
        file.write(content.prettify())
