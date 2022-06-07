from flask import Flask
from bugHarvesterWebserver.webserverCFG import WebserverConfig
from pyfiglet import Figlet
from server.db_working.clickhouse import BugHarvesterClickhouseDB
import os

app = Flask(__name__)


from bugHarvesterWebserver.mainPage import *

def run():
    cfg = WebserverConfig(os.getenv("BUGHARVESTER_FOLDER") + "/conf/bugHarvester.cfg")
    print(Figlet().renderText("BugHarvester"))
    app.run(cfg.host, cfg.port, cfg.ssl_contex)
    # pass
