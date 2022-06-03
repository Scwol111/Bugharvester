# # from configparser import ConfigParser
# # from server.db_working.functionMultipluer import standard
# # from server.webserver.flaskAppWrapper import FlaskAppWrapper
# import importlib
# import sys

# # app = FlaskAppWrapper(__name__)
# # app.run()
# # side = "standard"
# # from server.db_working.functionMultipluer import side as fun
# fun = importlib.import_module("server.db_working.functionMultipluer", ".")
# # load = importlib.find_loader("server.db_working.functionMultipluer", "standard")
# # print(load.exec_module(fun))
# # print(fun(15))
# cont = "standard"
# funct = getattr(sys.modules["server.db_working.functionMultipluer"], cont)
# print(getattr(sys.modules["server.db_working.functionMultipluer"], cont)(25))
# print(funct(25))
# # print(fun(25))


# import json
# import random

# with open(".\\server\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
#     data = json.load(file)
# output = dict()
# for i in data:
#     output[i] = {
#         "description": data[i],
#         "criticaly": random.choice(["critical", "higt", "low", "cosmetic"]),
#         "reason": "you trying programming",
#         "solve": "turn off computer"
#     }
# with open(".\\server\\db_working\\errors_list\\python312.json", "w", encoding="utf-8") as file:
#     json.dump(output, file, indent=4)

# from flask import render_template
import jinja2

templateLoader = jinja2.FileSystemLoader(searchpath="./server/db_working/sql_template")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "project_DB_init.sql"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(project_name="superJam")
print(outputText)

