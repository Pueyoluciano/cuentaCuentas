"""
"""
from jsonable import Jsonable


class Cuenta(Jsonable):
    """
    """

    def __init__(self, **args):
        self.nombre = args["nombre"]
        self.tarjetas = args["tarjetas"]

    def agregarTarjeta(self, nombreTarjeta, listaCreditos):
        if not nombreTarjeta in self.tarjetas:
            self.tarjetas[nombreTarjeta] = Tarjeta(nombre=nombreTarjeta, creditos=listaCreditos)

    def borrarTarjeta(self, nombreTarjeta):
        if nombreTarjeta in self.tarjetas:
            del(self.tarjetas[nombreTarjeta])

    def __str__(self):
        return "cuenta: " + self.nombre + "\n" + "Tarjetas: " + str(self.tarjetas.keys())


class Tarjeta(Jsonable):
    """
    """

    def __init__(self,  **args):
        self.nombre = args["nombre"]
        self.creditos = args["creditos"]

    def agregarCredito(self, identificador, fecha, cuotas_total, cuotas_pendientes, monto):
        self.creditos.append(Credito(identificador=identificador, fecha=fecha, cuotas_total=cuotas_total, cuotas_pendientes=cuotas_pendientes, monto=monto))


class Credito(Jsonable):
    """
    """

    def __init__(self, **args):
        self.identificador = args["identificador"]
        self.fecha = args["fecha"]
        self.cuotas_total = args["cuotas_total"]
        self.cuotas_pendientes = args["cuotas_pendientes"]
        self.monto = args["monto"]
