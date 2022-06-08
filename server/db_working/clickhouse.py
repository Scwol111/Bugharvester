import json
from clickhouse_driver import Client
from configparser import ConfigParser
from db_working.projectConfigParser import ProjectConfigParser
from db_working.errorListParser import ErrorListParser
from db_working.bugHarvesterBaseDB import BugHarvesterBaseDB
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

    def init_db(self) -> None:
        with open(os.getenv("BUGHARVESTER_FOLDER") + "/db_working/sql_template/ClickHouse_INIT_DB.sql", "r", encoding="utf-8") as file:
            sql_execute = " ".join(file.readlines())
        self.client.execute(sql_execute)
    
    def init_project_db(self, projectName: str) -> None:
        templateLoader = jinja2.FileSystemLoader(searchpath="./server/db_working/sql_template")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("/project_db_init.sql")
        sql_execute = template.render(project_name=projectName)
        self.client.execute(sql_execute)
        os.mkdir("./dumps/" + projectName)

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
        sql_exec = "INSERT INTO ?.Reports (*) VALUES ()"
        self.client.execute(sql_exec)
        pass #TODO now

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


    #return list of errors
    def getErrorList(self, projectName) -> tuple:
        pass #TODO now

    # data = dict()
    # data["Name"] = projectName
    # data["version"] = "0.1.25"
    # data["analysTime"] = str(datetime.now() - timedelta(days=30))[:19]
    # data["Description"] = "This is test project " + data["Name"]
    #return info about projectName
    def getProjectInfo(self, projectName) -> dict:
        data = dict()
        sql_exec = "SELECT * FROM BugHarvester.Projects WHERE project_name=?" # + projectName
        result = self.client.execute(sql_exec, (projectName))
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
        with open(os.getenv("BUGHARVESTER_FOLDER"), "r", encoding="utf-8") as file:
            anylize = json.load(file)
        sql_exec = "SELECT id, date, traceback, path_to_dump FROM ?.Reports WHERE error=? AND analyze_id=? ORDER BY date DESK"
        result = self.client.execute(sql_exec, (projectName, errorName, anylize["id"]))
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
        # sql_exec = "SELECT reason, solve FROM " + projectName + ".Errors WHERE error_name=" + error
        sql_exec = "SELECT reason, solve FROM ?.Errors WHERE error_name=?"
        result = self.client.execute(sql_exec, (projectName, error))
        return {"reason": result[0][0], "solve": result[0][1]}

    # error_name String,
    # language String,
    # weight UInt32,
    # reason String,
    # solve String
    def addErrorType(self, error: dict) -> dict:
        sql_exec = "INSERT INTO ?.Errors (*) VALUES(?,?,?,?,?)"
        self.client.execute(sql_exec, (error["project"], error["name"], error["language"], error["weight"], error["reason"], error["solve"]))

    def deleteErrorType(self, error: dict) -> dict:
        sql_exec = "DELETE FROM ?.Errors WHERE error_name=?"
        self.client.execute(sql_exec, (error["project"], error["name"]))

    # в кликхаусе запись не обновляется а заменяется по ключу
    def updateErrorType(self, error: dict) -> dict:
        self.addErrorType(error)

    def doAnalyze(self, projectData):
        pass #TODO now
