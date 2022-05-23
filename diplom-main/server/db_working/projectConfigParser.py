from configparser import ConfigParser

class ProjectConfigParser:
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        