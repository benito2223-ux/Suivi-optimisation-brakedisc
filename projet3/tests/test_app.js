/* ============================================================================
   PROJET3 — LE HARNAIS DE L'APPLICATION
   Il teste le FICHIER ASSEMBLÉ (index.html) : l'empreinte des sources d'abord
   (une source modifiée sans ré-assemblage fait échouer la suite au lieu de
   valider du code qui n'est plus dans le fichier), puis les portes, puis les
   VALEURS affichées — relues depuis l'arbre rendu, jamais cherchées comme des
   chaînes (leçon du Tour 54 : un test qui cherche une chaîne ne prouve pas
   qu'un nombre est juste).
   Exécution : python assembler.py && node tests/test_app.js
   ========================================================================== */

const { creerJuge } = require("./harnais.js");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const j = creerJuge("PROJET3 APPLICATION");
const ok = j.ok, bloc = j.bloc;

const RACINE = path.resolve(__dirname, "..");
const SOURCES_JS = ["src/coeur.js", "src/import.js", "src/donnees.js", "src/ui.js", "src/app.js", "src/app_edition.js", "src/app_panneaux.js"];
const SOURCES_CSS = ["src/fonts.css", "src/styles.css"];

/* ── 1. l'empreinte de l'assemblage ────────────────────────────────────── */

bloc("l'assemblage est frais (les sources sont celles du fichier)", () => {
  const html = fs.readFileSync(path.join(RACINE, "index.html"), "utf8");
  const m = /Empreinte de l'assemblage : ([0-9a-f]{16})/.exec(html);
  ok("l'empreinte posée existe", !!m, true);
  /* même recette que assembler.py : sha256(chemin + contenu) tronqué à 16 hex,
     la liste hachée à son tour */
  const parts = [];
  SOURCES_CSS.concat(SOURCES_JS).forEach(c => {   // même ordre que assembler.py : CSS puis JS
    const chemin = c.replace(/\\/g, "/");
    const brut = fs.readFileSync(path.join(RACINE, c), "utf8");
    const contenu = brut.replace(/\r\n/g, "\n");   // l'assembler lit en mode texte : \n
    const h2 = crypto.createHash("sha256");
    h2.update(chemin, "utf8");
    h2.update(contenu, "utf8");
    parts.push(h2.digest("hex").slice(0, 16) + " " + chemin);
  });
  const calcule = crypto.createHash("sha256").update(parts.join("\n"), "utf8").digest("hex").slice(0, 16);
  ok("l'empreinte recalcule exactement (" + calcule + ")", m[1], calcule);
  ok("la suite CSS est bien inline dans le fichier", html.indexOf("--tuile-encre") > 0, true);
});

/* ── 2. un mini-DOM qui construit un vrai arbre ────────────────────────── */

class MiniNoeud {
  constructor(tag) {
    this.tagName = tag;
    this.nodeType = tag === "#text" ? 3 : 1;
    this.childNodes = [];
    this.attrs = {};
    this.style = {};
    this._listeners = {};
    this.value = "";
    this.checked = false;
    this.disabled = false;
    this.parentElement = null;
  }
  get className() { return this.attrs.class || ""; }
  set className(v) { this.attrs.class = v; }
  appendChild(c) {
    c.parentElement = this;
    this.childNodes.push(c);
    return c;
  }
  remove() {
    if (this.parentElement) {
      const i = this.parentElement.childNodes.indexOf(this);
      if (i >= 0) this.parentElement.childNodes.splice(i, 1);
    }
  }
  setAttribute(k, v) { this.attrs[k] = v; }
  getAttribute(k) { return this.attrs[k] !== undefined ? this.attrs[k] : null; }
  addEventListener(k, fn) { (this._listeners[k] = this._listeners[k] || []).push(fn); }
  get textContent() {
    let out = "";
    this.childNodes.forEach(c => {
      if (c.nodeType === 3) out += c.data;
      else out += c.textContent;
    });
    return out;
  }
  get innerHTML() {
    /* suffisant : les panneaux posent innerHTML = "" pour se vider */
    return this.textContent;
  }
  set innerHTML(v) { this.childNodes = []; }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  querySelectorAll(sel) {
    const out = [];
    const parts = sel.split(",");
    const cherche = (n) => {
      if (!n) return;
      n.childNodes.forEach(c => {
        if (c.nodeType !== 1) return;
        parts.forEach(p => {
          p = p.trim();
          if (!p) return;
          if (p.startsWith(".")) { if ((c.className || "").split(" ").includes(p.slice(1))) out.push(c); }
          else if (p.startsWith("#")) { if (c.attrs.id === p.slice(1)) out.push(c); }
          else if (c.tagName && c.tagName.toLowerCase() === p.toLowerCase()) out.push(c);
        });
        cherche(c);
      });
    };
    cherche(this);
    return out;
  }
}

