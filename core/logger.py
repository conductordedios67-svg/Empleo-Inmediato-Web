import logging
import os

# Crear carpeta logs si no existe
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/empleo_inmediato.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)

def escribir_log(mensaje):
    logging.info(mensaje)
