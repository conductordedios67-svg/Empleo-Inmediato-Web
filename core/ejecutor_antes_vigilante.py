# ==========================================
# EJECUTOR PRINCIPAL
# EMPLEO INMEDIATO
# ==========================================

import importlib
import inspect
import queue
import threading

from core.gestor_plugins import obtener_plugins
from core.motor import Motor
from alarma import Alarma
from notificaciones import Notificaciones


class Ejecutor:

    def __init__(self):

        # ------------------------------------------
        # PLUGINS
        # ------------------------------------------

        self.plugins = []

        # ------------------------------------------
        # ALARMA Y NOTIFICACIONES
        # ------------------------------------------

        self.alarma = Alarma()
        self.notificaciones = Notificaciones()

        # ------------------------------------------
        # COLA DE OFERTAS NUEVAS
        # ------------------------------------------

        self.cola_ofertas = queue.Queue()

        self.hilo_notificaciones = None
        self.detener_notificaciones = threading.Event()

        # ------------------------------------------
        # CONTROL DE NOTIFICACIONES
        # ------------------------------------------

        self.intervalo_notificacion = 15

        # ------------------------------------------
        # RESULTADOS DE LA ÚLTIMA BÚSQUEDA
        # ------------------------------------------

        self.ultimas_ofertas_encontradas = []
        self.ultimas_ofertas_nuevas = []

        # ------------------------------------------
        # CONTROL DE BÚSQUEDA
        # ------------------------------------------

        self.bloqueo_busqueda = threading.Lock()

        self.detener_busqueda_evento = threading.Event()

        self.busqueda_activa = False

        # ------------------------------------------
        # CARGAR PLUGINS
        # ------------------------------------------

        self.cargar_plugins()

        # ------------------------------------------
        # INICIAR HILO DE NOTIFICACIONES
        # ------------------------------------------

        self.iniciar_cola_notificaciones()

    # ==========================================
    # CARGAR PLUGINS
    # ==========================================

    def cargar_plugins(self):

        self.plugins = []

        nombres = obtener_plugins()

        for nombre in nombres:

            try:

                modulo = importlib.import_module(
                    f"plugins.{nombre}"
                )

                clase_plugin = None

                for nombre_clase, clase in inspect.getmembers(
                    modulo,
                    inspect.isclass
                ):

                    if clase is Motor:
                        continue

                    try:

                        if issubclass(clase, Motor):

                            clase_plugin = clase
                            break

                    except TypeError:

                        continue

                if clase_plugin is None:
                    continue

                instancia = clase_plugin()

                self.plugins.append(instancia)

                print(
                    f"PLUGIN CARGADO: {nombre}"
                )

            except Exception as error:

                print(
                    f"ERROR CARGANDO PLUGIN {nombre}: "
                    f"{error}"
                )

        print()
        print(
            f"PLUGINS ACTIVOS: {len(self.plugins)}"
        )
        print()

    # ==========================================
    # INICIAR BÚSQUEDA
    # ==========================================

    def iniciar_busqueda(self):

        self.detener_busqueda_evento.clear()

        self.busqueda_activa = True

        print()
        print("BÚSQUEDA ACTIVADA.")
        print()

    # ==========================================
    # DETENER BÚSQUEDA
    # ==========================================

    def detener_busqueda(self):

        if not self.busqueda_activa:

            print()
            print("NO HAY UNA BÚSQUEDA ACTIVA.")
            print()

            return False

        self.detener_busqueda_evento.set()

        print()
        print("SOLICITUD DE DETENCIÓN RECIBIDA.")
        print()

        return True

    # ==========================================
    # ESTADO DE BÚSQUEDA
    # ==========================================

    def esta_busqueda_activa(self):

        return self.busqueda_activa

    # ==========================================
    # COMPROBAR SI DEBE DETENERSE
    # ==========================================

    def debe_detener_busqueda(self):

        return self.detener_busqueda_evento.is_set()

    # ==========================================
    # EJECUTAR BÚSQUEDAS
    # ==========================================

    def ejecutar_busquedas(self, palabras=None):

        if not palabras:
            return []

        # ------------------------------------------
        # NORMALIZAR PALABRAS
        # ------------------------------------------

        if isinstance(palabras, str):

            palabras = [palabras]

        palabras = [
            str(palabra).strip()
            for palabra in palabras
            if palabra and str(palabra).strip()
        ]

        if not palabras:
            return []

        # ------------------------------------------
        # EVITAR DOS BÚSQUEDAS SIMULTÁNEAS
        # ------------------------------------------

        if not self.bloqueo_busqueda.acquire(
            blocking=False
        ):

            print()
            print(
                "YA EXISTE UNA BÚSQUEDA EN EJECUCIÓN."
            )
            print()

            return []

        try:

            self.iniciar_busqueda()

            todas_las_ofertas = []
            nuevas_ofertas = []

            print()
            print("=" * 60)
            print("INICIANDO BÚSQUEDA")
            print("=" * 60)

            for palabra in palabras:

                # ----------------------------------
                # COMPROBAR DETENCIÓN
                # ----------------------------------

                if self.debe_detener_busqueda():

                    print()
                    print("BÚSQUEDA DETENIDA.")
                    print()

                    break

                print()
                print(
                    f"PALABRA DE BÚSQUEDA: {palabra}"
                )
                print()

                for plugin in self.plugins:

                    # ----------------------------------
                    # COMPROBAR DETENCIÓN
                    # ----------------------------------

                    if self.debe_detener_busqueda():

                        print()
                        print(
                            "BÚSQUEDA DETENIDA POR EL USUARIO."
                        )
                        print()

                        break

                    try:

                        nombre_plugin = getattr(
                            plugin,
                            "nombre",
                            plugin.__class__.__name__
                        )

                        print(
                            f"Buscando en {nombre_plugin}..."
                        )

                        resultado = plugin.buscar(
                            palabra
                        )

                        # ----------------------------------
                        # PLUGINS MODERNOS
                        # ----------------------------------

                        if isinstance(
                            resultado,
                            dict
                        ):

                            encontradas = resultado.get(
                                "encontradas",
                                []
                            )

                            nuevas = resultado.get(
                                "nuevas",
                                []
                            )

                            if encontradas:

                                todas_las_ofertas.extend(
                                    encontradas
                                )

                            if nuevas:

                                nuevas_ofertas.extend(
                                    nuevas
                                )

                        # ----------------------------------
                        # COMPATIBILIDAD CON PLUGINS ANTIGUOS
                        # ----------------------------------

                        elif isinstance(
                            resultado,
                            list
                        ):

                            todas_las_ofertas.extend(
                                resultado
                            )

                    except Exception as error:

                        print()
                        print(
                            f"ERROR EN PLUGIN "
                            f"{nombre_plugin}: {error}"
                        )
                        print()

                # ----------------------------------
                # SI SE DETUVO, NO CONTINUAR
                # ----------------------------------

                if self.debe_detener_busqueda():

                    break

            # ------------------------------------------
            # GUARDAR RESULTADOS
            # ------------------------------------------

            self.ultimas_ofertas_encontradas = (
                todas_las_ofertas
            )

            self.ultimas_ofertas_nuevas = (
                nuevas_ofertas
            )

            # ------------------------------------------
            # AGREGAR NUEVAS A LA COLA
            # ------------------------------------------

            if nuevas_ofertas:

                self.agregar_a_cola(
                    nuevas_ofertas
                )

            # ------------------------------------------
            # RESUMEN
            # ------------------------------------------

            print()
            print("=" * 60)
            print(
                f"OFERTAS ENCONTRADAS: "
                f"{len(todas_las_ofertas)}"
            )
            print(
                f"NUEVAS OFERTAS DETECTADAS: "
                f"{len(nuevas_ofertas)}"
            )
            print("=" * 60)
            print()

            if self.debe_detener_busqueda():

                print(
                    "RESULTADO: BÚSQUEDA DETENIDA POR EL USUARIO."
                )
                print()

            else:

                print(
                    "RESULTADO: BÚSQUEDA FINALIZADA."
                )
                print()

            return todas_las_ofertas

        finally:

            self.busqueda_activa = False

            self.detener_busqueda_evento.clear()

            self.bloqueo_busqueda.release()

            print(
                "ESTADO DE BÚSQUEDA: DETENIDA."
            )
            print()

    # ==========================================
    # INICIAR COLA DE NOTIFICACIONES
    # ==========================================

    def iniciar_cola_notificaciones(self):

        if (
            self.hilo_notificaciones
            and self.hilo_notificaciones.is_alive()
        ):

            return

        self.detener_notificaciones.clear()

        self.hilo_notificaciones = threading.Thread(
            target=self._procesar_cola,
            daemon=True
        )

        self.hilo_notificaciones.start()

    # ==========================================
    # PROCESAR COLA
    # ==========================================

    def _procesar_cola(self):

        while not self.detener_notificaciones.is_set():

            try:

                oferta = self.cola_ofertas.get(
                    timeout=0.5
                )

            except queue.Empty:

                continue

            try:

                self._presentar_oferta(
                    oferta
                )

            except Exception as error:

                print()
                print(
                    f"ERROR PRESENTANDO OFERTA: "
                    f"{error}"
                )
                print()

            finally:

                self.cola_ofertas.task_done()

            if self.detener_notificaciones.is_set():

                break

            # --------------------------------------
            # ESPERAR 15 SEGUNDOS
            # --------------------------------------

            self.detener_notificaciones.wait(
                timeout=self.intervalo_notificacion
            )

    # ==========================================
    # AGREGAR OFERTAS A LA COLA
    # ==========================================

    def agregar_a_cola(self, ofertas):

        if not ofertas:
            return

        if isinstance(ofertas, dict):

            ofertas = [ofertas]

        for oferta in ofertas:

            if not oferta:
                continue

            self.cola_ofertas.put(
                oferta
            )

    # ==========================================
    # PRESENTAR OFERTA
    # ==========================================

    def _presentar_oferta(self, oferta):

        if not oferta:
            return

        print()
        print("=" * 60)
        print("NUEVA OFERTA DE EMPLEO")
        print("=" * 60)

        print(
            f"Cargo: "
            f"{oferta.get('cargo', '')}"
        )

        print(
            f"Empresa: "
            f"{oferta.get('empresa', '')}"
        )

        print(
            f"Ciudad: "
            f"{oferta.get('ciudad', '')}"
        )

        print(
            f"Portal: "
            f"{oferta.get('portal', '')}"
        )

        print(
            f"Enlace: "
            f"{oferta.get('link', '')}"
        )

        print("=" * 60)
        print()

        # ------------------------------------------
        # ALARMA
        # ------------------------------------------

        try:

            self.alarma.activar(
                oferta
            )

        except Exception as error:

            print(
                f"ERROR EN ALARMA: {error}"
            )

        # ------------------------------------------
        # NOTIFICACIÓN
        # ------------------------------------------

        try:

            self.notificaciones.mostrar(
                oferta
            )

        except Exception as error:

            print(
                f"ERROR EN NOTIFICACIÓN: {error}"
            )

    # ==========================================
    # DETENER COLA DE NOTIFICACIONES
    # ==========================================

    def detener_cola(self):

        self.detener_notificaciones.set()

        if (
            self.hilo_notificaciones
            and self.hilo_notificaciones.is_alive()
        ):

            self.hilo_notificaciones.join(
                timeout=2
            )

        print(
            "COLA DE NOTIFICACIONES DETENIDA."
        )


# ==========================================
# PRUEBA DIRECTA
# ==========================================

if __name__ == "__main__":

    ejecutor = Ejecutor()

    try:

        ejecutor.ejecutar_busquedas(
            "ABOGADO"
        )

    finally:

        ejecutor.detener_cola()