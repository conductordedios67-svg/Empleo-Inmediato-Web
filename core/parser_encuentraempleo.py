# ==========================================
# PARSER ENCUENTRA EMPLEO
# EMPLEO INMEDIATO
# ==========================================

import re
import requests
import warnings

from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning


# ==========================================
# OCULTAR AVISO DEL PARSER
# ==========================================

warnings.filterwarnings(
    "ignore",
    category=XMLParsedAsHTMLWarning
)


# ==========================================
# CONFIGURACIÓN
# ==========================================

BASE_URL = (
    "https://encuentraempleo.trabajo.gob.ec"
)

URL_BUSQUEDA = (
    BASE_URL
    + "/socioEmpleo-war/paginas/procesos/"
    + "busquedaOfertaProvincia.jsf"
)


# ==========================================
# CLASE PRINCIPAL
# ==========================================

class ParserEncuentraEmpleo:

    def __init__(self):

        self.session = requests.Session()

        self.cabeceras = {

            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )

        }

    # ======================================
    # LIMPIAR TEXTO
    # ======================================

    def limpiar_texto(self, texto):

        if not texto:

            return ""

        texto = texto.replace(
            "\xa0",
            " "
        )

        texto = re.sub(
            r"\s+",
            " ",
            texto
        )

        return texto.strip()

    # ======================================
    # OBTENER CATEGORÍA
    # ======================================

    def obtener_categoria(self, palabra):

        palabra = self.limpiar_texto(
            palabra
        ).lower()

        categorias = {

            # ------------------------------
            # JURÍDICO
            # ------------------------------

            "abogado":
                "juridico",

            "abogada":
                "juridico",

            "procurador":
                "juridico",

            "procuradora":
                "juridico",

            # ------------------------------
            # CONTABILIDAD
            # ------------------------------

            "contador":
                "contabilidad",

            "contadora":
                "contabilidad",

            "auditor":
                "contabilidad",

            "auditora":
                "contabilidad",

            # ------------------------------
            # SALUD
            # ------------------------------

            "enfermero":
                "salud",

            "enfermera":
                "salud",

            "medico":
                "salud",

            "médico":
                "salud",

            "medica":
                "salud",

            "médica":
                "salud",

            "odontologo":
                "salud",

            "odontólogo":
                "salud",

            "odontologa":
                "salud",

            "odontóloga":
                "salud",

            "psicologo":
                "salud",

            "psicólogo":
                "salud",

            "psicologa":
                "salud",

            "psicóloga":
                "salud",

            "fisioterapeuta":
                "salud",

            "farmaceutico":
                "salud",

            "farmacéutico":
                "salud",

            "farmaceutica":
                "salud",

            "farmacéutica":
                "salud"
        }

        return categorias.get(
            palabra,
            None
        )

    # ======================================
    # DESCARGAR PÁGINA
    # ======================================

    def descargar(self, categoria):

        parametros = {

            "categoria":
                categoria

        }

        respuesta = self.session.get(

            URL_BUSQUEDA,

            params=parametros,

            headers=self.cabeceras,

            timeout=20

        )

        respuesta.raise_for_status()

        return respuesta.text

    # ======================================
    # OBTENER TOTAL DE PÁGINAS
    # ======================================

    def obtener_total_paginas(self, soup):

        texto = self.limpiar_texto(

            soup.get_text(
                " ",
                strip=True
            )

        )

        coincidencia = re.search(

            r"Total\s+páginas\s*:\s*(\d+)",

            texto,

            re.IGNORECASE

        )

        if coincidencia:

            return int(
                coincidencia.group(1)
            )

        return 1

    # ======================================
    # EXTRAER OFERTA
    # ======================================

    def extraer_oferta(self, fieldset):

        # ----------------------------------
        # EMPRESA
        # ----------------------------------

        empresa = ""

        legend = fieldset.find(
            "legend"
        )

        if legend:

            empresa = self.limpiar_texto(

                legend.get_text(
                    " ",
                    strip=True
                )

            )

        # ----------------------------------
        # CARGO
        # ----------------------------------

        cargo = ""

        subtitulo = fieldset.find(

            "span",

            class_="subTitle"

        )

        if subtitulo:

            cargo = self.limpiar_texto(

                subtitulo.get_text(
                    " ",
                    strip=True
                )

            )

        # ----------------------------------
        # NÚMERO DE OFERTA
        # ----------------------------------

        numero_oferta = ""

        for span in fieldset.find_all(
            "span"
        ):

            texto = self.limpiar_texto(

                span.get_text(
                    " ",
                    strip=True
                )

            )

            coincidencia = re.search(

                r"OFERTA-\d+-\d+",

                texto,

                re.IGNORECASE

            )

            if coincidencia:

                numero_oferta = (
                    coincidencia.group(0)
                )

                break

        # ----------------------------------
        # REMUNERACIÓN
        # ----------------------------------

        remuneracion = ""

        for td in fieldset.find_all(
            "td"
        ):

            texto = self.limpiar_texto(

                td.get_text(
                    " ",
                    strip=True
                )

            )

            if texto.lower().startswith(
                "remuneración:"
            ):

                coincidencia = re.search(

                    r"Remuneración\s*:\s*"
                    r"(\$[\d.,]+\s*-\s*\$[\d.,]+)",

                    texto,

                    re.IGNORECASE

                )

                if coincidencia:

                    remuneracion = (
                        coincidencia.group(1)
                    )

                break

        # ----------------------------------
        # CIUDAD Y FECHA
        # ----------------------------------

        ciudad = ""
        fecha = ""

        for td in fieldset.find_all(
            "td"
        ):

            texto = self.limpiar_texto(

                td.get_text(
                    " ",
                    strip=True
                )

            )

            if not re.search(
                r"\bHACE\s*:",
                texto,
                re.IGNORECASE
            ):

                continue

            # ------------------------------
            # FECHA
            # ------------------------------

            partes_hace = re.split(

                r"\s+HACE\s*:\s*",

                texto,

                maxsplit=1,

                flags=re.IGNORECASE

            )

            if len(partes_hace) != 2:

                continue

            antes_hace = self.limpiar_texto(
                partes_hace[0]
            )

            fecha = (
                "HACE: "
                + self.limpiar_texto(
                    partes_hace[1]
                )
            )

            # ------------------------------
            # CIUDAD
            # ------------------------------

            if remuneracion:

                posicion = antes_hace.lower().find(
                    remuneracion.lower()
                )

                if posicion >= 0:

                    ciudad = self.limpiar_texto(

                        antes_hace[
                            posicion
                            + len(remuneracion):
                        ]

                    )

            break

        # ----------------------------------
        # ACTIVIDADES
        # ----------------------------------

        actividades = ""

        texto_completo = self.limpiar_texto(

            fieldset.get_text(
                " ",
                strip=True
            )

        )

        marcador = re.search(

            r"Actividades\s+a\s+Desempeñar\s*:",

            texto_completo,

            re.IGNORECASE

        )

        if marcador:

            actividades = self.limpiar_texto(

                texto_completo[
                    marcador.end():
                ]

            )

        # ----------------------------------
        # VALIDAR CARGO
        # ----------------------------------

        if not cargo:

            return None

        # ----------------------------------
        # RESULTADO
        # ----------------------------------

        return {

            "portal":
                "Encuentra Empleo",

            "cargo":
                cargo,

            "empresa":
                empresa,

            "ciudad":
                ciudad,

            "fecha":
                fecha,

            "numero_oferta":
                numero_oferta,

            "remuneracion":
                remuneracion,

            "actividades":
                actividades,

            "link":
                URL_BUSQUEDA

        }

    # ======================================
    # EXTRAER OFERTAS
    # ======================================

    def extraer_ofertas(self, html):

        soup = BeautifulSoup(

            html,

            "lxml"

        )

        fieldsets = soup.find_all(

            "fieldset",

            class_=re.compile(
                r"fieldsetOferta"
            )

        )

        ofertas = []

        for fieldset in fieldsets:

            oferta = self.extraer_oferta(
                fieldset
            )

            if oferta:

                ofertas.append(
                    oferta
                )

        return ofertas

    # ======================================
    # BUSCAR
    # ======================================

    def buscar(self, palabra):

        if not palabra:

            return []

        palabra = self.limpiar_texto(
            palabra
        )

        if not palabra:

            return []

        print()
        print(
            "=" * 60
        )

        print(
            "ENCUENTRA EMPLEO"
        )

        print(
            f"Búsqueda: {palabra}"
        )

        print(
            "=" * 60
        )

        # ----------------------------------
        # CATEGORÍA
        # ----------------------------------

        categoria = self.obtener_categoria(
            palabra
        )

        print(

            f"Categoría utilizada: "
            f"{categoria}"
        )

        if not categoria:

           print(
               "Categoría no disponible para esta búsqueda."
           )

           return []
        

        # ----------------------------------
        # DESCARGAR
        # ----------------------------------

        try:

            html = self.descargar(
                categoria
            )

        except Exception as error:

            print(
                "✖ Error descargando "
                f"Encuentra Empleo: {error}"
            )

            return []

        # ----------------------------------
        # ANALIZAR
        # ----------------------------------

        soup = BeautifulSoup(

            html,

            "lxml"

        )

        total_paginas = (
            self.obtener_total_paginas(
                soup
            )
        )

        print(
            f"Total páginas detectadas: "
            f"{total_paginas}"
        )

        # ----------------------------------
        # PRIMERA PÁGINA
        # ----------------------------------

        ofertas = self.extraer_ofertas(
            html
        )

        print(
            f"Ofertas extraídas página 1: "
            f"{len(ofertas)}"
        )

        # ----------------------------------
        # ACEPTAR RESULTADOS
        # ----------------------------------
        #
        # La categoría del portal ya determina
        # el grupo profesional.
        #
        # Por ejemplo:
        #
        # abogado -> juridico
        #
        # Por eso NO hacemos una búsqueda
        # literal de "abogado" dentro del cargo.
        #
        # ----------------------------------

        print(
            f"Ofertas aceptadas: "
            f"{len(ofertas)}"
        )

        print(
            "=" * 60
        )

        return ofertas