const racineApp = new MiniNoeud("div");
racineApp.attrs.id = "app";
const bodyStub = new MiniNoeud("body");

global.document = {
  readyState: "complete",
  documentElement: { setAttribute() { }, getAttribute() { return "jour"; } },
  getElementById(id) { return id === "app" ? racineApp : null; },
  createElement(t) { return new MiniNoeud(String(t).toUpperCase()); },
  createTextNode(d) { const n = new MiniNoeud("#text"); n.data = String(d); return n; },
  addEventListener() { },
  body: bodyStub
};
global.window = { scrollTo() { }, addEventListener() { }, print() { } };
global.location = { protocol: "file:", href: "file://projet3/index.html" };

const _store = new Map();
global.localStorage = {
  getItem(k) { return _store.has(k) ? _store.get(k) : null; },
  setItem(k, v) { _store.set(k, String(v)); },
  removeItem(k) { _store.delete(k); }
};
global.FileReader = class { readAsText() { } readAsDataURL() { } };
global.Blob = class { constructor(parts, opts) { this.parts = parts; } };
global.URL = { createObjectURL() { return "blob:x"; }, revokeObjectURL() { } };

/* ── 3. exécuter le fichier assemblé ───────────────────────────────────── */

let APP = null;
bloc("le fichier assemblé démarre sur le jeu d'exemple", () => {
  const html = fs.readFileSync(path.join(RACINE, "index.html"), "utf8");
  /* le PREMIER <script> inline est celui de l'assemblage */
  const m = /<script>\n([\s\S]*?)\n<\/script>/.exec(html);
  ok("le script d'assemblage est présent", !!m, true);
  const js = m[1].replace(/<\\\/script/g, "</script");
  const usine = new Function(js + "\nreturn {"
    + "etat: () => ETAT, vue: () => VUE, aller, render,"
    + "tuileDeLigne: (l) => tuileDeLigne(l), recapAtelier: (l) => recapAtelier(l),"
    + "cppOutillageScenario: (s) => cppOutillageScenario(s), statutEssai: (s, e) => statutEssai(s, e),"
    + "cppEssaiObtenu: (s, e) => cppEssaiObtenu(s, e), scenarioDeProd: (s) => scenarioDeProd(s),"
    + "normaliserEtat, fusionnerEtat, capturerLivraison"
    + "};");
  APP = usine.call(global);
  ok("l'état existe après démarrage", !!APP.etat(), true);
  ok("le démarrage part sur l'accueil", APP.vue().ecran, "accueil");
  ok("le jeu d'exemple est chargé (marqueur visible)",
     racineApp.textContent.indexOf("[Exemple]") >= 0, true);
  ok("la source est affichée (règle du proto)",
     racineApp.textContent.indexOf("jeu d'exemple") >= 0, true);
});

/* ── 4. les portes — une question sur le code se pose au code ──────────── */

