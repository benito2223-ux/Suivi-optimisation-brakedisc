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
    matisPanel: "Classeur Matis",
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
