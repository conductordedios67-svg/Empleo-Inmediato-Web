// ==========================================
// EMPLEO INMEDIATO
// SERVICE WORKER
// ==========================================

const CACHE_NAME = "empleo-inmediato-v2";

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
    );

});

self.addEventListener("fetch", function (evento) {

    evento.respondWith(
        caches.match(evento.request)
            .then(function (respuesta) {

                if (respuesta) {
                    return respuesta;
                }

                return fetch(evento.request);
            })
    );

});