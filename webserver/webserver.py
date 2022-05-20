from flaskAppWrapper import FlaskAppWrapper
from configparser import ConfigParser
from webserverCFG import WebserverConfig
from pyfiglet import Figlet
import os

def main():
    print(Figlet().renderText("BugHarvester"))
    cfg = WebserverConfig()
    app = FlaskAppWrapper("BugHarverser-webserver")
    app.run(cfg.host, cfg.port, cfg.ssl_contex)

if (__name__ == "__main__"):
    main()