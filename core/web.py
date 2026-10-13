
import requests


def descargar(url):

    cabeceras = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0 Safari/537.36"
        )
    }

    respuesta = requests.get(
        url,
        headers=cabeceras,
        timeout=15
    )

    respuesta.raise_for_status()

    return respuesta.text
