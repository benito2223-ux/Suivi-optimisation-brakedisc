/* ============================================================================
   Suivi_optimisation_SPK — service worker (v4.18)
   ----------------------------------------------------------------------------
   Rend l'outil INSTALLABLE (PWA) et pousse les mises à jour sans jamais
   désinstaller/réinstaller : l'app installée se relance avec la dernière
   version dès que le réseau l'a vue, et retombe sur le cache hors ligne.

   Stratégie volontairement simple, calée sur la réalité de l'outil :
   - L'application = UN fichier HTML autonome (polices et logo inclus).
     Chaque ouverture passe par le RÉSEAU D'ABORD : la version à jour est
     servie dès qu'elle existe, le cache ne sert qu'en repli hors ligne.
     Une mise à jour est donc appliquée à l'ouverture suivante, sans
     manipulation — le numéro de version n'a pas à être dupliqué ici.
   - Les icônes et le manifeste sont du cache statique classique.
   - TOUT ce qui vient d'un autre domaine (Supabase : synchro, photos, auth)
     et toutes les requêtes non-GET NE SONT PAS INTERCEPTÉS : le comportement
     cloud et offline-first existant reste exactement le même.
   Le nom de cache ne change QUE si ce fichier lui-même change (il n'embarque
   pas la version de l'app : c'est la clé qui purge les vieux caches).
   ============================================================================ */
const CACHE = "spk-suivi-shell-v1";
const SHELL = [
  "./",
  "./index.html",
  "./bilan_economique.html",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-512-maskable.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(SHELL))
      .then(() => self.skipWaiting()) // la nouvelle version prend la main immédiatement
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((cles) => Promise.all(cles.filter((c) => c !== CACHE).map((c) => caches.delete(c))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;                 // POST synchro/photos : jamais interceptés
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;  // Supabase & co : jamais interceptés

  const estHtml = url.pathname.endsWith("bilan_economique.html") || url.pathname.endsWith("index.html");
  if (estHtml) {
    // réseau d'abord : mise à jour automatique à chaque ouverture en ligne ;
    // hors ligne, on sert la dernière version connue.
    e.respondWith(
      fetch(req).then((rep) => {
        const copie = rep.clone();
        caches.open(CACHE).then((c) => c.put(req, copie));
        return rep;
      }).catch(() =>
        caches.match(req).then((hit) => hit || caches.match("./bilan_economique.html"))
      )
    );
    return;
  }

  // le reste (manifeste, icônes) : cache d'abord, réseau en complément
  e.respondWith(
    caches.match(req).then((hit) =>
      hit ||
      fetch(req).then((rep) => {
        if (rep && rep.ok) {
          const copie = rep.clone();
          caches.open(CACHE).then((c) => c.put(req, copie));
        }
        return rep;
      })
    )
  );
});
