# ==========================================
# SISTEMA DE NOTIFICACIONES
# EMPLEO INMEDIATO
# MULTIPLATAFORMA
# ==========================================

import platform
import threading


class Notificaciones:

    def __init__(self):

        # ==========================================
        # ESTADO
        # ==========================================

        self.activas = True

        # Sistema operativo
        self.sistema = platform.system()


    # ==========================================
    # MOSTRAR NOTIFICACION
    # ==========================================

    def mostrar(self, oferta=None):

        print("DEBUG: se ejecutó Notificaciones.mostrar()")
        print("DEBUG: sistema =", self.sistema)

        if not self.activas:
            return

        titulo = "Empleo Inmediato"

        mensaje = (
            "¡Nueva oferta de empleo detectada!"
        )

        # ==========================================
        # INFORMACION DE LA OFERTA
        # ==========================================

        if oferta:

            cargo = str(
                oferta.get("cargo", "")
            ).strip()

            empresa = str(
                oferta.get("empresa", "")
            ).strip()

            ciudad = str(
                oferta.get("ciudad", "")
            ).strip()

            partes = []

            if cargo:
                partes.append(cargo)

            if empresa:
                partes.append(empresa)

            if ciudad:
                partes.append(ciudad)

            if partes:
                mensaje = "\n".join(partes)

        # ==========================================
        # WINDOWS
        # ==========================================

        if self.sistema == "Windows":

            hilo = threading.Thread(
                target=self._notificacion_windows,
                args=(titulo, mensaje),
                daemon=True
            )

            hilo.start()

        # ==========================================
        # ANDROID
        # ==========================================

        elif self.sistema == "Android":

            self._notificacion_android(
                titulo,
                mensaje
            )

        # ==========================================
        # OTROS SISTEMAS
        # ==========================================

        else:

            print()
            print("🔔 NOTIFICACIÓN")
            print(titulo)
            print(mensaje)
            print()


    # ==========================================
    # NOTIFICACION WINDOWS
    # ==========================================
    
    def _notificacion_windows(
        self,
        titulo,
        mensaje
    ):

        # Notificaciones emergentes de Windows desactivadas.
        # La alarma sonora y el buscador no se modifican.

        return

    # ==========================================
    # NOTIFICACION ANDROID
    # ==========================================

    def _notificacion_android(
        self,
        titulo,
        mensaje
    ):

        # La implementación Android
        # se conectará posteriormente
        # con la interfaz gui_android.

        print()
        print("🔔 NOTIFICACIÓN ANDROID")
        print(titulo)
        print(mensaje)
        print()


    # ==========================================
    # ACTIVAR NOTIFICACIONES
    # ==========================================

    def activar_notificaciones(self):

        self.activas = True


    # ==========================================
    # DESACTIVAR NOTIFICACIONES
    # ==========================================

    def desactivar_notificaciones(self):

        self.activas = False


    # ==========================================
    # CONSULTAR ESTADO
    # ==========================================

    def estan_activas(self):

        return self.activas
