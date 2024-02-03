from flask import Flask, url_for, render_template
import markdown
import locale
import logging

app = Flask(__name__)

locale.setlocale(locale.LC_ALL, "de_DE.UTF8") # Deutsche Namen für Tage und Monate

# Configure the logger
log_file_path = 'hp.log'
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler(log_file_path, mode='a')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

@app.route("/base/")
def showbase():
    files = ["quicklinks.html", "news.html"]
    return render_template("home.html", files = files)

@app.route("/geschichte")
def showgeschichte():
    files = ["geschichte.html"]
    return render_template("home.html", files = files)

@app.route("/mscdata")
def showmscdata():
    files = ["mscdatacarousel.html", "news.html"]
    return render_template("home.html", files = files)

@app.route("/allgemeines")
def showallgemeines():
    files = ["allgemeines.html"]
    return render_template("home.html", files = files)

