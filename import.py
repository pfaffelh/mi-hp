from bs4 import BeautifulSoup
import requests
import os

# import studiengaenge
files = [
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/bsc-2021.html",
    #     "target": "templates/studiengaenge/bsc-2021.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/2hfb-2021.html",
    #     "target": "templates/studiengaenge/2hfb-2021.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-2018.html",
    #     "target": "templates/studiengaenge/med-2018.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-erweiterung-2021.html",
    #     "target": "templates/studiengaenge/med-erweiterung-2021.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/msc-2014.html",
    #     "target": "templates/studiengaenge/msc-2014.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/index.html",
    #     "target": "templates/index.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/promotion.html",
    #     "target": "templates/studiengaenge/promotion.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/mathematikinteresse.html",
    #     "target": "templates/interesse/prospective.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/studienanfang.html",
    #     "target": "templates/interesse/studienanfang.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/pruefungsamt/index.html",
    #     "target": "templates/pruefungsamt/index.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/pruefungsamt/termine.html",
    #     "target": "templates/pruefungsamt/termine.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/pruefungsamt/pruefungen.html",
    #     "target": "templates/pruefungsamt/pruefungen.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/pruefungsamt/abschlussarbeiten.html",
    #     "target": "templates/pruefungsamt/abschlussarbeiten.html"
    # },
    # {
    #     "source": "https://www.math.uni-freiburg.de/lehre/pruefungsamt/modulhandbuecher.html",
    #     "target": "templates/pruefungsamt/modulhandbuecher.html"
    # },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studienberatung.html",
        "target": "templates/studienberatung.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studieninteresse/warum_mathematik.html",
        "target": "templates/interesse/warum_mathematik.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studieninteresse/mathestudium_in_freiburg.html",
        "target": "templates/interesse/mathestudium_in_freiburg.html"
    }
]

html="<html><div id='aussen'> 1 <div id='innen'> 2 </div> 3</div></html>"
soup = BeautifulSoup(html, 'lxml')
content = soup.find('div', id="aussen")
accordion = soup.new_tag("div", class_="accordion-item")
content.append(accordion)
print(content.prettify())

for file in files:
    print(file["source"])
    result = requests.get(file["source"], verify=False)
    soup = BeautifulSoup(result.text, 'lxml')
    content = soup.find('div', id="inhalt")
    content['class'] = "container"
#    content.find_all(class_ = "section fold")

    accordion = soup.new_tag("div")
    accordion["class"] = "accordion accordion-flush"
    accordion["id"] = "accordionExample"
    content.append(accordion)

    elements = content.find_all(class_ = "section fold")
    elements.extend(content.find_all(class_ = "fold"))
    elements.extend(content.find_all(class_ = "section"))
    for element in elements:
        accordion.append(element)

    for element in elements:
        element["class"] = "accordion-item"
        idloc = element["id"]
        header = element.find(["h2","h3"])
        header["class"] = "accordion-header"
        header["id"] = f"header{idloc}"
        
        button = soup.new_tag("button")
        button["class"] = "accordion-button"
        button["type"]="button"
        button["data-bs-toggle"]="collapse"
        button["data-bs-target"]=f"#{idloc}Content"
        button["aria-expanded"]="false"
        button["aria-controls"]=f"{idloc}Content"
        button.string = "hallo" #
        button.string.replace_with(header.text)
        header.clear()
        header.insert(0, button)

        b = soup.new_tag("div")
        b["id"] = f"{idloc}Content"
        b["aria-labelledby"]=f"{idloc}Content"
        b["data-bs-parent"]="#accordionExample"

        element_content = element.find(class_ = "foldContent collapse")
        if element_content:
            b["class"] = "accordion-collapse collapse"
            element_content["class"] = "accordion-body"
            element_content.wrap(b)
        element_content = element.find(class_ = "sectionContent collapse")
        if element_content:
            b["class"] = "accordion-collapse collapse"
            element_content["class"] = "accordion-body"
            element_content.wrap(b)

        element_content = element.find(class_ = "foldContent collapse open")
        if element_content:
            b["class"] = "accordion-collapse collapse show"
            element_content["class"] = "accordion-body"
            element_content.wrap(b)



    with open(file["target"], "w") as file:
        file.write(content.prettify())



# import mediathek, a local copy is in test

with open("test/mediathek.html", "r") as file:
    soup = BeautifulSoup(file.read(), 'lxml')
    images = soup.find_all('img')
    del images[0]
    for image in images:
        os.system(f"wget --no-check-certificate www.math.uni-freiburg.de/lehre/{image['src']}")
        x = image["src"].replace("bilder/", "")
        os.system(f"mv {x} static/Bilder")

