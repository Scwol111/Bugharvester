from configparser import ConfigParser
# from server.db_working.functionMultipluer import standard
from server.webserver.flaskAppWrapper import FlaskAppWrapper
import importlib
import sys

# app = FlaskAppWrapper(__name__)
# app.run()
# side = "standard"
# from server.db_working.functionMultipluer import side as fun
fun = importlib.import_module("server.db_working.functionMultipluer", ".")
# load = importlib.find_loader("server.db_working.functionMultipluer", "standard")
# print(load.exec_module(fun))
# print(fun(15))
cont = "standard"
print(getattr(sys.modules["server.db_working.functionMultipluer"], cont)(25))
# print(fun(25))
