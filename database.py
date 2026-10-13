# ==========================================
# BASE DE DATOS
# EMPLEO INMEDIATO
# MULTIPLATAFORMA
# ==========================================

import os
import sqlite3
from datetime import datetime


# ==========================================
# CONFIGURACIÓN
# ==========================================

CARPETA_DATOS = "datos"

DB = os.path.join(
    CARPETA_DATOS,
    "empleos.db"
)


# ==========================================
# CREAR CARPETA DE DATOS
# ==========================================

os.makedirs(
    CARPETA_DATOS,
    exist_ok=True
)


# ==========================================
# CONEXIÓN
# ==========================================

def conectar():

    conexion = sqlite3.connect(
        DB
    )

    return conexion


# ==========================================
# CREAR TABLAS
# ==========================================

def crear_tablas():

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleos (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                portal TEXT NOT NULL,

                empresa TEXT,

                cargo TEXT,

                ciudad TEXT,

                enlace TEXT UNIQUE,

                fecha_publicacion TEXT,

                fecha_registro TEXT

            )
        """)

        conexion.commit()

    finally:

        conexion.close()


# ==========================================
# NORMALIZAR ENLACE
# ==========================================

def normalizar_enlace(enlace):

    if not enlace:

        return ""

    enlace = str(
        enlace
    ).strip()

    if not enlace:

        return ""

    # --------------------------------------
    # ELIMINAR FRAGMENTO DEL ENLACE
    # --------------------------------------

    enlace = enlace.split(
        "#",
        1
    )[0]

    # --------------------------------------
    # ELIMINAR / FINAL
    # --------------------------------------

    enlace = enlace.rstrip("/")

    return enlace


# ==========================================
# COMPROBAR SI EXISTE UN EMPLEO
# ==========================================

def existe_empleo(enlace):

    enlace = normalizar_enlace(
        enlace
    )

    if not enlace:

        return False

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT id
            FROM empleos
            WHERE enlace = ?
            """,
            (enlace,)
        )

        resultado = cursor.fetchone()

        return resultado is not None

    finally:

        conexion.close()


# ==========================================
# GUARDAR EMPLEO
# ==========================================

def guardar_empleo(oferta):

    if not oferta:

        return False

    enlace = oferta.get(
        "link",
        ""
    )

    if not enlace:

        return False

    enlace = normalizar_enlace(
        enlace
    )

    if not enlace:

        return False

   

    # --------------------------------------
    # COMPROBAR DUPLICADO
    # --------------------------------------

    if existe_empleo(enlace):

        return False
    

    # --------------------------------------
    # OBTENER DATOS
    # --------------------------------------

    portal = oferta.get(
        "portal",
        "Computrabajo"
    )

    empresa = oferta.get(
        "empresa",
        ""
    )

    cargo = oferta.get(
        "cargo",
        ""
    )

    ciudad = oferta.get(
        "ciudad",
        ""
    )

    fecha_publicacion = oferta.get(
        "fecha",
        ""
    )

    # --------------------------------------
    # LIMPIAR DATOS
    # --------------------------------------

    portal = str(
        portal or ""
    ).strip()

    empresa = str(
        empresa or ""
    ).strip()

    cargo = str(
        cargo or ""
    ).strip()

    ciudad = str(
        ciudad or ""
    ).strip()

    fecha_publicacion = str(
        fecha_publicacion or ""
    ).strip()

    fecha_registro = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------
    # INSERTAR
    # --------------------------------------

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO empleos (

                portal,
                empresa,
                cargo,
                ciudad,
                enlace,
                fecha_publicacion,
                fecha_registro

            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                portal,
                empresa,
                cargo,
                ciudad,
                enlace,
                fecha_publicacion,
                fecha_registro
            )
        )

        conexion.commit()

        return True

    except sqlite3.IntegrityError:

        conexion.rollback()

        return False

    finally:

        conexion.close()


# ==========================================
# OBTENER EMPLEOS
# ==========================================

def obtener_empleos():

    conexion = conectar()

    try:

        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT

                portal,
                empresa,
                cargo,
                ciudad,
                fecha_publicacion,
                fecha_registro,
                enlace

            FROM empleos

            ORDER BY id DESC
            """
        )

        datos = cursor.fetchall()

        return datos

    finally:

        conexion.close()


# ==========================================
# INICIALIZAR BASE DE DATOS
# ==========================================

crear_tablas()
