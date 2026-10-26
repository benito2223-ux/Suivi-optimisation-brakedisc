/* ============================================================================
   Suivi_optimisation_SPK — service worker (v4.100.2 — mise a jour a chaud)
   ----------------------------------------------------------------------------
   Rend l'outil INSTALLABLE (PWA) et pousse les mises à jour sans jamais
   désinstaller/réinstaller : l'app installée se relance avec la dernière
   version dès que le réseau l'a vue, et retombe sur le cache hors ligne.

   Ce qui a changé en v4.100.0 : la coque (rail, barre d'onglets mobile,
   écrans plein écran) et ses polices sont maintenant dans le REPO GIT, donc
   dans le build de déploiement. Le service worker doit les connaître :
   - `spk-app.css` et `spk-shell.js` entrent dans le cache ;
   - v4.112 : les 8 fichiers `fonts/*.woff2` de la coque d'origine sont
     RETIRÉS (Barlow/Public Sans/IBM Plex mortes — l'app embarque ses
     polices en base64, elles ne servaient jamais) et le nom du cache passe
     en `spk-suivi-shell-v7` pour purger l'ancien.

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

   Ce qui a changé en v4.100.2 : la MISE À JOUR À CHAUD. Le 20/10, une
   correction du shell (le bouton « Retour » qui disparaissait sous un
   dialogue) est restée INVISIBLE sur les navigateurs déjà visités, alors
   qu'elle était déployée et vérifiée sur une URL publique. Deux raisons,
   qui se cumulaient :
   - `spk-shell.js` était servi CACHE D'ABORD : le cache ne se purge que si
     le service worker change, or c'est le shell qui changeait, pas le SW.
   - `caches.addAll(SHELL)` est TOUT OU RIEN : une seule police manquante
     faisait échouer l'installation, donc le nouveau SW ne prenait jamais
     la main et l'ancien continuait de servir l'ancien shell.
   D'où : le shell passe en réseau d'abord comme le HTML et le CSS, et
   l'installation met chaque entrée séparément (une entrée ratée n'annule
   pas les autres). Le cache passe en `v6` : l'ancien `v5` est purgé à
   l'activation.
   ============================================================================ */
const CACHE = "spk-suivi-shell-v7";
const SHELL = [
  "./",
  "./index.html",
  "./bilan_economique.html",
  "./spk-app.css",
  "./spk-shell.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-512-maskable.png"
];

self.addEventListener("install", (e) => {
  /* v4.100.2 — `addAll` est TOUT OU RIEN : si un seul des 17 fichiers manque
     (une police pas encore publiee, un 404), l'installation ECHOUE, le
     nouveau service worker n'est jamais active, et l'ancien continue de
     servir le vieux shell — le meme piege qu'avant, en plus sournois.
     On met donc chaque entree separement, et l'echec de l'une n'annule pas
     les autres. Le cache est de toute facon rafraichi a chaque requete
     reseau (voir le bloc fetch), donc une entree manquante se rattrape
     d'elle-meme. */
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => Promise.all(
        SHELL.map((url) => c.add(url).catch(() => null))
      ))
      .then(() => self.skipWaiting()) // la nouvelle version prend la main immediatement
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((cles) => Promise.all(cles.filter((c) => c !== CACHE).map((c) => caches.delete(c))))
      .then(() => self.clients.claim())
      /* v4.100.2 — le nouveau service worker prend la main : on PREVIENT les
         pages ouvertes, sinon elles continuent de tourner avec l'ancien shell
         jusqu'au rechargement. `skipWaiting` seul ne suffit pas : la page
         déjà chargée garde le script qu'elle a exécuté. */
      .then(() => self.clients.matchAll({ type: "window" }))
      .then((pages) => pages.forEach((p) => p.postMessage({ type: "SPK_MAJ", cache: CACHE })))
  );
});

/* v4.100.2 — la page demande : « y a-t-il du neuf ? ». On compare la version
   du service worker à celle qu'il a servie, et on répond. */
self.addEventListener("message", (e) => {
  if (!e.data || e.data.type !== "SPK_VERIF_MAJ") return;
  const rep = { type: "SPK_VERSION_SW", cache: CACHE, version: self.__spkVersion || null };
  if (e.source && e.source.postMessage) e.source.postMessage(rep);
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;                 // POST synchro/photos : jamais interceptés
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;  // Supabase & co : jamais interceptés

  const estHtml = url.pathname.endsWith("bilan_economique.html") || url.pathname.endsWith("index.html");
  const estCss = url.pathname.endsWith("spk-app.css");
  const estJs = url.pathname.endsWith("spk-shell.js");
  if (estHtml || estCss || estJs) {
    // réseau d'abord : mise à jour automatique à chaque ouverture en ligne ;
    // hors ligne, on sert la dernière version connue. cache:"no-cache" garantit que
    // le contrôle réseau n'est jamais répondu par le cache HTTP du navigateur (304)
    // — sinon une version neuve pourrait rester invisible derrière un 304.
    //
    // v4.100.1 — `spk-shell.js` rejoint le HTML et le CSS. AVANT, il tombait
    // dans le bloc « cache d'abord » ci-dessous : le shell étant servi depuis
    // le cache, une correction du shell (le bouton Retour qui disparaissait
    // sous un dialogue) restait INVISIBLE sur les navigateurs déjà visités —
    // et le SW ne se réinstallait pas, puisque le fichier SW lui-même
    // n'avait pas changé. Le cache ne se purge que si le SW change ; or
    // c'est le shell qui change, pas le SW. D'où la correction structurelle :
    // tout ce qui porte le comportement passe par le réseau d'abord.
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
