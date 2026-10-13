# ==========================================
# EQUIVALENCIAS DE BÚSQUEDA
# EMPLEO INMEDIATO
# ==========================================

EQUIVALENCIAS = {

    # ==========================================
    # FARMACÉUTICO
    # ==========================================

    "farmaceutico": [
        "farmaceutico",
        "farmaceutica",
        "quimico farmaceutico",
        "quimica farmaceutica"
    ],

    # ==========================================
    # SALUD
    # ==========================================

    "enfermera": [
        "enfermera",
        "enfermero"
    ],

    "medico": [
        "medico",
        "medica"
    ],

    "odontologo": [
        "odontologo",
        "odontologa"
    ],

    "psicologo": [
        "psicologo",
        "psicologa"
    ],

    "fisioterapeuta": [
        "fisioterapeuta"
    ],

    # ==========================================
    # JURÍDICO
    # ==========================================

    "abogado": [
        "abogado",
        "abogada"
    ],

    "procurador": [
        "procurador",
        "procuradora"
    ],

    # ==========================================
    # CONTABILIDAD
    # ==========================================

    "contador": [
        "contador",
        "contadora"
    ],

    "auditor": [
        "auditor",
        "auditora"
    ],

    "tesorero": [
        "tesorero",
        "tesorera"
    ],

    # ==========================================
    # DISEÑO GRÁFICO JUNIOR
    # ==========================================

    "disenador grafico junior": [
        "disenador grafico junior",
        "disenadora grafica junior",
        "graphic designer jr"
    ],

    # ==========================================
    # BELLEZA INTEGRAL
    # ==========================================

    "belleza integral": [
        "belleza integral"
    ],

    # ==========================================
    # ESTÉTICA
    # ==========================================

    "estetica": [
        "estetica",
        "esteticista",
        "esteticista facial",
        "esteticista corporal",
        "tecnica en estetica",
        "tecnico en estetica",
        "profesional de estetica",
        "especialista en estetica",
        "asistente de estetica",
        "cosmetologa",
        "cosmetologo",
        "belleza integral",
        "especialista en belleza integral",
        "tecnica en belleza integral",
        "tecnico en belleza integral",
        "profesional de belleza integral"
    ],

    # ==========================================
    # TECNOLOGÍA / COMPUTACIÓN
    # ==========================================

    "tecnologo en computacion": [
        "tecnologo en computacion",
        "tecnologa en computacion",
        "tecnologo en sistemas",
        "tecnologa en sistemas",
        "tecnologo en informatica",
        "tecnologa en informatica",
        "tecnologia en computacion",
        "tecnologia en sistemas",
        "tecnologia en informatica",
        "tecnico en computacion",
        "tecnica en computacion",
        "tecnico en sistemas",
        "tecnica en sistemas",
        "tecnico en informatica",
        "tecnica en informatica"
    ]
}


# ==========================================
# NORMALIZAR TEXTO
# ==========================================

def normalizar_texto(texto):

    import unicodedata

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

    return texto


# ==========================================
# OBTENER EQUIVALENCIAS
# ==========================================

def obtener_equivalencias(palabra):

    palabra = normalizar_texto(
        palabra
    )

    return EQUIVALENCIAS.get(
        palabra,
        [palabra]
    )


# ==========================================
# COMPROBAR EXISTENCIA
# ==========================================

def existe_equivalencia(palabra):

    palabra = normalizar_texto(
        palabra
    )

    return palabra in EQUIVALENCIAS


# ==========================================
# MOSTRAR EQUIVALENCIAS
# ==========================================

def mostrar_equivalencias(palabra):

    equivalencias = obtener_equivalencias(
        palabra
    )

    print()
    print(
        f"Búsqueda: {palabra}"
    )

    print(
        "Equivalencias:"
    )

    for termino in equivalencias:

        print(
            f"  • {termino}"
        )