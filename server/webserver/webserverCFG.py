from configparser import ConfigParser
import os

class WebserverConfig:
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        if (self.conf["worker"]["host"] != ''):
            self.host = self.conf["webserver"]["host"]
        else:
            self.host = self.conf["webserver"]["host"]
        self.port = int(self.conf["webserver"]["port"])
        self.ssl_contex = (self.conf["webserver"]["ssl_cert"], self.conf["webserver"]["ssl_key"])
        if (self.ssl_contex[0] == "" or self.ssl_contex[1] == ""):
            self.ssl_contex = None