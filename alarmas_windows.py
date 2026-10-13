
import os
import sys
import winsound
import tkinter as tk
from tkinter import ttk, messagebox


class AlarmasWindows:
    """Gestor independiente de alarmas para Empleo Inmediato."""

    def __init__(self):
        self.activa = True
        self.carpeta = os.path.dirname(os.path.abspath(__file__))
        self.carpeta_sonidos = os.path.join(self.carpeta, "sonidos")
             
        self.sonidos = {
            "01 - Alarma clásica": "alarma.wav",
            "02 - Nueva oferta": "alarma_04_nueva_oferta.wav",
            "03 - Ejecutivo sutil": "ejecutivo_sutil.wav",
            "04 - Campanilla doble": "campanilla_doble.wav",
            "05 - Confirmación profesional": "confirmacion_profesional.wav",
            "06 - Alerta profesional": "alerta_profesional.wav",
            "07 - Tono ascendente": "tono_ascendente.wav",
            "08 - Teléfono discreto": "telefono_discreto.wav",
            "09 - Notificación premium": "notificacion_premium.wav",
            "10 - Tres tonos ejecutivos": "tres_tonos_ejecutivos.wav",
        }     

        self.archivo_configuracion = os.path.join(
            self.carpeta, "alarma_windows.cfg"
        )

        self.sonido_seleccionado = self._cargar_preferencia()

    def _cargar_preferencia(self):
        try:
            with open(
                self.archivo_configuracion, "r", encoding="utf-8"
            ) as archivo:
                nombre = archivo.read().strip()
                if nombre in self.sonidos:
                    return nombre
        except OSError:
            pass

        return "02 - Nueva oferta"
        

    def guardar_preferencia(self, nombre):
        if nombre not in self.sonidos:
            return False

        try:
            with open(
                self.archivo_configuracion, "w", encoding="utf-8"
            ) as archivo:
                archivo.write(nombre)

            self.sonido_seleccionado = nombre
            return True
        except OSError as error:
            messagebox.showerror(
                "Empleo Inmediato",
                f"No se pudo guardar la preferencia:\n{error}"
            )
            return False

    def reproducir(self, nombre=None):
        if not self.activa:
            return False

        nombre = nombre or self.sonido_seleccionado
        archivo = self.sonidos.get(nombre)

        if not archivo:
            return False

        ruta = os.path.join(self.carpeta_sonidos, archivo)

        if not os.path.isfile(ruta):
            messagebox.showwarning(
                "Empleo Inmediato",
                f"No se encuentra el sonido:\n{ruta}"
            )
            return False

        try:
            winsound.PlaySound(
                ruta,
                winsound.SND_FILENAME | winsound.SND_ASYNC
            )
            return True
        except Exception as error:
            messagebox.showerror(
                "Error de alarma",
                str(error)
            )
            return False

    def activar(self, oferta=None):
        return self.reproducir()

    def detener(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    def activar_alarma(self):
        self.activa = True

    def desactivar_alarma(self):
        self.activa = False
        self.detener()

    def esta_activa(self):
        return self.activa


def abrir_configuracion():
    alarmas = AlarmasWindows()

    ventana = tk.Tk()
    ventana.title("Empleo Inmediato - Configuración de alarmas")
    ventana.geometry("460x260")
    ventana.resizable(False, False)

    marco = ttk.Frame(ventana, padding=20)
    marco.pack(fill="both", expand=True)

    ttk.Label(
        marco,
        text="CONFIGURACIÓN DE ALARMAS",
        font=("Arial", 13, "bold")
    ).pack(pady=(0, 15))

    ttk.Label(
        marco,
        text="Selecciona un sonido:"
    ).pack(anchor="w")

    seleccion = tk.StringVar(value=alarmas.sonido_seleccionado)

    lista = ttk.Combobox(
        marco,
        textvariable=seleccion,
        values=list(alarmas.sonidos.keys()),
        state="readonly",
        width=35
    )
    lista.pack(fill="x", pady=8)

    def probar():
        alarmas.reproducir(seleccion.get())

    def guardar():
        if alarmas.guardar_preferencia(seleccion.get()):
            messagebox.showinfo(
                "Empleo Inmediato",
                "Preferencia de alarma guardada."
            )

    botones = ttk.Frame(marco)
    botones.pack(pady=15)

    ttk.Button(
        botones, text="Probar sonido", command=probar
    ).pack(side="left", padx=5)

    ttk.Button(
        botones, text="Guardar selección", command=guardar
    ).pack(side="left", padx=5)

    ventana.protocol("WM_DELETE_WINDOW", lambda: (
        alarmas.detener(), ventana.destroy()
    ))

    ventana.mainloop()


if __name__ == "__main__":
    abrir_configuracion()
