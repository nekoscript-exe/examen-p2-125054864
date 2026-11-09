
#!/usr/bin/env python3
import sys
import csv
from datetime import datetime

PAGOS = {"Efectivo", "Tarjeta", "Transferencia", "Vales"}

for linea in sys.stdin:
    try:
        fila = next(csv.reader([linea]))

        if not fila or fila[0] == "id":
            continue

        if len(fila) != 8:
            continue

        fecha = datetime.strptime(
            fila[1], "%Y-%m-%d %H:%M:%S"
        )
        cantidad = int(fila[5])
        metodo_pago = fila[7].strip()

        if cantidad < 0 or metodo_pago not in PAGOS:
            continue

        dia_semana = fecha.weekday()

        print(f"{metodo_pago}|{dia_semana}\t{cantidad}")

    except (ValueError, IndexError, csv.Error):
        continue
