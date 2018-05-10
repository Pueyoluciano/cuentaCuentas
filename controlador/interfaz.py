"""
"""
from modelo.jsonable import jsonable
class Interfaz(jsonable):
    def __init__(self, **args):
        self.version = args["version"]