from typing import Any
from flask import Flask, Response

#TODO add gunicorn to run in daemon
class EndpointAction(object):
    def __init__(self, action:Any):
        self.action = action

    def __call__(self, *args, **kwargs):
        res = self.action(*args, **kwargs)
        self.response = Response(res, status=200, headers={})
        return self.response


class FlaskAppWrapper(object):
    def __init__(self, name: str):
        self.app = Flask(name)

    def run(self, host:str="127.0.0.1", port:int=12003, context:Any=None) -> None:
        self.app.run(host, port, ssl_context=context)

    def add_endpoint(self, endpoint:str=None, endpoint_name:str=None, handler:Any=None) -> None:
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler))

    # def add_endpoints(self, endpoint:list[str]=None, endpoint_name:list[str]=None, handler:list[Any]=None) -> None:
    #     pass

# def action():
#     pass

# a = FlaskAppWrapper('wrap')
# a.add_endpoint(endpoint='/ad', endpoint_name='ad', handler=action)
# a.run()
