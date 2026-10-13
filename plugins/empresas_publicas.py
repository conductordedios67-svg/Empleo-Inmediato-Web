# ==========================================
# PLUGIN EMPRESAS PÚBLICAS
# EMPLEO INMEDIATO
# ==========================================

from core.motor import Motor
from core.parser_encuentraempleo import (
    ParserEncuentraEmpleo
)
from database import guardar_empleo


class EmpresasPublicas(Motor):

    def __init__(self):

        super().__init__()

        self.nombre = "Empresas Públicas"

        self.fuentes = [
            "Encuentra Empleo"
        ]

        self.parser_encuentra = (
            ParserEncuentraEmpleo()
        )

    # ==========================================
    # BUSCAR OFERTAS
    # ==========================================

    def buscar(self, palabras=None):

        print(
            f"Buscando en {self.nombre}..."
        )

        if not palabras:

            print(
                "⚠ No se recibió ninguna palabra "
                "de búsqueda."
            )

            return {
                "encontradas": [],
                "nuevas": []
            }

        if isinstance(palabras, str):

            palabras = [palabras]

        ofertas_encontradas = []
        nuevas_ofertas = []

        # ======================================
        # RECORRER PALABRAS
        # ======================================

        for palabra in palabras:

            palabra = str(
                palabra
            ).strip()

            if not palabra:

                continue

            print()
            print(
                f"🔍 Encuentra Empleo: "
                f"{palabra.upper()}"
            )

            # ==================================
            # BUSCAR EN EL PORTAL
            # ==================================

            try:

                ofertas = (
                    self.parser_encuentra.buscar(
                        palabra
                    )
                )

            except Exception as error:

                print(
                    "✖ Error buscando en "
                    f"Encuentra Empleo: {error}"
                )

                continue

            if not ofertas:

                print(
                    f"✔ {palabra}: "
                    "0 ofertas encontradas"
                )

                continue

            print(
                f"Ofertas recibidas: "
                f"{len(ofertas)}"
            )

            # ==================================
            # LAS OFERTAS YA VIENEN FILTRADAS
            # POR LA CATEGORÍA DEL PORTAL
            # ==================================

            for oferta in ofertas:

                if not isinstance(
                    oferta,
                    dict
                ):

                    continue

                cargo = oferta.get(
                    "cargo",
                    ""
                )

                if not cargo:

                    continue

                ofertas_encontradas.append(
                    oferta
                )

                # ==============================
                # GUARDAR EN BASE DE DATOS
                # ==============================

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
                            "🎉 NUEVA OFERTA"
                        )

                        print(
                            "Portal   :",
                            oferta.get(
                                "portal",
                                ""
                            )
                        )

                        print(
                            "Cargo    :",
                            oferta.get(
                                "cargo",
                                ""
                            )
                        )

                        print(
                            "Empresa  :",
                            oferta.get(
                                "empresa",
                                ""
                            )
                        )

                        print(
                            "Ciudad   :",
                            oferta.get(
                                "ciudad",
                                ""
                            )
                        )

                        print(
                            "Oferta   :",
                            oferta.get(
                                "numero_oferta",
                                ""
                            )
                        )

                        print(
                            "Enlace   :",
                            oferta.get(
                                "link",
                                ""
                            )
                        )

                    else:

                        print(
                            "• Ya existe:",
                            cargo
                        )

                except Exception as error:

                    print(
                        "✖ Error guardando oferta: "
                        f"{error}"
                    )

        # ======================================
        # RESUMEN
        # ======================================

        print()
        print(
            "=" * 60
        )

        print(
            f"{self.nombre}"
        )

        print(
            f"Ofertas encontradas: "
            f"{len(ofertas_encontradas)}"
        )

        print(
            f"Nuevas ofertas: "
            f"{len(nuevas_ofertas)}"
        )

        print(
            "=" * 60
        )

        # ======================================
        # RESULTADO MODERNO
        # ======================================

        return {

            "encontradas":
                ofertas_encontradas,

            "nuevas":
                nuevas_ofertas

        }


# ==========================================
# PRUEBA DIRECTA
# ==========================================

def probar_plugin():

    plugin = EmpresasPublicas()

    print()
    print(
        "=" * 60
    )

    print(
        "PRUEBA PLUGIN EMPRESAS PÚBLICAS"
    )

    print(
        "=" * 60
    )

    resultado = plugin.buscar(
        "abogado"
    )

    ofertas = resultado.get(
        "encontradas",
        []
    )

    nuevas = resultado.get(
        "nuevas",
        []
    )

    print()
    print(
        "=" * 60
    )

    print(
        "RESULTADO FINAL"
    )

    print(
        "=" * 60
    )

    print(
        "Ofertas encontradas:",
        len(ofertas)
    )

    print(
        "Ofertas nuevas:",
        len(nuevas)
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


# ==========================================
# EJECUCIÓN DIRECTA
# ==========================================

if __name__ == "__main__":

    probar_plugin()