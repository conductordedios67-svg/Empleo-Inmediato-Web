
const CACHE_NAME = "empleo-inmediato-v3";

const ARCHIVOS = [
    "./",
    "./index.html",
    "./style.css",
    "./app.js",
    "./manifest.json"
];

self.addEventListener("install", function (evento) {
    evento.waitUntil(
        caches.open(CACHE_NAME)
            .then(function (cache) {
                return cache.addAll(ARCHIVOS);
            })
            .then(function () {
                return self.skipWaiting();
            })
    );
});

self.addEventListener("activate", function (evento) {
    evento.waitUntil(
        caches.keys()
            .then(function (nombres) {
                return Promise.all(
                    nombres
                        .filter(function (nombre) {
                            return nombre.startsWith("empleo-inmediato-")
                                && nombre !== CACHE_NAME;
                        })
                        .map(function (nombre) {
                            return caches.delete(nombre);
                        })
                );
            })
            .then(function () {
                return self.clients.claim();
            })
    );
});

self.addEventListener("fetch", function (evento) {
    const solicitud = evento.request;
    const url = new URL(solicitud.url);

    // La API siempre consulta al servidor, nunca a la caché.
    if (
        url.origin !== self.location.origin ||
        url.pathname.startsWith("/api/") ||
        solicitud.method !== "GET"
    ) {
        return;
    }

    // Los archivos de la PWA pueden utilizar la caché.
    evento.respondWith(
        caches.match(solicitud)
            .then(function (respuesta) {
                if (respuesta) {
                    return respuesta;
                }

                return fetch(solicitud);
            })
    );
});
