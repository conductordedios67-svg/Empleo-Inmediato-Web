# ==========================================
# PLUGIN DINERS CLUB
# EMPLEO INMEDIATO
# ==========================================

import html
import re

import requests

from core.motor import Motor
from filtros import filtrar_ofertas
from database import guardar_empleo


class Diners(Motor):

    def __init__(self):

        super().__init__()

        self.nombre = "Diners Club"

        self.url = (
            "https://dce.twiinshrm.com/"
            "talento_api/index.php/vector_controller"
        )

        self.portal_codigo = "2"


    # ======================================
    # BUSCAR OFERTAS
    # ======================================

    def buscar(self, palabras=None):

        print(
            f"Buscando en {self.nombre}..."
        )

        if not palabras:

            print(
                "⚠ No se recibió ninguna palabra "
                "de búsqueda."
            )

            return []


        if isinstance(palabras, str):

            palabras = [palabras]


        try:

            ofertas = self._obtener_ofertas()

        except Exception as error:

            print(
                "✖ Error consultando Diners Club:"
            )

            print(error)

            return []


        print(
            f"Se encontraron "
            f"{len(ofertas)} procesos activos."
        )


        nuevas_ofertas = []


        for palabra in palabras:

            palabra = palabra.strip()

            if not palabra:
                continue


            print()
            print(
                f"🔍 Buscando: {palabra}"
            )


            ofertas_filtradas = (
                filtrar_ofertas(
                    ofertas,
                    palabra
                )
            )


            print(
                f'Coinciden con "{palabra}": '
                f"{len(ofertas_filtradas)}"
            )


            for oferta in ofertas_filtradas:

                try:

                    guardada = guardar_empleo(
                        oferta
                    )


                    if guardada:

                        nuevas_ofertas.append(
                            oferta
                        )

                        print()
                        print(
                            "🆕 NUEVA OFERTA DINERS"
                        )

                        print(
                            "Cargo   :",
                            oferta.get(
                                "cargo",
                                ""
                            )
                        )

                        print(
                            "Empresa :",
                            oferta.get(
                                "empresa",
                                ""
                            )
                        )

                        print(
                            "Ciudad  :",
                            oferta.get(
                                "ciudad",
                                ""
                            )
                        )

                        print(
                            "Fecha   :",
                            oferta.get(
                                "fecha",
                                ""
                            )
                        )

                        print(
                            "Código  :",
                            oferta.get(
                                "numero_oferta",
                                ""
                            )
                        )

                        print(
                            "Enlace  :",
                            oferta.get(
                                "link",
                                ""
                            )
                        )

                    else:

                        print(
                            "• Ya existe:",
                            oferta.get(
                                "cargo",
                                ""
                            )
                        )


                except Exception as error:

                    print(
                        "✖ Error guardando oferta Diners: "
                        f"{error}"
                    )


        print()
        print("=" * 60)
        print("DINERS CLUB")
        print(
            f"Nuevas ofertas: "
            f"{len(nuevas_ofertas)}"
        )
        print("=" * 60)


        return nuevas_ofertas


    # ======================================
    # CONSULTAR API
    # ======================================

    def _obtener_ofertas(self):

        filtros = {
            "portalCodigo":
                self.portal_codigo,

            "vectorEventoEstado":
                "1"
        }


        parametros = {

            "portales":
                "S",

            "camposFiltro":
                self._convertir_json(filtros)
        }


        respuesta = requests.get(

            self.url,

            params=parametros,

            timeout=15

        )


        respuesta.raise_for_status()


        datos = respuesta.json()


        respuesta_api = datos.get(
            "response",
            {}
        )


        ofertas_api = respuesta_api.get(
            "data",
            []
        )


        ofertas = []


        for item in ofertas_api:

            oferta = self._convertir_oferta(
                item
            )


            if oferta:

                ofertas.append(
                    oferta
                )


        return ofertas


    # ======================================
    # CONVERTIR OFERTA
    # ======================================

    def _convertir_oferta(self, item):

        codigo = str(
            item.get(
                "vectorEventoCodigo",
                ""
            )
        ).strip()


        cargo = (
            item.get(
                "cargoNombre",
                ""
            )
            or
            item.get(
                "vectorEventoNombre",
                ""
            )
        )


        cargo = self._limpiar_cargo(
            cargo
        )


        empresa = item.get(
            "empresaNombre",
            ""
        )


        fecha = item.get(
            "vectorEventoFechaInicio",
            ""
        )


        texto = item.get(
            "seleccionSolicitudTexto",
            ""
        )


        ciudad = self._extraer_ciudad(
            texto
        )


        link = self._crear_enlace(
            codigo
        )


        if not cargo or not codigo:

            return None


        return {

            "portal":
                self.nombre,

            "cargo":
                cargo,

            "empresa":
                empresa,

            "ciudad":
                ciudad,

            "fecha":
                fecha,

            "link":
                link,

            "numero_oferta":
                codigo,

            "detalle":
                texto
        }


    # ======================================
    # LIMPIAR CARGO
    # ======================================

    def _limpiar_cargo(self, cargo):

        if not cargo:

            return ""


        cargo = str(cargo).strip()


        # El vectorEventoNombre puede contener
        # códigos internos y números al final.
        #
        # Ejemplo:
        # (1000027) ANALISTA GESTION FINANCIERA
        # JUNIOR - 247

        cargo = re.sub(
            r"^\(\d+\)\s*",
            "",
            cargo
        )


        cargo = re.sub(
            r"\s*-\s*\d+\s*$",
            "",
            cargo
        )


        return cargo.strip()


    # ======================================
    # EXTRAER CIUDAD
    # ======================================

    def _extraer_ciudad(self, texto):

        if not texto:

            return ""


        texto = html.unescape(
            str(texto)
        )


        texto = re.sub(
            r"<[^>]+>",
            " ",
            texto
        )


        texto = re.sub(
            r"\s+",
            " ",
            texto
        ).strip()


        patrones = [

            r"para la ciudad de\s+([A-Za-zÁÉÍÓÚáéíóúÑñ ]+?)(?:,|\s+el mismo|\s+la misma|\.)",

            r"para la ciudad de\s+([A-Za-zÁÉÍÓÚáéíóúÑñ ]+)",

            r"ciudad de\s+([A-Za-zÁÉÍÓÚáéíóúÑñ ]+?)(?:,|\s+el mismo|\s+\.)"
        ]


        for patron in patrones:

            resultado = re.search(
                patron,
                texto,
                re.IGNORECASE
            )


            if resultado:

                ciudad = resultado.group(
                    1
                ).strip()


                return ciudad.title()


        return ""


    # ======================================
    # CREAR ENLACE
    # ======================================

    def _crear_enlace(self, codigo):

        if not codigo:

            return ""


        return (
            "https://dce.twiinshrm.com/"
            "views/02_candidatos/"
            "frm_registrocandidatototal.php"
            f"?codigoEvento={codigo}"
            "&mostForm=S"
        )


    # ======================================
    # JSON
    # ======================================

    def _convertir_json(self, datos):

        import json

        return json.dumps(
            datos,
            separators=(
                ",",
                ":"
            )
        )