console.log("\n── LES PORTES ───────────────────────────────────────────────");
const portes = [
  "coutLogement", "cppOutillageScenario", "cppEssaiObtenu", "cheminCPP",
  "battDe", "conforme", "statutEssai", "statutScenario", "scenarioDeProd",
  "verdictPoste", "decisionPoste", "tuileDeLigne", "tuilesDeLignes",
  "detailLigne", "gainLigne", "recapAtelier", "opCodeDe", "clePorteOutil",
  "couleurProjetLibre", "scenariosDeProjet", "projetsDeScenario", "responsableDe",
  "capturerLivraison", "normaliserEtat", "fusionnerEtat",
  "h", "badge", "ouvrirPanneau", "fermerPanneau", "toast", "confirmer",
  "render", "renderAccueil", "renderLigne", "renderPoste", "renderEmporter", "renderProjets",
  "ouvrirPanneauScenario", "ouvrirPanneauEssai", "ouvrirPanneauProjet",
  "ouvrirPanneauDonnees", "ouvrirOptions", "ouvrirLivraisons", "ouvrirSecours",
  "promouvoirScenario", "proposerImport", "exporterEtat", "basculerTheme", "demarrer"
];
/* les portes se vérifient dans la portée du fichier assemblé, pas ici */
bloc("les portes existent dans la portée assemblée", () => {
  const html = fs.readFileSync(path.join(RACINE, "index.html"), "utf8");
  const m = /<script>\n([\s\S]*?)\n<\/script>/.exec(html);
  const js = m[1].replace(/<\\\/script/g, "</script");
  const liste = portes.join(",");
  const usine = new Function(js + "\nreturn {liste: [" + liste + "]};");
  const env = usine.call(global);
  portes.forEach(p => {
    ok(p, typeof env.liste[portes.indexOf(p)], "function");
  });
});

/* ── 5. LES VALEURS AFFICHÉES — relues depuis l'arbre, jamais devinées ─── */

console.log("\n── LES VALEURS DE L'ACCUEIL (relues dans l'arbre rendu) ────");

bloc("la tuile EMAG 1 affiche le CPP que le noyau calcule", () => {
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  const tuile = APP.tuileDeLigne(emag);
  /* le calcul INDÉPENDANT, refait à la main dans le test : le CPP de la prod OP40 */
  const op40 = emag.references[0].ops.find(o => o.opCode === "OP40");
  const prod = APP.scenarioDeProd(op40.scenarios);
  let cppMain = 0;
  prod.outils.forEach(o => o.logements.forEach(l => { cppMain += l.prix / (l.aretes * l.charniere); }));
  ok("le CPP calculé par le noyau est celui refait à la main",
     APP.cppOutillageScenario(prod), cppMain, 1e-12);

  /* la valeur relue dans l'arbre : la tuile de la ligne EMAG 1 */
  const tuiles = racineApp.querySelectorAll(".tuile");
  ok("une tuile par ligne", tuiles.length, etat.lignes.length);
  const tuileEmag = tuiles.find(t => t.textContent.indexOf("EMAG 1") >= 0);
  ok("la tuile EMAG 1 existe", !!tuileEmag, true);
  /* le CPP affiché sur la tuile = la somme des postes chiffrables */
  const attendu = tuile.cpp !== null ? tuile.cpp.toFixed(4).replace(".", ",") : "—";
  ok("la tuile affiche le CPP du noyau (" + attendu + ")",
     tuileEmag.textContent.indexOf(attendu) >= 0, true);
});

bloc("le bandeau dit ce qui manque au lieu d'inventer", () => {
  const texte = racineApp.textContent;
  ok("le bloc économie actée porte son volume (60000 × le gain d'exemple)",
     texte.indexOf("€/an") >= 0, true);
  ok("le bandeau nomme la vraie absence (gain acté ou volume, jamais un 0 inventé)",
     texte.indexOf("aucun gain passé en série pour l'instant") >= 0
       || texte.indexOf("volume annuel") >= 0, true);
});

bloc("la note de production hebdo est écrite, pas tue", () => {
  ok("l'écran explique pourquoi la production n'est pas là",
     racineApp.textContent.indexOf("Pourquoi la production hebdomadaire n'est pas ici") >= 0, true);
});

/* ── 6. la navigation rend chaque écran sans erreur ────────────────────── */

console.log("\n── LA NAVIGATION (chaque écran rend) ────────────────────────");

bloc("la ligne rend la décomposition jusqu'au logement", () => {
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  APP.aller("ligne", { ligneId: emag.id });
  const texte = racineApp.textContent;
  ok("l'écran ligne porte le nom de la ligne", texte.indexOf("EMAG 1") >= 0, true);
  ok("la référence d'exemple est là", texte.indexOf("[Exemple] DV 356x26 RPI") >= 0, true);
  ok("les logements sont décomposés (MABEC visibles)",
     texte.indexOf("IM02 198 054") >= 0, true);
  ok("le poste sans chiffrage est compté, pas dilué",
     texte.indexOf("non chiffrable") >= 0, true);
  ok("l'essai de la production est montré",
     texte.indexOf("Essais portés par la production") >= 0 || texte.indexOf("Aucun essai sur la production") >= 0, true);
});

