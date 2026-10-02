/* ============================================================================
   PROJET3 — L'APPLICATION
   L'atelier d'abord : accueil (tuiles) → ligne → poste → optimisation →
   emporter. Les informations arrivent en douceur : le gros chiffre d'abord,
   la fiche derrière un geste. Le rendu lit le noyau, il ne calcule rien.
   ========================================================================== */

"use strict";

/* ============================================================================
   1. L'ÉTAT GLOBAL ET LA PERSISTANCE
   ========================================================================== */

const STORAGE_KEY = "spk_projet3_v1";
const SECOURS_KEY = "spk_projet3_secours";
const THEME_KEY = "spk_projet3_theme";
const MAX_SECOURS = 5;

/* Toute globale est déclarée AVANT le premier usage — le piège TDZ de
   l'ancienne app (repli silencieux sur l'exemple, zéro message) ne doit pas
   se reproduire ici. */
let ETAT = null;         // les données
let VUE = {              // où on en est
  ecran: "accueil",      // accueil | ligne | poste | emporter | projets
  ligneId: "", refId: "", opId: "", scId: "",
  filtreProjetId: ""
};
let SOURCE_IMPORT = null;   // la dernière source affichée (d'où viennent les chiffres)

/* Le chargement : le local d'abord, l'exemple ensuite, et le message dit
   lequel des deux on lit. */
function chargerEtatInitial() {
  try {
    const brut = localStorage.getItem(STORAGE_KEY);
    if (brut) {
      const mig = normaliserEtat(JSON.parse(brut));
      if (mig.ok) {
        ETAT = mig.etat;
        SOURCE_IMPORT = "suivi local de ce poste";
        return;
      }
    }
  } catch (e) { /* le local abîmé ne bloque pas l'outil : on repart propre */ }
  ETAT = etatExemple();
  SOURCE_IMPORT = "jeu d'exemple — aucun chiffre réel";
  toast("Jeu d'exemple chargé — importez vos données quand vous voulez (bouton Données).");
}

let saveTimer = null;
function saveData() {
  if (!ETAT) return;
  ETAT.modifieLe = new Date().toISOString();
  if (saveTimer) clearTimeout(saveTimer);
  saveTimer = setTimeout(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(ETAT)); }
    catch (e) {
      toast("Sauvegarde locale impossible (stockage plein) — exportez vos données maintenant.");
    }
  }, 250);
}

/* Les instantanés de secours : avant toute action risquée, l'état courant
   part au fond du tiroir. Cinq places, le plus récent en tête. */
function pousserSecours() {
  try {
    const pile = JSON.parse(localStorage.getItem(SECOURS_KEY) || "[]");
    pile.unshift({ date: new Date().toISOString(), etat: ETAT });
    while (pile.length > MAX_SECOURS) pile.pop();
    localStorage.setItem(SECOURS_KEY, JSON.stringify(pile));
  } catch (e) { /* un secours manqué vaut mieux qu'un outil bloqué */ }
}

function lireSecours() {
  try { return JSON.parse(localStorage.getItem(SECOURS_KEY) || "[]"); }
  catch (e) { return []; }
}

/* ============================================================================
   2. LA NAVIGATION ET LE FIL
   ========================================================================== */

function aller(ecran, ids) {
  VUE.ecran = ecran;
  if (ids) ["ligneId", "refId", "opId", "scId"].forEach(k => {
    if (k in ids) VUE[k] = ids[k];
  });
  window.scrollTo(0, 0);
  render();
}

function ligneActive() {
  return (ETAT.lignes || []).find(l => l.id === VUE.ligneId) || null;
}
function referenceActive(ligne) {
  const l = ligne || ligneActive();
  if (!l) return null;
  return (l.references || []).find(r => r.id === VUE.refId) || null;
}
function opActive(ref) {
  const r = ref || referenceActive();
  if (!r) return null;
  return (r.ops || []).find(o => o.id === VUE.opId) || null;
}
function scenarioActif(op) {
  const o = op || opActive();
  if (!o) return null;
  return (o.scenarios || []).find(s => s.id === VUE.scId) || null;
}

/* Le fil : une seule ligne, le maillon actif plus fort (CDC UX §3.1). */
function filDOM(maillons) {
  const el = h("nav", { class: "fil" });
  maillons.forEach((m, i) => {
    if (i) el.appendChild(h("span", { class: "sep" }, "›"));
    if (m.action) el.appendChild(h("a", { onclick: m.action, href: "javascript:void(0)" }, m.libelle));
    else el.appendChild(h("span", { class: "maillon-actif" }, m.libelle));
  });
  return el;
}

function basculerFiltreProjet(id) {
  VUE.filtreProjetId = (VUE.filtreProjetId === id) ? "" : id;
  render();
}

/* ============================================================================
   3. LA PROCHAINE ÉTAPE, EN TOUTES LETTRES
   ========================================================================== */

function prochaineEtape(v) {
  if (!v || !v.verdict) return "";
  const code = v.verdict.code;
  if (code === "vide") return "Poser ce qui tourne réellement : le scénario de production, puis le trio prix / arêtes / charnière.";
  if (code === "achiffrer") {
    if (!v.prod) return "Poser le scénario de production — aucun scénario en prod sur ce poste.";
    return "Renseigner le trio prix / arêtes / charnière des logements — le poste est non chiffrable.";
  }
  if (code === "gagne") return "Le gain est acté : le scénario passe en production.";
  if (code === "pret") return "Passer le scénario validé " + (v.verdict.validations || 5) + "× en série — ou dire non, avec la raison.";
  if (code === "essai") {
    const s = v.meilleur && v.meilleur.sc;
    if (!s) return "";
    const conformes = (s.essais || []).filter(e => statutEssai(s, e).code === "conforme").length;
    const seuil = s.validationThreshold || 5;
    return "Poursuivre le protocole 5× — " + conformes + "/" + seuil + " essais conformes sur « " + s.name + " ».";
  }
  return "Au meilleur connu : aucun essai ne fait mieux que la prod — surveiller l'usure, rien à décider.";
}

/* ============================================================================
   4. LA BARRE DU HAUT ET LE PIED
   ========================================================================== */

function topbarDOM() {
  return h("div", { class: "topbar" },
    h("div", { class: "marque", title: APP_NOM + " — génération 3" },
      "Suivi optimisation SPK ",
      h("span", { class: "site" }, "· Sept Fons"),
      h("span", { class: "confidentiel" }, "Confidentiel interne")),
    h("div", { class: "actions" },
      h("button", {
        class: "bouton", onclick: () => aller("emporter"),
        title: "La page A4 pour la hiérarchie"
      }, h("span", { class: "texte-long" }, "Emporter la page")),
      h("button", { class: "bouton primaire", onclick: () => ouvrirMenuActions() }, "Données · Options"),
      h("button", {
        class: "theme-bascule", "aria-label": "Thème jour / nuit",
        onclick: basculerTheme, title: "Jour / nuit"
      }, document.documentElement.getAttribute("data-theme") === "nuit" ? "☀" : "☾"))
  );
}

