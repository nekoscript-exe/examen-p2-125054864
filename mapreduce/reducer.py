
#!/usr/bin/env python3
import sys

clave_actual = None
total = 0

for linea in sys.stdin:
    try:
        clave, cantidad = linea.rstrip("\n").split("\t", 1)
        cantidad = int(cantidad)
    except ValueError:
        continue

    if clave_actual is not None and clave != clave_actual:
        print(f"{clave_actual}\t{total}")
        total = 0

    clave_actual = clave
    total += cantidad

if clave_actual is not None:
    print(f"{clave_actual}\t{total}")
