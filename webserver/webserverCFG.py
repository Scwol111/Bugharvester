from configparser import ConfigParser
import os

class WebserverConfig:
    def __init__(self) -> None:
        conf = ConfigParser()
        conf.read(os.getenv("BUGHARVESTER_FOLDER") + "/bugHarvester.cfg")
        self.host = conf["webserver"]["host"]
        self.port = int(conf["webserver"]["port"])
        self.ssl_contex = (conf["webserver"]["ssl_cert"], conf["webserver"]["ssl_key"])
        if (self.ssl_contex[0] == "" or self.ssl_contex[1] == ""):
            self.ssl_contex = None