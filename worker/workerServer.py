from socketlistener import Server
from configparser import ConfigParser
from pyfiglet import Figlet
import os

def main():
    print(Figlet().renderText("BugHarvester"))
    config = ConfigParser()
    config.read(os.getenv("BUGHARVESTER_FOLDER") + "/bugHarvester.cfg")
    app = Server(config["worker"]["host"], int(config["worker"]["port"]))
    app.run()
    app.stop_server()

if (__name__ == "__main__"):
    main()