from inspect import trace
from itertools import count
from bugHarvesterWebserver import app
from flask import render_template, abort, redirect, request, send_from_directory ,send_file
from os.path import isfile
from datetime import datetime
from uuid import uuid4
from collections import Counter
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
    err = 0
    warn = 0
    for i in data:
        count = random.randint(0, 50)
        # count = 0
        error_mass = random.choice([25, 5, 1, 0.25]) * count
        tmp = error_mass / 50
        if (tmp >= 1):
            img = "../static/images/warning-64.png"
            err += 1
        elif (tmp > 0.75):
            img = "../static/images/warning-5-64.png"
            warn += 1
        else:
            img = "../static/images/ok-64.png"
        errors.append((i, data[i], count, error_mass, img))
    return errors, {"errors": err, "warnings": warn}

def generateProjectInfo(projectName: str):
    data = dict()
    data["Name"] = projectName
    data["version"] = "0.1.25"
    data["analysTime"] = str(datetime.now())[:19]
    data["Description"] = "With is test project"
    return data

def generateReportsList():
    reports = list()
    tracebacks = list()
    for i in range(20):
        tmp = dict()
        tmp["id"] = uuid4().hex
        tmp["date"] = str(datetime.now())[:19]
        tmp["traceback"] = "Traceback is real " + str(random.randint(0, 5))
        reports.append(tmp)
        tracebacks.append(tmp["traceback"])
    return reports, tracebacks

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404NotFound.html", login="username")

@app.route('/main')
def mainFunction():
    return render_template("main.html", login="username", projects=generateProjectList())

@app.route('/contacts')
def contacFunction():
    return render_template("Contacts.html", login="username")

# @app.route('/projects', defaults={'req_path': ''})
@app.route('/projects/<req_path>')
def projects(req_path: str):
    print("PROJECTS")
    err, cont = generateErrorsList()
    err.sort(key=lambda x: x[3], reverse=True)
    return render_template("projectTemplate.html", login="username", errors=err, project=generateProjectInfo(req_path), count = cont)

@app.route('/projects/<req_path>/<errorType>')
def errors(req_path: str, errorType: str):
    err, trace = generateReportsList()
    con = Counter(trace).most_common(1)[0][0]
    return render_template("projectErrorTemplate.html", login="username", project=generateProjectInfo(req_path), errorList = err, errorType = errorType, mostCommonTraceback = con)

@app.route('/projects/<req_path>/<errorType>/<reportId>/dump')
def download(req_path: str, errorType: str, reportId: str):
    return send_from_directory("C:\\Users\\Nikita\\Desktop\\diplom\\server\\bugHarvesterWebserver", "test_dump.txt", as_attachment=True)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def indexFunction(req_path: str):
    print(req_path)
    if (req_path == ""):
        return render_template("index.html", login="username", projects=generateProjectList())
    if (req_path.find(".html") != -1):
        return redirect(req_path.replace(".html", "").lower())
    abort(404)