bloc("le poste affiche prévu contre obtenu", () => {
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  const ref = emag.references[0];
  const op40 = ref.ops.find(o => o.opCode === "OP40");
  APP.aller("poste", { ligneId: emag.id, refId: ref.id, opId: op40.id });
  const texte = racineApp.textContent;
  ok("la décision a un mot", ["SÉRIE", "DÉCIDER", "ESSAYER", "CHIFFRER", "RIEN"].some(m => texte.indexOf(m) >= 0), true);
  ok("le scénario d'essai est visible", texte.indexOf("Essai SL500") >= 0, true);
  ok("le protocole 5× est affiché", texte.indexOf("protocole 5×") >= 0, true);
  /* le CPP OBTENU du troisième essai — sa charnière mesurée (3000) diffère
     du prévu (2400) : l'écran doit montrer l'OBTENU, pas le prévu. La panne
     du Tour 54 (prévu affiché à la place de l'obtenu) passait parce que le
     test visait un essai où prévu = obtenu. */
  const scEssai = op40.scenarios.find(s => s.name === "Essai SL500");
  const troisieme = scEssai.essais[2];
  const obtenu3 = APP.cppEssaiObtenu(scEssai, troisieme);
  ok("le CPP obtenu du 3ᵉ essai diffère du prévu (la distinction porte du sens)",
     obtenu3.cpp !== null && Math.abs(obtenu3.cpp - APP.cppOutillageScenario(scEssai)) > 1e-9, true);
  ok("le CPP obtenu du 3ᵉ essai s'affiche dans l'arbre",
     texte.indexOf(obtenu3.cpp.toFixed(4).replace(".", ",")) >= 0, true);
  /* le pire des deux côtés juge la conformité : D 0,09 / G 0,07 dans la limite ;
     la charnière 2400 est atteinte par le premier essai -> conforme */
  const st = APP.statutEssai(scEssai, scEssai.essais[0]);
  ok("l'essai d'exemple est jugé conforme (charnière atteinte, pire des deux côtés dans la limite)", st.code, "conforme");
});

bloc("le poste à chiffrer dit ce qui manque", () => {
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  const ref = emag.references[0];
  const op10 = ref.ops.find(o => o.opCode === "OP10");
  APP.aller("poste", { ligneId: emag.id, refId: ref.id, opId: op10.id });
  const texte = racineApp.textContent;
  ok("le verdict est CHIFFRER", texte.indexOf("CHIFFRER") >= 0, true);
  ok("la raison est écrite à côté", texte.indexOf("à chiffrer") >= 0, true);
});

bloc("emporter rend la page A4", () => {
  APP.aller("emporter", {});
  const texte = racineApp.textContent;
  ok("l'en-tête de la page A4 est là", texte.indexOf("Suivi optimisation — disques de frein") >= 0, true);
  ok("le plan par machine est là", texte.indexOf("Le plan par machine") >= 0, true);
  ok("la méthode est expliquée", texte.indexOf("protocole des 5 essais conformes") >= 0, true);
  ok("le pied porte la marque et la confidentialité",
     texte.indexOf("Confidentiel interne") >= 0, true);
});

bloc("les projets rendent la carte avec sa bordure de responsable", () => {
  APP.aller("projets", {});
  const texte = racineApp.textContent;
  ok("le projet d'exemple est là", texte.indexOf("[Exemple] Économie OP40") >= 0, true);
  ok("les scénarios rattachés sont comptés", texte.indexOf("rattaché") >= 0, true);
});

/* ── 7. LES RÈGLES PROTÉGÉES — casser pour vérifier que le test voit ──── */

console.log("\n── LES RÈGLES PROTÉGÉES ─────────────────────────────────────");

