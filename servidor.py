
from flask import Flask, jsonify, request
from database import obtener_empleos
from core.ejecutor import Ejecutor
import threading

app = Flask(
    __name__,
    static_folder="pwa",
    static_url_path=""
)

# Una sola instancia del ejecutor para el servidor PWA.
ejecutor = Ejecutor()

estado = {
    "activa": False,
    "mensaje": "Listo para buscar empleo.",
    "error": ""
}

bloqueo_estado = threading.Lock()


@app.route("/")
def inicio():
    return app.send_static_file("index.html")


@app.route("/api/ofertas")
def api_ofertas():
    try:
        empleos = obtener_empleos()
        ofertas = []

        for empleo in empleos:
            (
                portal,
                empresa,
                cargo,
                ciudad,
                fecha_publicacion,
                fecha_registro,
                enlace
            ) = empleo

            ofertas.append({
                "portal": portal or "",
                "empresa": empresa or "",
                "cargo": cargo or "",
                "ciudad": ciudad or "",
                "fecha": fecha_publicacion or "",
                "fecha_registro": fecha_registro or "",
                "enlace": enlace or ""
            })

        termino = request.args.get(
            "buscar", ""
        ).strip().casefold()

        ciudad_filtro = request.args.get(
            "ciudad", ""
        ).strip().casefold()

        if termino:
            ofertas = [
                oferta for oferta in ofertas
                if termino in (
                    oferta["cargo"] + " " +
                    oferta["empresa"] + " " +
                    oferta["ciudad"]
                ).casefold()
            ]

        if ciudad_filtro:
            ofertas = [
                oferta for oferta in ofertas
                if oferta["ciudad"].casefold()
                == ciudad_filtro
            ]

        return jsonify({
            "total": len(ofertas),
            "ofertas": ofertas
        })

    except Exception:
        app.logger.exception(
            "Error consultando ofertas"
        )
        return jsonify({
            "error": "No se pudieron consultar las ofertas."
        }), 500


def ejecutar_busqueda(palabra):
    try:
        with bloqueo_estado:
            estado["mensaje"] = (
                "Buscando ofertas en los portales..."
            )
            estado["error"] = ""

        # Usa los plugins y el motor ya existentes.
        ejecutor.ejecutar_busquedas(palabra)

        with bloqueo_estado:
            estado["mensaje"] = (
                "Búsqueda finalizada. Actualiza las ofertas."
            )

    except Exception as error:
        app.logger.exception(
            "Error durante la búsqueda real"
        )
        with bloqueo_estado:
            estado["error"] = str(error)
            estado["mensaje"] = "La búsqueda terminó con un error."

    finally:
        with bloqueo_estado:
            estado["activa"] = False


@app.route("/api/buscar", methods=["POST"])
def iniciar_busqueda():
    datos = request.get_json(silent=True) or {}
    palabra = str(datos.get("palabra", "")).strip()

    if not palabra:
        return jsonify({
            "error": "Escribe un cargo o palabra de búsqueda."
        }), 400

    with bloqueo_estado:
        if estado["activa"]:
            return jsonify({
                "error": "Ya hay una búsqueda en curso."
            }), 409

        estado["activa"] = True
        estado["mensaje"] = "Preparando búsqueda real..."
        estado["error"] = ""

    hilo = threading.Thread(
        target=ejecutar_busqueda,
        args=(palabra,),
        name="BusquedaPWA",
        daemon=True
    )
    hilo.start()

    return jsonify({
        "ok": True,
        "mensaje": "Búsqueda iniciada.",
        "activa": True
    }), 202


@app.route("/api/detener", methods=["POST"])
def detener_busqueda():
    with bloqueo_estado:
        activa = estado["activa"]

    if not activa:
        return jsonify({
            "ok": True,
            "mensaje": "No hay una búsqueda activa."
        })

    detenido = ejecutor.detener_busqueda()

    return jsonify({
        "ok": detenido,
        "mensaje": (
            "Se solicitó detener la búsqueda."
            if detenido else
            "La búsqueda todavía se está preparando."
        )
    })


@app.route("/api/estado")
def estado_busqueda():
    with bloqueo_estado:
        return jsonify({
            "activa": estado["activa"],
            "mensaje": estado["mensaje"],
            "error": estado["error"]
        })


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )
