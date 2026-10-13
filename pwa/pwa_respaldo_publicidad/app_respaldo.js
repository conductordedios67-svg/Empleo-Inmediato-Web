
// ==========================================
// EMPLEO INMEDIATO
// BUSCADOR DE OFERTAS DE EMPLEO
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Empleo Inmediato iniciado");

    let ofertasPrueba = [];
    let controladorBusqueda = null;

    const campoBuscar = document.getElementById("buscar");
    const campoCiudad = document.getElementById("ciudad");
    const botonBuscar = document.getElementById("botonBuscar");
    const botonDetener = document.getElementById("botonDetener");
    const listaOfertas = document.getElementById("listaOfertas");
    const estadoOfertas = document.getElementById("estadoOfertas");

    // Comprobar que existen los elementos necesarios.
    if (
        !campoBuscar ||
        !campoCiudad ||
        !botonBuscar ||
        !botonDetener ||
        !listaOfertas ||
        !estadoOfertas
    ) {
        console.error(
            "Error: no se encontraron todos los elementos de la interfaz."
        );
        return;
    }

    // Al iniciar, el botón DETENER permanece desactivado.
    botonDetener.disabled = true;

    // ==========================================
    // MOSTRAR OFERTAS
    // ==========================================

    function mostrarOfertas(ofertas) {

        listaOfertas.replaceChildren();

        if (ofertas.length === 0) {
            estadoOfertas.textContent =
                "No se encontraron ofertas con esos criterios.";

            estadoOfertas.hidden = false;
            return;
        }

        estadoOfertas.textContent =
            "Ofertas encontradas: " + ofertas.length;

        estadoOfertas.hidden = false;

        ofertas.forEach(function (oferta) {

            const tarjeta = document.createElement("article");
            tarjeta.className = "tarjeta-oferta";

            const titulo = document.createElement("h3");
            titulo.textContent = oferta.cargo;

            const empresa = document.createElement("p");
            empresa.textContent = "Empresa: " + oferta.empresa;

            const ciudad = document.createElement("p");
            ciudad.textContent = "Ciudad: " + oferta.ciudad;

            const fecha = document.createElement("p");
            fecha.textContent = "Publicación: " + oferta.fecha;

            const portal = document.createElement("p");
            portal.textContent = "Portal: " + oferta.portal;

            const enlace = document.createElement("a");
            enlace.className = "boton-oferta";
            enlace.textContent = "VER OFERTA";
            enlace.href = oferta.enlace;
            enlace.target = "_blank";
            enlace.rel = "noopener noreferrer";

            tarjeta.append(
                titulo,
                empresa,
                ciudad,
                fecha,
                portal,
                enlace
            );

            listaOfertas.appendChild(tarjeta);
        });
    }

    // ==========================================
    // BUSCAR OFERTAS
    // ==========================================
     
    async function buscarOfertas() {
        const palabra = campoBuscar.value.trim();

        if (!palabra) {
            estadoOfertas.textContent =
                "Escribe un cargo o profesión para buscar.";
            return;
        }

        botonBuscar.disabled = true;
        botonDetener.disabled = false;
        estadoOfertas.textContent =
            "Buscando ofertas reales en los portales...";

        try {
            const respuesta = await fetch("/api/buscar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ palabra })
            });

            const datos = await respuesta.json();

            if (!respuesta.ok) {
                throw new Error(
                    datos.error || "No se pudo iniciar la búsqueda."
                );
            }

            // Consultar el estado hasta que termine la búsqueda.
            while (true) {
                await new Promise(resolve =>
                    setTimeout(resolve, 2000)
                );

                const respuestaEstado = await fetch(
                    "/api/estado",
                    { cache: "no-store" }
                );

                if (!respuestaEstado.ok) {
                    throw new Error(
                        "No se pudo consultar el estado del buscador."
                    );
                }

                const resultado = await respuestaEstado.json();

                estadoOfertas.textContent = resultado.mensaje;

                if (!resultado.activa) {
                    if (resultado.error) {
                        throw new Error(resultado.error);
                    }
                    break;
                }
            }

            // Al terminar, mostrar las ofertas guardadas.
            await cargarOfertas();

        } catch (error) {
            console.error("Error buscando ofertas:", error);
            estadoOfertas.textContent =
                "Error: " + error.message;
        } finally {
            botonBuscar.disabled = false;
            botonDetener.disabled = true;
        }
    }
   
    
    // ==========================================
    // CARGAR OFERTAS GUARDADAS EN SQLITE
    // ==========================================

    async function cargarOfertas() {
        const termino = campoBuscar.value.trim();
        const ciudad = campoCiudad.value.trim();

        const parametros = new URLSearchParams();

        if (termino) {
            parametros.set("buscar", termino);
        }

        if (ciudad && ciudad.toLowerCase() !== "todas") {
            parametros.set("ciudad", ciudad);
        }

        estadoOfertas.textContent = "Cargando ofertas guardadas...";

        try {
            const respuesta = await fetch(
                "/api/ofertas?" + parametros.toString(),
                { cache: "no-store" }
            );

            if (!respuesta.ok) {
                throw new Error("Error HTTP " + respuesta.status);
            }

            const datos = await respuesta.json();
            mostrarOfertas(datos.ofertas || []);

        } catch (error) {
            console.error("Error cargando ofertas:", error);
            estadoOfertas.textContent =
                "No se pudieron cargar las ofertas: " + error.message;
        }
     }
          
    // ==========================================
    // BOTÓN BUSCAR EMPLEO
    // ==========================================

    botonBuscar.addEventListener("click", buscarOfertas);

    // Buscar también al pulsar Enter en el campo de cargo.
    campoBuscar.addEventListener("keydown", function (evento) {

        if (evento.key === "Enter") {
            evento.preventDefault();
            cargarOfertas();
        }
    });

    // ==========================================
    // BOTÓN ROJO DETENER
    // ==========================================
   
    botonDetener.addEventListener("click", async () => {
        botonDetener.disabled = true;
        document.getElementById("estadoOfertas").textContent =
        "Solicitando detener la búsqueda...";

    try {
        const respuesta = await fetch("/api/detener", {
            method: "POST"
        });

        const datos = await respuesta.json();

        document.getElementById("estadoOfertas").textContent =
            datos.mensaje || "Solicitud enviada.";

    } catch (error) {
        document.getElementById("estadoOfertas").textContent =
            "No se pudo enviar la orden de detener.";
    }
});


    // ==========================================
    // REGISTRAR SERVICE WORKER
    // ==========================================

    if ("serviceWorker" in navigator) {

        navigator.serviceWorker.register("./service-worker.js")
            .then(function () {

                console.log(
                    "Service Worker registrado correctamente"
                );

            })
            .catch(function (error) {

                console.error(
                    "Error registrando Service Worker:",
                    error
                );
            });
    }

    // ==========================================
    // CARGAR OFERTAS AL ABRIR LA PÁGINA
    // ==========================================

    cargarOfertas();
    
    });
