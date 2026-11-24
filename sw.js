const VERSION = "v8";
const CACHE = "faucets-" + VERSION;
const ROOT = new URL("./", self.location).href;
const SHELL = ["", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon.svg"];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(CACHE).then(function (cache) {
      return cache.addAll(SHELL.map(function (path) { return new URL(path, ROOT).href; }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (key) { return key !== CACHE; }).map(function (key) { return caches.delete(key); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (event) {
  var request = event.request;
  if (request.method !== "GET") return;
  if (new URL(request.url).origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(
      caches.open(CACHE).then(function (cache) {
        var cached = function () {
          return cache.match(new URL("index.html", ROOT).href).then(function (hit) {
            return hit || Response.error();
          });
        };
        return fetch(request, { cache: "no-cache" }).then(function (fresh) {
          if (fresh && fresh.ok) {
            cache.put(new URL("index.html", ROOT).href, fresh.clone());
            return fresh;
          }
          return cached();
        }).catch(cached);
      })
    );
    return;
  }

  event.respondWith(
    caches.open(CACHE).then(function (cache) {
      return cache.match(request).then(function (hit) {
        var network = fetch(request).then(function (response) {
          if (response.ok) cache.put(request, response.clone());
          return response;
        }).catch(function () { return null; });
        return hit || network.then(function (response) { return response || Response.error(); });
      });
    })
  );
});
