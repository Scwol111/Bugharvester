from configparser import ConfigParser

class BugHarvesterObserverConfig:
    def __init__(self, filename: str) -> None:
        self.conf = ConfigParser()
        print(filename)
        print(self.conf.read(filename))
        print(self.conf.sections(), self.conf.default_section)
        self.api = {"host": self.conf["default"]["api_host"], "port": int(self.conf["default"]["api_port"])}
        self.worker = {"host": self.conf["default"]["worker_host"], "port": int(self.conf["default"]["worker_port"])}