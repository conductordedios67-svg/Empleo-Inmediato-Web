# ==========================================
# PLUGIN DE PRUEBA
# ==========================================

from core.motor import Motor
from core.web import descargar


class Prueba(Motor):

    def __init__(self):
        super().__init__()
        self.nombre = "Prueba"

    # ==========================================
    # BUSCAR
    # ==========================================

    def buscar(self, palabras=None):

        print(f"Buscando en {self.nombre}...")

        if not palabras:
            print(
                "⚠ No se recibió ninguna "
                "palabra de búsqueda."
            )
            return []

        if isinstance(palabras, str):
            palabras = [palabras]

        for palabra in palabras:

            palabra = palabra.strip()

            if not palabra:
                continue

            print(
                f"Palabra clave: {palabra}"
            )

        # ======================================
        # CONEXIÓN DE PRUEBA
        # ======================================

        try:

            html = descargar(
                "https://example.com"
            )

            if html:
                print(
                    "Conexión de prueba correcta."
                )

        except Exception as error:

            print(
                f"✖ Error en prueba: {error}"
            )

        return []
