# ==========================================
# FILTROS DE BÚSQUEDA
# EMPLEO INMEDIATO
# ==========================================

from core.equivalencias import obtener_equivalencias

import re
import unicodedata


# ==========================================
# PALABRAS QUE INDICAN QUE EL TÉRMINO
# ENCONTRADO NO ES EL CARGO PRINCIPAL
# ==========================================

PALABRAS_ANTERIORES_EXCLUIDAS = {

    "visitador",
    "visitadora",

    "director",
    "directora",

    "jefe",
    "jefa",

    "gerente",
    "gerenta",

    "coordinador",
    "coordinadora",

    "docente",

    "profesor",
    "profesora",

    "asesor",
    "asesora",

    "vendedor",
    "vendedora",

    "ejecutivo",
    "ejecutiva",

    "sector",
    "industria",

    "experiencia",

    "experto",
    "experta",

    "conocimiento",
    "conocimientos"
}


# ==========================================
# NORMALIZAR TEXTO
# ==========================================

def normalizar_texto(texto):

    if not texto:
        return ""

    texto = str(texto).strip().lower()

    texto = unicodedata.normalize(
        "NFD",
        texto
    )

    texto = "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )

    texto = re.sub(
        r"\b([a-z0-9]+)/(?:a|o|as|os)\b",
        r"\1",
        texto
    )

    texto = texto.replace(
        "/",
        " "
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()


# ==========================================
# OBTENER PALABRAS
# ==========================================

def obtener_palabras(texto):

    texto = normalizar_texto(
        texto
    )

    if not texto:
        return []

    return texto.split()


# ==========================================
# LIMPIAR PALABRA
# ==========================================

def limpiar_palabra(palabra):

    palabra = normalizar_texto(
        palabra
    )

    palabra = re.sub(
        r"[^a-z0-9]+",
        "",
        palabra
    )

    return palabra


# ==========================================
# COMPROBAR REFERENCIA SECUNDARIA
# ==========================================

def es_referencia_secundaria(
    palabras_cargo,
    posicion
):

    if posicion <= 0:
        return False

    inicio = max(
        0,
        posicion - 3
    )

    anteriores = palabras_cargo[
        inicio:posicion
    ]

    for palabra in anteriores:

        palabra = limpiar_palabra(
            palabra
        )

        if palabra in PALABRAS_ANTERIORES_EXCLUIDAS:

            return True

    return False


# ==========================================
# COMPROBAR UNA EQUIVALENCIA
# ==========================================

def coincide_equivalencia(
    cargo,
    equivalencia
):

    cargo_normalizado = normalizar_texto(
        cargo
    )

    equivalencia_normalizada = normalizar_texto(
        equivalencia
    )

    if not cargo_normalizado:
        return False

    if not equivalencia_normalizada:
        return False

    terminos = equivalencia_normalizada.split()

    # ======================================
    # EQUIVALENCIA DE VARIAS PALABRAS
    # ======================================

    if len(terminos) > 1:

        palabras_cargo = (
            cargo_normalizado.split()
        )

        cantidad = len(terminos)

        for posicion in range(
            len(palabras_cargo) - cantidad + 1
        ):

            bloque = palabras_cargo[
                posicion:
                posicion + cantidad
            ]

            bloque_limpio = [
                limpiar_palabra(
                    palabra
                )
                for palabra in bloque
            ]

            if bloque_limpio != terminos:

                continue

            if es_referencia_secundaria(
                palabras_cargo,
                posicion
            ):

                continue

            return True

        return False

    # ======================================
    # EQUIVALENCIA DE UNA SOLA PALABRA
    # ======================================

    palabra_buscada = limpiar_palabra(
        equivalencia_normalizada
    )

    palabras_cargo = (
        cargo_normalizado.split()
    )

    for posicion, palabra_cargo in enumerate(
        palabras_cargo
    ):

        palabra_limpia = limpiar_palabra(
            palabra_cargo
        )

        if palabra_limpia != palabra_buscada:

            continue

        if es_referencia_secundaria(
            palabras_cargo,
            posicion
        ):

            continue

        return True

    return False


# ==========================================
# COINCIDENCIA DE UNA PALABRA
# ==========================================

def coincide_palabra(
    cargo,
    palabra
):

    equivalencias = obtener_equivalencias(
        palabra
    )

    for equivalencia in equivalencias:

        if coincide_equivalencia(
            cargo,
            equivalencia
        ):

            return True

    return False


# ==========================================
# COINCIDENCIA DE BÚSQUEDA
# ==========================================

def coincide_busqueda(
    cargo,
    palabra
):

    cargo = normalizar_texto(
        cargo
    )

    palabra = normalizar_texto(
        palabra
    )

    if not cargo or not palabra:

        return False

    terminos = palabra.split()

    # ======================================
    # BÚSQUEDA DE VARIAS PALABRAS
    # ======================================

    if len(terminos) > 1:

        equivalencias = obtener_equivalencias(
            palabra
        )

        for equivalencia in equivalencias:

            if coincide_equivalencia(
                cargo,
                equivalencia
            ):

                return True

        return False

    # ======================================
    # BÚSQUEDA DE UNA SOLA PALABRA
    # ======================================

    return coincide_palabra(
        cargo,
        palabra
    )


# ==========================================
# FILTRAR OFERTAS
# ==========================================

def filtrar_ofertas(
    ofertas,
    palabra
):

    resultado = []

    for oferta in ofertas:

        cargo = oferta.get(
            "cargo",
            ""
        )

        if coincide_busqueda(
            cargo,
            palabra
        ):

            resultado.append(
                oferta
            )

    return resultado