function basculerTheme() {
  const actuel = document.documentElement.getAttribute("data-theme") === "nuit" ? "nuit" : "jour";
  const suivant = actuel === "nuit" ? "jour" : "nuit";
  document.documentElement.setAttribute("data-theme", suivant);
  try { localStorage.setItem(THEME_KEY, suivant); } catch (e) { }
  render();
}

function ouvrirMenuActions() {
  ouvrirMenu([
    { famille: "Consulter", libelle: "Projets", action: () => aller("projets") },
    { famille: "Consulter", libelle: "Livraisons (les instantanés figés)", action: ouvrirLivraisons },
    { famille: "Documenter", libelle: "Emporter la page A4", action: () => aller("emporter") },
    { famille: "Gérer", libelle: "Données — export, import, fusion", action: ouvrirPanneauDonnees },
    { famille: "Gérer", libelle: "Options — responsables, réglages", action: ouvrirOptions },
    { famille: "Gérer", libelle: "Recharger le jeu d'exemple", action: () => {
        confirmer("Recharger le jeu d'exemple remplacera l'affichage par des données fictives. Vos données locales actuelles passeront en instantané de secours.",
          "Recharger l'exemple", () => {
            pousserSecours();
            ETAT = etatExemple();
            SOURCE_IMPORT = "jeu d'exemple — aucun chiffre réel";
            saveData(); fermerPanneau(); render();
          });
      } },
    { famille: "Zone rouge", libelle: "Restaurer un instantané de secours", action: ouvrirSecours },
    { famille: "Zone rouge", libelle: "Réinitialiser (état vierge, topologie seule)", action: () => {
        confirmer("Tout l'état courant (données, projets, livraisons) sera remplacé par un état vierge. Un instantané de secours est pris avant — c'est le seul chemin arrière.",
          "Réinitialiser", () => {
            pousserSecours();
            ETAT = etatVierge();
            SOURCE_IMPORT = "état vierge";
            saveData(); fermerPanneau(); aller("accueil");
          }, { danger: true });
      } }
  ]);
}

function piedDOM() {
  return h("div", { class: "pied" },
    h("span", {}, APP_NOM + " v" + VERSION + " — génération 3"),
    h("span", {}, "SPK by CeramTec · Confidentiel interne"),
    h("span", { class: "droite" }, "source : " + (SOURCE_IMPORT || "inconnue")));
}

/* ============================================================================
   5. L'ÉCRAN ACCUEIL — les tuiles, le bandeau, la matrice
   ========================================================================== */

function renderAccueil() {
  const rec = recapAtelier(ETAT.lignes || []);
  const projets = (ETAT.projets || []);
  const filtreActif = VUE.filtreProjetId ? projets.find(p => p.id === VUE.filtreProjetId) : null;

  const page = h("div", { class: "page" });
  page.appendChild(h("div", { class: "page-titre" },
    h("h1", {}, "L'atelier"),
    filtreActif ? h("span", { class: "peri" }, "filtré : " + filtreActif.nom) : null));
  page.appendChild(h("p", { class: "sous-titre" },
    "Une tuile par ligne. La couleur ET le mot disent l'état — on ne lit jamais une couleur seule."));

  /* Le bandeau : chaque chiffre remonte à sa source ; une absence est nommée
     avec SA raison — le volume manquant et l'absence de gain acté sont deux
     absences différentes, elles ne portent pas le même message. */
  page.appendChild(h("div", { class: "bandeau" },
    h("div", { class: "bloc acte" },
      h("div", { class: "etiquette" }, "Économie actée"),
      h("div", { class: "valeur" }, rec.gainAnnuelActe !== null ? fmt(rec.gainAnnuelActe, 0) : "—", h("span", { class: "unite" }, "€/an")),
      h("div", { class: "contexte" },
        rec.gainAnnuelActe !== null
          ? "gains d'outillage passés en série, volumes annuels saisis"
          : (rec.gainActe !== null && rec.gainActe > 0
            ? "des gains sont actés mais aucun volume annuel n'est saisi : le €/an ne s'invente pas"
            : "aucun gain passé en série pour l'instant — les essais d'abord"))),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Gains en cours"),
      h("div", { class: "valeur" }, rec.gainProjete !== null ? fmt(rec.gainProjete, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" }, "validés ou prometteurs, pas encore en série — jamais sommés aux actés")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Décisions en attente"),
      h("div", { class: "valeur" }, String(rec.decisions)),
      h("div", { class: "contexte" }, "validés 5× à confirmer + essais prometteurs à suivre")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "À chiffrer"),
      h("div", { class: "valeur" }, String(rec.aChiffrer)),
      h("div", { class: "contexte" }, "postes dont le trio prix / arêtes / charnière n'est pas complet")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Lignes engagées"),
      h("div", { class: "valeur" }, rec.lignesEngagees + "/" + rec.nbLignes),
      h("div", { class: "contexte" }, "au moins un poste travaillé"))
  ));

  /* Les projets posés sur l'atelier (filtre + pastilles). */
  if (projets.length) {
    page.appendChild(h("div", { class: "liste-actions" },
      h("span", { class: "etiquette", style: { color: "var(--label)", fontSize: "12px", fontFamily: "var(--font-disp)", fontWeight: "700" } }, "Projets :"),
      projets.map(pj => pastilleProjet(pj, VUE.filtreProjetId === pj.id)),
      filtreActif ? h("button", { class: "bouton petit", onclick: () => basculerFiltreProjet("") }, "Tout montrer") : null));
  }

  /* Les tuiles, dans l'ordre physique de l'atelier. */
  const tuiles = rec.tuiles.filter(t => {
    if (!filtreActif) return true;
    return t.postes.some(p => projetsDeOP(ETAT, t.ligne.id,
      (p.ref || {}).id, (p.op || {}).id).some(x => x.id === filtreActif.id));
  });
  if (!tuiles.length) {
    page.appendChild(h("div", { class: "aucun" },
      h("span", { class: "grand" }, "Aucun poste de ce projet sur cette vue"),
      "Le projet regroupe des scénarios d'autres lignes — retirez le filtre pour tout voir."));
  } else {
    page.appendChild(h("div", { class: "grille-tuiles" }, tuiles.map(tuileDOM)));
  }

  /* Ce qui n'est pas ici, dit haut et clair (le proto a posé cette règle). */
  page.appendChild(h("div", { class: "note" },
    h("span", { class: "note-titre" }, "Pourquoi la production hebdomadaire n'est pas ici ?"),
    "Elle se détaille par lot de lignes, pas par poste d'outillage — et aucune cadence n'est mesurée par ligne. L'outil ne l'estime pas."));

  /* La matrice : toutes les lignes, tous les postes — l'écran de la hiérarchie. */
  page.appendChild(h("div", { class: "page-titre", style: { marginTop: "26px" } }, h("h2", { style: { fontSize: "17px" } }, "Tous les postes")));
  page.appendChild(matricePostesDOM(tuiles));

  return page;
}

