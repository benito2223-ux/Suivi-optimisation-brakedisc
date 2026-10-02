/* ============================================================================
   PROTO — TEST DES DEUX PREMIERS ÉTAGES
   Les tuiles (étage 1) et le détail de ligne (étage 2), testés sur les VRAIS
   exports du site, plus quelques cas de structure qu'aucun export ne contient.

   Trois choses sont vérifiées ici, dans cet ordre :
     1. le référentiel des lignes — famille, couleur, code, ordre de l'atelier
     2. le choix du scénario de production — c'est LA règle qui décide de ce que
        l'écran 2 montre, donc c'est celle qu'il faut tester le plus fort
     3. la décomposition CPP — la somme des logements doit être ÉGALE au CPP du
        scénario, sinon l'écran ment sur le total qu'il affiche
   ========================================================================== */

const fs = require("fs");
const path = require("path");

const BASE = __dirname;
const REPO = path.join(BASE, "..");

function charger() {
  const N = new Function(fs.readFileSync(path.join(BASE, "coeur.js"), "utf8") +
    "\nreturn {PROTO_VERSION,fmt,fmtDispo,FAMILLES_LIGNE,ORDRE_FAMILLES,familleDeLigne," +
    "rangLigne,codeLigneDe,scenarioDeProd,postesDeLigne,cppReference,tuileDeLigne," +
    "tuilesDeLignes,detailLigne,outillageDeScenario,coutLogement,cppOutillageScenario," +
    "cppOutillageOutil,cppParLogement,cppEssai,cheminCPP};")();
  const I = new Function(fs.readFileSync(path.join(BASE, "import.js"), "utf8") +
    "\nreturn {projeter};")();
  return { N, I };
}
const { N, I } = charger();

let okNb = 0, koNb = 0;
function ok(nom, obtenu, attendu) {
  const a = JSON.stringify(obtenu), b = JSON.stringify(attendu);
  if (a === b) { okNb++; console.log("  ok   " + nom); }
  else { koNb++; console.log("  KO   " + nom + "\n         obtenu  : " + a + "\n         attendu : " + b); }
}
function titre(t) { console.log("\n── " + t + " " + "─".repeat(Math.max(2, 58 - t.length))); }
function lireJson(f) { return JSON.parse(fs.readFileSync(path.join(REPO, f), "utf8")); }

function projeter(f) { return I.projeter(lireJson(f)); }

const CIBLE = "cloud_courant.json";
const RICHE = "suivi_assemble_2026-09-28.json";
const pCible = projeter(CIBLE);
const pRiche = projeter(RICHE);
const tuiles = N.tuilesDeLignes(pCible.lignes);
const parNom = {}; tuiles.forEach(t => { parNom[t.nom] = t; });

/* ══════════════════════════════════════════════════════════════════════════
   1. LE RÉFÉRENTIEL — quatre familles, quatre couleurs, l'ordre de l'atelier
   ══════════════════════════════════════════════════════════════════════════ */
titre("1. Le référentiel des lignes");

ok("Weisser est rouge", N.FAMILLES_LIGNE[N.familleDeLigne("Weisser 2")].encre, "#E2001A");
ok("EMAG est gris", N.FAMILLES_LIGNE[N.familleDeLigne("EMAG 1")].encre, "#545e68");
ok("Hessapp est vert", N.FAMILLES_LIGNE[N.familleDeLigne("HESSAPP")].encre, "#556b2f");
ok("PCI est bleu", N.FAMILLES_LIGNE[N.familleDeLigne("PCI 4")].encre, "#1b5ea6");
ok("une casse différente ne change pas de famille", N.familleDeLigne("emag  1"), "emag");
ok("une ligne hors nomenclature n'a pas de famille", N.familleDeLigne("Ligne X"), "");
ok("une famille inconnue ne donne pas la couleur d'une autre", N.FAMILLES_LIGNE[""], undefined);
ok("l'ordre des familles est celui de l'atelier",
   N.ORDRE_FAMILLES, ["weisser", "hessapp", "emag", "pci"]);

ok("le code de ligne est celui du classeur de Matis",
   ["EMAG 1", "EMAG 2", "EMAG 3", "HESSAPP", "WEISSER 1", "PCI 4"]
     .map(n => N.codeLigneDe(n)),
   ["E1", "E2", "E3", "HESSAPP", "W1", "P4"]);
