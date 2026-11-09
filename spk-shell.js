/* v4.145.3 — lève l'écran de chargement une fois la coque posée (le monolithe ne le fait plus dans le livré). Planifié en
   tête : il part même si une partie de la coque échoue ; le filet à 5 s du monolithe reste le dernier recours. */
setTimeout(function(){ requestAnimationFrame(function(){ requestAnimationFrame(function(){ document.documentElement.setAttribute("data-pret", "1"); }); }); }, 0);
/* Coque de navigation et surfaces de travail.
   Ne touche pas aux données : déplace la navigation existante dans un rail,
   ajoute un bouton de sortie aux surfaces plein écran et marque l'onglet actif.
   v4 (20/10/2026) : rail repliable au glissement, version reprise de l'app. */
(function () {
  "use strict";

  if (document.body.dataset.spkShell === "on") return;
  document.body.dataset.spkShell = "on";

  const nav = document.querySelector(".toolbar-ecrans");
  if (!nav) return;

  // Préférence de repli lue AVANT toute création : appliquée sans animation.
  let railFermé = false;
  try { railFermé = localStorage.getItem("spk-rail-closed") === "1"; } catch (e) { /* stockage indisponible */ }
  if (railFermé) {
    document.documentElement.classList.add("spk-boot");
    document.body.classList.add("spk-rail-off");
  }

  const rail = document.createElement("aside");
  rail.className = "spk-rail";
  rail.setAttribute("aria-label", "Navigation principale");
  rail.setAttribute("role", "navigation");

  rail.innerHTML = [
    '<div class="spk-rail-head">',
    '  <div class="spk-rail-mark">Suivi<span>d\'optimisation</span></div>',
    '  <div class="spk-rail-title">Suivi d’optimisation</div>',
    '</div>',
    '<div class="spk-rail-label">Parcours</div>',
    '<div class="spk-rail-nav" id="spkRailNav"></div>',
    /* v4.125 — le bouton Importer du pied de rail est retiré : l'import vit
       dans le menu Transmettre (groupe « L'archive »), comme l'export. */
    '  <span class="spk-rail-live"><i></i>Données locales</span>',
    '  <span class="spk-rail-version"></span>',
    '</div>'
  ].join("");

  const sourceLogo = document.querySelector(".hd-left img");
  if (sourceLogo) {
    const logo = sourceLogo.cloneNode();
    logo.className = "spk-rail-logo";
    logo.alt = "";
    rail.querySelector(".spk-rail-head").prepend(logo);
  }

  // La version affichée suit l'application, pas la coque.
  try {
    if (typeof TOOL_VERSION === "string") {
      rail.querySelector(".spk-rail-version").textContent = "v" + TOOL_VERSION;
    }
  } catch (e) { /* pas de version connue */ }

  const navHost = rail.querySelector(".spk-rail-nav");
  navHost.appendChild(nav);
  nav.classList.add("spk-rail-links");

  document.body.prepend(rail);
  document.body.classList.add("spk-has-rail");

  /* v4.125 — le câblage rail→import a disparu avec le bouton : l'import vit
     dans le menu Transmettre (bilan_economique.html, importMenuBtn). */

  // Le libellé reste accessible quand le rail se réduit en icônes.
  nav.querySelectorAll("button").forEach((btn) => {
    const label = btn.textContent.replace(/\s+/g, " ").trim();
    if (label) {
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    }
  });

  // --- Poignée de repli du rail (bureau et tablette uniquement) -----------
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.id = "spkRailToggle";
  toggle.setAttribute("aria-controls", "spkRailNav");
  toggle.setAttribute("aria-expanded", "true");
  toggle.innerHTML =
    '<svg viewBox="0 0 12 12" width="12" height="12" aria-hidden="true">' +
    '<path d="M7.5 2 3.5 6l4 4" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  toggle.addEventListener("click", () => {
    const off = document.body.classList.toggle("spk-rail-off");
    try { localStorage.setItem("spk-rail-closed", off ? "1" : "0"); } catch (e) { /* stockage indisponible */ }
    syncRailToggle();
  });

  function syncRailToggle() {
    const off = document.body.classList.contains("spk-rail-off");
    toggle.setAttribute("aria-expanded", off ? "false" : "true");
    const label = off ? "Afficher la navigation" : "Masquer la navigation";
    toggle.setAttribute("aria-label", label);
    toggle.setAttribute("title", label);
  }

  document.body.appendChild(toggle);
  syncRailToggle();

  // On retire le verrou d'animation après deux frames (filet de secours par
  // timeout : les rAF d'un onglet en arrière-plan peuvent ne jamais partir).
  const finBoot = () => document.documentElement.classList.remove("spk-boot");
  requestAnimationFrame(() => requestAnimationFrame(finBoot));
  setTimeout(finBoot, 300);

  /* v4.132 — UNE SEULE BANDE EN TÊTE DE PAGE, ET UNE NAVIGATION RANGÉE.
     Constat (rendu de la 4.129.1) : cinq couches avant le contenu — bandeau
     bleu, barre d'actions, aide seule, « Créer un projet » seul, fil d'Ariane,
     bannière — la « Réponse » démarrait à 570 px sur 900. On DÉPLACE les
     éléments existants (ids, handlers et gardes de verrouillage suivent) :
     les actions entrent dans le bandeau bleu, le fil d'Ariane et les projets
     partagent une ligne fine, l'aide devient une icône des actions. Rien ne
     se calcule ici. */
  (function () {
    const hd = document.querySelector(".hd");
    const tb = document.getElementById("toolbarWrap");
    if (!hd || !tb) return;
    const bar = document.createElement("div");
    bar.className = "spk-hd-actions";
    bar.id = "spkHdActions";
    hd.appendChild(bar);

    const rech = document.createElement("button");
    rech.type = "button";
    rech.className = "ghost spk-hd-btn";
    rech.id = "spkRechercheBtn";
    rech.setAttribute("aria-label", "Rechercher (Ctrl+K)");
    rech.title = "Rechercher (Ctrl+K)";
    rech.innerHTML = '<svg class="icon" viewBox="0 0 18 18" aria-hidden="true"><circle cx="8" cy="8" r="4.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m11.5 11.5 3 3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';
    rech.addEventListener("click", () => {
      if (typeof window.ouvrirRecherche === "function") window.ouvrirRecherche();
    });

    const addBtn = document.getElementById("addBtn");
    if (addBtn) { addBtn.classList.remove("ghost"); addBtn.classList.add("primary"); bar.appendChild(addBtn); }
    bar.appendChild(rech);
    ["transmettreWrap", "modeBtn", "lockBtn"].forEach((id) => {
      const el = document.getElementById(id);
      if (el) bar.appendChild(el);
    });
    const plus = document.getElementById("moreBtn");
    const plusWrap = plus && plus.closest ? plus.closest(".toolbar-more-wrap") : null;
    if (plusWrap) bar.appendChild(plusWrap);
    /* v4.134 — « Atelier » désignait trois choses (le mode tactile, la carte des
       machines, « Voir l'atelier ») : le mode tactile se dit « mode gants ». */
    const modeB = document.getElementById("modeBtn");
    if (modeB) {
      modeB.setAttribute("title", "Mode gants : grandes cibles tactiles, gros chiffres — pour l'écran de la machine");
      modeB.setAttribute("aria-label", "Mode gants");
    }
    ["modeBtn", "lockBtn"].forEach((id) => {
      const b = document.getElementById(id);
      if (b && !b.getAttribute("title")) b.setAttribute("title", b.textContent.replace(/\s+/g, " ").trim());
    });
    const aide = document.getElementById("aideBlock");
    if (aide) bar.appendChild(aide);
    const save = document.getElementById("saveStatus");
    if (save) bar.appendChild(save);

    /* ligne fine sous le bandeau : fil d'Ariane + projets */
    const ctx = document.createElement("div");
    ctx.className = "spk-ctx";
    ctx.id = "spkCtx";
    const rail = document.getElementById("ctxRail") || document.getElementById("filAriane");
    if (rail) ctx.appendChild(rail);
    const pj = document.getElementById("projetsBandeau");
    if (pj) ctx.appendChild(pj);
    hd.after(ctx);

    /* navigation : « Scénarios » (l'écran de travail) devient une vraie
       destination ; le classeur Matis passe dans un groupe « Contrôle » et se
       nomme par ce qu'il montre. Les ids ne bougent pas. */
    const travail = document.createElement("button");
    travail.type = "button";
    travail.id = "spkTravailBtn";
    travail.className = "ghost";
    travail.innerHTML = '<svg class="icon" viewBox="0 0 18 18" aria-hidden="true"><path d="M3 4.5h12M3 9h12M3 13.5h8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>Scénarios';
    travail.addEventListener("click", () => {
      if (typeof window.fermerPanneaux === "function") window.fermerPanneaux();
      try { window.scrollTo({ top: 0, behavior: "instant" }); } catch (e) { window.scrollTo(0, 0); }
    });
    nav.insertBefore(travail, nav.firstChild);

    const matis = document.getElementById("matisBtn");
    if (matis) {
      const sep = document.createElement("span");
      sep.className = "spk-nav-sep";
      sep.textContent = "Contrôle";
      nav.insertBefore(sep, matis);
      matis.childNodes.forEach((n) => {
        if (n.nodeType === 3 && n.textContent.trim()) n.textContent = "Réel vs budget";
      });
      matis.setAttribute("aria-label", "Réel vs budget (classeur Matis)");
      matis.setAttribute("title", "Réel vs budget (classeur Matis)");
    }
  })();

  /* v4.132.2 — ouvrir une carte de scénario AMÈNE à sa fiche. Avant : la fiche
     changeait 900 px plus bas et l'écran ne bougeait pas — on croyait que le clic
     n'avait rien fait. On laisse l'application rendre, puis on défile (en douceur,
     sauf si l'utilisateur a demandé moins d'animations). Les étiquettes de projet
     sur la carte ne déclenchent pas le défilement. */
  document.addEventListener("click", (e) => {
    const t = e.target;
    if (!t || !t.closest) return;
    const carte = t.closest(".tab-card");
    if (!carte || t.closest(".tag-pill")) return;
    requestAnimationFrame(() => requestAnimationFrame(() => {
      const fiche = document.getElementById("scenarioDetail");
      if (!fiche) return;
      const doux = !(window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches);
      try { fiche.scrollIntoView({ behavior: doux ? "smooth" : "auto", block: "start" }); }
      catch (err) { fiche.scrollIntoView(true); }
    }));
  });

  /* v4.132.2 — téléphone : la hauteur réelle de la barre d'onglets du bas nourrit
     --spk-nav-h (les écrans plein écran s'arrêtent au-dessus d'elle). */
  (function () {
    const poser = () => {
      const h = window.matchMedia("(max-width:900px)").matches ? rail.offsetHeight : 0;
      document.documentElement.style.setProperty("--spk-nav-h", h + "px");
    };
    poser();
    window.addEventListener("resize", poser);
    if (window.ResizeObserver) new ResizeObserver(poser).observe(rail);
  })();

  /* ══ v4.133 — LA FICHE EN TROIS ONGLETS, LES CRITÈRES REPLIÉS, LA PIÈCE DANS LA RÉPONSE ══
     La fiche du scénario faisait 2 400 px sur PC, 3 860 sur téléphone : Composition,
     Tendance, Essais et Rebut empilés. Elle se lit maintenant par onglet — Essais
     (ouvert par défaut : le geste du quotidien), Composition, Suivi (tendance + rebut).
     Le bandeau de chiffres reste au-dessus, toujours visible. Tout est fait APRÈS le
     rendu de l'application (observateur) : rien n'est recalculé, les éléments sont
     seulement montrés / masqués / déplacés — ids et écouteurs suivent. */
  const ONGLETS = [
    { id: "essais", lib: "Essais", secs: [".sec-essais"] },
    { id: "composition", lib: "Composition", secs: [".sec-plaquettes"] },
    { id: "suivi", lib: "Suivi", secs: [".sec-graph", ".sec-rebut"] }
  ];
  let ongletFiche = "essais";
  const criteresOuverts = {};

  function poserOnglet(sc, id) {
    ongletFiche = id;
    sc.setAttribute("data-onglet", id);
    sc.querySelectorAll(".spk-onglets button").forEach((b) => {
      const on = b.getAttribute("data-onglet") === id;
      b.classList.toggle("is-on", on);
      b.setAttribute("aria-selected", on ? "true" : "false");
    });
    /* l'onglet Suivi n'a que Tendance et Rebut : on les ouvre (une fois par fiche) */
    if (id === "suivi" && !sc.dataset.suiviOuvert) {
      sc.dataset.suiviOuvert = "1";
      sc.querySelectorAll(":scope > .sec-graph > details, :scope > .sec-rebut > details").forEach((d) => { if (!d.open) d.open = true; });
    }
  }

  function equiperFiche() {
    const detail = document.getElementById("scenarioDetail");
    const sc = detail && detail.querySelector(":scope > .scenario");
    if (!sc || sc.querySelector(":scope > .spk-onglets")) return;
    const premiere = sc.querySelector(":scope > .sec-plaquettes") || sc.querySelector(":scope > .sec-essais");
    if (!premiere) return;
    const nEssais = sc.querySelectorAll(".essais-list > .essai-card").length;
    const barre = document.createElement("div");
    barre.className = "spk-onglets";
    barre.setAttribute("role", "tablist");
    ONGLETS.forEach((o) => {
      const b = document.createElement("button");
      b.type = "button";
      b.setAttribute("role", "tab");
      b.setAttribute("data-onglet", o.id);
      b.innerHTML = o.lib + (o.id === "essais" ? ' <span class="spk-onglet-n">' + nEssais + "</span>" : "");
      b.addEventListener("click", () => poserOnglet(sc, o.id));
      barre.appendChild(b);
    });
    sc.insertBefore(barre, premiere);
    ONGLETS.forEach((o) => o.secs.forEach((s) => {
      const el = sc.querySelector(":scope > " + s);
      if (el) el.setAttribute("data-dans-onglet", o.id);
    }));
    poserOnglet(sc, ongletFiche);

    /* les critères de jugement (battement, côtés, Ra/VE, seuil) : réglés une fois par
       scénario, ils occupaient 170 px éparpillés au-dessus des essais. Ils se replient
       derrière une ligne qui les résume ; ouverts d'office tant qu'aucun essai n'existe. */
    const meta = sc.querySelector(".sec-essais .log-meta");
    if (meta && !meta.closest(".spk-criteres")) {
      const idSc = (sc.querySelector("[data-id]") || { getAttribute: () => "" }).getAttribute("data-id") || "";
      const det = document.createElement("details");
      det.className = "spk-criteres";
      const sum = document.createElement("summary");
      const bat = meta.querySelector('input[data-field="battActif"]');
      const lib = meta.querySelector("input.limit-label");
      const valBat = meta.querySelector("input.limit-value:not([data-csup]):not([data-field='validationThreshold'])");
      const valSeuil = meta.querySelector("input[data-field='validationThreshold']");
      const cote = meta.querySelector("select");
      const morceaux = [];
      if (!bat || bat.checked) {
        morceaux.push((lib && lib.value ? lib.value : "Battement") + " ≤ " + (valBat && valBat.value ? valBat.value : "—")
          + (cote && cote.selectedOptions && cote.selectedOptions[0] ? " (" + cote.selectedOptions[0].textContent.trim() + ")" : ""));
      }
      const autres = meta.querySelectorAll(".csup-item, .csup-row").length;
      if (autres) morceaux.push("+ " + autres + " critère" + (autres > 1 ? "s" : ""));
      const seuil = valSeuil && valSeuil.value ? valSeuil.value : null;
      if (seuil) morceaux.push("validé à " + seuil + " essais conformes");
      sum.innerHTML = '<span class="spk-crit-l">Critères de jugement</span><span class="spk-crit-v"></span>';
      sum.querySelector(".spk-crit-v").textContent = morceaux.join(" · ");
      det.appendChild(sum);
      meta.parentNode.insertBefore(det, meta);
      det.appendChild(meta);
      det.open = (idSc in criteresOuverts) ? criteresOuverts[idSc] : nEssais === 0;
      det.addEventListener("toggle", () => { criteresOuverts[idSc] = det.open; });
    }
    /* v4.134 — ‹ n / N › : le scénario précédent / suivant, sans remonter aux cartes.
       L'ordre est celui des numéros des cartes (le rang dans l'OP). */
    const head = sc.querySelector(":scope > .scenario-head");
    const cartes = [...document.querySelectorAll("#tabsStrip .tab-card")]
      .map((c) => ({ c, n: parseInt((c.querySelector(".tc-num") || {}).textContent, 10) || 0 }))
      .sort((a, b) => a.n - b.n);
    const iAct = cartes.findIndex((x) => x.c.classList.contains("active"));
    if (head && cartes.length > 1 && iAct >= 0 && !head.querySelector(".spk-sc-nav")) {
      const nav = document.createElement("div");
      nav.className = "spk-sc-nav";
      const aller = (d) => { const x = cartes[iAct + d]; if (x) x.c.click(); };
      nav.innerHTML = '<button type="button" aria-label="Scénario précédent" title="Scénario précédent">‹</button>'
        + "<span>" + (iAct + 1) + " / " + cartes.length + "</span>"
        + '<button type="button" aria-label="Scénario suivant" title="Scénario suivant">›</button>';
      const [bPrec, , bSuiv] = nav.children;
      bPrec.disabled = iAct === 0;
      bSuiv.disabled = iAct === cartes.length - 1;
      bPrec.addEventListener("click", () => aller(-1));
      bSuiv.addEventListener("click", () => aller(1));
      head.appendChild(nav);
      /* glisser horizontalement sur l'en-tête ou les chiffres (écran tactile) */
      let x0 = null, y0 = null;
      [head, sc.querySelector(":scope > .scenario-foot")].forEach((zone) => {
        if (!zone) return;
        zone.addEventListener("touchstart", (e) => { const t = e.touches[0]; x0 = t.clientX; y0 = t.clientY; }, { passive: true });
        zone.addEventListener("touchend", (e) => {
          if (x0 === null) return;
          const t = e.changedTouches[0];
          const dx = t.clientX - x0, dy = t.clientY - y0;
          x0 = null;
          if (Math.abs(dx) > 70 && Math.abs(dy) < 45) aller(dx < 0 ? 1 : -1);
        }, { passive: true });
      });
    }

    const h3 = sc.querySelector(".sec-essais .log-section > h3");
    if (h3 && !h3.dataset.court) {
      h3.dataset.court = "1";
      h3.title = h3.textContent.trim();
      h3.textContent = "Essais";
    }
  }

  /* « Ce que coûte la pièce » répétait la Réponse dans un second bandeau : il entre
     DANS la carte Réponse, en pied, sur une ligne. */
  function equiperReponse() {
    const strip = document.getElementById("tabsStrip");
    if (!strip) return;
    const hero = strip.querySelector(".hero");
    const pcb = strip.querySelector(":scope > .pcb-banner, :scope > .pcb-vide");
    if (hero && pcb) {
      pcb.classList.add("pcb-dans-reponse");
      hero.appendChild(pcb);
    }
  }

  /* un défilement programmé vers un élément d'un onglet masqué (recherche, verdict,
     lien « voir l'essai ») ouvre d'abord le bon onglet */
  const scrollNatif = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function () {
    try {
      const sec = this.closest && this.closest("[data-dans-onglet]");
      if (sec) {
        const sc = sec.closest(".scenario");
        const id = sec.getAttribute("data-dans-onglet");
        if (sc && sc.getAttribute("data-onglet") !== id) poserOnglet(sc, id);
      }
    } catch (e) { /* jamais bloquant */ }
    return scrollNatif.apply(this, arguments);
  };
  /* idem au focus clavier (Tab, Ctrl+K) */
  document.addEventListener("focusin", (e) => {
    const sec = e.target && e.target.closest ? e.target.closest("[data-dans-onglet]") : null;
    if (!sec) return;
    const sc = sec.closest(".scenario");
    const id = sec.getAttribute("data-dans-onglet");
    if (sc && sc.getAttribute("data-onglet") !== id) poserOnglet(sc, id);
  });
  /* « Continuer les essais » de la Réponse mène à l'onglet Essais */
  document.addEventListener("click", (e) => {
    if (e.target && e.target.closest && e.target.closest("#heroCta")) ongletFiche = "essais";
  }, true);

  (function () {
    const detail = document.getElementById("scenarioDetail");
    const strip = document.getElementById("tabsStrip");
    if (window.MutationObserver) {
      if (detail) new MutationObserver(equiperFiche).observe(detail, { childList: true });
      if (strip) new MutationObserver(equiperReponse).observe(strip, { childList: true });
    }
    equiperFiche();
    equiperReponse();
  })();

  /* ══ v4.135 — L'ESSENTIEL PAR DÉFAUT, LE RESTE À UN CLIC ══════════════════════════
     Mesuré le 01/11 : 253 mots et 22 commandes sur le premier écran, 64 commandes
     dans la fiche, 40 dans un essai ouvert. Chaque version avait ajouté ses
     explications, aucune n'en avait retiré. L'outil s'ouvre maintenant en
     « Essentiel » : le chiffre, le verdict, le geste suivant. Le bouton « Détails »
     du bandeau rend TOUT visible (mémorisé sur ce poste). Rien n'est supprimé du
     calcul ; le simulateur de prix seul quitte l'interface (décision Benjamin). */
  const CLE_DETAILS = "spk-details";
  let details = false;
  try { details = localStorage.getItem(CLE_DETAILS) === "1"; } catch (e) { /* stockage indisponible */ }
  document.body.classList.toggle("spk-details", details);
  (function () {
    const bar = document.getElementById("spkHdActions");
    if (!bar) return;
    const b = document.createElement("button");
    b.type = "button";
    b.id = "spkDetailsBtn";
    b.className = "ghost spk-details-btn";
    const poser = () => {
      b.setAttribute("aria-pressed", details ? "true" : "false");
      b.textContent = details ? "Essentiel" : "Détails";
      b.title = details ? "Revenir à l'essentiel : le chiffre, le verdict, le geste suivant"
                        : "Tout afficher : explications, compteurs, outils secondaires";
    };
    poser();
    b.addEventListener("click", () => {
      details = !details;
      document.body.classList.toggle("spk-details", details);
      try { localStorage.setItem(CLE_DETAILS, details ? "1" : "0"); } catch (e) { /* stockage indisponible */ }
      poser();
    });
    /* sur la ligne fine (fil d'Ariane), à droite : le bandeau bleu est déjà plein
       sur téléphone */
    const ctx = document.getElementById("spkCtx");
    if (ctx) ctx.appendChild(b); else bar.appendChild(b);
  })();

  /* Le menu « Outils » du rail : ce qui était éparpillé (9 boutons au pied de la Vue
     d'ensemble, « Livraisons » et « Carte atelier » dans la fiche, la campagne et le
     tableau dans •••) au même endroit. Chaque entrée appelle l'ouvreur EXISTANT, après
     avoir refermé l'écran en cours (les écrans restent exclusifs). */
  (function () {
    const OUTILS = [
      { lib: "Carte atelier", sous: "chaque machine, son état, sa fiche", f: () => window.ouvrirCarte && window.ouvrirCarte() },
      { lib: "Livraisons", sous: "figer les gains du jour dans un document daté", f: () => {
          if (window.ouvrirCarte) window.ouvrirCarte();
          setTimeout(() => { const bl = document.querySelector("#cartePanel .lv-bloc"); if (bl) bl.scrollIntoView({ behavior: "smooth", block: "start" }); }, 60);
        } },
      { lib: "La campagne", sous: "essais, validations, passages en série — sur une timeline", f: () => { const x = document.getElementById("campagneBtn"); if (x) x.click(); } },
      { lib: "Tableau de bord", sous: "les chiffres de toutes les lignes", f: () => { const x = document.getElementById("dashboardBtn"); if (x) x.click(); } },
      { lib: "Vue CPP", sous: "le coût pièce obtenu vs la référence, OP par OP", f: () => window.ouvrirVueCpp && window.ouvrirVueCpp() },
      { lib: "Catalogue", sous: "un MABEC = un prix ; import / export CSV", f: () => window.ouvrirCatalogue && window.ouvrirCatalogue() },
      { lib: "Plan de conversion", sous: "article par article, la cible et le gain", f: () => window.ouvrirPlan && window.ouvrirPlan() },
      { lib: "Dossier de visite", sous: "ce qui s'est passé depuis la dernière visite", f: () => window.ouvrirVisite && window.ouvrirVisite() }
    ];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.id = "spkOutilsBtn";
    btn.className = "ghost";
    btn.setAttribute("aria-haspopup", "true");
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-label", "Outils");
    btn.title = "Outils";
    btn.innerHTML = '<svg class="icon" viewBox="0 0 18 18" aria-hidden="true"><rect x="2.5" y="2.5" width="5" height="5" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="10.5" y="2.5" width="5" height="5" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="2.5" y="10.5" width="5" height="5" rx="1" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M13 10.5v5M10.5 13h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>Outils';
    nav.appendChild(btn);
    const pop = document.createElement("div");
    pop.className = "spk-outils";
    pop.id = "spkOutils";
    pop.hidden = true;
    pop.setAttribute("role", "menu");
    pop.innerHTML = '<div class="spk-outils-t">Outils</div>';
    OUTILS.forEach((o) => {
      const it = document.createElement("button");
      it.type = "button";
      it.setAttribute("role", "menuitem");
      it.innerHTML = "<b></b><span></span>";
      it.querySelector("b").textContent = o.lib;
      it.querySelector("span").textContent = o.sous;
      it.addEventListener("click", () => {
        fermerOutils();
        if (typeof window.fermerPanneaux === "function") window.fermerPanneaux();
        try { o.f(); } catch (e) { /* l'ouvreur dit lui-même ce qui manque */ }
      });
      pop.appendChild(it);
    });
    document.body.appendChild(pop);
    function fermerOutils() { pop.hidden = true; btn.setAttribute("aria-expanded", "false"); }
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const ouvrir = pop.hidden;
      pop.hidden = !ouvrir;
      btn.setAttribute("aria-expanded", ouvrir ? "true" : "false");
      if (ouvrir && window.matchMedia("(min-width:901px)").matches) {
        const r = btn.getBoundingClientRect();
        pop.style.left = (r.right + 8) + "px";
        pop.style.top = Math.max(8, Math.min(r.top, window.innerHeight - pop.offsetHeight - 8)) + "px";
      } else { pop.style.left = ""; pop.style.top = ""; }
    }, true);
    document.addEventListener("click", (e) => { if (!pop.hidden && !pop.contains(e.target) && e.target !== btn) fermerOutils(); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !pop.hidden) fermerOutils(); });
  })();

  /* La fiche, en Essentiel : l'en-tête garde le nom et le statut, les gestes rares
     (définir comme référence, dupliquer, supprimer) passent dans un menu « ⋯ » ; les
     précisions (durée de vie, €/arête, temps de cycle) rejoignent l'onglet Composition ;
     les phrases sous les chiffres deviennent l'infobulle de leur tuile. Un essai ouvert
     garde « + Ajouter un prélèvement » et son tableau ; le reste est derrière « ⋯ Plus ». */
  function epurerFiche() {
    const sc = document.querySelector("#scenarioDetail > .scenario");
    if (!sc || sc.dataset.epure) return;
    sc.dataset.epure = "1";
    const head = sc.querySelector(":scope > .scenario-head");
    if (head) {
      const actions = head.querySelector(".sc-actions");
      const pill = head.querySelector(".baseline-pill:not(.active)");
      if (actions || pill) {
        const m = document.createElement("details");
        m.className = "spk-plus-menu";
        m.innerHTML = '<summary aria-label="Autres actions" title="Autres actions">⋯</summary><div class="spk-plus-corps"></div>';
        const corps = m.querySelector(".spk-plus-corps");
        if (pill) corps.appendChild(pill);
        if (actions) [...actions.children].forEach((c) => corps.appendChild(c));
        const navSc = head.querySelector(".spk-sc-nav");
        head.insertBefore(m, navSc || null);
        document.addEventListener("click", (e) => { if (m.open && !m.contains(e.target)) m.open = false; });
      }
    }
    const second = sc.querySelector(":scope > .scenario-foot > .foot-second");
    const compo = sc.querySelector(":scope > .sec-plaquettes");
    if (second && compo) { second.classList.add("spk-precisions"); compo.insertBefore(second, compo.firstChild); }
    sc.querySelectorAll(":scope > .scenario-foot > .foot-cell").forEach((cell) => {
      const subs = [...cell.querySelectorAll(".foot-sub")].map((s) => s.textContent.trim()).filter(Boolean);
      if (subs.length && !cell.title) cell.title = subs.join("\n");
    });
    sc.querySelectorAll(".essai-card .essai-body").forEach((body) => {
      if (body.querySelector(".spk-essai-plus")) return;
      const add = body.querySelector(".prel-add");
      if (!add) return;
      const b = document.createElement("button");
      b.type = "button";
      b.className = "ghost spk-essai-plus";
      b.textContent = "⋯ Plus";
      b.title = "Mode gants, comparer, rapport, photos, Marposs, contexte";
      b.addEventListener("click", () => {
        const on = body.classList.toggle("spk-plus");
        b.textContent = on ? "Moins" : "⋯ Plus";
      });
      add.after(b);
    });
  }

  /* La Vue d'ensemble, en Essentiel : la grande table des opérations derrière un lien,
     les outils du pied dans le menu Outils. */
  function epurerAccueil() {
    const p = document.getElementById("accueilPanel");
    if (!p || p.querySelector(".spk-mx-lien")) return;
    const t = p.querySelector(".mx-titre");
    if (!t) return;
    const l = document.createElement("button");
    l.type = "button";
    l.className = "ghost spk-mx-lien";
    const poser = () => { l.textContent = p.classList.contains("spk-mx-on") ? "Masquer le tableau des opérations" : "Voir le tableau des opérations"; };
    poser();
    l.addEventListener("click", () => { p.classList.toggle("spk-mx-on"); poser(); });
    t.parentNode.insertBefore(l, t);
  }
  /* la Réponse : « Ce que coûte la pièce » n'apporte rien de plus qu'elle tant que la
     référence n'a qu'une OP */
  function marquerPcb() {
    const hero = document.querySelector("#tabsStrip .hero");
    if (hero) hero.classList.toggle("pcb-multi", document.querySelectorAll("#tabsStrip .pcb-op").length > 1);
  }
  (function () {
    const detail = document.getElementById("scenarioDetail");
    const strip = document.getElementById("tabsStrip");
    const acc = document.getElementById("accueilPanel");
    if (window.MutationObserver) {
      if (detail) new MutationObserver(epurerFiche).observe(detail, { childList: true });
      if (strip) new MutationObserver(marquerPcb).observe(strip, { childList: true });
      if (acc) new MutationObserver(epurerAccueil).observe(acc, { childList: true });
    }
    epurerFiche(); marquerPcb(); epurerAccueil();
  })();

  /* ══ v4.136 — VENDRE : présentation client, bilan PDF ══════════════════
     Le MODE PRÉSENTATION CLIENT se projette chez le client sans risque : lecture
     seule (le verrou existant), et tout ce qui est commercial s'efface —
     plan de conversion, catalogue, dossier de visite, prix unitaires des plaquettes,
     menus d'export et d'options. Il reste les PREUVES : réponse, gains, essais,
     courbes, bilan PDF. Il vit le temps de la session (jamais rouvert par surprise). */
  const CLE_CLIENT = "spk-client";
  function marquerPrix() {
    document.querySelectorAll("#scenarioDetail .ap-l, #scenarioDetail .fs-l").forEach((l) => {
      const t = l.textContent.trim().toLowerCase();
      if (t === "plaquette" || t.indexOf("€ / arête") === 0) l.parentElement.classList.add("spk-prix");
    });
  }
  function poserClient(on, depuisSession) {
    document.body.classList.toggle("spk-client", on);
    let etat = null;
    try { etat = JSON.parse(sessionStorage.getItem(CLE_CLIENT) || "null"); } catch (e) { /* rien */ }
    if (on && !depuisSession) {
      const dejaVerrou = typeof lectureSeule !== "undefined" && lectureSeule;
      try { sessionStorage.setItem(CLE_CLIENT, JSON.stringify({ verrouAvant: dejaVerrou })); } catch (e) { /* rien */ }
      if (!dejaVerrou && typeof window.toggleLock === "function") window.toggleLock();
    }
    if (!on) {
      try { sessionStorage.removeItem(CLE_CLIENT); } catch (e) { /* rien */ }
      if (etat && !etat.verrouAvant && typeof lectureSeule !== "undefined" && lectureSeule && typeof window.toggleLock === "function") window.toggleLock();
    }
    puce.hidden = !on;
    marquerPrix();
  }
  const puce = document.createElement("div");
  puce.className = "spk-client-puce";
  puce.hidden = true;
  puce.innerHTML = '<span class="spk-client-l">Présentation client · lecture seule</span>'
    + '<button type="button" class="spk-client-pdf">Bilan PDF</button>'
    + '<button type="button" class="spk-client-quitter">Quitter</button>';
  document.body.appendChild(puce);
  puce.querySelector(".spk-client-pdf").addEventListener("click", () => { if (typeof window.imprimerBilanClient === "function") window.imprimerBilanClient(); });
  puce.querySelector(".spk-client-quitter").addEventListener("click", () => poserClient(false));

  /* les nouvelles entrées du menu Outils : en tête, le bilan ; en pied, la bascule de présentation.
     Les entrées commerciales portent data-commercial. (v4.142 : l'écran « Pipeline » est retiré — l'outil
     suit des essais, il ne tient pas un carnet de commandes.) */
  (function () {
    const pop = document.getElementById("spkOutils");
    if (!pop) return;
    const titre = pop.querySelector(".spk-outils-t");
    const fermer = () => { pop.hidden = true; const b = document.getElementById("spkOutilsBtn"); if (b) b.setAttribute("aria-expanded", "false"); };
    const entree = (lib, sous, f, commercial) => {
      const it = document.createElement("button");
      it.type = "button";
      it.setAttribute("role", "menuitem");
      it.innerHTML = "<b></b><span></span>";
      it.querySelector("b").textContent = lib;
      it.querySelector("span").textContent = sous;
      if (commercial) it.setAttribute("data-commercial", "1");
      it.addEventListener("click", () => { fermer(); f(); });
      return it;
    };
    const bilanIt = entree("Bilan client (PDF)", "une page par ligne : avant/après, preuves, gain figé", () => {
      if (typeof window.imprimerBilanClient === "function") window.imprimerBilanClient();
    }, false);
    titre.after(bilanIt);
    [...pop.querySelectorAll("button")].forEach((b) => {
      const lib = (b.querySelector("b") || {}).textContent || "";
      if (/^(Plan de conversion|Catalogue|Dossier de visite)$/.test(lib)) b.setAttribute("data-commercial", "1");
    });
    const sep = document.createElement("div");
    sep.className = "spk-outils-sep";
    pop.appendChild(sep);
    const clientIt = entree("Mode présentation client", "lecture seule, rien de commercial à l'écran", () => poserClient(!document.body.classList.contains("spk-client")), false);
    clientIt.id = "spkClientBtn";
    pop.appendChild(clientIt);
    new MutationObserver(() => {
      const on = document.body.classList.contains("spk-client");
      clientIt.querySelector("b").textContent = on ? "Quitter la présentation client" : "Mode présentation client";
    }).observe(document.body, { attributes: true, attributeFilter: ["class"] });
  })();
  /* le bilan aussi dans Transmettre */
  (function () {
    const menu = document.getElementById("transmettreMore");
    if (!menu || menu.querySelector(".spk-bilan-tm")) return;
    const b = document.createElement("button");
    b.type = "button";
    b.className = "ghost spk-bilan-tm";
    b.innerHTML = '<svg class="icon" viewBox="0 0 18 18" aria-hidden="true"><path d="M5 2.5h6l3 3v10H5z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M7.5 9h4M7.5 12h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>Bilan client (PDF)';
    b.addEventListener("click", () => { if (typeof window.imprimerBilanClient === "function") window.imprimerBilanClient(); });
    const premier = menu.querySelector("button");
    if (premier) premier.parentNode.insertBefore(b, premier); else menu.appendChild(b);
  })();
  /* après chaque rendu de la fiche : les prix se re-marquent */
  (function () {
    const detail = document.getElementById("scenarioDetail");
    if (detail && window.MutationObserver) new MutationObserver(marquerPrix).observe(detail, { childList: true });
    let etat = null;
    try { etat = JSON.parse(sessionStorage.getItem(CLE_CLIENT) || "null"); } catch (e) { /* rien */ }
    if (etat) poserClient(true, true);
  })();

  const panelToButton = {
    accueilPanel: "accueilBtn",
    dashboardPanel: "accueilBtn",
    cartePanel: "accueilBtn",
    matisPanel: "matisBtn",
    matisDetailPanel: "matisBtn",
    /* v4.100.4 — la Synthèse est un écran du rail à part entière (elle
       n'emprunte pas ouvrirPanneau : c'est le bloc en flux de l'app d'avant
       la coque). Sans cette entrée, cliquer Synthèse ne marque jamais
       l'onglet actif. */
    syntheseWrap: "syntheseBtn",
    planPanel: "accueilBtn",
    simulPanel: "accueilBtn",
    cataloguePanel: "accueilBtn",
    comparePanel: "accueilBtn",
    historiquePanel: "accueilBtn"
  };

  /* v4.100.4 — Les écrans du rail sont EXCLUSIFS : en ouvrir un referme les
     autres. Constat du 21/10 (Benjamin : « les onglets tableau et synthese ne
     fonctionnent pas ») : chaque surface s'empilait sur la précédente — et la
     Synthèse, bloc en flux de l'app d'avant la coque (aucun z-index), passait
     SOUS l'Accueil ou le Tableau de bord restés ouverts (z 80). Mesuré :
     Accueil ouvert -> clic Synthèse -> l'écran reste sur l'accueil ; le
     panneau s'ouvre bel et bien, mais DERRIÈRE. Cinq écrans qui se
     recouvrent ne sont pas une navigation, c'est un tas. On referme donc les
     surfaces voisines AVANT que le handler de l'app n'ouvre (ou ne bascule)
     la surface cliquée — en phase de capture, pour ne pas réécrire la
     logique de l'application. */
  const SURFACES_DU_BOUTON = {
    /* v4.122 acte II : fusion — le bouton unique possede les trois surfaces */
    accueilBtn: ["accueilPanel", "cartePanel", "dashboardPanel"],
    syntheseBtn: ["syntheseWrap"],
    matisBtn: ["matisPanel", "matisDetailPanel"]
  };
  /* v4.104 — les panneaux DÉRIVÉS de l'Accueil (Plan, Simulateur, Catalogue,
     Comparaison, Historique, Backlog) ne sont pas des destinations du rail,
     mais ce sont des espaces de travail : s'ils restent ouverts, ils
     RECOUVRENT l'écran du rail cliqué (même z-index, plus tard dans le DOM).
     Constat Benjamin 22/10 : « l'onglet tableau ne s'affiche plus quand on
     clique dessus » après être passé par le Plan de conversion. Fermés à
     chaque changement d'écran du rail. */
  const SURFACES_SECONDAIRES = ["planPanel", "simulPanel", "cataloguePanel", "comparePanel", "historiquePanel", "backlogWrap"];
  const TOUTES_SURFACES = [];
  Object.keys(SURFACES_DU_BOUTON).forEach((b) => {
    SURFACES_DU_BOUTON[b].forEach((id) => {
      if (TOUTES_SURFACES.indexOf(id) === -1) TOUTES_SURFACES.push(id);
    });
  });

  nav.addEventListener("click", (e) => {
    const btn = e.target && e.target.closest ? e.target.closest("button") : null;
    if (!btn) return;
    const siennes = SURFACES_DU_BOUTON[btn.id] || [];
    TOUTES_SURFACES.concat(SURFACES_SECONDAIRES).forEach((id) => {
      if (siennes.indexOf(id) !== -1) return;
      const pan = document.getElementById(id);
      if (pan && !pan.hidden) pan.hidden = true;
    });
  }, true); /* capture : passer AVANT le handler de l'application */

  /* La Synthèse ne passe pas par ouvrirPanneau : son onglet actif est posé
     ici, après coup, d'après la surface réellement visible. */
  nav.addEventListener("click", () => {
    requestAnimationFrame(() => {
      clearActive();
      const visible = TOUTES_SURFACES.find((id) => {
        const pan = document.getElementById(id);
        return pan && !pan.hidden;
      });
      if (!visible) return;
      const btnId = panelToButton[visible];
      const btn = btnId && document.getElementById(btnId);
      if (btn) btn.classList.add("is-active");
      /* La Synthèse vit dans le flux de la page : on la montre depuis le
         haut, sinon on atterrit au milieu du défilement d'avant. */
      if (visible === "syntheseWrap") {
        try { window.scrollTo({ top: 0, behavior: "instant" }); } catch (e) { window.scrollTo(0, 0); }
      }
    });
  });

  function clearActive() {
    nav.querySelectorAll("button").forEach((b) => b.classList.remove("is-active"));
  }

  function markActive(panelId) {
    clearActive();
    const btnId = panelToButton[panelId];
    if (!btnId) return;
    const btn = document.getElementById(btnId);
    if (btn) btn.classList.add("is-active");
  }

  const close = document.createElement("button");
  close.type = "button";
  close.id = "spkWorkspaceClose";
  close.className = "spk-workspace-close";
  close.hidden = true;
  close.innerHTML = '<span aria-hidden="true">←</span> Retour';
  close.setAttribute("aria-label", "Fermer l’espace de travail");
  close.addEventListener("click", () => {
    if (typeof window.fermerPanneaux === "function") window.fermerPanneaux();
  });
  document.body.appendChild(close);

  function workspaceOpen() {
    /* v4.100.4 — #syntheseWrap compte comme un espace ouvert : c'est un écran
       du rail, il doit afficher Retour et replier la poignée comme les
       autres. */
    return !!document.querySelector(".panel-large:not([hidden]), #backlogWrap:not([hidden]), #syntheseWrap:not([hidden])");
  }

  /* Un dialogue (ou la recherche) se pose PAR-DESSUS un espace de travail :
     il ne le remplace pas. Il faut donc le distinguer d'un petit panneau qui,
     lui, remplace vraiment l'espace (Options, Import, Nouveau projet...).

     AVANT, on comptait tout `.panel` non-`panel-large` visible. Conséquence :
     la lecture d'un classeur (qui ouvre un dialogue) faisait disparaitre le
     bouton Retour au milieu du Plan de conversion, et le rail redevenait
     « non repliable » alors que le Plan etait toujours ouvert. Mesure :
     Plan ouvert -> retour visible ; Plan + dialogue -> retour disparu ;
     dialogue ferme -> retour revenu.

     On ne garde donc que les petits panneaux qui sont de VRAIS panneaux
     (pas les surcouches). */
  const SURCOUCHES = ["dialogPanel", "searchPanel", "photoAnnotWrap"];
  function petitPanneauAuPremierPlan() {
    /* Tous les petits panneaux visibles, pas seulement le premier : un
       surcouche (dialogue) peut preceder dans le document un vrai panneau
       (Options, Import...), et le dialogue ne doit pas le masquer. */
    const petits = document.querySelectorAll(
      ".panel:not(.panel-large):not(#backlogWrap):not([hidden])"
    );
    for (let i = 0; i < petits.length; i++) {
      if (SURCOUCHES.indexOf(petits[i].id) === -1) return true;
    }
    return false;
  }

  function syncWorkspace() {
    const smallOpen = petitPanneauAuPremierPlan();
    const open = workspaceOpen() && !smallOpen;
    const shouldHide = !open;
    if (close.hidden !== shouldHide) close.hidden = shouldHide;
    if (document.body.classList.contains("spk-workspace-open") !== open) {
      document.body.classList.toggle("spk-workspace-open", open);
    }
    if (!open) clearActive();
  }

  const workspaceTitles = {
    matisPanel: "Réel vs budget — classeur Matis",
    matisDetailPanel: "Détail du classeur",
    backlogWrap: "Backlog atelier"
  };

  function ensureWorkspaceTitle(panel) {
    if (!panel || (!panel.classList.contains("panel-large") && panel.id !== "backlogWrap")) return;
    if (panel.querySelector("h3")) return;
    const title = workspaceTitles[panel.id];
    if (!title) return;
    const h3 = document.createElement("h3");
    h3.textContent = title;
    panel.prepend(h3);
  }

  document.querySelectorAll(".panel-large, #backlogWrap").forEach((panel) => {
    ensureWorkspaceTitle(panel);
    const titleObserver = new MutationObserver(() => ensureWorkspaceTitle(panel));
    titleObserver.observe(panel, { childList: true });
  });

  // Les fonctions sont globales dans l'application 4.97 : on les enveloppe
  // sans réécrire la logique d'ouverture, de focus ou de fermeture.
  if (typeof window.ouvrirPanneau === "function") {
    const openPanel = window.ouvrirPanneau;
    window.ouvrirPanneau = function (id) {
      openPanel(id);
      const pan = document.getElementById(id);
      if (pan) pan.scrollTop = 0;
      markActive(id);
      requestAnimationFrame(syncWorkspace);
    };
  }

  if (typeof window.fermerPanneaux === "function") {
    const closePanels = window.fermerPanneaux;
    window.fermerPanneaux = function () {
      closePanels();
      /* v4.100.4 — la Synthèse n'est pas un .panel : fermerPanneaux de l'app
         ne la voit pas. Sans ça, Retour depuis la Synthèse ne fermait rien. */
      const synthese = document.getElementById("syntheseWrap");
      if (synthese) synthese.hidden = true;
      clearActive();
      requestAnimationFrame(syncWorkspace);
    };
  }

  const observer = new MutationObserver(syncWorkspace);
  observer.observe(document.body, {
    subtree: true,
    attributes: true,
    attributeFilter: ["hidden"]
  });

  syncWorkspace();
})();

