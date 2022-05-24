from bugHarvesterWebserver import app
from flask import render_template, abort, redirect, request
from os.path import isfile
import random
import json

def generateProjectList():
    projects = list()
    for i in range(15):
        projects.append(("project_" + str(i), random.choice(["../static/images/ok-64.png", "../static/images/warning-5-64.png", "../static/images/warning-64.png"])))
    return projects

def generateErrorsList():
    errors = list()
    with open("C:\\Users\\Nikita\\Desktop\\diplom\\server\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    for i in data:
        count = random.randint(0, 50)
        error_mass = random.choice([25, 5, 1, 0.25]) * count
        tmp = error_mass / 50
        if (tmp >= 1):
            img = "../static/images/warning-64.png"
        elif (tmp > 0.75):
            img = "../static/images/warning-5-64.png"
        else:
            img = "../static/images/ok-64.png"
        errors.append((i, data[i], count, error_mass, img))
    return errors

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404NotFound.html", login="username")

@app.route('/main')
def mainFunction():
    return render_template("main.html", login="username", projects=generateProjectList())

@app.route('/contacts')
def contacFunction():
    return render_template("Contacts.html", login="username")

@app.route('/projects', defaults={'req_path': ''})
@app.route('/projects/<path:req_path>')
def projects(req_path: str):
    # print(request.base_url)
    return render_template("projectTemplate.html", login="username", errors=generateErrorsList(), project_name=req_path)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def indexFunction(req_path: str):
    print(req_path)
    if (req_path == ""):
        return render_template("index.html", login="username", projects=generateProjectList())
    # if (request.base_url.find("/projects/") != -1):
    #     projects("")
    if (req_path.find(".html") != -1):
        return redirect(req_path.replace(".html", "").lower())
    abort(404)