/* LA TUILE — ce qu'un chef d'atelier lit en passant. */
function tuileDOM(t) {
  const dom = h("div", { class: "tuile", style: { "--tuile-encre": t.encre }, onclick: () => aller("ligne", { ligneId: t.ligne.id }) });
  dom.appendChild(h("div", { class: "t-ete" }));
  const corps = h("div", { class: "t-corps" });
  corps.appendChild(h("div", { class: "t-entete" },
    h("span", { class: "t-nom" }, t.nom),
    h("span", { class: "t-code" }, t.code || "")));
  corps.appendChild(h("div", { class: "t-chiffre" },
    h("span", { class: "t-cpp mono" }, t.cpp !== null ? fmt(t.cpp, 4) : "—"),
    h("span", { class: "t-cpp-unite" }, "€ outillage / pièce"),
    h("span", { class: "droite" })));
  if (t.cpp === null) {
    if (t.postes.length) {
      corps.appendChild(h("div", { class: "t-ecart manque" },
        "— " + t.nonChiffrables + " poste(s) non chiffré(s) : le trio prix / arêtes / charnière est incomplet"));
    }
  } else if (t.distanceCible !== null && t.dominante) {
    const sur = t.distanceCible > 0;
    corps.appendChild(h("div", {
      class: "t-ecart " + (sur ? "sur" : "sous"),
      title: "écart à la cible du site"
    },
      sur ? "+" : "", fmt(Math.abs(t.distanceCible), 4), " €/pièce ",
      sur ? "au-dessus de la cible " : "sous la cible de ",
      t.dominante.cible !== null ? fmt(t.dominante.cible, 4) : "(— cible non saisie)"));
  } else {
    corps.appendChild(h("div", { class: "t-ecart manque" }, "— cible du site non saisie : pas d'écart affiché"));
  }
  if (t.dominante) {
    corps.appendChild(h("div", { class: "t-dominante" },
      "référence dominante : ", h("span", { class: "surbrillance" }, t.dominante.ref.nom || "?")));
  } else {
    corps.appendChild(h("div", { class: "t-dominante" }, absence("— aucune référence chiffrable sur cette ligne")));
  }
  corps.appendChild(h("div", { class: "t-bas" },
    badgeEtat(t.postes.some(p => p.verdict.verdict.code === "gagne") ? "gagne"
      : t.postes.some(p => p.verdict.verdict.code === "pret") ? "pret"
        : t.postes.some(p => p.verdict.verdict.code === "essai") ? "essai"
          : t.aChiffrer ? "achiffrer"
            : t.postes.every(p => p.verdict.verdict.code === "vide") ? "vide" : "rien"),
    t.decisions ? badge("bleu", t.decisions + " décision" + (t.decisions > 1 ? "s" : "") + " en attente") : null,
    h("span", { class: "t-suite" }, "Ouvrir la ligne →")));
  dom.appendChild(corps);
  return dom;
}

/* La matrice des postes : une table, toutes les lignes, tri stable. */
function matricePostesDOM(tuiles) {
  const env = h("div", { class: "tableau-enveloppe" });
  const table = h("table", { class: "tableau" });
  table.appendChild(h("thead", {}, h("tr", {},
    h("th", {}, "Ligne"), h("th", {}, "Poste"), h("th", {}, "Référence"),
    h("th", { class: "mono" }, "CPP outillage prod"),
    h("th", { class: "mono" }, "Gain acté"), h("th", { class: "mono" }, "Gain en cours"),
    h("th", { class: "mono" }, "Chemin cible"), h("th", {}, "État"), h("th", {}, "Où entrer"))));
  const corps = h("tbody", {});
  tuiles.forEach(t => {
    corps.appendChild(h("tr", { class: "ligne-groupe" }, h("td", { colspan: "9" },
      (t.ligne.nom || "?") + (t.cpp !== null ? " — CPP ligne " + fmt(t.cpp, 4) + " €/pièce" : " — ligne non chiffrable"))));
    const postes = t.postes.filter(p => {
      if (!VUE.filtreProjetId) return true;
      return projetsDeOP(ETAT, t.ligne.id, (p.ref || {}).id, (p.op || {}).id).some(x => x.id === VUE.filtreProjetId);
    });
    if (!postes.length) {
      corps.appendChild(h("tr", {}, h("td", { colspan: "9" }), h("td", { colspan: "8", style: { color: "var(--label)", fontStyle: "italic" } },
        "aucun poste de ce projet sur cette ligne")));
    }
    postes.forEach((p, i) => {
      const v = p.verdict;
      const cheminTxt = (v.chemin !== null) ? Math.round(v.chemin) + " %" : "— pas de chemin calculable";
      const tr = h("tr", { class: i === postes.length - 1 ? "dernier" : "" },
        h("td", { style: { color: "var(--label)" } }, t.code || t.ligne.nom),
        h("td", {}, opCodeDe(p.op)),
        h("td", {}, (p.ref && p.ref.nom) || "—"),
        h("td", { class: "mono" }, v.cppProd !== null ? fmt(v.cppProd, 4) : "non chiffrable"),
        h("td", { class: "mono juste" }, v.gainActe !== null ? "+" + fmt(v.gainActe, 4) : "±0,000"),
        h("td", { class: "mono" }, v.gainProjete !== null ? "+" + fmt(v.gainProjete, 4) : "±0,000"),
        h("td", { class: "mono" }, cheminTxt),
        h("td", {}, badgeEtat(v.verdict.code)),
        h("td", {}, h("a", { href: "javascript:void(0)", onclick: () => ouvrirPoste(t.ligne.id, p) }, "ouvrir →")));
      corps.appendChild(tr);
    });
  });
  table.appendChild(corps);
  env.appendChild(table);
  return env;
}

function ouvrirPoste(ligneId, p) {
  aller("poste", { ligneId: ligneId, refId: (p.ref || {}).id || "", opId: (p.op || {}).id || "" });
}

/* ============================================================================
   6. L'ÉCRAN LIGNE — la production décomposée jusqu'au logement
   ========================================================================== */