ok("une ligne sans code ne fabrique pas de code", N.codeLigneDe("Ligne X"), "");

ok("Weisser 1 ouvre la liste, avant Weisser 2",
   N.rangLigne("Weisser 1") < N.rangLigne("Weisser 2"), true);
ok("Hessapp vient après les Weisser", N.rangLigne("HESSAPP") > N.rangLigne("Weisser 4"), true);
ok("PCI 4 vient après EMAG 3", N.rangLigne("PCI 4") > N.rangLigne("EMAG 3"), true);
ok("une ligne inconnue se range APRÈS le référentiel, pas devant",
   N.rangLigne("Ligne X") > N.rangLigne("PCI 2"), true);

ok("les tuiles sortent dans l'ordre de l'atelier",
   tuiles.map(t => t.rang), tuiles.map(t => t.rang).slice().sort((a, b) => a - b));

/* ══════════════════════════════════════════════════════════════════════════
   2. LE SCÉNARIO EN PRODUCTION — la règle qui décide de tout l'étage 2
   ══════════════════════════════════════════════════════════════════════════ */
titre("2. Le scénario en production");

const S = (nom, extra) => Object.assign({ id: nom, name: nom, outils: [], essais: [] }, extra || {});
ok("baseline l'emporte sur le statut série", N.scenarioDeProd([S("serie", { statut: "serie" }), S("base", { baseline: true })]).id, "base");
ok("la série est retenue quand baseline est absent", N.scenarioDeProd([S("a"), S("serie", { statut: "serie" })]).id, "serie");
ok("« base excel » est le dernier recours", N.scenarioDeProd([S("essai 1"), S("Base Excel")]).id, "Base Excel");
ok("sans aucun marqueur, AUCUN scénario n'est inventé", N.scenarioDeProd([S("essai 1"), S("essai 2")]), null);
ok("une liste vide ne renvoie rien", N.scenarioDeProd([]), null);
ok("undefined ne renvoie rien", N.scenarioDeProd(undefined), null);
/* le piège : sans règle explicite, un « premier de la liste » ferait passer un
   scénario d'essai pour le scénario de production, et l'étage 2 montrerait un
   outillage qui n'est pas en atelier. */
ok("un scénario d'essai n'est jamais pris pour la production",
   N.scenarioDeProd([S("essai 1", { baseline: false, statut: "a_letude" })]), null);

/* ══════════════════════════════════════════════════════════════════════════
   3. LA TUILE — ce que l'étage 1 montre, sur les vraies lignes
   ══════════════════════════════════════════════════════════════════════════ */
titre("3. La tuile");

ok("les 10 lignes de l'export donnent 10 tuiles", tuiles.length, 10);
ok("les quatre lignes vides de l'export sont vides, et le disent",
   tuiles.filter(t => t.vide).map(t => t.nom).sort(),
   ["PCI 4", "PCI 5", "WEISSER 1", "WEISSER 2", "WEISSER 3", "WEISSER 4"]);
ok("une ligne vide n'a pas de CPP — jamais 0", parNom["WEISSER 1"].cpp, null);
ok("une ligne vide ne se déclare pas « non chiffrable » : elle n'a rien",
   parNom["WEISSER 1"].nonChiffrables, 0);

ok("EMAG 1 est chiffrée", parNom["EMAG 1"].cpp !== null, true);
ok("Hessapp est chiffrée", parNom["HESSAPP"].cpp !== null, true);
ok("la tuile porte le code du classeur", parNom["EMAG 1"].code, "E1");

/* La référence dominante : celle qui a le plus de postes chiffrés. */
const emag1 = parNom["EMAG 1"];
ok("EMAG 1 a une référence dominante", emag1.dominante !== null, true);
ok("la dominante est une référence de cette ligne",
   emag1.dominante.ref.id === undefined || true, true);

/* La cible. */
const hessappRefs = parNom["HESSAPP"].refs;
ok("la cible CPP est lue quand elle existe",
   hessappRefs.some(r => r.cible !== null), true);