/* v4.139 — NOMS ACCESSIBLES. Mesuré en PROD : 75 commandes sans nom pour un lecteur d'écran (cellules de tableaux
   de prélèvements, boutons de suppression, statut, tolérance…). Un nom se déduit : règles connues, sinon
   l'en-tête de la colonne (+ la 1re cellule de la ligne), sinon le nom du champ. Passe légère, différée, sur
   chaque rendu ; ne touche jamais un contrôle qui a déjà un nom. */
(function nommerControles(){
  const CONNUS = [
    [".log-del", "Supprimer cette ligne"], [".sc-name", "Nom du scénario"], [".statut-select", "Statut du scénario"],
    [".limit-label", "Libellé de la grandeur suivie"], [".limit-value", "Tolérance"], [".params-sync", "Synchroniser les paramètres"]
  ];
  const lisible = (s) => String(s || "").replace(/([a-z])([A-Z])/g, "$1 $2").replace(/[-_]/g, " ").trim();
  const propre = (t) => String(t || "").trim().replace(/\s+/g, " ");
  function nom(el){
    for (const [sel, n] of CONNUS) if (el.matches(sel)) return n;
    const cell = el.closest("td,th");
    if (cell && cell.closest("table")) {
      const tr = cell.parentElement, table = cell.closest("table");
      const th = table.tHead && table.tHead.rows[0] ? table.tHead.rows[0].cells[cell.cellIndex] : null;
      const tete = th ? propre(th.innerText) : "";
      const premiere = tr.cells[0] && tr.cells[0] !== cell ? propre(tr.cells[0].innerText).slice(0, 24) : "";
      if (tete) return premiere ? tete + " — " + premiere : tete;
    }
    const champ = el.getAttribute("data-field") || el.getAttribute("data-marposs-field") || "";
    return champ ? lisible(champ) : "";
  }
  function passer(){
    document.querySelectorAll("button:not([aria-label]):not([title]), input:not([aria-label]):not([title]):not([type=hidden]):not([type=file]), select:not([aria-label]):not([title]), textarea:not([aria-label]):not([title])").forEach((el) => {
      if (el.tagName === "BUTTON" && propre(el.innerText)) return;
      if (el.placeholder || el.getAttribute("aria-labelledby") || el.closest("label")) return;
      if (el.id && document.querySelector('label[for="' + el.id + '"]')) return;
      const n = nom(el);
      if (n) el.setAttribute("aria-label", n);
    });
  }
  let t = null;
  const planifier = () => { clearTimeout(t); t = setTimeout(passer, 400); };
  try { new MutationObserver(planifier).observe(document.body, { childList: true, subtree: true }); } catch (e) { /* ancien navigateur */ }
  planifier();
})();

