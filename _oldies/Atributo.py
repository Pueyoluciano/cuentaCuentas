import json
import copy

class Atributo(object):
    """
    """
    tipo = None

    def __init__(self, tipo, valor=None):
        self.valor = valor

        if valor:
            if isinstance(valor, tipo):
                self.tipo = tipo

            else:
                raise TypeError("El tipo pasado por parametro y el tipo del valor no coinciden.", tipo, type(valor))

        else:
            self.tipo = tipo

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
    def deserialize(cls, tipo, valor):
        return cls(tipo, valor)


class AtributoIndirectoSimple(Atributo):
    """
    """

    def __set__(self, obj, value):
        self.valor = value
        self.tipo = type(value)

    def serialize(self):
        return self.valor.serialize()

    @classmethod
    def deserialize(cls, tipo, valor):
        return cls(tipo, tipo.deserialize(valor))


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
    def deserialize(cls, tipo, valor):
        return cls([tipo.deserialize(x) for x in valor])


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
    def deserialize(cls, tipo, valor):
        ret = {}

        for key, value in obj.iteritems():
            ret[key] = tipo.deserialize(valor)

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
            deserialize_me[key] = cls.atributos[key].deserialize(cls.atributos[key].tipo, value)
    
        return cls(**deserialize_me)

    # def __repr__(self):
        # return str(self.serialize())

class Credito(Jsonable):
    atributos = {
        "nombre" : AtributoDirecto(str),
        "cuotas_total" : AtributoDirecto(int),
        "cuotas_pendientes" : AtributoDirecto(int),
        "monto" : AtributoDirecto(float)
    }

class Prueba(Jsonable):
    atributos = {
        "attr1" : AtributoIndirectoSimple(Credito)
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


def deserialize(obj, tipo):
    return tipo.deserialize(obj)


# --------------------------------------------------------------------------

# micuenta = Cuenta(nombre="Cuenta1", json_indent=4, json_sort_keys=True)

# micuenta.tarjetas["Mastercard"] = Tarjeta()
# micuenta.tarjetas["Mastercard"].creditos.append(Credito(nombre="farabella", cuotas_total=12, cuotas_pendientes=5, monto=124.5))
# micuenta.tarjetas["Mastercard"].creditos.append(Credito(nombre="ogt", cuotas_total=6, cuotas_pendientes=5, monto=51.5))

# micuenta.tarjetas["Visa"] = Tarjeta()
# micuenta.tarjetas["Visa"].creditos.append(Credito(nombre="GAS", cuotas_total=1, cuotas_pendientes=1, monto=600.5))
# micuenta.tarjetas["Visa"].creditos.append(Credito(nombre="LUZ", cuotas_total=1, cuotas_pendientes=1, monto=801.5))

# with open("files/resumen.txt", 'w+') as output_file:
#     json.dump(micuenta.serialize(), output_file, sort_keys=4, indent=True)

# with open("files/resumen.txt", 'r') as input_file:
#     obj = json.load(input_file)
#     a = Cuenta.deserialize(obj)
#     print a.tarjetas
# print json.dumps(micuenta.serialize(), indent=4, sort_keys=True)

print "---------------------------------------------------------------------"
credito1 = Credito(nombre="PRUEBA1", cuotas_total=1, cuotas_pendientes=1, monto=555.5)


print json.dumps(credito1.serialize(), indent=4, sort_keys=True)
j = json.dumps(credito1.serialize(), indent=4, sort_keys=True)

print type(credito1.serialize())
print deserialize(credito1.serialize(), Credito)
print credito1.deserialize(credito1.serialize())
print Credito.deserialize(credito1.serialize())

print "---------------------------------------------------------------------"
prueba1 = Prueba(attr1=Credito(nombre="PRUEBA2", cuotas_total=1, cuotas_pendientes=1, monto=555.5))

# prueba1 = Prueba()
print "attr1 vacio:", prueba1.attr1
prueba1["attr1"] = Credito(nombre="PRUEBA3", cuotas_total=1, cuotas_pendientes=1, monto=555.5)
print "attr1 con algo:", prueba1.attr1
print "\nprueba1:.serialize:\n", prueba1.serialize()
# print "\nprueba1.repr:\n", prueba1

print deserialize(prueba1.serialize(), Prueba).serialize()
print prueba1.deserialize(prueba1.serialize()).serialize()
print Prueba.deserialize(prueba1.serialize()).serialize()

print "---------------------------------------------------------------------"

tarjeta1 = Tarjeta()
tarjeta1.creditos.append(credito1)

print deserialize(tarjeta1.serialize(), Tarjeta).serialize()
print tarjeta1.creditos


# Resumen al 7/5/18
c = [['08/04/17', 'PARUOLO', [12,12], 209.45],
['02/05/17', 'GARBARINO SUC RIVADA',[12,12], 97.74],
['11/06/17', 'REVER PASS', [10,12],221.09],
['11/06/17', 'GRIMOLDI', [10,12], 236.84],
['07/10/17', 'EASY RIVADAVIA', [06,06], 299.85],
['25/01/18', 'WWW.OPSIONESARGENTIN', [03,12], 618.66],
['27/01/18', 'GASTRONOMIA BASMIR', [03,03], 198.73],
['12/02/18', 'EASY CABALLITO', [02,03], 372.28],
['17/02/18', 'LA PRIMAVERA CASA', [02,06], 226.66],
['16/03/18', 'GRIMOLDI', [01,06], 406.70],
['19/03/18', 'PERSONAL', [01,06], 1099.86],
['31/03/18', 'CARREFOUR MINI-AVELLAN', [01,03], 475.11]]

b = [['16/06/17', 'COQUETA INSOLENTE',  [11,12], 208.33],
['28/07/17', 'VENI A LA COCINA',        [9,12], 149.00],
['18/08/17', 'ORSO BIANCO',             [9,12], 70.83],
['30/01/18', 'ODONTOLOGIA INTEGRAL',    [3,4], 200.00],
['02/03/18', 'ADRIANO GIARDINO',        [2,2], 472.50],
['05/03/18', 'WETTING DAY',             [2,3], 366.66],
['09/03/18', 'HEYAS',                   [2,6], 215.00],
['22/03/18', 'PUPPIS',                  [1,1], 205.90],
['03/04/18', 'MYSTIQUE',                [1,3], 820.00],
['12/04/18', 'PUPPIS',                  [1,3], 200.16]]


# Reporte000
def total(cuotas, mes):
    a = 0
    for b in cuotas:
        if b[2][0] + mes <= b[2][1]:
            a += b[3]
            
    return a        