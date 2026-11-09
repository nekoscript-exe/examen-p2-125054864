
#!/usr/bin/env python3
import csv
import sys
from collections import defaultdict
from datetime import datetime

PAGOS = {"Efectivo", "Tarjeta", "Transferencia", "Vales"}


def main():
    archivo = sys.argv[1]
    resultados = defaultdict(int)

    with open(archivo, newline="", encoding="utf-8") as f:
        lector = csv.reader(f)

        for fila in lector:
            try:
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
                clave = f"{metodo_pago}|{dia_semana}"

                resultados[clave] += cantidad

            except (ValueError, IndexError, csv.Error):
                continue

    for clave in sorted(resultados):
        print(f"{clave}\t{resultados[clave]}")


if __name__ == "__main__":
    main()
