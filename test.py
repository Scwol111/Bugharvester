from configparser import ConfigParser
from webserver.flaskAppWrapper import FlaskAppWrapper

app = FlaskAppWrapper(__name__)
app.run()