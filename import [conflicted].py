from bs4 import BeautifulSoup
import requests

# import studiengaenge
files = [
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/bsc-2021.html",
        "target": "templates/studiengaenge/bsc-2021.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/2hfb-2021.html",
        "target": "templates/studiengaenge/2hfb-2021.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-2018.html",
        "target": "templates/studiengaenge/med-2018.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/med-erweiterung-2021.html",
        "target": "templates/studiengaenge/med-erweiterung-2021.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studiengaenge/msc-2014.html",
        "target": "templates/studiengaenge/msc-2014.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/index.html",
        "target": "templates/index.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/promotion.html",
        "target": "templates/studiengaenge/promotion.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/mathematikinteresse.html",
        "target": "templates/interesse/prospective.html"
    },
    {
        "source": "https://www.math.uni-freiburg.de/lehre/studienanfang.html",
        "target": "templates/interesse/studienanfang.html"
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


#        new_element = element_content.extract()
#        element.insert_after(new_element)



#        element.nextSibling = element_content

    with open(file["target"], "w") as file:
        file.write(content.prettify())

