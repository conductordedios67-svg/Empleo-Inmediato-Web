# ==========================================
# PERFILES DE BUSQUEDA
# EMPLEO INMEDIATO
# ==========================================


PERFILES = {

    # ======================================
    # JURIDICO
    # ======================================

    "Jurídico": [
        "abogado",
        "asesor jurídico",
        "abogado corporativo",
        "abogado junior",
        "abogado senior",
        "analista legal",
        "procurador",
        "coordinador legal",
        "especialista legal",
        "consultor legal",
        "compliance",
        "oficial de cumplimiento",
        "contratación pública",
        "sercop",
        "compras públicas",
        "recuperación de cartera"
    ],


    # ======================================
    # SALUD
    # ======================================

    "Salud": [
        "enfermera",
        "médico",
        "odontólogo",
        "psicólogo",
        "fisioterapeuta",
        "farmacéutico"
    ],


    # ======================================
    # ADMINISTRATIVO
    # ======================================

    "Administrativo": [
        "asistente administrativo",
        "auxiliar administrativo",
        "analista administrativo",
        "secretaria",
        "recepcionista",
        "administrador"
    ],


    # ======================================
    # CONTABILIDAD
    # ======================================

    "Contabilidad": [
        "contador",
        "auxiliar contable",
        "analista contable",
        "auditor",
        "tesorero"
    ],


    # ======================================
    # DISEÑO GRAFICO
    # ======================================

    "Diseño Gráfico": [
    "Diseñador Gráfico",
    "Diseñador Gráfico Junior",
    "Asistente de Diseño Gráfico",
    "Diseño Gráfico y Marketing"
    ],
    

    # ======================================
    # TECNOLOGIA / COMPUTACION
    # ======================================

    "Tecnología / Computación": [
        "Tecnólogo en Computación",
        "Tecnóloga en Computación",
        "Tecnólogo en Sistemas",
        "Tecnóloga en Sistemas",
        "Tecnólogo en Informática",
        "Tecnóloga en Informática",
        "Tecnología en Computación",
        "Tecnología en Sistemas",
        "Tecnología en Informática"
    ]

}


# ==========================================
# OBTENER PERFILES
# ==========================================

def obtener_perfiles():

    return list(PERFILES.keys())


# ==========================================
# OBTENER NOMBRE REAL DEL PERFIL
# ==========================================

def obtener_nombre_perfil(perfil):

    if not perfil:
        return None

    perfil_buscado = str(perfil).strip().casefold()

    for nombre in PERFILES:

        if nombre.casefold() == perfil_buscado:

            return nombre

    return None


# ==========================================
# OBTENER PALABRAS DEL PERFIL
# ==========================================

def obtener_palabras(perfil):

    nombre_real = obtener_nombre_perfil(perfil)

    if nombre_real is None:

        return []

    return PERFILES[nombre_real]


# ==========================================
# COMPROBAR SI EXISTE EL PERFIL
# ==========================================

def existe_perfil(perfil):

    return obtener_nombre_perfil(perfil) is not None


# ==========================================
# MOSTRAR PERFIL
# ==========================================

def mostrar_perfil(perfil):

    nombre_real = obtener_nombre_perfil(perfil)

    if nombre_real is None:

        print(f"⚠ Perfil no encontrado: {perfil}")

        return

    palabras = obtener_palabras(nombre_real)

    print()
    print(f"Perfil: {nombre_real}")
    print("Palabras de búsqueda:")

    for palabra in palabras:

        print(f"  • {palabra}")