"""
"""
from modelo.entidades import Cuenta, Tarjeta, Credito


csm = []
csm.append(Credito(identificador="gasto1", cuotas_total=12,
                   cuotas_pendientes=1, monto=60.4))
csm.append(Credito(identificador="gasto2", cuotas_total=6,
                   cuotas_pendientes=5, monto=15.4))
csm.append(Credito(identificador="gasto3", cuotas_total=3,
                   cuotas_pendientes=3, monto=111.4))

csv = []
csv.append(Credito(identificador="gasto4", cuotas_total=12,
                   cuotas_pendientes=12, monto=1360.4))
csv.append(Credito(identificador="gasto5", cuotas_total=1,
                   cuotas_pendientes=1, monto=1.4))
csv.append(Credito(identificador="gasto6", cuotas_total=12,
                   cuotas_pendientes=8, monto=666.4))

ts = {}
ts["Mastercard"] = Tarjeta(nombre="Mastercard", creditos=csm)
ts["Visa"] = Tarjeta(nombre="Visa", creditos=csv)
cuenta1 = Cuenta(nombre="MiCuenta", tarjetas=ts)

print "------------------------------------------------------------------"

print cuenta1.serialize()
print Cuenta.deserialize(cuenta1.serialize())

print "------------------------------------------------------------------"
f = ts["Mastercard"].serialize()
g = Tarjeta.deserialize(f)

print f
print g

print "------------------------------------------------------------------"

c = Credito(nombre="gasto1", cuotas_total=12, cuotas_pendientes=1, monto=60.4)
d = c.serialize()
e = Credito.deserialize(d)
print e

# with open("files/resumen.txt", 'w+') as output_file:
# json.dump(ret, output_file, sort_keys=self.json_sort_keys,
# indent=self.json_indent)
