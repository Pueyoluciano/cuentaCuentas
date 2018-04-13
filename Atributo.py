import json
import copy

class Atributo(object):
    """
    """
    tipo = None

    def __init__(self, tipo, valor=None):
        self.valor = valor

        if valor:
            if isinstance(valor, type(tipo)):
                self.tipo = tipo

            else:
                raise TypeError("El tipo pasado por parametro y el tipo del valor no coinciden.", tipo, type(valor))

        else:
            self.tipo = None

    def __get__(self, obj, objtype):
        return self.valor

    def __set__(self, obj, val):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError

    @classmethod
    def deserialize(cls, obj):
        raise NotImplementedError

    def __repr__(self):
        return str(self.valor)


class AtributoDirecto(Atributo):
    """
    """

    def __set__(self, obj, value):
        self.valor = value
        self.tipo = type(value)
        
    def serialize(self):
        return self.valor

    @classmethod
    def deserialize(cls, obj):
        return cls(obj)


class AtributoIndirectoSimple(Atributo):
    """
    """

    def __set__(self, obj, value):
        self.valor = value
        self.tipo = type(value)

    def serialize(self):
        return self.valor.serialize()

    @classmethod
    def deserialize(cls, obj):
        return cls(cls.tipo.deserialize(obj))


class AtributoIndirectoLista(Atributo):
    """
    """

    def __init__(self, tipo, valor=None):
        super(AtributoIndirectoLista, self).__init__(tipo, valor if valor else [])

    def __set__(self, obj, val):
        if(isinstance(val, list)):
            self.valor = val
        else:
            raise Exception("Error al asignar un valor no iterable a self.valor")

    def __getitem__(self, key):
        return self.valor[key]

    def __setitem__(self, key, value):
        self.valor[key] = value
        self.tipo = type(value)

    def serialize(self):
        ret = []

        for item in self.valor:
            ret.append(item.serialize())

        return ret

    @classmethod
    def deserialize(cls, obj):
        return cls([cls.tipo.deserialize(x) for x in obj])


class AtributoIndirectoDiccio(Atributo):
    """
    """
    def __init__(self, tipo, valor=None):
        super(AtributoIndirectoDiccio, self).__init__(tipo, valor if valor else {})

    def __set__(self, obj, val):
        if isinstance(val, dict):
            self.valor = val
        else:
            raise Exception("Error al asignar un valor no iterable a self.valor")

    def __getitem__(self, key):
        return self.valor[key]

    def __setitem__(self, key, value):
        self.valor[key] = value
        self.tipo = type(value)

    def serialize(self):
        ret = {}

        for key, value in self.valor.iteritems():
            ret[key] = value.serialize()

        return ret

    @classmethod
    def deserialize(cls, obj):
        ret = {}

        for key, value in obj.iteritems():
            ret[key] = cls.tipo.deserialize(value)

        return cls(ret)    

#-----------------------------------------------------------


class Jsonable(object):
    """
    """
    atributos = {}

    def __init__(self, **args):
        self.atributos = copy.deepcopy(type(self).atributos)
        for key, value in args.iteritems():
            self.atributos[key].valor = value

    # return Jsonable[key]
    def __getitem__(self, key):
        return self.atributos[key].valor

    # Jsonable[key] = value
    def __setitem__(self, key, value):
        self.atributos[key].valor = value

    def __getattr__(self, key):
        return self.atributos[key].valor

    def serialize(self):
        ret = {}

        for key, value in self.atributos.iteritems():
            ret[key] = value.serialize()

        return ret

    @classmethod
    def deserialize(cls, obj):
        deserialize_me = {}

        for key, value in obj.iteritems():
            deserialize_me[key] = type(cls.atributos[key]).deserialize(value)

        return cls(**deserialize_me)


class Credito(Jsonable):
    atributos = {
        "nombre" : AtributoDirecto(str),
        "cuotas_total" : AtributoDirecto(int),
        "cuotas_pendientes" : AtributoDirecto(int),
        "monto" : AtributoDirecto(float)
    }


class Tarjeta(Jsonable):
    atributos = {
        "creditos": AtributoIndirectoLista(Credito)
    }


class Cuenta(Jsonable):
    atributos = {
        "json_indent" : AtributoDirecto(int),
        "json_sort_keys" : AtributoDirecto(bool),
        "nombre" : AtributoDirecto(str),
        "tarjetas" : AtributoIndirectoDiccio(Tarjeta)
    }


# --------------------------------------------------------------------------

micuenta = Cuenta(nombre="Cuenta1", json_indent=4, json_sort_keys=True)

micuenta.tarjetas["Mastercard"] = Tarjeta()
micuenta.tarjetas["Mastercard"].creditos.append(Credito(nombre="farabella", cuotas_total=12, cuotas_pendientes=5, monto=124.5))
micuenta.tarjetas["Mastercard"].creditos.append(Credito(nombre="ogt", cuotas_total=6, cuotas_pendientes=5, monto=51.5))

micuenta.tarjetas["Visa"] = Tarjeta()
micuenta.tarjetas["Visa"].creditos.append(Credito(nombre="GAS", cuotas_total=1, cuotas_pendientes=1, monto=600.5))
micuenta.tarjetas["Visa"].creditos.append(Credito(nombre="LUZ", cuotas_total=1, cuotas_pendientes=1, monto=801.5))

with open("files/resumen.txt", 'w+') as output_file:
    json.dump(micuenta.serialize(), output_file, sort_keys=4, indent=True)

with open("files/resumen.txt", 'r') as input_file:
    obj = json.load(input_file)
    a = Cuenta.deserialize(obj)
    print a.tarjetas
# print json.dumps(micuenta.serialize(), indent=4, sort_keys=True)

