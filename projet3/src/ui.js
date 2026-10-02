/* ============================================================================
   PROJET3 — LES COMPOSANTS
   Des briques DOM réutilisées partout : un badge n'a qu'une forme, un panneau
   n'a qu'un squelette. Le rendu lit le noyau, il ne calcule rien (cahier §5.1).
   ========================================================================== */

"use strict";

/* Le créateur d'éléments : h("div", {class: "x", onclick: fn}, enfant, …). */
function h(tag, attrs) {
  const el = document.createElement(tag);
  if (attrs) Object.keys(attrs).forEach(k => {
    const v = attrs[k];
    if (v === null || v === undefined || v === false) return;
    if (k === "class") el.className = v;
    else if (k === "html") el.innerHTML = v;      // uniquement du texte contrôlé par nous
    else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
    else if (k.slice(0, 2) === "on" && typeof v === "function") el.addEventListener(k.slice(2), v);
    else if (k === "value") el.value = v;
    else if (k === "checked") el.checked = !!v;
    else if (k === "selected") el.selected = !!v;
    else if (k === "disabled") el.disabled = !!v;
    else el.setAttribute(k, v === true ? "" : String(v));
  });
  for (let i = 2; i < arguments.length; i++) {
    const c = arguments[i];
    if (c === null || c === undefined || c === false) continue;
    if (Array.isArray(c)) c.forEach(x => { if (x !== null && x !== undefined && x !== false) el.appendChild(x); });
    else if (typeof c === "object" && c.nodeType) el.appendChild(c);
    else el.appendChild(document.createTextNode(String(c)));
  }
  return el;
}

/* UNE forme de badge : seule la couleur change (CDC UX §3.4). */
function badge(classe, texte, opts) {
  const o = opts || {};
  return h("span", { class: "badge " + (classe || ""), title: o.title || null }, texte);
}

/* L'état en toutes lettres — jamais la couleur seule (constitution §5.2).
   Les codes sont en ASCII, les libellés en français. */
const ETATS_POSTE = {
  gagne:     { badge: "vert",  mot: "gagné" },
  pret:      { badge: "ambre", mot: "décider" },
  essai:     { badge: "bleu",  mot: "essai en cours" },
  achiffrer: { badge: "ambre", mot: "à chiffrer" },
  vide:      { badge: "gris",  mot: "jamais travaillée" },
  rien:      { badge: "gris",  mot: "au meilleur connu" }
};
function badgeEtat(codeVerdict) {
  const e = ETATS_POSTE[codeVerdict] || ETATS_POSTE.rien;
  return badge(e.badge, e.mot);
}

function badgeEtoile() { return badge("etoile", "★ en production"); }

const STATUTS_SCENARIO = {
  serie: { badge: "vert", mot: "En série" },
  valide: { badge: "ambre", mot: "Validé" },
  essai: { badge: "bleu", mot: "En essai" },
  etude: { badge: "gris", mot: "À l'étude" },
  abandonne: { badge: "contour", mot: "Abandonné" }
};
function badgeStatutScenario(sc) {
  const s = STATUTS_SCENARIO[sc && sc.statut] || STATUTS_SCENARIO.essai;
  return badge(s.badge, s.mot);
}

/* Le chiffre clé et son unité. */
function chiffre(valeur, unite, opts) {
  const o = opts || {};
  return h("div", { class: "celle" + (o.class ? " " + o.class : "") },
    h("div", { class: "etiquette" }, o.etiquette || ""),
    h("div", { class: "valeur mono" + (o.grand ? " grand" : "") + (o.couleur ? " " + o.couleur : "") },
      valeur,
      unite ? h("span", { class: "unite" }, unite) : null),
    o.contexte ? h("div", { class: "contexte" }, o.contexte) : null);
}

/* La barre de ralliement vers la cible. */
function barreCible(pct) {
  const p = Math.max(0, Math.min(100, pct || 0));
  return h("div", { class: "barre-cible", title: "ralliement de la cible : " + Math.round(p) + " %" },
    h("div", { class: "remplissage", style: { width: p + "%" } }));
}

/* ============================================================================
   LES PANNEAUX — un tiroir, un seul à la fois
   ========================================================================== */

let voileActif = null;

