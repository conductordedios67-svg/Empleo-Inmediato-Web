# ==========================================
# MOTOR BASE DE EMPLEO INMEDIATO
# ==========================================


class Motor:

    def __init__(self):
        self.nombre = "Motor"

    # ==========================================
    # BUSCAR EMPLEOS
    # ==========================================

    def buscar(self, palabras=None):
        """
        Método base para los plugins.

        palabras:
            Puede recibir una palabra o una lista
            de palabras de búsqueda.

        Cada portal implementará su propia
        versión de este método.
        """

        return []
