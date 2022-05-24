from flaskAppWrapper import FlaskAppWrapper
from webserverCFG import WebserverConfig
from pyfiglet import Figlet
import os

from flask import request as req
from flask import render_template

def function(*args, **kwargs):
    return render_template("./server/webserver/templates/index.html")
    # print(args)
    # print(kwargs)
    # print(req.headers)

def main():
    print(Figlet().renderText("BugHarvester"))
    cfg = WebserverConfig(os.getenv("BUGHARVESTER_FOLDER") + "/conf/bugHarvester.cfg")
    app = FlaskAppWrapper("BugHarverser-webserver")
    app.add_endpoint("/", "/", function)
    app.run(cfg.host, cfg.port, cfg.ssl_contex)

if (__name__ == "__main__"):
    main()