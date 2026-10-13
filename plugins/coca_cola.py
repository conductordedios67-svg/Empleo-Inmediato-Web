import html
import re
import requests

from core.motor import Motor
from filtros import filtrar_ofertas
from database import guardar_empleo


class CocaCola(Motor):

    def __init__(self):
        super().__init__()

        self.nombre = "Coca-Cola"

        self.url = (
            "https://jobsapi-internal.m-cloud.io/"
            "api/job"
        )

        self.organization = "2110"

        self.filtros = [
            "ats_portalid:CocaCola-Workday-External",
            "is_internal:coca-cola-careers"
        ]

        self.limite = 300

    def buscar(self, palabras=None):

        print(f"Buscando en {self.nombre}...")

        if not palabras:
            print("⚠ No se recibió ninguna palabra de búsqueda.")
            return []

        if isinstance(palabras, str):
            palabras = [palabras]

        try:
            ofertas = self._obtener_ofertas()

        except Exception as error:
            print("✖ Error consultando Coca-Cola:")
            print(error)
            return []

        print(f"Se encontraron {len(ofertas)} ofertas activas.")

        nuevas_ofertas = []

        for palabra in palabras:

            palabra = palabra.strip()

            if not palabra:
                continue

            print()
            print(f"🔍 Buscando: {palabra}")

            ofertas_filtradas = filtrar_ofertas(
                ofertas,
                palabra
            )

            print(
                f'Coinciden con "{palabra}": '
                f'{len(ofertas_filtradas)}'
            )

            for oferta in ofertas_filtradas:

                try:

                    guardada = guardar_empleo(oferta)

                    if guardada:

                        nuevas_ofertas.append(oferta)

                        print()
                        print("🆕 NUEVA OFERTA COCA-COLA")
                        print(
                            "Cargo   :",
                            oferta.get("cargo", "")
                        )
                        print(
                            "Empresa :",
                            oferta.get("empresa", "")
                        )
                        print(
                            "Ciudad  :",
                            oferta.get("ciudad", "")
                        )
                        print(
                            "País    :",
                            oferta.get("pais", "")
                        )
                        print(
                            "Fecha   :",
                            oferta.get("fecha", "")
                        )
                        print(
                            "Código  :",
                            oferta.get("numero_oferta", "")
                        )
                        print(
                            "Enlace  :",
                            oferta.get("link", "")
                        )

                    else:

                        print(
                            "• Ya existe:",
                            oferta.get("cargo", "")
                        )

                except Exception as error:

                    print(
                        "✖ Error guardando oferta Coca-Cola:",
                        error
                    )

        print()
        print("=" * 60)
        print("COCA-COLA")
        print(
            f"Nuevas ofertas: "
            f"{len(nuevas_ofertas)}"
        )
        print("=" * 60)

        return nuevas_ofertas

    def _obtener_ofertas(self):

        parametros = [
            ("Organization", self.organization)
        ]

        for filtro in self.filtros:
            parametros.append(
                ("facet", filtro)
            )

        parametros.extend([
            ("offset", "1"),
            ("limit", str(self.limite))
        ])

        respuesta = requests.get(
            self.url,
            params=parametros,
            timeout=30
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        ofertas_api = datos.get(
            "queryResult",
            []
        )

        ofertas = []

        for item in ofertas_api:

            oferta = self._convertir_oferta(item)

            if oferta:
                ofertas.append(oferta)

        return ofertas

    def _convertir_oferta(self, item):

        codigo = str(
            item.get("id", "")
        ).strip()

        cargo = item.get(
            "title",
            ""
        )

        empresa = item.get(
            "company_name",
            ""
        )

        ciudad = item.get(
            "primary_city",
            ""
        )

        estado = item.get(
            "primary_state",
            ""
        )

        pais = item.get(
            "primary_country",
            ""
        )

        fecha = item.get(
            "open_date",
            ""
        )

        descripcion = item.get(
            "description",
            ""
        )

        enlace = item.get(
            "url",
            ""
        )

        if not cargo or not codigo:
            return None

        ciudad_completa = self._crear_ciudad(
            ciudad,
            estado,
            pais
        )

        descripcion_limpia = (
            self._limpiar_html(descripcion)
        )

        return {
            "portal": self.nombre,
            "cargo": cargo.strip(),
            "empresa": empresa.strip(),
            "ciudad": ciudad_completa,
            "pais": pais.strip(),
            "fecha": fecha,
            "link": enlace,
            "numero_oferta": codigo,
            "detalle": descripcion_limpia
        }

    def _crear_ciudad(
        self,
        ciudad,
        estado,
        pais
    ):

        partes = []

        if ciudad:
            partes.append(
                str(ciudad).strip()
            )

        if estado:
            partes.append(
                str(estado).strip()
            )

        if pais:
            partes.append(
                str(pais).strip()
            )

        return ", ".join(partes)

    def _limpiar_html(self, texto):

        if not texto:
            return ""

        texto = html.unescape(
            str(texto)
        )

        texto = re.sub(
            r"<br\s*/?>",
            "\n",
            texto,
            flags=re.IGNORECASE
        )

        texto = re.sub(
            r"</p\s*>",
            "\n",
            texto,
            flags=re.IGNORECASE
        )

        texto = re.sub(
            r"</li\s*>",
            "\n",
            texto,
            flags=re.IGNORECASE
        )

        texto = re.sub(
            r"<[^>]+>",
            " ",
            texto
        )

        texto = re.sub(
            r"[ \t]+",
            " ",
            texto
        )

        texto = re.sub(
            r"\n\s*\n+",
            "\n",
            texto
        )

        return texto.strip()


if __name__ == "__main__":

    coca_cola = CocaCola()

    ofertas = coca_cola._obtener_ofertas()

    print()
    print("COCA-COLA OK")
    print(
        "TOTAL:",
        len(ofertas)
    )

    if ofertas:

        primera = ofertas[0]

        print(
            "PRIMERA OFERTA:"
        )

        print(
            "Cargo   :",
            primera.get("cargo", "")
        )

        print(
            "Empresa :",
            primera.get("empresa", "")
        )

        print(
            "Ciudad  :",
            primera.get("ciudad", "")
        )

        print(
            "País    :",
            primera.get("pais", "")
        )

        print(
            "Fecha   :",
            primera.get("fecha", "")
        )

        print(
            "Código  :",
            primera.get("numero_oferta", "")
        )

        print(
            "Enlace  :",
            primera.get("link", "")
        )