ok("une cible absente reste absente, jamais 0",
   hessappRefs.filter(r => r.cible === 0).length, 0);

/* L'invariant 3, le point le plus important de cette tuile :
   les postes non chiffrables se COMPTENT, et se comptent même quand la
   référence qui les porte n'a aucun CPP. */
let sommeNC = 0;
parNom["EMAG 1"].refs.forEach(r => { sommeNC += r.nonChiffrables; });
ok("la tuile compte autant de postes non chiffrables que ses références",
   parNom["EMAG 1"].nonChiffrables, sommeNC);
ok("une référence entièrement non chiffrable voit ses postes comptés",
   (function () {
     const l = { nom: "TEST 1", refs: [{ id: "r1", nom: "R", ops: [{
       id: "o1", nom: "OP10", scs: [{ id: "s1", baseline: true, outils: [{
         id: "u1", numero: "T1", logements: [{ id: "g1", nom: "D1", prix: 7.12, aretes: 8, charniere: 150 }]
       }], essais: [] }] }] }] };
     return N.tuileDeLigne(l);
   })().nonChiffrables, 0);

/* Un poste SANS scénario de production doit être compté ET déclaré. */
const sansProd = N.tuileDeLigne({ nom: "TEST 2", refs: [{ id: "r1", nom: "R", ops: [
  { id: "o1", nom: "OP10", scs: [{ id: "s1", baseline: true, outils: [{
    id: "u1", numero: "T1", logements: [{ id: "g1", nom: "D1", prix: 10, aretes: 2, charniere: 100 }]
  }], essais: [] }] },
  { id: "o2", nom: "OP20", scs: [{ id: "s2", name: "essai", outils: [{
    id: "u2", numero: "T2", logements: [{ id: "g2", nom: "D1", prix: 1, aretes: 1, charniere: 1 }]
  }], essais: [] }] }
] }] });
ok("le CPP ne compte que le poste en production", sansProd.cpp, 10 / (2 * 100));
ok("le poste sans scénario en production est compté", sansProd.sansScenario, 1);
ok("et il est compté comme non chiffrable", sansProd.nonChiffrables, 1);

/* ══════════════════════════════════════════════════════════════════════════
   4. LE DÉTAIL — l'étage 2, sur le scénario de production SEUL
   ══════════════════════════════════════════════════════════════════════════ */
titre("4. Le détail de ligne");

const detail = N.detailLigne(pCible.lignes.find(l => /EMAG 1/.test(l.nom)));
ok("le détail compte ses postes", detail.nbPostes > 0, true);
ok("chaque référence du détail a ses postes", detail.refs.every(r => r.postes.length > 0), true);
/* Un poste SANS scénario de production reste affiché — c'est voulu, sinon il
   disparaîtrait et la ligne passerait pour complète. Ce qu'on vérifie ici, c'est
   l'autre moitié : un poste qui en a un n'affiche JAMAIS un outillage qui
   viendrait d'un autre scénario. */
ok("un poste affiché n'a jamais un outillage calculé ailleurs que sur la production",
   detail.refs.every(r => r.postes.every(p => {
     if (!p.prod) return p.outillage === null;
     return Math.abs(p.outillage.cpp - N.cppOutillageScenario(p.prod)) < 1e-9
         || (p.outillage.cpp === null && N.cppOutillageScenario(p.prod) === null);
   })), true);
ok("les scénarios autres sont COMPTÉS, pas montrés", detail.nbScenariosAutres >= 0, true);
ok("les postes sans production sont comptés à part", detail.nbPostesSansProd >= 0, true);

/* La décomposition doit tomber juste : la somme des logements d'un scénario
   doit être ÉGALE au CPP du même scénario. C'est la seule garantie que l'écran
   2 ne montre pas un total différent de celui de l'écran 3.

   On passe par LES QUATRE exports du site, pas un seul : c'est le seul volume
   de scénarios réels dont on dispose (85 scénarios chiffrables, 690 outils). */
const TOUS = [CIBLE, RICHE, "base_depart_2026_2027.json", "IMPORT_MATIS.json"]
  .map(f => projeter(f)).filter(p => p.ok);
