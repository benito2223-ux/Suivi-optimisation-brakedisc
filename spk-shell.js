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
    '<div class="spk-rail-foot">',
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
    dashboardPanel: "dashboardBtn",
    cartePanel: "carteBtn",
    matisPanel: "matisBtn",
    matisDetailPanel: "matisBtn",
    planPanel: "accueilBtn",
    simulPanel: "accueilBtn",
    cataloguePanel: "accueilBtn",
    comparePanel: "accueilBtn",
    historiquePanel: "accueilBtn"
  };

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
    return !!document.querySelector(".panel-large:not([hidden]), #backlogWrap:not([hidden])");
  }

  function syncWorkspace() {
    const smallOpen = !!document.querySelector(".panel:not(.panel-large):not(#backlogWrap):not([hidden])");
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