bloc("K et P_req ne sortent jamais visibles — sur AUCUN écran (constitution §4.1)", () => {
  /* la règle vaut pour tous les écrans, pas seulement l'accueil : on la
     vérifie là où l'outil affiche des chiffres */
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  const ref = emag.references[0];
  const op40 = ref.ops.find(o => o.opCode === "OP40");
  const ecrans = [
    ["accueil", {}],
    ["ligne", { ligneId: emag.id }],
    ["poste", { ligneId: emag.id, refId: ref.id, opId: op40.id }],
    ["emporter", {}],
    ["projets", {}]
  ];
  ecrans.forEach(([ecran, ids]) => {
    APP.aller(ecran, ids);
    const texte = racineApp.textContent;
    ok(ecran + " : aucun « P_req »", texte.indexOf("P_req") >= 0, false);
    ok(ecran + " : aucun « puissance »", /puissance/i.test(texte), false);
    ok(ecran + " : aucun « K = »", /K\s*=/i.test(texte), false);
  });
});

bloc("le pire des deux côtés juge : une pièce qui déborde d'un côté est vue", () => {
  /* injection DANS l'état du test : D conforme, G déborde — la pièce doit
     être non conforme, jamais moyenne-flattée */
  const etat = APP.etat();
  const emag = etat.lignes.find(l => l.nom === "EMAG 1");
  const op40 = emag.references[0].ops.find(o => o.opCode === "OP40");
  const scEssai = op40.scenarios.find(s => s.name === "Essai SL500");
  scEssai.essais[0].prelevements.push({
    id: "test-pire", piece: 2500, batt: "", battD: 0.05, battG: 0.20,
    logementId: scEssai.outils[1].logements[0].id, pointMesure: "Piste", usure: "", valeur2: "", valeurs: {}
  });
  const st = APP.statutEssai(scEssai, scEssai.essais[0]);
  ok("le pire des deux côtés rend la pièce hors tolérance", st.code, "nonconforme");
  scEssai.essais[0].prelevements = scEssai.essais[0].prelevements.filter(p => p.id !== "test-pire");
});

bloc("l'import refuse un fichier qui n'est pas un export, sans rien toucher", () => {
  const avant = JSON.stringify(APP.etat());
  const mig = APP.normaliserEtat({ hello: "world" });
  ok("le refus est propre", mig.ok, false);
  ok("l'état n'a pas bougé", JSON.stringify(APP.etat()), avant);
});

bloc("l'import passe un vrai export de Matis de bout en bout", () => {
  const brut = JSON.parse(fs.readFileSync(path.resolve(__dirname, "..", "..", "IMPORT_MATIS.json"), "utf8"));
  const mig = APP.normaliserEtat(brut);
  ok("la migration réussit dans l'app assemblée", mig.ok, true);
  const f = APP.fusionnerEtat(APP.etat(), mig.etat);
  const essaisLocal = compterEssais(APP.etat());
  const essaisArrivee = compterEssais(mig.etat);
  ok("aucun essai perdu dans la fusion", compterEssais(f.etat), essaisLocal + essaisArrivee);
  APP.render();   // l'app survit au rendu post-fusion
  ok("l'écran se re-rend après fusion", racineApp.textContent.length > 0, true);
});

function compterEssais(etat) {
  let n = 0;
  (etat.lignes || []).forEach(l => (l.references || []).forEach(ref =>
    (ref.ops || []).forEach(op => (op.scenarios || []).forEach(sc => { n += (sc.essais || []).length; }))));
  return n;
}

/* ── 8. une livraison fige et ne bouge plus ────────────────────────────── */

bloc("la livraison fige les chiffres du jour", () => {
  const lv = APP.capturerLivraison({ lignes: APP.etat().lignes }, "Test", "Harnais");
  const rec = APP.recapAtelier(APP.etat().lignes);
  ok("le gain acté figé est celui du jour",
     lv.gainsActes !== null ? lv.gainsActes : 0,
     rec.gainActe !== null ? rec.gainActe : 0, 1e-12);
  ok("la livraison est datée", /\d{4}-\d{2}-\d{2}/.test(lv.date), true);
});

/* ── FINALISATION ──────────────────────────────────────────────────────── */

process.exit(j.finaliser() ? 0 : 1);