function ouvrirPanneau(titre, sous, contenu, opts) {
  const o = opts || {};
  fermerPanneau();
  const panneau = h("div", { class: "panneau" + (o.large ? " large" : "") });
  const boutonFermer = h("button", { class: "bouton petit p-fermer", onclick: fermerPanneau, "aria-label": "Fermer" }, "Fermer");
  panneau.appendChild(h("div", { class: "p-entete" },
    h("div", { class: "p-titre" }, titre), boutonFermer));
  if (sous) panneau.appendChild(h("div", { class: "p-sous" }, sous));
  if (Array.isArray(contenu)) contenu.forEach(c => c && panneau.appendChild(c));
  else if (contenu) panneau.appendChild(contenu);
  voileActif = h("div", {
    class: "voile",
    onclick: (e) => { if (e.target === voileActif) fermerPanneau(); }
  }, panneau);
  document.body.appendChild(voileActif);
  return panneau;
}

function fermerPanneau() {
  if (voileActif) { voileActif.remove(); voileActif = null; }
}

/* Le menu groupé : Consulter / Documenter / Gérer / zone rouge en dernier. */
function ouvrirMenu(items) {
  const familles = {};
  items.forEach(it => { (familles[it.famille] = familles[it.famille] || []).push(it); });
  const ordre = ["Consulter", "Documenter", "Gérer"];
  const contenu = h("div", {});
  ordre.forEach(f => {
    if (!familles[f]) return;
    const bloc = h("div", { class: "menu-famille" }, h("div", { class: "titre-famille" }, f));
    familles[f].forEach(it => bloc.appendChild(h("button", {
      class: "item", onclick: () => { fermerPanneau(); it.action(); }
    }, it.libelle)));
    contenu.appendChild(bloc);
  });
  if (familles["Zone rouge"]) {
    const bloc = h("div", { class: "menu-famille zone-rouge" },
      h("div", { class: "titre-famille" }, "Zone rouge — chaque clic est réfléchi"));
    familles["Zone rouge"].forEach(it => bloc.appendChild(h("button", {
      class: "item rouge", onclick: () => { fermerPanneau(); it.action(); }
    }, it.libelle)));
    contenu.appendChild(h("div", { class: "separateur" }));
    contenu.appendChild(bloc);
  }
  ouvrirPanneau("Actions", "", contenu, {});
}

/* Le toast : un mot, quelques secondes, jamais un blocage. */
let toastActif = null, toastTimer = null;
function toast(message) {
  if (toastActif) toastActif.remove();
  if (toastTimer) clearTimeout(toastTimer);
  toastActif = h("div", { class: "toast" }, message);
  document.body.appendChild(toastActif);
  toastTimer = setTimeout(() => { if (toastActif) { toastActif.remove(); toastActif = null; } }, 3200);
}

/* Une confirmation honnête : elle dit ce qui va arriver, et exige un mot. */
function confirmer(question, libelleAction, action, opts) {
  const o = opts || {};
  ouvrirPanneau("Confirmer", "", [
    h("p", {}, question),
    h("div", { class: "liste-actions" },
      h("button", { class: "bouton", onclick: fermerPanneau }, "Annuler"),
      h("button", {
        class: "bouton " + (o.danger ? "danger" : "primaire"),
        onclick: () => { fermerPanneau(); action(); }
      }, libelleAction))
  ]);
}

/* Le champ de formulaire standard. */
function champ(etiquette, type, valeur, attrs, aide) {
  const a = attrs || {};
  const el = h("input", Object.assign({ type: type, value: valeur === null || valeur === undefined ? "" : valeur }, a));
  return h("label", { class: "champ" },
    h("span", { class: "etiquette" }, etiquette),
    el,
    aide ? h("span", { class: "aide" }, aide) : null);
}
function champSelect(etiquette, options, valeur, attrs, aide) {
  const sel = h("select", attrs || {});
  (options || []).forEach(o => sel.appendChild(h("option", { value: o.value, selected: String(o.value) === String(valeur) }, o.libelle)));
  return h("label", { class: "champ" },
    h("span", { class: "etiquette" }, etiquette),
    sel,
    aide ? h("span", { class: "aide" }, aide) : null);
}

/* Les pastilles de projet (couleur de projet assignée à la création). */
function pastilleProjet(pj, active) {
  return h("button", {
    class: "etiquette-pj" + (active ? "" : " off"),
    style: active ? { "--couleur-pj": pj.couleur || "#545e68" } : {},
    title: (active ? "projet actif — cliquer pour le retirer du filtre" : "cliquer pour filtrer sur ce projet"),
    onclick: () => basculerFiltreProjet(pj.id)
  }, pj.nom);
}

/* Un « — » n'existe pas : l'absence dit ce qui manque (cahier §5.2). */
function absence(raison) {
  return h("span", { class: "absence", style: { color: "var(--label)", fontStyle: "italic" } }, raison);
}
