from inspect import trace
from itertools import count
import os
from bugHarvesterWebserver import app
from flask import render_template, abort, redirect, request, send_from_directory ,send_file
from os.path import isfile
from datetime import datetime, timedelta
from uuid import uuid4
from collections import Counter
from server.db_working.clickhouse import BugHarvesterClickhouseDB
import random
import json

def sortStatus(x):
    status = ["/static/images/ok-64.png", "/static/images/warning-5-64.png", "/static/images/warning-64.png", "/static/images/ok-16.png", "/static/images/warning-5-16.png", "/static/images/warning-16.png"]
    if (x[1] == status[0] or x[1] == status[3]):
        return 0
    elif (x[1] == status[1] or x[1] == status[4]):
        return 1
    return 2

def generateProjectList():
    projects = list()
    for i in range(15):
        projects.append(("project_" + str(i), random.choice(["/static/images/ok-64.png", "/static/images/warning-5-64.png", "/static/images/warning-64.png"])))
    return projects

def generateErrorsList():
    errors = list()
    mass = {
        "critical": 25, 
        "higt": 5, 
        "low": 1, 
        "cosmetic": 0.25
    }
    with open("C:\\Users\\Nikita\\Desktop\\diplom\\server\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    err = 0
    warn = 0
    preparedErrors = []
    for i in data:
        count = random.randint(0, 15)
        # count = 0
        error_mass = mass[data[i]["criticaly"]] * count
        tmp = error_mass / 50
        if (tmp >= 0.75):
            img = "/static/images/warning-64.png"
            err += 1
            preparedErrors.append((i, img.replace("64", "16")))
        elif (tmp > 0.35):
            img = "/static/images/warning-5-64.png"
            warn += 1
            preparedErrors.append((i, img.replace("64", "16")))
        else:
            img = "../static/images/ok-64.png"
        print(preparedErrors[-1])
        errors.append((i, data[i]["description"], count, error_mass, img))
    preparedErrors.sort(key=sortStatus, reverse=True)
    return errors, {"errors": err, "warnings": warn}, preparedErrors

def generateProjectInfo(projectName: str):
    data = dict()
    data["Name"] = projectName
    data["version"] = "0.1.25"
    data["analysTime"] = str(datetime.now() - timedelta(days=30))[:19]
    data["Description"] = "This is test project " + data["Name"]
    return data

def generateReportsList():
    reports = list()
    tracebacks = list()
    for i in range(20):
        tmp = dict()
        tmp["id"] = uuid4().hex
        tmp["date"] = str(datetime.now() - timedelta(days=30))[:19]
        tmp["traceback"] = "Traceback is real " + str(random.randint(0, 5))
        reports.append(tmp)
        tracebacks.append(tmp["traceback"])
    return reports, tracebacks

@app.errorhandler(404)
def pageNotFound(e):
    return render_template("404NotFound.html", login="username")

@app.route('/main')
def mainFunction():
    sql = BugHarvesterClickhouseDB()
    # prjct = generateProjectList()
    prjct = sql.getProjectList()
    prjct.sort(key=sortStatus)
    return render_template("main.html", login="username", projects=prjct)

@app.route('/contacts')
def contacFunction():
    return render_template("Contacts.html", login="username")

# @app.route('/projects', defaults={'projectName': ''})
@app.route('/projects/<projectName>')
def projects(projectName: str):
    sql = BugHarvesterClickhouseDB()
    projectInfo = sql.getProjectInfo(projectName)
    # err, cont, preparedErrors = generateErrorsList()
    err, cont, preparedErrors = sql.getErrorList(projectName)
    err.sort(key=lambda x: x[3], reverse=True)
    if (cont["errors"] > 0):
        recomendation = "Необходима новая версия с исправленными ошибками"
    elif (cont["warnings"] > 0):
        recomendation = "Неободимо исправить некоторые ошибки"
    else:
        recomendation = "С проектом все в порядке. Так держать!"
    # project=generateProjectInfo(projectName)
    return render_template("projectTemplate.html", login="username", errors=err, project=projectInfo, count=cont, recomendation=recomendation, preparedErrors=preparedErrors)

@app.route('/projects/<projectName>/<errorType>')
def errors(projectName: str, errorType: str):
    sql = BugHarvesterClickhouseDB()
    # err, trace = generateReportsList()
    try:
        err, trace = sql.getReportList()
        con = Counter(trace).most_common(1)[0][0]
        data = sql.getErrorTypeInfo(projectName, errorType)
        prjct = sql.getProjectInfo(projectName)
    except:
        abort(404)
    # with open("C:\\Users\\Nikita\\Desktop\\diplom\\server\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
    #     data = json.load(file)
    error = {
        'type': errorType,
        "solve": data["solve"],
        "reason": data["reason"]
    }
    return render_template("projectErrorTemplate.html", login="username", project=prjct, errorList = err, error = error, mostCommonTraceback = con)
    # return render_template("projectErrorTemplate.html", login="username", project=generateProjectInfo(projectName), errorList = err, error = error, mostCommonTraceback = con)

@app.route('/projects/<projectName>/<errorType>/<reportId>/dump')
def download(projectName: str, errorType: str, reportId: str):
    folder = os.getenv("BUGHARVESTER_FOLDER") + "/".join(["dumps", projectName, errorType])
    # return send_from_directory("C:\\Users\\Nikita\\Desktop\\diplom\\server\\bugHarvesterWebserver", "test_dump.txt", as_attachment=True)
    return send_from_directory(folder, reportId + ".txt", as_attachment=True)

@app.route('/api/<projectName>/addReport', methods=["POST"])
def addReport(projectName: str):
    sql = BugHarvesterClickhouseDB()
    return sql.insert(projectName, request.json)

@app.route('/api/errors', methods=['POST', 'DELETE', 'UPDATE'])
def errorApiWork():
    sql = BugHarvesterClickhouseDB()
    if request.method == "POST":
        return sql.addErrorType(request.json)
    elif request.method == "UPDATE":
        return sql.updateErrorType(request.json)
    return sql.deleteErrorType(request.json)

# @app.route('/', defaults={'projectName': ''})
# @app.route('/<projectName>')
@app.route("/")
def indexFunction():
    sql = BugHarvesterClickhouseDB()
    prjct = sql.getProjectList()
    prjct.sort(key=sortStatus, reverse=True)
    # prjct = sorted(generateProjectList(), key=sortStatus, reverse=True)
    return render_template("index.html", login="username", projects=prjct)
