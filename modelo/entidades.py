"""
"""
from jsonable import Jsonable


class Cuenta(Jsonable):
    """
    """

    def __init__(self, **args):
        self.nombre = args["nombre"]
        self.tarjetas = args["tarjetas"]


class Tarjeta(Jsonable):
    """
    """

    def __init__(self,  **args):
        self.nombre = args["nombre"]
        self.creditos = args["creditos"]


class Credito(Jsonable):
    """
    """

    def __init__(self, **args):
        self.nombre = args["nombre"]
        self.cuotas_total = args["cuotas_total"]
        self.cuotas_pendientes = args["cuotas_pendientes"]
        self.monto = args["monto"]
