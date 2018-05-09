import json
import pickle

class Credito(object):
    def __init__(self, nombre, cuotas_total, cuotas_pendientes, monto):
        self.nombre = nombre
        self.cuotas_total = cuotas_total
        self.cuotas_pendientes = cuotas_pendientes
        self.monto = monto

    # def __repr__(self):
    #     return str({
    #         "nombre": self.nombre,
    #         "cuotas_total": self.cuotas_total,
    #         "cuotas_pendientes": self.cuotas_pendientes,
    #         "monto": self.monto
    #     })


class Tarjeta(object):
    def __init__(self, nombre):
        self.nombre = nombre
        self.creditos = []

    # def __repr__(self):
    #     return str({
    #         "nombre": self.nombre,
    #         "creditos": self.creditos
    #     })


class Cuenta(object):
    def __init__(self, nombre):
        self.json_indent = 4
        self.json_sort_keys = True
        self.nombre = nombre
        self.tarjetas = {}

    # def __repr__(self):
    #     return str({
    #         "json_indent": self.json_indent,
    #         "json_sort_keys": self.json_sort_keys,
    #         "nombre": self.nombre,
    #         "tarjetas": self.tarjetas
    #     })



cuenta = Cuenta("c1")
tarjeta = Tarjeta("Mastercard")
cuenta.tarjetas["Mastercard"] = Tarjeta("Mastercard")
cuenta.tarjetas["Mastercard"].creditos.append(Credito("farabella",12,5,152.14))

print cuenta.__dict__
