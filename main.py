"""
    Cuenta Cuentas V1.0
"""

import json


class Cuenta(object):
    """
        CUENTA CUENTAS v1.0
    """

    def __init__(self, nombre):
        print "CUENTA CUENTAS v1.0"
        self.json_indent = 4
        self.json_sort_keys = True
        self.nombre = nombre
        self.tarjetas = {}

    def json_to_class_creditos(self, creditos):
        """
        """
        ret = []
        for credito in creditos:
            ret.append(Credito(credito['nombre'], credito['monto'],
                               credito['cuotas_total'], credito['cuotas_pendientes']))

        return ret

    def json_to_class_tarjetas(self, tarjetas):
        """
        """
        ret = {}
        for nombre, obj in tarjetas.iteritems():
            ret[nombre] = Tarjeta(nombre)
            ret[nombre].creditos = self.json_to_class_creditos(obj['creditos'])

        return ret

    def load_json(self):
        """
            Levantar de un archivo externo en formato JSON.
        """

        with open("files/resumen.txt", 'r') as input_file:
            obj = json.load(input_file)

            self.json_indent = obj['json_indent']
            self.json_sort_keys = obj['json_sort_keys']
            self.nombre = obj['nombre']
            self.tarjetas = self.json_to_class_tarjetas(obj['tarjetas'])

    def to_json(self):
        """
            Guardar en un archivo externo en formato JSON.
        """
        ret = {}

        # pasar a JSON friendly los atributos
        ret['nombre'] = self.nombre
        ret['json_sort_keys'] = self.json_sort_keys
        ret['json_indent'] = self.json_indent
        ret['tarjetas'] = {}

        for nombre, objeto in self.tarjetas.iteritems():
            ret['tarjetas'][nombre] = objeto.to_json()

        with open("files/resumen.txt", 'w+') as output_file:
            json.dump(ret, output_file, sort_keys=self.json_sort_keys,
                      indent=self.json_indent)

        return ret


class Tarjeta(object):
    """
        Principalmente (por lo menos por ahora) para llevar
        registro de los gastos acumulados en una tarjeta de credito.
    """

    def __init__(self, nombre):
        self.nombre = nombre
        self.creditos = []

    def agregar_credito(self, nombre, monto, total, parcial):
        """
            Agregar un gasto a la tarjeta.
        """
        self.creditos.append(Credito(nombre, monto, total, parcial))

    def load_json(self, json_obj):
        """
        """
        pass

    def to_json(self):
        """
            Devuelve la version JSONificada de la clase.
        """
        ret = {'nombre': self.nombre, 'creditos': []}

        for credito in self.creditos:
            ret['creditos'].append(credito.to_json())

        return ret


class Credito(object):
    """
        Una compra hecha con una tarjeta de credito.
    """

    def __init__(self, nombre, monto, total, pendientes):
        self.nombre = nombre
        self.cuotas_total = total
        self.cuotas_pendientes = pendientes
        self.monto = monto

    @classmethod
    def load_json(cls, obj_list):
        """
            Recibe una lista de objetos (que son la version JSON 
            de la instancia de la clase).

            Devuelve una lista de instancias de la clase.
        """
        ret = []

        # for cred in obj_list:
        #     nombre = cred["nombre"]
        #     monto = cred["monto"]
        #     total = cred["cuotas_total"]
        #     pendientes = cred["cuotas_pendientes"]
        #     ret.append(Credito())


    def to_json(self):
        """
            Devuelve la version JSONificada de la clase.
        """
        return self.__dict__


class Jsonable(object):
    """
        Clase base para poder exportar e importar desde JSON
    """
    atributos = ["nombre"]

    def __init__(self, **attrs):
        self.campos = {}
        
        for key in self.atributos:
            self.campos[key] = Campo()

    @classmethod
    def load_json(cls, obj_list):
        """
            Recibe una lista de objetos (que son la version Json de la clase)
            y devuelve una lista de instancias.
        """

    def to_json(self):
        """
            Convierte una instancia de la clase a formato Json.
            Devuelve un String con dicha representacion.
        """
        ret = {}
        for key in self.campos.iteritems():
            self.campos[key].to_json()

class Campo(object):
    def __init__(self, identificador, valor, is_class):
        self.identificador = identificador
        self.valor = valor
        self.is_class = is_class

    @classmethod
    def load_json(cls, obj_list):
        pass

    def to_json(self):    
        if self.is_class:
            return self.valor.to_json()

        else:
            return self.valor

class Asd(Jsonable):
    """
    """
    atributos = ["asd1", "asd2"]


a = Asd(asd1="231",asd2="518")
a.to_json()
# a.load_json()


def main():
    cc = Cuenta('Tarjetas Credito Lucho')
    cc.tarjetas['MasterCard'] = Tarjeta('MasterCard')


    cc.tarjetas['MasterCard'].agregar_credito("HONKY TONK", 701.25, 12, 12)
    cc.tarjetas['MasterCard'].agregar_credito("PARUOLO", 209.45, 12, 9)
    cc.tarjetas['MasterCard'].agregar_credito("GARBARINO SUC RIVADA", 97.73, 12, 9)
    cc.tarjetas['MasterCard'].agregar_credito("REVER PASS", 221.08, 12, 7)
    cc.tarjetas['MasterCard'].agregar_credito("GRIMOLDI", 236.83, 12, 7)
    cc.tarjetas['MasterCard'].agregar_credito("WWW.MERCADOPAGO.COM", 343.42, 9, 7)
    cc.tarjetas['MasterCard'].agregar_credito("EASY RIVADAVIA", 299.85, 6, 3)
    cc.tarjetas['MasterCard'].agregar_credito("JUANITA JO", 600.00, 3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("LA JUANO SRL", 488.25, 2, 1)
    cc.tarjetas['MasterCard'].agregar_credito("WWW.VILLAGECINES.COM", 215.00, 1, 1)
    cc.tarjetas['MasterCard'].agregar_credito("SUPERMERCADO PUEYRREDO", 733.63, 1, 1)
    cc.tarjetas['MasterCard'].agregar_credito("LA PHARMACIE & LA PARF", 199.683, 3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("KOSIUKO", 733.34, 3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("BOBBI LA MER", 166.68, 3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("EXTRA LARGE XL", 864.00, 3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("WWW.STEAMPOWERED.COM", 279.96, 1, 1)
    cc.tarjetas['MasterCard'].agregar_credito("REVER PASS", 495.68,3, 1)
    cc.tarjetas['MasterCard'].agregar_credito("FALABELLA II", 1902.88, 2, 1)
    cc.tarjetas['MasterCard'].agregar_credito("MERPAGO*Bip Bip Regalo", 329.4, 1, 1)

    cc.tarjetas['Visa'] = Tarjeta('Visa')
    cc.tarjetas['Visa'].agregar_credito("GastoNro4", 500, 12, 2)
    cc.tarjetas['Visa'].agregar_credito("GastoNro5", 700, 6, 5)
    cc.tarjetas['Visa'].agregar_credito("GastoNro6", 200, 3, 1)

    cc.to_json()
    cc.load_json()


if __name__ == '__main__':
    main()