function renderLigne() {
  const ligne = ligneActive();
  if (!ligne) return h("div", { class: "page" }, h("div", { class: "aucun" },
    h("span", { class: "grand" }, "Ligne introuvable"),
    h("a", { href: "javascript:void(0)", onclick: () => aller("accueil") }, "← revenir à l'accueil")));

  const det = detailLigne(ligne);
  const page = h("div", { class: "page" });

  page.appendChild(filDOM([
    { libelle: "Accueil", action: () => aller("accueil") },
    { libelle: ligne.nom }
  ]));
  page.appendChild(h("div", { class: "page-titre" },
    h("h1", {}, ligne.nom),
    ligne.coutHoraire ? h("span", { class: "peri" }, fmt(ligne.coutHoraire, 0) + " €/h") : null,
    h("span", { class: "droite liste-actions" },
      h("button", { class: "bouton petit", onclick: () => ouvrirPanneauLigne(ligne) }, "Fiche ligne"),
      h("button", { class: "bouton petit", onclick: () => ouvrirPanneauReference(ligne, null) }, "+ Référence"))));
  page.appendChild(h("p", { class: "sous-titre" },
    "Ce qui tourne aujourd'hui : le scénario de production de chaque opération, décomposé jusqu'au logement."));

  if (!det.refs.length) {
    page.appendChild(h("div", { class: "aucun" },
      h("span", { class: "grand" }, "Aucune référence sur cette ligne"),
      "Commencez par poser une référence disque : ",
      h("button", { class: "bouton", onclick: () => ouvrirPanneauReference(ligne, null) }, "+ Référence")));
    return page;
  }

  det.refs.forEach(rc => {
    const carte = h("div", { class: "carte" });
    carte.appendChild(h("div", { class: "c-entete" },
      h("span", { class: "c-titre" }, rc.nom),
      h("span", { class: "mono", style: { color: "var(--label)" } },
        "cible : ", rc.cible !== null ? fmt(rc.cible, 4) + " €/pièce" : "— non saisie"),
      h("span", { class: "droite liste-actions", style: { margin: 0 } },
        h("button", { class: "bouton petit", onclick: () => ouvrirPanneauReference(ligne, rc.ref) }, "Fiche référence"))));
    carte.appendChild(h("div", { class: "c-chiffres" },
      chiffre(rc.cpp !== null ? fmt(rc.cpp, 4) : "—", " €/pièce", { etiquette: "CPP outillage de la référence" }),
      chiffre(rc.nonChiffrables ? "hors " + rc.nonChiffrables + " OP non chiffrée(s)" : "postes tous chiffrés", "", { etiquette: "Périmètre" }),
      (() => {
        const projetsOP = projetsSurReference(ligne.id, rc.ref.id);
        return chiffre(String(projetsOP.length), " projet(s)", { etiquette: "Projets posés ici" });
      })()));

    /* Les OPs de la référence : la production, et la porte vers l'optimisation. */
    rc.postes.forEach(p => {
      carte.appendChild(posteResumeDOM(ligne, rc, p));
    });

    carte.appendChild(h("div", { class: "liste-actions" },
      h("button", {
        class: "bouton petit", onclick: () => ouvrirPanneauOp(ligne, rc.ref, null),
      }, "+ Opération")));
    page.appendChild(carte);
  });

  return page;
}

function projetsSurReference(ligneId, refId) {
  const ids = {};
  ((ETAT.projets) || []).forEach(pj => ((pj.tags) || []).forEach(t => {
    if (t.ligneId === ligneId && t.referenceId === refId) ids[pj.id] = pj;
  }));
  return Object.values(ids);
}

/* Le résumé d'un poste dans l'écran ligne : la prod, ses logements, les essais. */
function posteResumeDOM(ligne, rc, p) {
  const v = p.verdict;
  const el = h("div", { class: "porte" });
  const entete = h("div", { class: "outil-ligne", style: { marginBottom: "4px" } },
    h("span", { class: "outil-numero" },
      p.code + (p.nom && !p.nom.toUpperCase().startsWith(p.code) ? " · " + p.nom : "")),
    p.prod ? badgeEtoile() : badge("ambre", "sans production"),
    v.gainActe !== null ? badge("vert", "+" + fmt(v.gainActe, 4) + " €/pièce acté") : null,
    v.gainProjete !== null ? badge("bleu", "+" + fmt(v.gainProjete, 4) + " €/pièce en essai") : null,
    h("span", { class: "outil-cpp mono" },
      p.cpp !== null ? fmt(p.cpp, 4) + " €/pièce" : "non chiffrable"),
    h("span", { class: "droite" }),
    h("button", { class: "bouton petit", onclick: () => aller("poste", { ligneId: ligne.id, refId: rc.ref.id, opId: p.op.id }) },
      p.nbAutres ? "Optimiser (" + p.nbAutres + " scénario" + (p.nbAutres > 1 ? "s" : "") + ") →" : "Ouvrir le poste →"));
  el.appendChild(entete);

  if (!p.prod) {
    el.appendChild(h("div", { class: "note" },
      "Aucun scénario en production sur ce poste : ce qui tourne réellement n'est pas posé. ",
      h("a", { href: "javascript:void(0)", onclick: () => ouvrirPoste(ligne.id, { ref: rc.ref, op: p.op }) }, "Ouvrir le poste pour le créer.")));
    return el;
  }

  const outillage = p.outillage || outillageDeScenario(p.prod);
  const cppTotal = outillage.cpp;
  outillage.outils.forEach(o => {
    const bloc = h("div", { class: "outil-bloc" });
    bloc.appendChild(h("div", { class: "outil-ligne" },
      h("span", { class: "outil-numero" }, o.numero),
      o.description ? h("span", { class: "outil-desc" }, o.description) : null,
      h("span", { class: "outil-cpp mono" }, o.cpp !== null ? fmt(o.cpp, 4) + " €/pièce" : "— non chiffrable")));
    const table = h("table", {});
    table.appendChild(h("thead", {}, h("tr", {},
      h("th", {}, "Logement"), h("th", {}, "Plaquette / article"),
      h("th", {}, "MABEC"),
      h("th", { class: "mono" }, "Prix"), h("th", { class: "mono" }, "Arêtes"), h("th", { class: "mono" }, "Charnière"),
      h("th", { class: "mono" }, "€/pièce"), h("th", { class: "mono" }, "Part"))));
    const corps = h("tbody", {});
    o.logements.forEach(l => {
      const part = (l.cpp !== null && cppTotal) ? Math.round(l.cpp / cppTotal * 100) + " %" : "—";
      const tr = h("tr", { class: l.cpp === null ? "non-chiffrable" : "" },
        h("td", {}, h("span", { class: "logement-nom" }, l.logementNom)),
        h("td", {}, l.article || "", l.article ? h("span", { class: "article" }, "") : null),
        h("td", { class: "mono" }, l.mabec || ""),
        h("td", { class: "mono" }, l.prix !== null ? fmt(l.prix, 2) : "—"),
        h("td", { class: "mono" }, l.aretes !== null ? fmt(l.aretes, 0) : "—"),
        h("td", { class: "mono" }, l.charniere !== null ? fmt(l.charniere, 0) : "—"),
        h("td", { class: "mono" }, l.cpp !== null ? fmt(l.cpp, 4) : "— non chiffrable"),
        h("td", { class: "mono part" }, part));
      corps.appendChild(tr);
    });
    table.appendChild(corps);
    bloc.appendChild(table);
    el.appendChild(bloc);
  });

  /* Les essais portés par la production : des mesures réelles, jamais cachées. */
  const essaisProd = p.prod.essais || [];
  if (essaisProd.length) {
    el.appendChild(h("div", { class: "note" },
      h("span", { class: "note-titre" }, "Essais portés par la production"),
      essaisProd.map(e => {
        const o = cppEssaiObtenu(p.prod, e);
        const st = statutEssai(p.prod, e);
        return h("div", {}, e.titre + " — " + st.texte +
          (o.cpp !== null ? " · CPP obtenu " + fmt(o.cpp, 4) + " €/pièce (prévu " + fmt(p.cpp, 4) + ")" : " · CPP non mesurable"));
      })));
  } else if (p.cpp !== null) {
    el.appendChild(h("div", { class: "note" },
      "Aucun essai sur la production : son CPP est celui qu'on a prévu, pas celui qu'on a mesuré."));
  }

  /* Le résumé des projets posés sur ce poste (CDC Projets v2 §1.4). */
  const projetsOP = projetsDeOP(ETAT, ligne.id, rc.ref.id, p.op.id);
  if (projetsOP.length) {
    el.appendChild(h("div", { class: "etiquettes", style: { marginTop: "8px" } },
      h("span", { style: { fontSize: "12px", color: "var(--label)" } },
        projetsOP.length + " projet" + (projetsOP.length > 1 ? "s" : "") + " sur ce poste : "),
      projetsOP.map(pj => pastilleProjet(pj, VUE.filtreProjetId === pj.id))));
  }

  return el;
}