# ==========================================
# PRUEBA DIRECTA
# ==========================================

if __name__ == "__main__":

    parser = ParserEncuentraEmpleo()

    ofertas = parser.buscar(
        "abogado"
    )

    print()
    print(
        "=" * 60
    )

    print(
        "RESULTADO DE PRUEBA"
    )

    print(
        "=" * 60
    )

    print(
        "TOTAL:",
        len(ofertas)
    )

    for numero, oferta in enumerate(
        ofertas,
        start=1
    ):

        print()
        print(
            f"OFERTA {numero}"
        )

        print(
            "Portal:",
            oferta.get(
                "portal",
                ""
            )
        )

        print(
            "Cargo:",
            oferta.get(
                "cargo",
                ""
            )
        )

        print(
            "Empresa:",
            oferta.get(
                "empresa",
                ""
            )
        )

        print(
            "Ciudad:",
            oferta.get(
                "ciudad",
                ""
            )
        )

        print(
            "Fecha:",
            oferta.get(
                "fecha",
                ""
            )
        )

        print(
            "Número:",
            oferta.get(
                "numero_oferta",
                ""
            )
        )

        print(
            "Remuneración:",
            oferta.get(
                "remuneracion",
                ""
            )
        )

    print()
    print(
        "=" * 60
    )

    print(
        "PRUEBA TERMINADA"
    )

    print(
        "=" * 60
    )