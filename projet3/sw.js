/* PROJET3 — le service worker.
   Réseau d'abord : chaque ouverture reçoit la dernière version de l'outil.
   Cache en secours : hors ligne, la dernière version connue répond.
   (Un cache-first servirait éternellement la première version installée —
   exactement le piège que le rituel « vérifier par curl » évite.) */
const CACHE = "projet3-v3.0.0";
const PAGES = ["./", "./index.html", "./manifest.webmanifest", "./icons/icon-192.png", "./icons/icon-512.png", "./icons/icon-512-maskable.png"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(PAGES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    fetch(e.request).then(rep => {
      if (rep && rep.ok) {
        const copie = rep.clone();
        caches.open(CACHE).then(c => c.put(e.request, copie));
      }
      return rep;
    }).catch(() =>
      caches.match(e.request, { ignoreSearch: true })
        .then(hit => hit || caches.match("./index.html"))
    )
  );
});