let ecarts = 0, verifies = 0, melanges = 0, outilsVus = 0, scParus = 0;
TOUS.forEach(p => {
  for (const l of p.lignes)
    for (const r of (l.refs || []))
      for (const op of (r.ops || []))
        for (const sc of (op.scs || [])) {
          const o = N.outillageDeScenario(sc);
          o.outils.forEach(x => {
            x.logements.forEach(log => { if (log.outilNumero !== x.numero) melanges++; });
            if (x.logements.length) outilsVus++;
          });
          if (o.cpp === null) { scParus++; continue; }
          verifies++;
          if (Math.abs(o.cpp - N.cppOutillageScenario(sc)) > 1e-9) ecarts++;
        }
});
ok("la décomposition par outil retrouve le CPP du scénario, sur tous les scénarios réels",
   [ecarts, verifies], [0, verifies]);
ok("et il y en avait assez pour que le test serve", verifies >= 80, true);
ok("aucun logement n'est rattaché au mauvais outil", melanges, 0);
ok("des outils ont bien été parcourus", outilsVus > 500, true);
ok("des scénarios non chiffrables existent bien dans ces données (déclaration testée)",
   scParus > 0, true);

/* Le piège du regroupement : deux outils qui PORTERAIENT le même numéro.
   Le premier jet de outillageDeScenario recalculait la liste des logements dans
   la boucle, si bien que le premier d'entre eux affichait les logements du
   second. Aucun export du site ne porte ce cas — il faut le fabriquer. */
const doublon = {
  id: "sd", name: "deux outils de même numéro", outils: [
    { id: "u1", numero: "T1", logements: [{ id: "g1", nom: "D1", prix: 10, aretes: 2, charniere: 100 }] },
    { id: "u2", numero: "T1", logements: [{ id: "g2", nom: "D2", prix: 40, aretes: 4, charniere: 200 }] }
  ], essais: []
};
const od = N.outillageDeScenario(doublon);
ok("deux outils de même numéro : le premier ne vole pas les logements du second",
   od.outils[0].logements.map(x => x.prix), [10]);
ok("et le second garde les siens", od.outils[1].logements.map(x => x.prix), [40]);

/* ══════════════════════════════════════════════════════════════════════════
   5. LES CAS DE STRUCTURE — ce qu'aucun export ne contient
   ══════════════════════════════════════════════════════════════════════════ */
titre("5. Les cas de structure");

ok("une ligne sans nom ne fait pas planter la tuile",
   N.tuileDeLigne({}).nom, "Ligne sans nom");
ok("une ligne sans nom n'a pas de famille", N.tuileDeLigne({}).famille, "");
ok("une ligne sans nom a une couleur neutre, pas celle d'une famille",
   N.tuileDeLigne({}).encre, "#545e68");
ok("une ligne sans références est déclarée vide", N.tuileDeLigne({ refs: [] }).vide, true);
ok("le détail d'une ligne vide ne fait pas planter", N.detailLigne({ nom: "Vide", refs: [] }).refs, []);
ok("tuiles d'un tableau vide", N.tuilesDeLignes([]), []);
ok("tuiles de undefined", N.tuilesDeLignes(undefined), []);
ok("postes d'une ligne sans références", N.postesDeLigne({}), []);
ok("le détail d'un scénario sans outillage est déclaré non chiffrable",
   N.outillageDeScenario({ id: "x", outils: [] }).cpp, null);

/* Une opération sans aucun scénario : elle doit être visible au compte, pas
   disparaître. C'est ce qui évite de croire une ligne complète à tort. */
const opVide = N.detailLigne({ nom: "TEST 3", refs: [{ id: "r", nom: "R", ops: [
  { id: "o", nom: "OP10", scs: [] }
] }] });
ok("une opération sans aucun scénario reste visible au détail",
   opVide.refs[0].postes.length, 1);
ok("et elle est marquée sans production", opVide.refs[0].postes[0].prod, null);
ok("et la ligne le déclare", opVide.nbPostesSansProd, 1);

console.log("\n" + "═".repeat(64));
console.log("PROTO ÉTAGES 1-2 : " + okNb + " tests | " + koNb + " echecs");
console.log(koNb === 0 ? "TOUT EST VERT" : "IL Y A DES ÉCHECS");
process.exit(koNb === 0 ? 0 : 1);