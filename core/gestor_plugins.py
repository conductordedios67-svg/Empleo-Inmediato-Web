import os

CARPETA_PLUGINS = "plugins"


def obtener_plugins():
    plugins = []

    for archivo in os.listdir(CARPETA_PLUGINS):

        if archivo.endswith(".py") and archivo != "__init__.py":

            plugins.append(archivo[:-3])

    return sorted(plugins)
