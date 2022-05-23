from bugHarvesterWebserver import app
from flask import render_template, abort, redirect
from os.path import isfile
import random

def generateProjectList():
    projects = list()
    for i in range(15):
        projects.append(("project_" + str(i), random.choice(["../static/images/ok-64.png", "../static/images/warning-5-64.png", "../static/images/warning-64.png"])))
    return projects

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404NotFound.html", login="username")

@app.route('/main')
def mainFunction():
    lst = generateProjectList()
    print(lst)
    return render_template("main.html", login="username", projects=lst)

@app.route('/contacts')
def contacFunction():
    return render_template("Contacts.html", login="username")

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def indexFunction(req_path: str):
    print(req_path)
    if (req_path == ""):
        return render_template("index.html", login="username", projects=generateProjectList())
    return redirect(req_path.replace(".html", "").lower())

