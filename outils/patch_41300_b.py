# -*- coding: utf-8 -*-
# Tour 109 — 4.130.0 — patch B : la coque (spk-shell.js)
# Le rail vertical devient l'en-tête du design system (UN remplacement qui
# couvre toute l'ancienne construction : préférence de repli, rail, logo,
# version, poignée) :
#   rangée 1 (barre navy fixe) : mark SPK + titre de la référence (le h1 du
#   bandeau .hd, DÉPLACÉ) + actions à droite (Rechercher câblé sur la
#   recherche existante, Transmettre avec son menu, verrou, mode, •••) ;
#   rangée 2 : navigation à onglets soulignés (la nav existante, déplacée) +
#   fil d'Ariane (déplacé) + « + Scénario » (sort de la barre) ;
#   le bandeau projets (« + Créer un projet » + ⓘ) suit dans la rangée 2 —
#   conteneur et rendu JS inchangés ;
#   « Données locales » et la version descendent dans le pied de page.
# Toute la logique d'exclusivité, de marquage et d'espaces de travail est
# conservée : elle opère sur les boutons et les panneaux, pas sur le rail.
import io

F = "spk-shell.js"
src = io.open(F, encoding="utf-8").read()

DEBUT = """  // Préférence de repli lue AVANT toute création : appliquée sans animation.
  let railFermé = false;
  try { railFermé = localStorage.getItem("spk-rail-closed") === "1"; } catch (e) { /* stockage indisponible */ }
  if (railFermé) {
    document.documentElement.classList.add("spk-boot");
    document.body.classList.add("spk-rail-off");
  }
"""
FIN = """  document.body.appendChild(toggle);
  syncRailToggle();
"""
i = src.find(DEBUT)
j = src.find(FIN)
assert i != -1 and j != -1 and i < j, "bornes de la construction du rail introuvables"

NOUVEAU = """  /* v4.130 — l'en-tête du design system remplace le rail : une barre fixe
     de deux rangées. La logique (exclusivité des écrans, marquage de
     l'onglet actif, espaces de travail) opère sur les boutons et les
     panneaux : rien d'elle ne change. */
  const head = document.createElement("header");
  head.className = "spk-head";
  head.setAttribute("aria-label", "En-tête");

  const r1 = document.createElement("div");
  r1.className = "spk-head-r1";
  r1.innerHTML = [
    '<div class="spk-head-mark">SPK<span>by CeramTec</span></div>',
    '<div class="spk-head-titre" id="spkHeadTitre"></div>',
    '<div class="spk-head-actions" id="spkHeadActions"></div>'
  ].join("");

  const r2 = document.createElement("div");
  r2.className = "spk-head-r2";
  r2.innerHTML = '<div class="spk-head-onglets" id="spkHeadOnglets"></div>'
    + '<div class="spk-head-contexte" id="spkHeadContexte"></div>';

  head.appendChild(r1);
  head.appendChild(r2);
  document.body.prepend(head);
  document.body.classList.add("spk-has-head");

  /* le titre de la référence vit déjà dans le bandeau du monolithe
     (hdTitle, mis à jour par l'app) : on le DÉPLACE dans la barre — les
     références du rendu restent valides, le h1 continue de se mettre à
     jour. Le bandeau bleu .hd, sans titre, est masqué par la feuille. */
  const hdTitle = document.getElementById("hdTitle");
  if (hdTitle) r1.querySelector(".spk-head-titre").appendChild(hdTitle);

  /* les actions : la recherche existante (Ctrl+K), Transmettre avec son
     menu, le verrou, le mode, le menu •••. On déplace les éléments — ids,
     handlers et gardes de verrouillage (body.locked) suivent. */
  const actions = r1.querySelector(".spk-head-actions");
  const btnRecherche = document.createElement("button");
  btnRecherche.type = "button";
  btnRecherche.className = "ghost spk-head-btn";
  btnRecherche.id = "spkRechercheBtn";
  btnRecherche.setAttribute("aria-label", "Rechercher (Ctrl+K)");
  btnRecherche.title = "Rechercher (Ctrl+K)";
  btnRecherche.innerHTML = '<svg class="icon" viewBox="0 0 18 18" aria-hidden="true"><circle cx="8" cy="8" r="4.5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="m11.5 11.5 3 3" stroke-linecap="round"/></svg><span class="label-tb">Rechercher</span>';
  btnRecherche.addEventListener("click", () => {
    if (typeof window.ouvrirRecherche === "function") window.ouvrirRecherche();
  });
  actions.appendChild(btnRecherche);
  ["transmettreWrap", "lockBtn", "modeBtn", "moreBtn", "saveStatus"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) actions.appendChild(el);
  });

  /* rangée 2 : la navigation à onglets (déplacée telle quelle), puis le
     fil d'Ariane et « + Scénario » — la zone de travail porte son bouton
     principal, la barre ne porte plus que la navigation. */
  const onglets = r2.querySelector(".spk-head-onglets");
  onglets.appendChild(nav);
  nav.classList.add("spk-head-links");
  const contexte = r2.querySelector(".spk-head-contexte");
  const fil = document.getElementById("filAriane");
  if (fil) contexte.appendChild(fil);
  const addBtn = document.getElementById("addBtn");
  if (addBtn) contexte.appendChild(addBtn);
  /* le bandeau projets (« + Créer un projet » + ⓘ, rendu par l'app dans
     son conteneur) quitte les rangées de tête : il suit dans la rangée 2,
     compacté par la feuille. Rendu et ids inchangés. */
  const pjBanner = document.getElementById("projetsBandeau");
  if (pjBanner) contexte.appendChild(pjBanner);

  /* le pied : « Données locales » et la version descendent du rail vers le
     pied de page existant (footCloud y vit déjà). */
  const foot = document.querySelector(".foot");
  if (foot) {
    const live = document.createElement("span");
    live.className = "foot-poids";
    live.innerHTML = '<i class="spk-live-puce"></i>Données locales';
    foot.insertBefore(live, foot.firstChild);
    try {
      if (typeof TOOL_VERSION === "string") {
        const ver = document.createElement("span");
        ver.className = "foot-poids";
        ver.textContent = "v" + TOOL_VERSION;
        foot.insertBefore(ver, foot.firstChild);
      }
    } catch (e) { /* pas de version connue */ }
  }

  // Le libellé reste accessible en lecture d'écran.
  nav.querySelectorAll("button").forEach((btn) => {
    const label = btn.textContent.replace(/\\s+/g, " ").trim();
    if (label) {
      btn.setAttribute("aria-label", label);
      btn.setAttribute("title", label);
    }
  });

  /* l'ancien verrou d'animation du boot : retiré après deux frames
     (filet de secours par timeout, comme avant). */
  const finBoot = () => document.documentElement.classList.remove("spk-boot");
  requestAnimationFrame(() => requestAnimationFrame(finBoot));
  setTimeout(finBoot, 300);
"""
src = src[:i] + NOUVEAU + src[j + len(FIN):]
print("ok  rail -> en-tête 2 rangées (construction complète remplacée)")

io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch B (4.130.0) appliqué.")
