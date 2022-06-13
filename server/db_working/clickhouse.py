from datetime import datetime
import json
from clickhouse_driver import Client
from configparser import ConfigParser
# from db_working.projectConfigParser import ProjectConfigParser
# from db_working.errorListParser import ErrorListParser
from db_working.bugHarvesterBaseDB import BugHarvesterBaseDB
# from bugHarvesterWebserver.mainPage import sortStatus
import os
import jinja2

class BugHarvesterClickhouseDB(BugHarvesterBaseDB):
    def __init__(self) -> None:
        filename = os.getenv("BUGHARVESTER_FOLDER") + "/conf/bugHarvester.cfg"
        self.conf = ConfigParser()
        self.conf.read(filename)
        self.host = self.conf["db"]["db_host"]
        self.port = int(self.conf["db"]["db_port"])
        self.client = Client(host=self.host)

    def sortStatus(x):
        status = ["/static/images/ok-64.png", "/static/images/warning-5-64.png", "/static/images/warning-64.png", "/static/images/ok-16.png", "/static/images/warning-5-16.png", "/static/images/warning-16.png"]
        if (x[1] == status[0] or x[1] == status[3]):
            return 0
        elif (x[1] == status[1] or x[1] == status[4]):
            return 1
        return 2

    def init_db(self) -> None:
        with open(os.getenv("BUGHARVESTER_FOLDER") + "/db_working/sql_template/ClickHouse_INIT_DB.sql", "r", encoding="utf-8") as file:
            sql_execute = " ".join(file.readlines()).split(";")
        for i in sql_execute:
            self.client.execute(i)

    # project_name String,
    # project_description String,
    # current_version String,
    # maximal Int32
    def init_project_db(self, projectName: str, projectData: dict) -> None:
        sql_execute = "INSERT INTO BugHarvester.Projects (*) VALUES (%(pn)s, %(pd)s, %(cv)s, %(max)i)"
        self.client.execute(sql_execute, (projectData))
        templateLoader = jinja2.FileSystemLoader(searchpath="./db_working/sql_template")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("/project_DB_init.sql")
        sql_execute = template.render(project_name=projectName).split(";")
        if not os.path.exists(os.getenv("BUGHARVESTER_FOLDER") + "/dumps/" + projectName):
            os.mkdir(os.getenv("BUGHARVESTER_FOLDER") + "/dumps/" + projectName)
        for i in sql_execute:
            self.client.execute(i)            

    def __contain_project_name__(self, projectName: str) -> bool:
        sql_exec = "SELECT * FROM BugHarvester.Projects WHERE project_name=%(pn)s"
        result = self.client.execute(sql_exec, ({"pn": projectName}))
        if len(result) > 0:
            return True
        return False

    def __contain_error_type__(self, projectName: str, error_type: str) -> bool:
        sql_exec = "SELECT * FROM " + projectName + ".projects WHERE project_name=%(et)s"
        result = self.client.execute(sql_exec, ({"et": error_type}))
        if len(result) > 0:
            return True
        return False

    # id String,
    # error_name String,
    # version String,
    # license String,
    # techInfo String,
    # traceback String,
    # path_to_dump String,
    # date Date,
    # analyze_id String,
    # analyze_time Date
    #Insert report to db
    def insert(self, projectName: str, data: dict):
        if (not self.__contain_project_name__(projectName)):
            raise Exception("Project does not exists")
        sql_exec = "INSERT INTO " + projectName + ".Reports (id, error_name, version, license, techInfo, traceback, path_to_dump, date) VALUES (%(id)s, %(error_name)s, %(version)s, %(license)s, %(techInfo)s, %(traceback)s, %(path_to_dump)s, %(date)s)"
        self.client.execute(sql_exec, (data))

    #archive reports
    def archive(self, projectName):
        pass #TODO later

    # def generateProjectList():
    #     projects = list()
    #     for i in range(15):
    #         projects.append(("project_" + str(i), random.choice(["/static/images/ok-64.png", "/static/images/warning-5-64.png", "/static/images/warning-64.png"])))
    #     return projects
    #return list of projects
    def getProjectList(self) -> list:
        with open(os.getenv("BUGHARVESTER_FOLDER"), "r", encoding="utf-8") as file:
            anylize = json.load(file)["projects"]
        sql_exec = "SELECT project_name FROM BugHarvester.Projects"
        result = self.client.execute(sql_exec)
        projects = list()
        for i in result:
            if (anylize[i[0]] == "ok"):
                img = "/static/images/ok-64.png"
            elif (anylize[i[0]] == "warning"):
                img = "/static/images/warning-5-64.png"
            elif (anylize[i[0]] == "error"):
                img = "/static/images/warning-64.png"
            projects.append((i[0], img))
        return projects

    # def generateErrorsList():
    #     errors = list()
    #     mass = {
    #         "critical": 25, 
    #         "higt": 5, 
    #         "low": 1, 
    #         "cosmetic": 0.25
    #     }
    #     with open("C:\\Users\\Nikita\\Desktop\\diplom\\server\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
    #         data = json.load(file)
    #     err = 0
    #     warn = 0
    #     preparedErrors = []
    #     for i in data:
    #         count = random.randint(0, 15)
    #         # count = 0
    #         error_mass = mass[data[i]["criticaly"]] * count
    #         tmp = error_mass / 50
    #         if (tmp >= 0.75):
    #             img = "/static/images/warning-64.png"
    #             err += 1
    #             preparedErrors.append((i, img.replace("64", "16")))
    #         elif (tmp > 0.35):
    #             img = "/static/images/warning-5-64.png"
    #             warn += 1
    #             preparedErrors.append((i, img.replace("64", "16")))
    #         else:
    #             img = "../static/images/ok-64.png"
    #         print(preparedErrors[-1])
    #         errors.append((i, data[i]["description"], count, error_mass, img))
    #     preparedErrors.sort(key=sortStatus, reverse=True)
    #     return errors, {"errors": err, "warnings": warn}, preparedErrors
    #return list of errors
    def getErrorList(self, projectName) -> tuple:
        if (not self.__contain_project_name__(projectName)):
            raise Exception("Project does not exists")
        sql_exec = "SELECT error_name, weight, description FROM " + projectName + ".Errors"
        result = self.client.execute(sql_exec)
        with open(os.getenv() + "/anylize.json", "w", encoding="utf-8") as file:
            data = json.load(file)
        errors = list()
        preparedErrors = list()
        sql_exec = "SELECT maximal FROM Bugharvester.Projects WHERE project_name=%(pn)s"
        maximal = self.client.execute(sql_exec, ({"pn": projectName}))
        for i in result:
            sql_exec = "SELECT id FROM " + projectName + ".Reports WHERE analyze_id=%(analyze_id)s AND error_name=%(error_name)s"
            lst = self.client.execute(sql_exec, ({"analyze_id": data["id"], "error_name": i[0]}))
            count = len(lst)
            weight = count**2 * i[1]
            tmp = weight / maximal
            err = warn = 0
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
            errors.append((i[0], i[2], count, weight, img))
        preparedErrors.sort(key=self.sortStatus, reverse=True)
        return errors, {"errors": err, "warnings": warn}, preparedErrors

    # data = dict()
    # data["Name"] = projectName
    # data["version"] = "0.1.25"
    # data["analysTime"] = str(datetime.now() - timedelta(days=30))[:19]
    # data["Description"] = "This is test project " + data["Name"]
    #return info about projectName
    def getProjectInfo(self, projectName) -> dict:
        data = dict()
        sql_exec = "SELECT * FROM BugHarvester.Projects WHERE project_name=%(pn)s" # + projectName
        result = self.client.execute(sql_exec, ({"pn": projectName}))
        data["Name"] = projectName
        data["version"] = result[0][2]
        data["Description"] = result[0][1]
        with open(os.getenv("BUGHARVESTER_FOLDER"), "r", encoding="utf-8") as file:
            anylize = json.load(file)
        # sql_exec = "SELECT date FROM ?.Analyze ORDER BY analyze_time DESC LIMIT 1" # + projectName
        # result = self.client.execute(sql_exec, (projectName))
        data["analysTime"] = str(anylize["datetime"])
        return data

    # def generateReportsList():
        # reports = list()
        # tracebacks = list()
        # for i in range(20):
        #     tmp = dict()
        #     tmp["id"] = uuid4().hex
        #     tmp["date"] = str(datetime.now() - timedelta(days=30))[:19]
        #     tmp["traceback"] = "Traceback is real " + str(random.randint(0, 5))
        #     reports.append(tmp)
        #     tracebacks.append(tmp["traceback"])
        # return reports, tracebacks
    #return list of reports about errorName
    def getReportList(self, projectName, errorName) -> tuple:
        if (not self.__contain_project_name__(projectName)):
            raise Exception("Project does not exists")
        with open(os.getenv("BUGHARVESTER_FOLDER"), "r", encoding="utf-8") as file:
            anylize = json.load(file)
        sql_exec = "SELECT id, date, traceback, path_to_dump FROM " + projectName + ".Reports WHERE error=%(errorName)s AND analyze_id=%(anylize_id)s ORDER BY date DESK"
        result = self.client.execute(sql_exec, ({"errorName": errorName, "anylize_id": anylize["id"]}))
        reports = list()
        traceback = list()
        for i in result:
            tmp = dict()
            tmp["id"] = i[0]
            tmp["date"] = i[1]
            tmp["traceback"] = i[2]
            tmp["dump"] = i[3]
            reports.append(tmp)
            traceback.append(i[2])
        return reports, traceback

    #return info about error
    def getErrorTypeInfo(self, projectName: str, error: str) -> dict:
        if (not self.__contain_project_name__(projectName)):
            raise Exception("Project does not exists")
        # sql_exec = "SELECT reason, solve FROM " + projectName + ".Errors WHERE error_name=" + error
        sql_exec = "SELECT reason, solve FROM " + projectName + ".Errors WHERE error_name=%(error)s"
        result = self.client.execute(sql_exec, ({"error": error}))
        return {"reason": result[0][0], "solve": result[0][1]}

    # error_name String,
    # language String,
    # weight UInt32,
    # reason String,
    # solve String
    def addErrorType(self, error: dict) -> dict:
        if (not self.__contain_project_name__(error["project"])):
            raise Exception("Project does not exists")
        sql_exec = "INSERT INTO " + error["project"] + ".Errors (*) VALUES(%(name)s,%(language)s,%(weight)i,%(reason)s,%(solve)s, %(description)s)"
        self.client.execute(sql_exec, (error))

    def deleteErrorType(self, error: dict) -> dict:
        if (not self.__contain_project_name__(error["project"])):
            raise Exception("Project does not exists")
        sql_exec = "DELETE FROM " + error["project"] + ".Errors WHERE error_name=%(name)s"
        self.client.execute(sql_exec, (error))

    # в кликхаусе запись не обновляется а заменяется по ключу
    def updateErrorType(self, error: dict) -> dict:
        self.addErrorType(error)


    # id String,
    # error_name String,
    # version String,
    # license String,
    # techInfo String,
    # traceback String,
    # path_to_dump String,
    # date Date,
    # analyze_id String,
    # analyze_time Date
    #Insert report to db
    def doAnalyze(self, projectData):
        if (not self.__contain_project_name__(projectData["name"])):
            raise Exception("Project does not exists")
        sql_exec = "SELECT (id, error_name, version, license, techInfo, traceback, path_to_dump, date) FROM " + projectData["name"] + ".Reports WHERE analyze_id=''"
        result = self.client.execute(sql_exec)
        sql_exec = "INSERT INTO " + projectData["name"] + ".Reports (*) VALUES (%(id)s, %(error_name)s, %(version)s, %(license)s, %(techInfo)s, %(traceback)s, %(path_to_dump)s, %(date)s, %(analyze_id)s, %(analyze_time)s)"
        for i in result:
            self.client.execute(sql_exec, ({"anylize_id": projectData["id"], "anylize_time": projectData["time"], "id": i[0], "error_name": i[1], "version": i[2], "license": i[3], "techInfo": i[4], "traceback": i[5], "path_to_dump": i[6], "date": i[7]}))
