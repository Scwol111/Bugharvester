from typing import List
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
    
    def init_project_db(self, pojectName: str) -> None:
        templateLoader = jinja2.FileSystemLoader(searchpath="./server/db_working/sql_template")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template("/project_db_init.sql")
        sql_execute = template.render(project_name=pojectName)
        self.client.execute(sql_execute)

    #Insert report to db
    def insert(self, projectName: str, data: dict):
        pass #TODO now

    #archive reports
    def archive(self, projectName):
        pass #TODO later

    #return list of projects
    def getProjectList(self) -> list:
        pass #TODO now

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
        sql_exec = "SELECT date FROM ?.Analyze ORDER BY analyze_time DESC LIMIT 1" # + projectName
        result = self.client.execute(sql_exec, (projectName))
        data["analysTime"] = str(result[0][0])
        return data

    #return list of reports about errorName
    def getReportList(self, projectName, errorName) -> tuple:
        pass #TODO now

    #return info about error
    def getErrorTypeInfo(self, projectName: str, error: str) -> dict:
        # sql_exec = "SELECT reason, solve FROM " + projectName + ".Errors WHERE error_name=" + error
        sql_exec = "SELECT reason, solve FROM ?.Errors WHERE error_name=?"
        result = self.client.execute(sql_exec, (projectName, error))
        return {"reason": result[0][0], "solve": result[0][1]}

    def addErrorType(self, error: dict) -> dict:
        pass #TODO now

    def deleteErrorType(self, error: dict) -> dict:
        pass #TODO now

    def updateErrorType(self, error: dict) -> dict:
        pass #TODO now