/* ============================================================================
   7. L'ÉCRAN POSTE — la décision : prévu contre obtenu, prod contre essais
   ========================================================================== */

function renderPoste() {
  const ligne = ligneActive();
  const ref = referenceActive(ligne);
  const op = opActive(ref);
  if (!ligne || !ref || !op) return h("div", { class: "page" }, h("div", { class: "aucun" },
    h("span", { class: "grand" }, "Poste introuvable"),
    h("a", { href: "javascript:void(0)", onclick: () => aller("accueil") }, "← revenir à l'accueil")));

  const v = verdictPoste(ref, op, op.scenarios);
  const dec = decisionPoste(v);
  const page = h("div", { class: "page" });

  page.appendChild(filDOM([
    { libelle: "Accueil", action: () => aller("accueil") },
    { libelle: ligne.nom, action: () => aller("ligne", { ligneId: ligne.id, refId: "", opId: "", scId: "" }) },
    { libelle: ref.nom, action: () => aller("ligne", { ligneId: ligne.id, refId: ref.id, opId: "", scId: "" }) },
    { libelle: opCodeDe(op) + (op.nom && !op.nom.includes(opCodeDe(op)) ? " · " + op.nom : "") }
  ]));

  /* Le bandeau de décision : le mot, la raison, les chiffres à côté. */
  page.appendChild(h("div", { class: "page-titre" }, h("h1", {}, "Poste " + opCodeDe(op)),
    h("span", { class: "peri" }, ref.nom)));
  page.appendChild(h("div", { class: "bandeau" },
    h("div", { class: "bloc " + (v.verdict.code === "gagne" ? "acte" : v.verdict.code === "achiffrer" ? "" : "") },
      h("div", { class: "etiquette" }, "La décision"),
      h("div", { class: "valeur", style: { fontSize: "24px" } }, dec.mot),
      h("div", { class: "contexte" }, dec.pourquoi)),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "CPP outillage prod"),
      h("div", { class: "valeur" }, v.cppProd !== null ? fmt(v.cppProd, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" },
        v.cppProd !== null
          ? (v.nonChiffrables ? "hors " + v.nonChiffrables + " logement(s) non chiffrable(s)" : "tous les logements sont chiffrés")
          : "— trio prix / arêtes / charnière incomplet")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Cible du site"),
      h("div", { class: "valeur" }, v.cible !== null ? fmt(v.cible, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" }, v.cible !== null ? "la valeur de référence du classeur" : "— cible non saisie sur la référence")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Chemin vers la cible"),
      h("div", { class: "valeur" }, v.chemin !== null ? Math.round(v.chemin) + " %" : "—"),
      h("div", { class: "contexte" },
        v.chemin !== null
          ? "par le meilleur scénario connu : " + ((v.meilleur && v.meilleur.sc.name) || "")
          : "— ni cible, ni scénario chiffrable : pas de chemin calculable"))
  ));

  /* Les deux gains, côte à côte, jamais sommés. */
  page.appendChild(h("div", { class: "carte" },
    h("div", { class: "c-entete" }, h("span", { class: "c-titre" }, "Les gains"),
      h("span", { style: { color: "var(--label)", fontSize: "13px" } }, "deux blocs distincts — on ne les additionne jamais")),
    h("div", { class: "c-chiffres" },
      chiffre(v.gainActe !== null ? "+" + fmt(v.gainActe, 4) : "±0,000", " €/pièce",
        { etiquette: "Acté (en série)", couleur: v.gainActe !== null ? "juste" : "" }),
      chiffre(v.gainActe !== null && v.gainAnnuelActe !== null ? "+" + fmt(v.gainAnnuelActe, 0) : "—", " €/an",
        { etiquette: "Acté, à l'année", contexte: v.gainAnnuelActe !== null
          ? "volume annuel saisi : " + fmt(v.volume, 0) + " pièces"
          : (v.gainActe !== null ? "— volume annuel non saisi : le €/an ne s'invente pas"
            : "aucun gain acté en série ici pour l'instant") }),
      chiffre(v.gainProjete !== null ? "+" + fmt(v.gainProjete, 4) : "±0,000", " €/pièce",
        { etiquette: "En essai (projeté)", couleur: v.gainProjete !== null ? "surbrillance" : "" }),
      chiffre(v.gainProjete !== null && v.gainAnnuelProjete !== null ? "+" + fmt(v.gainAnnuelProjete, 0) : "—", " €/an",
        { etiquette: "Projeté, à l'année", contexte: v.gainAnnuelProjete !== null
          ? "volume annuel saisi : " + fmt(v.volume, 0) + " pièces"
          : "— volume annuel non saisi : le €/an ne s'invente pas" }))));

  /* Le scénario de production. */
  if (v.prod) {
    page.appendChild(carteScenarioDOM(ligne, ref, op, v.prod, true, v));
  } else {
    page.appendChild(h("div", { class: "carte" },
      h("div", { class: "c-entete" }, h("span", { class: "c-titre" }, "Aucun scénario en production"),
        badge("ambre", "à poser")),
      h("p", { style: { color: "var(--body)" } }, "Ce qui tourne réellement sur la machine n'est pas posé ici. Créez-le (ou marquez un scénario existant ★) pour que le poste ait sa base 100."),
      h("div", { class: "liste-actions" },
        h("button", { class: "bouton primaire", onclick: () => ouvrirPanneauScenario(ligne, ref, op, null, true) }, "+ Scénario de production"),
        h("button", { class: "bouton", onclick: () => ouvrirPanneauScenario(ligne, ref, op, null, false) }, "+ Scénario d'essai"))));
  }

  /* Les scénarios d'optimisation : ce qu'on teste, où ils en sont. */
  const autres = (op.scenarios || []).filter(s => !v.prod || s.id !== v.prod.id);
  page.appendChild(h("div", { class: "page-titre", style: { marginTop: "22px" } },
    h("h2", { style: { fontSize: "17px" } }, "Ce qu'on teste"),
    h("span", { style: { color: "var(--label)", fontSize: "13px" } },
      autres.length ? autres.length + " scénario" + (autres.length > 1 ? "s" : "") + " contre la prod" : "")));
  if (!autres.length) {
    page.appendChild(h("div", { class: "aucun" },
      h("span", { class: "grand" }, "Aucun scénario d'optimisation ici"),
      "Un scénario est une configuration d'outils testée contre la production : plaquette différente, vitesse, avances…",
      v.prod ? h("div", { style: { marginTop: "12px" } },
        h("button", { class: "bouton primaire", onclick: () => dupliquerProd(op, v.prod) }, "Dupliquer la prod comme point de départ"),
        h("button", { class: "bouton", onclick: () => ouvrirPanneauScenario(ligne, ref, op, null, false) }, "Partir de zéro")) : null));
  }
  autres.forEach(s => page.appendChild(carteScenarioDOM(ligne, ref, op, s, false, v)));

  /* Les actions du poste. */
  page.appendChild(h("div", { class: "liste-actions" },
    h("button", { class: "bouton", onclick: () => ouvrirPanneauOp(ligne, ref, op) }, "Fiche OP (modules, ordre)"),
    op.ficheOutil ? h("span", { style: { color: "var(--label)", fontSize: "12px" } }, "fiche outil jointe à l'OP") : null));
  return page;
}