/* v4.140 — ÉCRAN TACTILE. (1) Safari (iPhone, iPad) zoome la page au focus d'un champ dont la police fait moins de
   16 px : mesuré, 94 champs sur 155 étaient dans ce cas. On monte à 16 px ceux-là seulement (jamais un champ plus
   grand : l'écran Atelier garde ses gros chiffres), après chaque rendu. (2) iOS efface les données d'un site non
   ouvert pendant 7 jours, sauf s'il est ajouté à l'écran d'accueil : on le demande au navigateur (persist) et on
   le rappelle une fois toutes les deux semaines. */
(function ecranTactile(){
  const coarse = (() => { try { return matchMedia("(pointer: coarse)").matches; } catch (e) { return false; } })();
  if (coarse) {
    let t = null;
    const agrandir = () => {
      document.querySelectorAll("input:not([type=checkbox]):not([type=radio]):not([type=range]):not([type=file]):not([type=color]):not([type=hidden]), select, textarea").forEach((el) => {
        if (el.dataset.f16) return;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs && fs < 16) { el.style.fontSize = "16px"; }
        el.dataset.f16 = "1";
      });
    };
    const planifier = () => { clearTimeout(t); t = setTimeout(agrandir, 120); };
    try { new MutationObserver(planifier).observe(document.body, { childList: true, subtree: true }); } catch (e) { /* ancien navigateur */ }
    planifier();
  }
  const ua = navigator.userAgent || "";
  const ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  if (!ios) return;
  try { if (navigator.storage && navigator.storage.persist) navigator.storage.persist(); } catch (e) { /* refusé : sans suite */ }
  const autonome = window.navigator.standalone === true || (window.matchMedia && matchMedia("(display-mode: standalone)").matches);
  if (autonome) return;
  const CLE = "spk_conseil_ios";
  let vu = 0;
  try { vu = parseInt(localStorage.getItem(CLE) || "0", 10) || 0; } catch (e) { /* stockage indisponible */ }
  if (Date.now() - vu < 14 * 86400000) return;
  const b = document.createElement("div");
  b.className = "spk-conseil-ios";
  b.setAttribute("role", "status");
  b.innerHTML = "<span><b>iPhone / iPad :</b> Safari efface les données d’un site qu’on n’ouvre pas pendant 7 jours. Pour les garder : <b>Partager ▸ Sur l’écran d’accueil</b>, puis ouvrez l’outil depuis cette icône. Pensez aussi à exporter régulièrement.</span><button type=\"button\">Compris</button>";
  b.querySelector("button").addEventListener("click", () => { b.remove(); try { localStorage.setItem(CLE, String(Date.now())); } catch (e) { /* tant pis */ } });
  document.body.appendChild(b);
})();
