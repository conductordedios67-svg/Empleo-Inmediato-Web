# ==========================================
# SISTEMA DE ALARMA
# EMPLEO INMEDIATO
# ==========================================

import os
import sys

class Alarma:

    def __init__(self):

        self.activa = True

        self.archivo_sonido = os.path.join(
            "sonidos",
            "alarma_04_nueva_oferta.wav"
        )

    # ==========================================
    # ACTIVAR ALARMA
    # ==========================================

    def activar(self, oferta=None):

        if not self.activa:
            return

        # La alarma solamente se encarga
        # del aviso sonoro.
        self.reproducir()


    # ==========================================
    # REPRODUCIR SONIDO
    # ==========================================

    def reproducir(self):

        if os.path.exists(
            self.archivo_sonido
        ):
          
            try:

                from kivy.core.audio import SoundLoader

                sonido = SoundLoader.load(
                    self.archivo_sonido
                )

                if sonido:
                    sonido.play()

            except Exception as error:

                print(
                    f"✖ Error reproduciendo "
                    f"alarma: {error}"
                )                      

        else:

            print(
                "⚠ No se encontró el archivo "
                "de sonido:"
            )

            print(
                self.archivo_sonido
            )

            # Alarma de respaldo.
            try:

                winsound.MessageBeep(
                    winsound.MB_ICONEXCLAMATION
                )

            except Exception:

                pass


    # ==========================================
    # ACTIVAR / DESACTIVAR
    # ==========================================

    def activar_alarma(self):

        self.activa = True


    def desactivar_alarma(self):

        self.activa = False


    def esta_activa(self):

        return self.activa