function dupliquerProd(op, prod) {
  const copie = JSON.parse(JSON.stringify(prod));
  copie.id = uid("sc");
  copie.name = "Essai — copie de " + prod.name;
  copie.baseline = false;
  copie.statut = "etude";
  copie.essais = [];
  copie.modifieLe = new Date().toISOString();
  op.scenarios.push(copie);
  saveData();
  toast("Scénario de travail créé à partir de la prod — modifiez ce qui change.");
  ouvrirPanneauScenario(ligneActive(), referenceActive(), op, copie, false);
}

/* La carte d'un scénario : prévu, obtenu, preuve, décision. */
function carteScenarioDOM(ligne, ref, op, sc, estProd, vPoste) {
  const d = cppScenarioDetail(sc);
  const carte = h("div", { class: "carte" });

  carte.appendChild(h("div", { class: "c-entete" },
    h("span", { class: "c-titre mono" }, sc.name),
    estProd ? badgeEtoile() : badgeStatutScenario(sc),
    (sc.statut === "valide") ? badge("ambre", "décision à prendre") : null,
    h("span", { class: "droite liste-actions", style: { margin: 0 } },
      h("button", { class: "bouton petit", onclick: () => ouvrirPanneauScenario(ligne, ref, op, sc, false) }, "Fiche scénario"),
      h("button", { class: "bouton petit", onclick: () => ouvrirEtiquetage(ligne, ref, op, sc) }, "Étiqueter"),
      estProd ? null : h("button", {
        class: "bouton petit", onclick: () => promouvoirScenario(ligne, ref, op, sc),
        title: "Faire de ce scénario le scénario de production"
      }, "★ Passer en série"))));

  carte.appendChild(h("div", { class: "c-chiffres" },
    chiffre(d.cpp !== null ? fmt(d.cpp, 4) : "—", " €/pièce",
      { etiquette: "CPP prévu", grand: true, contexte: d.nbNonChiffrables ? "hors " + d.nbNonChiffrables + " logement(s) non chiffrable(s)" : "tous les logements chiffrés" })));

  /* Les essais : la preuve. Prévu contre obtenu, conformité, protocole. */
  const essais = sc.essais || [];
  const st = statutScenario(sc);
  if (!estProd || essais.length) {
    const bloc = h("div", { class: "porte" });
    bloc.appendChild(h("div", { class: "outil-ligne" },
      h("span", { class: "outil-numero" }, "La preuve — protocole 5×"),
      badge(st.code === "valide" ? "ambre" : st.code === "serie" ? "vert" : "gris", st.texte)));
    if (!essais.length) {
      bloc.appendChild(h("div", { class: "note" },
        "Aucun essai consigné. Un essai se saisit en 90 secondes : qui, quand, les logements suivis, la charnière mesurée.",
        h("div", { style: { marginTop: "10px" } },
          h("button", { class: "bouton primaire", onclick: () => ouvrirPanneauEssai(ligne, ref, op, sc, null) }, "+ Consigner un essai"))));
    } else {
      const table = h("table", {});
      table.appendChild(h("thead", {}, h("tr", {},
        h("th", {}, "Essai"), h("th", {}, "Date"),
        h("th", { class: "mono" }, "CPP obtenu"), h("th", { class: "mono" }, "vs prévu"),
        h("th", {}, "Conformité"), h("th", {}, ""))));
      const corps = h("tbody", {});
      essais.forEach(e => {
        const o = cppEssaiObtenu(sc, e);
        const se = statutEssai(sc, e);
        const ecart = (o.cpp !== null && d.cpp !== null) ? o.cpp - d.cpp : null;
        corps.appendChild(h("tr", {},
          h("td", {}, e.titre || "Essai"),
          h("td", {}, e.date || "—"),
          h("td", { class: "mono" },
            o.cpp !== null ? fmt(o.cpp, 4)
              : absence(o.nbLogements ? "— " + o.nonChiffrables + " logement(s) non chiffrable(s)" : "— charnière mesurée non saisie")),
          h("td", { class: "mono" }, ecart !== null
            ? (ecart <= 0 ? h("span", { class: "juste" }, fmt(ecart, 4)) : h("span", { class: "faux" }, "+" + fmt(ecart, 4)))
            : "—"),
          h("td", {}, badge(se.code === "conforme" ? "vert" : se.code === "nonconforme" ? "rouge" : "gris", se.texte)),
          h("td", {}, h("a", { href: "javascript:void(0)", onclick: () => ouvrirPanneauEssai(ligne, ref, op, sc, e) }, "ouvrir →"))));
      });
      table.appendChild(corps);
      bloc.appendChild(table);
      bloc.appendChild(h("div", { class: "liste-actions" },
        h("button", { class: "bouton petit primaire", onclick: () => ouvrirPanneauEssai(ligne, ref, op, sc, null) }, "+ Consigner un essai")));
    }
    carte.appendChild(bloc);
  }

  /* La décomposition de l'outillage : où part l'argent. */
  if (d.cpp !== null) {
    const outillage = outillageDeScenario(sc);
    const porte = h("div", { class: "porte" });
    porte.appendChild(h("div", { class: "outil-ligne" },
      h("span", { class: "outil-numero" }, "Où part l'argent"),
      h("span", { class: "part" }, "part du CPP outillage par logement")));
    outillage.outils.forEach(o => {
      const bloc = h("div", { class: "outil-bloc" });
      bloc.appendChild(h("div", { class: "outil-ligne" },
        h("span", { class: "outil-numero" }, o.numero),
        o.description ? h("span", { class: "outil-desc" }, o.description) : null,
        o.correcteur ? h("span", { class: "outil-desc" }, "correcteur " + o.correcteur) : null,
        h("span", { class: "outil-cpp mono" }, o.cpp !== null ? fmt(o.cpp, 4) + " €/pièce" : "—")));
      const table = h("table", {});
      table.appendChild(h("thead", {}, h("tr", {},
        h("th", {}, "Logement"), h("th", {}, "Plaquette"), h("th", {}, "MABEC"),
        h("th", { class: "mono" }, "Prix"), h("th", { class: "mono" }, "Arêtes"),
        h("th", { class: "mono" }, "Charnière"), h("th", { class: "mono" }, "€/pièce"), h("th", { class: "mono" }, "Part"))));
      const corps = h("tbody", {});
      o.logements.forEach(l => {
        const part = (l.cpp !== null && outillage.cpp) ? Math.round(l.cpp / outillage.cpp * 100) + " %" : "—";
        corps.appendChild(h("tr", { class: l.cpp === null ? "non-chiffrable" : "" },
          h("td", {}, h("span", { class: "logement-nom" }, l.logementNom)),
          h("td", {}, l.article || "—"),
          h("td", { class: "mono" }, l.mabec || ""),
          h("td", { class: "mono" }, l.prix !== null ? fmt(l.prix, 2) : "—"),
          h("td", { class: "mono" }, l.aretes !== null ? fmt(l.aretes, 0) : "—"),
          h("td", { class: "mono" }, l.charniere !== null ? fmt(l.charniere, 0) : "—"),
          h("td", { class: "mono" }, l.cpp !== null ? fmt(l.cpp, 4) : "— non chiffrable"),
          h("td", { class: "mono part" }, part)));
      });
      table.appendChild(corps);
      bloc.appendChild(table);
      porte.appendChild(bloc);
    });
    carte.appendChild(porte);
  }

  /* Les projets posés sur CE scénario. */
  const pjIci = projetsDeScenario(ETAT, ligne.id, ref.id, op.id, sc.id);
  if (pjIci.length) {
    carte.appendChild(h("div", { class: "etiquettes", style: { marginTop: "10px" } },
      h("span", { style: { fontSize: "12px", color: "var(--label)" } }, "projets : "),
      pjIci.map(pj => pastilleProjet(pj, VUE.filtreProjetId === pj.id))));
  }

  return carte;
}

