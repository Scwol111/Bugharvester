from clickhouse_driver import Client
from configparser import ConfigParser
from db_working.projectConfigParser import ProjectConfigParser
from db_working.errorListParser import ErrorListParser
from db_working.bugHarvesterBaseDB import BugHarvesterBaseDB

class BugHarvesterClickhouseDB(BugHarvesterBaseDB):
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        self.host = self.conf["db"]["db_host"]
        self.port = int(self.conf["db"]["db_port"])
        self.client = Client(host=self.host)

    def init_db(self, projectConfig: ProjectConfigParser):
        pass

    def insert(self, projectConfig: ProjectConfigParser):
        pass

    def archive(self, projectConfig: ProjectConfigParser):
        pass

    def getProjectList():
        pass

    def getErrorList():
        pass

    def getProjectInfo():
        pass

    def getReportList():
        pass
