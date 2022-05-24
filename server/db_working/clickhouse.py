from clickhouse_driver import Client
from configparser import ConfigParser
from projectConfigParser import ProjectConfigParser
from errorListParser import ErrorListParser

class ClickhouseDB:
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