/* ============================================================================
   8. LES ACTIONS MÉTIER
   ========================================================================== */

/* La promotion : l'échange annoncé (v4.4 de l'app). L'ancien ★ repasse
   « Validé » — il n'a rien raté, il a été remplacé par mieux. */
function promouvoirScenario(ligne, ref, op, sc) {
  const actuel = scenarioDeProd(op.scenarios);
  confirmer(
    "« " + sc.name + " » devient le scénario de production de " + opCodeDe(op) + "."
    + (actuel ? " L'ancien (« " + actuel.name + " ») repasse en Validé." : "")
    + " Le CPP de la référence sera recalculé sur la nouvelle base.",
    "Passer en série", () => {
      (op.scenarios || []).forEach(s => {
        if (s.id === sc.id) { s.baseline = true; s.statut = "serie"; s.statutDate = new Date().toISOString().slice(0, 10); }
        else if (s.baseline) { s.baseline = false; if (s.statut === "serie") s.statut = "valide"; }
      });
      sc.modifieLe = new Date().toISOString();
      saveData();
      toast("« " + sc.name + " » est le scénario de production.");
      render();
    });
}

/* ============================================================================
   9. L'ÉCRAN EMPORTER — la page A4 pour la hiérarchie
   ========================================================================== */

function renderEmporter() {
  const rec = recapAtelier(ETAT.lignes || []);
  const page = h("div", { class: "page" });
  page.appendChild(filDOM([
    { libelle: "Accueil", action: () => aller("accueil") },
    { libelle: "Emporter" }
  ]));
  page.appendChild(h("div", { class: "page-titre" }, h("h1", {}, "La page à emporter"),
    h("span", { class: "droite liste-actions", style: { margin: 0 } },
      h("button", { class: "bouton primaire", onclick: () => window.print() }, "Imprimer / PDF"))));
  page.appendChild(h("p", { class: "sous-titre" },
    "Ce que la hiérarchie lit : les gains actés, ce qui arrive, le plan par machine. Tout chiffre remonte à sa source."));

  const a4 = h("div", { class: "a4-veille" });
  a4.appendChild(h("div", { class: "a4-entete" },
    h("div", {},
      h("div", { class: "a4-marque" }, "Suivi optimisation — disques de frein"),
      h("div", { style: { fontSize: "12px", color: "var(--label)" } },
        "usinage céramique · site Sept Fons · partenariat outillage SPK by CeramTec")),
    h("div", { class: "a4-date" }, dateCourte())));

  a4.appendChild(h("div", { class: "bandeau" },
    h("div", { class: "bloc acte" },
      h("div", { class: "etiquette" }, "Économie actée"),
      h("div", { class: "valeur" }, rec.gainAnnuelActe !== null ? fmt(rec.gainAnnuelActe, 0) : "—", h("span", { class: "unite" }, "€/an")),
      h("div", { class: "contexte" }, rec.gainAnnuelActe !== null
        ? "passée en série, volumes saisis"
        : (rec.gainActe !== null && rec.gainActe > 0 ? "gains actés mais volumes annuels non saisis" : "aucun gain passé en série pour l'instant"))),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Gains en cours"),
      h("div", { class: "valeur" }, rec.gainProjete !== null ? fmt(rec.gainProjete, 4) : "—", h("span", { class: "unite" }, "€/pièce")),
      h("div", { class: "contexte" }, "non sommés aux actés")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Décisions en attente"),
      h("div", { class: "valeur" }, String(rec.decisions)),
      h("div", { class: "contexte" }, "validés 5× + essais prometteurs")),
    h("div", { class: "bloc" },
      h("div", { class: "etiquette" }, "Lignes engagées"),
      h("div", { class: "valeur" }, rec.lignesEngagees + "/" + rec.nbLignes),
      h("div", { class: "contexte" }, "sur le parc suivi"))));

  a4.appendChild(h("h2", {}, "Le plan par machine"));
  const table = h("table", { class: "tableau" });
  table.appendChild(h("thead", {}, h("tr", {},
    h("th", {}, "Ligne"), h("th", {}, "Référence dominante"),
    h("th", { class: "mono" }, "CPP outillage"), h("th", { class: "mono" }, "Écart cible"),
    h("th", { class: "mono" }, "Décisions"), h("th", {}, "La prochaine étape"))));
  const corps = h("tbody", {});
  rec.tuiles.forEach(t => {
    const vDominante = t.postes.length ? t.postes[0].verdict : null;
    corps.appendChild(h("tr", {},
      h("td", {}, t.nom),
      h("td", {}, t.dominante ? t.dominante.ref.nom : "—"),
      h("td", { class: "mono" }, t.cpp !== null ? fmt(t.cpp, 4) : "— non chiffrable"),
      h("td", { class: "mono" }, t.distanceCible !== null
        ? (t.distanceCible > 0 ? "+" : "−") + fmt(Math.abs(t.distanceCible), 4) : "— cible non saisie"),
      h("td", { class: "mono" }, String(t.decisions)),
      h("td", {}, t.postes.length
        ? prochaineEtape(t.postes.reduce((meilleur, p) =>
          (!meilleur || (p.verdict.verdict.code !== "rien" && p.verdict.verdict.code !== "achiffrer")) ? p.verdict : meilleur, null))
        : "— aucune opération posée sur cette ligne")));
  });
  table.appendChild(corps);
  a4.appendChild(h("div", { class: "tableau-enveloppe" }, table));

  a4.appendChild(h("h2", {}, "La méthode"));
  a4.appendChild(h("p", { style: { fontSize: "12px", color: "var(--body)" } },
    "Chaque opération est travaillée opération par opération, outil par outil, logement par logement : le CPP outillage "
    + "(prix de la plaquette ramené à la pièce) est mesuré contre la cible du site, chaque candidat est éprouvé par le "
    + "protocole des 5 essais conformes (battement et Ra dans la tolérance, charnière atteinte) avant de passer en série. "
    + "Les gains actés et les gains en cours sont comptés séparément, jamais additionnés."));

  a4.appendChild(h("div", { class: "a4-pied" },
    "Suivi optimisation SPK v" + VERSION + " · SPK by CeramTec · Confidentiel interne — données locales du poste, source : "
    + (SOURCE_IMPORT || "inconnue") + " · CPP = coût outillage de la pièce, non comparable aux totaux machine."));

  page.appendChild(a4);
  return page;
}

