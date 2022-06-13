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

# import jinja2

# templateLoader = jinja2.FileSystemLoader(searchpath="./server/db_working/sql_template")
# templateEnv = jinja2.Environment(loader=templateLoader)
# TEMPLATE_FILE = "project_DB_init.sql"
# template = templateEnv.get_template(TEMPLATE_FILE)
# outputText = template.render(project_name="superJam")
# print(outputText)

# from clickhouse_driver import Client

# cli = Client(host="127.0.0.1")
# print(cli.execute("SELECT * FROM test.test WHERE info=%(ids)s", ({"dbName":'test', "ids":''})))



from datetime import datetime, timedelta
import json
import random
from uuid import uuid4
from server.db_working.clickhouse import BugHarvesterClickhouseDB as cl
from secrets import token_hex

db = cl()

# db.init_db()

with open(".\\db_working\\errors_list\\python312.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    mass = {
        "critical": 25, 
        "higt": 5, 
        "low": 1, 
        "cosmetic": 0.25
    }
#     for j in range(15):
#         tmp = {
#             "pn": "project_" + str(j),
#             "cv": "0.12.25",
#             "pd":"This is ptoject",
#             "max": 50
#         }
#         db.init_project_db(tmp["pn"], tmp)
#         for i in data:
#             tmp = data[i]
#             tmp["project"] = "project_" + str(j)
#             tmp["name"] = i
#             tmp["language"] = 'python310'
#             tmp["weight"] = mass[tmp["criticaly"]]
#             db.addErrorType(tmp)

#     # id String,
#     # error_name String,
#     # version String,
#     # license String,
#     # techInfo String,
#     # traceback String,
#     # path_to_dump String,
#     # date Date,
#     # analyze_id String,
#     # analyze_time DateTime


    for j in range(15):
        for i in data:
            count = random.randint(0, 15)
            for k in range(count):
                id = uuid4().hex
                insert = {
                    "version": "0.12.25",
                    "id": id,
                    "error_name": i,
                    "license": uuid4().hex,
                    "techInfo": "",
                    "traceback": "Traceback is real " + str(random.randint(0, 5)),
                    "path_to_dump": "./dumps/project_" + str(j) + "/" + id,
                    "date": str(datetime.now() - timedelta(days=random.randint(0, 15), hours=random.randint(0, 60), minutes=random.randint(0, 60)))
                }
                db.insert("project_" + str(j), insert)
                pass
