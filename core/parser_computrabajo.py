# ==========================================
# PARSER COMPUTRABAJO
# EMPLEO INMEDIATO
# ==========================================

from bs4 import BeautifulSoup


BASE_URL = "https://ec.computrabajo.com"


def limpiar_cargo(cargo):

    if not cargo:
        return ""

    cargo = cargo.strip()

    # Computrabajo puede incluir estos textos
    # de interfaz junto al título real.
    cargo = cargo.replace(
        "Postulado Vista",
        ""
    )

    cargo = cargo.strip()

    return cargo


def extraer_empresa(parrafos):

    if not parrafos:
        return ""

    # En la estructura actual de Computrabajo,
    # la empresa aparece normalmente en el
    # primer párrafo.

    primer_parrafo = parrafos[0]

    enlace = primer_parrafo.find("a")

    if enlace:

        empresa = enlace.get_text(
            " ",
            strip=True
        )

        if empresa:
            return empresa

    # Respaldo: utilizar directamente el
    # texto del primer párrafo.

    empresa = primer_parrafo.get_text(
        " ",
        strip=True
    )

    return empresa


def extraer_ciudad(parrafos):

    if len(parrafos) < 2:
        return ""

    return parrafos[1].get_text(
        " ",
        strip=True
    )


def extraer_fecha(parrafos):

    if len(parrafos) < 3:
        return ""

    return parrafos[2].get_text(
        " ",
        strip=True
    )


def extraer_enlace(h2):

    if not h2:
        return ""

    enlace = h2.find("a")

    if not enlace:
        return ""

    href = enlace.get("href")

    if not href:
        return ""

    if href.startswith("http"):

        return href

    return BASE_URL + href


def extraer_ofertas(html):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    articulos = soup.find_all(
        "article"
    )

    ofertas = []

    for articulo in articulos:

        # ======================================
        # CARGO
        # ======================================

        cargo = ""

        h2 = articulo.find("h2")

        if h2:

            enlace = h2.find("a")

            if enlace:

                cargo = enlace.get_text(
                    " ",
                    strip=True
                )

        cargo = limpiar_cargo(
            cargo
        )


        # ======================================
        # ENLACE
        # ======================================

        link = extraer_enlace(
            h2
        )


        # ======================================
        # PÁRRAFOS
        # ======================================

        parrafos = articulo.find_all(
            "p"
        )


        # ======================================
        # EMPRESA
        # ======================================

        empresa = extraer_empresa(
            parrafos
        )


        # ======================================
        # CIUDAD
        # ======================================

        ciudad = extraer_ciudad(
            parrafos
        )


        # ======================================
        # FECHA
        # ======================================

        fecha = extraer_fecha(
            parrafos
        )


        # ======================================
        # OFERTA
        # ======================================

        oferta = {
            "cargo": cargo,
            "empresa": empresa,
            "ciudad": ciudad,
            "fecha": fecha,
            "link": link
        }

        ofertas.append(
            oferta
        )


    return ofertas
