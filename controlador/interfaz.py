"""
"""
import json
from modelo.jsonable import Jsonable
from modelo.entidades import Cuenta

class Interfaz(Jsonable):
    def __init__(self, **args):
        self.cuenta = args["cuenta"]
        # self.version = args["version"]
        # self.nombre = args["nombre"]

    def consola(self):
        print "CUENTA CUENTAS"
        print "--------------"
        print self.cuenta
        print "--------------"
        print "Elige una opcion:"
        print "1 - Levantar desde archivo"
        print "2 - Actualizar archivo"
        print "0 - Salir"

        opt = ""

        while opt != "0":
            opt = raw_input("> ")

            if opt == "1":
                pass

            if opt == "2":
                self.saveToFile(self.cuenta)

    def loadFromFile(self):
        with open("archivos/resumen.txt", 'r') as input_file:
            return Cuenta.deserialize(input_file)

    def saveToFile(self, cuenta):
        with open("archivos/resumen.txt", 'w+') as output_file:
            cuenta.serialize(output_file)

    
if __name__ == '__main__':  
    a = Interfaz()
    a.consola()
        