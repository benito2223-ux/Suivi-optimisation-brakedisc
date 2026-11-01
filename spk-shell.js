/* SPK — coque de navigation et surfaces de travail.
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

  rail.innerHTML = [
    '<div class="spk-rail-head">',
    '  <div class="spk-rail-mark">SPK<span>by CeramTec</span></div>',
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
