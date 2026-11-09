
import os
from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


DIAS = [
    "Lunes", "Martes", "Miercoles",
    "Jueves", "Viernes", "Sabado", "Domingo"
]

PAGOS = [
    "Efectivo", "Tarjeta", "Transferencia", "Vales"
]


def conectar():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "db"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "datamart"),
        user=os.getenv("POSTGRES_USER", "datamart_user"),
        password=os.environ["POSTGRES_PASSWORD"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resultados (
                metodo_pago VARCHAR(30) NOT NULL,
                dia_semana VARCHAR(20) NOT NULL,
                unidades BIGINT NOT NULL CHECK (unidades >= 0),
                PRIMARY KEY (metodo_pago, dia_semana)
            )
        """)
    yield


app = FastAPI(
    title="DataMart - Pipeline de datos",
    description="Examen P2 - Matricula 125054864",
    version="1.0.0",
    lifespan=lifespan,
)


class Resultado(BaseModel):
    metodo_pago: str
    dia_semana: str
    unidades: int = Field(ge=0)


@app.get("/")
def inicio():
    return {
        "proyecto": "DataMart",
        "matricula": "125054864",
        "estado": "API funcionando"
    }


@app.get("/salud")
def salud():
    with conectar() as conn:
        conn.execute("SELECT 1")
    return {"api": "OK", "database": "OK"}


@app.get("/resultados")
def obtener_resultados():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT metodo_pago, dia_semana, unidades
                FROM resultados
                ORDER BY metodo_pago, dia_semana
            """)
            filas = cur.fetchall()

    return [
        {
            "metodo_pago": fila[0],
            "dia_semana": fila[1],
            "unidades": fila[2]
        }
        for fila in filas
    ]


@app.get("/resultados/{clave}")
def filtrar_resultados(clave: str):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT metodo_pago, dia_semana, unidades
                FROM resultados
                WHERE LOWER(metodo_pago) = LOWER(%s)
                ORDER BY dia_semana
            """, (clave,))
            filas = cur.fetchall()

    return [
        {
            "metodo_pago": fila[0],
            "dia_semana": fila[1],
            "unidades": fila[2]
        }
        for fila in filas
    ]


@app.post("/resultados", status_code=201)
def agregar_resultado(resultado: Resultado):
    if resultado.metodo_pago not in PAGOS:
        raise HTTPException(400, "Metodo de pago invalido")

    if resultado.dia_semana not in DIAS:
        raise HTTPException(400, "Dia de la semana invalido")

    with conectar() as conn:
        conn.execute("""
            INSERT INTO resultados
                (metodo_pago, dia_semana, unidades)
            VALUES (%s, %s, %s)
            ON CONFLICT (metodo_pago, dia_semana)
            DO UPDATE SET unidades = EXCLUDED.unidades
        """, (
            resultado.metodo_pago,
            resultado.dia_semana,
            resultado.unidades
        ))

    return {
        "mensaje": "Resultado guardado",
        "resultado": resultado
    }
