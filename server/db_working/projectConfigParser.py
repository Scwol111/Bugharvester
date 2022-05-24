from configparser import ConfigParser
import importlib
import sys

class ProjectConfigParser:
    def __init__(self, filename) -> None:
        self.conf = ConfigParser()
        self.conf.read(filename)
        self.name = self.conf["name"]
        self.citical_multipluer = float(self.conf["citical_multipluer"])
        self.high_multipluer = float(self.conf["high_multipluer"])
        self.low_multipluer = float(self.conf["low_multipluer"])
        self.cosmetic_multipluer = float(self.conf["cosmetic_multipluer"])
        self.function_multipluer_module = importlib.import_module(self.conf["function_multipluer_module"], ".")
        self.function_multipluer = getattr(sys.modules[self.conf["function_multipluer_module"]], self.conf["function_multipluer"])
        