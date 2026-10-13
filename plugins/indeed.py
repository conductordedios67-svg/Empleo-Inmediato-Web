# ==========================================
# PLUGIN INDEED
# ==========================================

from core.motor import Motor


class Indeed(Motor):

    def __init__(self):

        super().__init__()

        self.nombre = "Indeed"

    # ==========================================
    # BUSCAR EMPLEOS
    # ==========================================

    def buscar(self, palabras=None):

        print(
            f"Buscando en {self.nombre}..."
        )

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

        # --------------------------------------
        # SCRAPING DE INDEED
        # SE IMPLEMENTARÁ POSTERIORMENTE
        # --------------------------------------

        return []
