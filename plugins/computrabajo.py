# ==========================================
# PLUGIN COMPUTRABAJO
# EMPLEO INMEDIATO
# ==========================================

from core.motor import Motor
from core.web import descargar
from core.parser_computrabajo import extraer_ofertas

from filtros import filtrar_ofertas
from database import guardar_empleo


class Computrabajo(Motor):

    def __init__(self):

        super().__init__()

        self.nombre = "Computrabajo"

    def buscar(self, palabras=None):

        print(
            f"Buscando en {self.nombre}..."
        )

        if not palabras:

            print(
                "⚠ No se recibió ninguna "
                "palabra de búsqueda."
            )

            return []

        if isinstance(palabras, str):

            palabras = [palabras]

        todas_las_ofertas = []
        nuevas_ofertas = []

        for palabra in palabras:

            palabra = palabra.strip()

            if not palabra:
                continue

            print(
                f"\nPalabra clave: {palabra}"
            )

            palabra_url = palabra.replace(
                " ",
                "-"
            )

            url = (
                "https://ec.computrabajo.com/"
                f"trabajo-de-{palabra_url}"
            )

            try:

                html = descargar(url)

            except Exception as error:

                print(
                    f"✖ Error descargando "
                    f"Computrabajo: {error}"
                )

                continue

            try:

                ofertas = extraer_ofertas(
                    html
                )

            except Exception as error:

                print(
                    f"✖ Error procesando "
                    f"ofertas: {error}"
                )

                continue

            print(
                f"Se encontraron "
                f"{len(ofertas)} ofertas "
                f"en el portal."
            )

    
            # ==================================
            # FILTRO EXACTO
            # ==================================

            ofertas_filtradas = filtrar_ofertas(
                ofertas,
                palabra
            )

            print(
                f'Coinciden exactamente con '
                f'"{palabra}": '
                f'{len(ofertas_filtradas)}'
            )

            # ==================================
            # PROCESAR SOLO OFERTAS EXACTAS
            # ==================================

            for oferta in ofertas_filtradas:

                todas_las_ofertas.append(
                    oferta
                )

                try:

                    guardada = guardar_empleo(
                        oferta
                    )

                    if guardada:

                        nuevas_ofertas.append(
                            oferta
                        )

                        print(
                            "🆕 NUEVA OFERTA EXACTA"
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

                        print()

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
                        "✖ Error guardando "
                        f"oferta: {error}"
                    )

        print(
            f"\nOfertas exactas encontradas: "
            f"{len(todas_las_ofertas)}"
        )

        print(
            f"Ofertas nuevas exactas: "
            f"{len(nuevas_ofertas)}"
        )
        
        return {
            "encontradas": todas_las_ofertas,
            "nuevas": nuevas_ofertas
        } 
        


