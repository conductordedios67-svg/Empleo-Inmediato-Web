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

        self.plugins = []

        if __import__("platform").system() == "Windows":
            from alarmas_windows import AlarmasWindows
            self.alarma = AlarmasWindows()
        else:
            self.alarma = Alarma()
        
        self.notificaciones = Notificaciones()

        self.cola_ofertas = queue.Queue()

        self.hilo_notificaciones = None
        self.detener_notificaciones = threading.Event()

        self.intervalo_notificacion = 15

        self.ultimas_ofertas_encontradas = []
        self.ultimas_ofertas_nuevas = []

        self.bloqueo_busqueda = threading.Lock()

        self.detener_busqueda_evento = threading.Event()

        # ------------------------------------------
        # VIGILANTE AUTOMÁTICO
        # ------------------------------------------

        self.hilo_vigilante = None
        self.detener_vigilante_evento = threading.Event()
        self.vigilante_activo = False
        self.intervalo_vigilante = 300
        self.palabras_vigilante = []

        self.busqueda_activa = False

        self.cargar_plugins()
        self.iniciar_cola_notificaciones()

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
                    f"ERROR CARGANDO PLUGIN {nombre}: {error}"
                )

        print()
        print(
            f"PLUGINS ACTIVOS: {len(self.plugins)}"
        )
        print()

    # ==========================================
    # BÚSQUEDA MANUAL
    # ==========================================

    def iniciar_busqueda(self):

        self.detener_busqueda_evento.clear()

        self.busqueda_activa = True

        print()
        print("BÚSQUEDA ACTIVADA.")
        print()

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

    def esta_busqueda_activa(self):

        return self.busqueda_activa

    def debe_detener_busqueda(self):

        return self.detener_busqueda_evento.is_set()

    # ==========================================
    # VIGILANTE AUTOMÁTICO
    # ==========================================

    def iniciar_vigilante(
        self,
        palabras,
        intervalo=300
    ):

        if not palabras:

            print()
            print(
                "NO HAY PALABRAS PARA EL VIGILANTE."
            )
            print()

            return False

        if isinstance(palabras, str):

            palabras = [palabras]

        palabras = [
            str(palabra).strip()
            for palabra in palabras
            if palabra and str(palabra).strip()
        ]

        if not palabras:

            return False

        if self.vigilante_activo:

            print()
            print(
                "EL VIGILANTE YA ESTÁ ACTIVO."
            )
            print()

            return False

        self.palabras_vigilante = palabras

        self.intervalo_vigilante = max(
            1,
            int(intervalo)
        )

        self.detener_vigilante_evento.clear()

        self.vigilante_activo = True

        self.hilo_vigilante = threading.Thread(
            target=self._ejecutar_vigilante,
            daemon=True
        )

        self.hilo_vigilante.start()

        print()
        print("VIGILANTE ACTIVADO.")
        print(
            "PALABRAS: "
            + ", ".join(self.palabras_vigilante)
        )
        print(
            f"INTERVALO: "
            f"{self.intervalo_vigilante} SEGUNDOS"
        )
        print()

        return True

    def _ejecutar_vigilante(self):

        try:

            while not self.detener_vigilante_evento.is_set():

                print()
                print(
                    "VIGILANTE: EJECUTANDO BÚSQUEDA..."
                )
                print()

                try:

                    self.ejecutar_busquedas(
                        self.palabras_vigilante
                    )

                except Exception as error:

                    print()
                    print(
                        f"ERROR EN VIGILANTE: {error}"
                    )
                    print()

                if self.detener_vigilante_evento.is_set():

                    break

                print()
                print(
                    "VIGILANTE: PRÓXIMA BÚSQUEDA "
                    f"EN {self.intervalo_vigilante} "
                    "SEGUNDOS."
                )
                print()

                self.detener_vigilante_evento.wait(
                    timeout=self.intervalo_vigilante
                )

        finally:

            self.vigilante_activo = False

            print()
            print("VIGILANTE: DETENIDO.")
            print()

    def detener_vigilante(self):

        if not self.vigilante_activo:
            return False

        self.detener_vigilante_evento.set()

        if (
            self.hilo_vigilante
            and self.hilo_vigilante.is_alive()
        ):

            if (
                threading.current_thread()
                is not self.hilo_vigilante
            ):

                self.hilo_vigilante.join(
                    timeout=2
                )

        self.vigilante_activo = False

        print()
        print(
            "SOLICITUD DE DETENCIÓN "
            "DEL VIGILANTE RECIBIDA."
        )
        print()

        return True

    def esta_vigilante_activo(self):

        return self.vigilante_activo

    # ==========================================
    # EJECUCIÓN DE BÚSQUEDAS
    # ==========================================

    def ejecutar_busquedas(self, palabras=None):

        if not palabras:

            return []

        if isinstance(palabras, str):

            palabras = [palabras]

        palabras = [
            str(palabra).strip()
            for palabra in palabras
            if palabra and str(palabra).strip()
        ]

        if not palabras:

            return []

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

                    if self.debe_detener_busqueda():

                        print()
                        print(
                            "BÚSQUEDA DETENIDA "
                            "POR EL USUARIO."
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
                            f"Buscando en "
                            f"{nombre_plugin}..."
                        )

                        resultado = plugin.buscar(
                            palabra
                        )

                        if isinstance(
                            resultado,
                            dict
                        ):

                            encontradas = (
                                resultado.get(
                                    "encontradas",
                                    []
                                )
                            )

                            nuevas = (
                                resultado.get(
                                    "nuevas",
                                    []
                                )
                            )

                            if encontradas:

                                todas_las_ofertas.extend(
                                    encontradas
                                )

                            if nuevas:

                                nuevas_ofertas.extend(
                                    nuevas
                                )

                        elif isinstance(
                            resultado,
                            list
                        ):

                            todas_las_ofertas.extend(
                                resultado
                            )

                        # ------------------------------------------
                        # SI EL USUARIO PIDIÓ DETENER,
                        # NO CONTINUAR CON EL SIGUIENTE PLUGIN
                        # ------------------------------------------

                        if self.debe_detener_busqueda():

                            print()
                            print(
                                "BÚSQUEDA DETENIDA "
                                "POR EL USUARIO."
                            )
                            print()

                            break

                    except Exception as error:

                        print()
                        print(
                            f"ERROR EN PLUGIN "
                            f"{nombre_plugin}: "
                            f"{error}"
                        )
                        print()

                if self.debe_detener_busqueda():

                    break

            self.ultimas_ofertas_encontradas = (
                todas_las_ofertas
            )

            self.ultimas_ofertas_nuevas = (
                nuevas_ofertas
            )

            if nuevas_ofertas:

                self.agregar_a_cola(
                    nuevas_ofertas
                )

            print()
            print("=" * 60)
            print(
                "OFERTAS ENCONTRADAS: "
                f"{len(todas_las_ofertas)}"
            )
            print(
                "NUEVAS OFERTAS DETECTADAS: "
                f"{len(nuevas_ofertas)}"
            )
            print("=" * 60)
            print()

            if self.debe_detener_busqueda():

                print(
                    "RESULTADO: BÚSQUEDA "
                    "DETENIDA POR EL USUARIO."
                )
                print()

            else:

                print(
                    "RESULTADO: BÚSQUEDA "
                    "FINALIZADA."
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
    # COLA DE NOTIFICACIONES
    # ==========================================

    def iniciar_cola_notificaciones(self):

        if (
            self.hilo_notificaciones
            and self.hilo_notificaciones.is_alive()
        ):

            return

        self.detener_notificaciones.clear()

        self.hilo_notificaciones = (
            threading.Thread(
                target=self._procesar_cola,
                daemon=True
            )
        )

        self.hilo_notificaciones.start()

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

            self.detener_notificaciones.wait(
                timeout=self.intervalo_notificacion
            )

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

        try:

            self.alarma.activar(
                oferta
            )

        except Exception as error:

            print(
                f"ERROR EN ALARMA: "
                f"{error}"
            )

        try:

            self.notificaciones.mostrar(
                oferta
            )

        except Exception as error:

            print(
                f"ERROR EN NOTIFICACIÓN: "
                f"{error}"
            )

    # ==========================================
    # DETENER COLA
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
