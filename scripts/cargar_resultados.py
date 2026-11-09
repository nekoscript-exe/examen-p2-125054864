
import os
from pathlib import Path

import psycopg

ARCHIVO = Path("/data/output/resultado/part-00000")

PAGOS = {"Efectivo", "Tarjeta", "Transferencia", "Vales"}

DIAS = [
    "Lunes", "Martes", "Miercoles",
    "Jueves", "Viernes", "Sabado", "Domingo"
]


def cargar_resultados():
    if not ARCHIVO.is_file():
        raise FileNotFoundError(
            f"No existe la salida de Hadoop: {ARCHIVO}"
        )

    registros = []

    with ARCHIVO.open(encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            clave, unidades = linea.strip().split("\t")
            metodo_pago, dia = clave.split("|")

            dia = int(dia)
            unidades = int(unidades)

            if metodo_pago not in PAGOS or not 0 <= dia <= 6:
                raise ValueError(f"Clave invalida en linea {numero}")

            if unidades < 0:
                raise ValueError(f"Cantidad negativa en linea {numero}")

            registros.append(
                (metodo_pago, DIAS[dia], unidades)
            )

    with psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    ) as conn:
        with conn.cursor() as cur:
            for registro in registros:
                cur.execute(
                    """
                    INSERT INTO resultados
                        (metodo_pago, dia_semana, unidades)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (metodo_pago, dia_semana)
                    DO UPDATE SET
                        unidades = EXCLUDED.unidades
                    """,
                    registro,
                )

            cur.execute("SELECT COUNT(*) FROM resultados")
            total = cur.fetchone()[0]

    print(f"Registros leidos de Hadoop: {len(registros)}")
    print(f"Registros almacenados en PostgreSQL: {total}")
    print("Carga finalizada correctamente")


if __name__ == "__main__":
    cargar_resultados()
