/* ============================================================================
   Suivi_optimisation_SPK — service worker (v4.100.0 — coque « Console d'atelier »)
   ----------------------------------------------------------------------------
   Rend l'outil INSTALLABLE (PWA) et pousse les mises à jour sans jamais
   désinstaller/réinstaller : l'app installée se relance avec la dernière
   version dès que le réseau l'a vue, et retombe sur le cache hors ligne.

   Ce qui a changé en v4.100.0 : la coque (rail, barre d'onglets mobile,
   écrans plein écran) et ses polices sont maintenant dans le REPO GIT, donc
   dans le build de déploiement. Le service worker doit les connaître :
   - `spk-app.css` et `spk-shell.js` entrent dans le cache ;
   - les polices `fonts/*.woff2` aussi (elles sont en local, jamais distantes :
     l'outil doit rester utilisable hors ligne) ;
   - le nom du cache change (`spk-suivi-shell-v5`) pour purger l'ancien.

   Stratégie volontairement simple, calée sur la réalité de l'outil :
   - L'application = UN fichier HTML + la coque (CSS + JS) + les polices
     locales. Chaque ouverture passe par le RÉSEAU D'ABORD : la version à jour
     est servie dès qu'elle existe, le cache ne sert qu'en repli hors ligne.
     Une mise à jour est donc appliquée à l'ouverture suivante, sans
     manipulation — le numéro de version n'a pas à être dupliqué ici.
   - Les icônes et le manifeste sont du cache statique classique.
   - TOUT ce qui vient d'un autre domaine (Supabase : synchro, photos, auth)
     et toutes les requêtes non-GET NE SONT PAS INTERCEPTÉS : le comportement
     cloud et offline-first existant reste exactement le même.
   Le nom de cache ne change QUE si ce fichier lui-même change (il n'embarque
   pas la version de l'app : c'est la clé qui purge les vieux caches).
   ============================================================================ */
const CACHE = "spk-suivi-shell-v5";
const SHELL = [
  "./",
  "./index.html",
  "./bilan_economique.html",
  "./spk-app.css",
  "./spk-shell.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-512-maskable.png",
  "./fonts/barlow-condensed-600.woff2",
  "./fonts/barlow-condensed-700.woff2",
  "./fonts/public-sans-400.woff2",
  "./fonts/public-sans-500.woff2",
  "./fonts/public-sans-600.woff2",
  "./fonts/public-sans-700.woff2",
  "./fonts/ibm-plex-mono-400.woff2",
  "./fonts/ibm-plex-mono-500.woff2"
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
  const estCss = url.pathname.endsWith("spk-app.css");
  if (estHtml || estCss) {
    // réseau d'abord : mise à jour automatique à chaque ouverture en ligne ;
    // hors ligne, on sert la dernière version connue. cache:"no-cache" garantit que
    // le contrôle réseau n'est jamais répondu par le cache HTTP du navigateur (304)
    // — sinon une version neuve pourrait rester invisible derrière un 304.
    // Le CSS de la coque est dans ce lot : sans cela, une retouche de thème
    // resterait invisible sur les navigateurs déjà visités (le shell est
    // servi cache-first, la version servie resterait celle d'avant).
    e.respondWith(
      fetch(req, { cache: "no-cache" }).then((rep) => {
        if (rep && rep.ok) {
          const copie = rep.clone();
          caches.open(CACHE).then((c) => c.put(req, copie));
        }
        return rep.ok ? rep : (caches.match(req).then((hit) => hit || caches.match("./bilan_economique.html")));
      }).catch(() =>
        caches.match(req).then((hit) => hit || caches.match("./bilan_economique.html"))
      )
    );
    return;
  }

  // le reste (manifeste, icônes, polices, coque JS) : cache d'abord, réseau en complément
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