/* ============================================================================
   10. L'ÉCRAN PROJETS — qui pilote quoi, où en sont les projets
   ========================================================================== */

function renderProjets() {
  const page = h("div", { class: "page" });
  page.appendChild(filDOM([{ libelle: "Accueil", action: () => aller("accueil") }, { libelle: "Projets" }]));
  page.appendChild(h("div", { class: "page-titre" }, h("h1", {}, "Projets"),
    h("span", { class: "droite liste-actions", style: { margin: 0 } },
      h("button", { class: "bouton primaire", onclick: () => ouvrirPanneauProjet(null) }, "+ Créer un projet"))));
  page.appendChild(h("p", { class: "sous-titre" },
    "Un projet regroupe des scénarios qui répondent à une même question — c'est une étiquette de travail, jamais un propriétaire. La bordure de carte porte la personne, la pastille porte le projet."));

  const projets = ETAT.projets || [];
  if (!projets.length) {
    page.appendChild(h("div", { class: "aucun" },
      h("span", { class: "grand" }, "Aucun projet"),
      "Créez le premier : il posera des étiquettes sur les scénarios que vous choisirez, sans rien déplacer."));
    return page;
  }

  projets.forEach(pj => {
    const resp = responsableDe(ETAT, pj);
    const lie = scenariosDeProjet(ETAT, pj);
    const carte = h("div", {
      class: "carte bordure-responsable",
      style: { "--bordure-couleur": resp ? (resp.couleur || "var(--filet-fort)") : "var(--filet-fort)" },
      onclick: () => ouvrirPanneauProjet(pj)
    });
    carte.appendChild(h("div", { class: "c-entete" },
      h("span", { class: "badge pastille", style: { background: pj.couleur || "#545e68", color: "#fff" } }, pj.nom),
      badge(PROJET_STATUTS[pj.statut] === "En cours" ? "bleu" : "contour", PROJET_STATUTS[pj.statut] || pj.statut),
      pj.dateCible ? h("span", { class: "mono", style: { color: "var(--label)", fontSize: "12px" } }, "cible " + pj.dateCible) : null,
      h("span", { class: "droite", style: { color: "var(--label)", fontSize: "12px" } },
        resp ? "piloté par " + resp.nom : "— aucun responsable")));
    if (pj.description) carte.appendChild(h("p", { style: { color: "var(--body)", fontSize: "13.5px", margin: "6px 0 10px", whiteSpace: "pre-line" } }, pj.description));
    carte.appendChild(h("div", { class: "etiquettes" },
      h("span", { style: { fontSize: "12px", color: "var(--label)" } },
        lie.lies.length + " scénario" + (lie.lies.length > 1 ? "s" : "") + " rattaché(s)"),
      lie.lies.slice(0, 6).map(x =>
        h("span", { class: "badge contour", style: { cursor: "pointer" }, onclick: (e) => { e.stopPropagation(); ouvrirPoste(x.ligne ? x.ligne.id : "", { ref: x.ref, op: x.op }); } },
          (x.ligne ? codeLigneDe(x.ligne.nom) || x.ligne.nom : "?") + " · " + opCodeDe(x.op) + " · " + x.sc.name)),
      lie.orphelins.length ? badge("ambre", lie.orphelins.length + " étiquette(s) orpheline(s) — scénario supprimé") : null));
    page.appendChild(carte);
  });

  return page;
}
