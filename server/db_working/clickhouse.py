from clickhouse_driver import Client
from configparser import ConfigParser

class ClickhouseDB:
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        self.host = self.conf["db"]["db_host"]
        self.port = int(self.conf["db"]["db_port"])
        self.client = Client(host=self.host)

    def init_db():
        pass

    def insert():
        pass

    def archive():
        pass
