from bs4 import BeautifulSoup

    (institut, seite) = name.split("_")
    # This will determine what past and future events are being displayed
    print("enter")
    # Hier wird das Skelett der zu zeigenden Seite hergenommen (ohne Inhalt)
    url_skel = "https://www."+institut+".uni-freiburg.de/"+seite
    print(url_skel)
    result = requests.get(url_skel, verify=False)
    doc = BeautifulSoup(result.text, 'lxml')
   
    if(True):
    #if(name == "fdm_seminar"):
        yearsinthepast = 2
        # edit the html page from above by taking the skeleton and replace the content with empty.
        # replace the content div with a block for the template
        content = doc.find('div', id="content")
        content.string = "{% block content%}Content{% endblock %}"
        html = doc.prettify("utf-8")
        # Write the skelet
        with open("templates/talks_skel.html", "wb") as file:
            file.write(html)
