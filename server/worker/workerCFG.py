from configparser import ConfigParser

class WorkerCFG:
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        if (self.conf["worker"]["host"] != ''):
            self.host = self.conf["worker"]["host"]
        else:
            self.host = self.conf["default"]["host"]
        self.port = int(self.conf["worker"]["port"])
