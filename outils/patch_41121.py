# -*- coding: utf-8 -*-
"""Tour 96 — v4.112.1 — LE CORRECTIF CRITIQUE de la répétition générale.

`consoSemaines`, `planReglages`, `consoReelle`, `planSource` étaient déclarées
lignes ~16719-16722, APRÈS l'appel `loadAll()` (~3904). Leur assignation dans
loadAll lève une ReferenceError (TDZ), avalée par le catch silencieux : les
données réelles retombent sur l'EXEMPLE — et le premier saveData écraserait
le localStorage. Présent depuis 4.101.1 (21/10) ; invisible au harnais
(localStorage stubbé vide) ; frôlé au Tour 94 (« loadAll manuel ») sans
diagnostic. Vu le 26/10 par la répétition générale pré-prod, à la question de
Benjamin : « aucune friction à Matis ».

Le correctif : les 4 déclarations montent AVANT loadAll (le piège documenté
au topo le demandait), et une PORTE runTests garde l'avenir : un état présent
au chargement doit se charger, jamais l'exemple."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()
n0 = len(s)


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. retirer les 4 déclarations de leur place fautive ──────────────────────
remplace(
"""let consoSemaines = 52;   /* v4.90 — l'extrapolation × 52 devient un réglage éditable */
let planReglages = { relSpk: 100 };  /* v4.90 — l'hypothèse de durée de vie sort du code (revue Claude P3) ; v4.103.0 — le prix SPK défaut sort du code À SON TOUR (décision Benjamin du 20/10, désormais dans la SOURCE et plus seulement dans le build : chaque plaquette a son prix) */
let consoReelle = null;   /* { lueLe, fichiers: [], parArticle: { ART: { qtySemaine, lignes: [] } } } */
let planSource = "theo";  /* "theo" | "reel" | "annuel" */

/* ═══ v4.92 — LA CONSOMMATION ANNUELLE 2025""",
"""/* v4.112.1 — les quatre déclarations qui vivaient ici (consoSemaines,
   planReglages, consoReelle, planSource) sont montées avant loadAll() :
   déclarées après son appel, leur assignation au chargement levait une
   ReferenceError TDZ avalée par le catch silencieux — les données réelles
   retombaient sur l'exemple (vu par la répétition générale pré-prod). */

/* ═══ v4.92 — LA CONSOMMATION ANNUELLE 2025""",
"1. retrait des 4 déclarations fautives")

# ── 2. les repose avant loadAll, avec les autres états du suivi ─────────────
remplace(
"""let conso2025 = null;
let conso2025SectionsOn = null; /* Set des postes retenus — null = tous (état de session) */
""",
"""let conso2025 = null;
let conso2025SectionsOn = null; /* Set des postes retenus — null = tous (état de session) */
/* v4.112.1 — ces quatre états sont déclarés ICI, AVANT l'appel loadAll()
   (le piège TDZ du cahier : une globale assignée dans loadAll mais déclarée
   après son appel lève silencieusement, et les données réelles retombent sur
   l'exemple). Elles vivaient près du lecteur de classeurs — la place du
   CALCUL, pas celle du CHARGEMENT. */
let consoSemaines = 52;   /* v4.90 — l'extrapolation × 52 devient un réglage éditable */
let planReglages = { relSpk: 100 };  /* v4.90 — l'hypothèse de durée de vie sort du code (revue Claude P3) ; v4.103.0 — le prix SPK défaut sort du code À SON TOUR (décision Benjamin du 20/10 : chaque plaquette a son prix) */
let consoReelle = null;   /* { lueLe, fichiers: [], parArticle: { ART: { qtySemaine, lignes: [] } } } */
let planSource = "theo";  /* "theo" | "reel" | "annuel" */
""",
"2. déclarations montées avant loadAll")

# ── 3. la porte runTests : un état présent ne retombe jamais sur l'exemple ──
remplace(
"""          ok("badge codification : la fiche « Scénarios en validation » porte le badge — état et codification visibles ensemble",
             [planScenariosHTML(recapB).indexOf("codification attendue") > -1,
              planScenariosHTML(recapB).indexOf("En série — gain acté") > -1],
             [true, true]);
        } finally { catalogue = catAvB; }
      }""",
"""          ok("badge codification : la fiche « Scénarios en validation » porte le badge — état et codification visibles ensemble",
             [planScenariosHTML(recapB).indexOf("codification attendue") > -1,
              planScenariosHTML(recapB).indexOf("En série — gain acté") > -1],
             [true, true]);
        } finally { catalogue = catAvB; }
      }
      {
        /* v4.112.1 — LA PORTE TDZ (le bug vu par la répétition générale
           pré-prod du 26/10) : une globale assignée dans loadAll() mais
           déclarée après son appel lève ReferenceError, avalée par le catch
           silencieux — un état PRÉSENT au chargement retombait sur l'exemple
           (depuis la 4.101.1, invisible ici parce que le localStorage du
           harnais était vide). On rejoue le chargement avec un état : il doit
           se charger ENTIER — lignes, catalogue, conso2025. */
        const mem = {};
        const lsAvant = localStorage;
        global.localStorage = { getItem: k => (k in mem ? mem[k] : null),
                                setItem: (k, v) => { mem[k] = String(v); },
                                removeItem: k => { delete mem[k]; },
                                clear: () => { Object.keys(mem).forEach(k => delete mem[k]); } };
        const etatAv = [lignes, activeLigneId, activeReferenceId, activeOpId, data, config, activeId, catalogue, conso2025];
        try {
          mem["spk_suivi_optimisation_v1"] = JSON.stringify({ format: 8,
            lignes: [ normalizeLigne({ id: "lTdz", nom: "EMAG 1", references: [ normalizeReference({ id: "rTdz", nom: "356x26",
              productionAnnuelle: 10000, ops: [ normalizeOp({ id: "oTdz", nom: "OP10", opCode: "OP10",
                scenarios: [ normalizeScenario({ id: "sTdzB", name: "Base TDZ", baseline: true }) ] }) ] }) ] }) ],
            catalogue: [ { mabec: "TDZ 001" } ],
            conso2025: { parMabec: { "TDZ 001": { parSection: { "PCI": 100 } } } } });
          loadAll();
          ok("porte TDZ : un état présent au chargement se charge ENTIER — jamais l'exemple (toute globale de loadAll se déclare avant son appel)",
             [ lignes.length, (lignes[0] || {}).id, catalogue.some(a => a.mabec === "TDZ 001"),
               !!(conso2025 && conso2025.parMabec && conso2025.parMabec["TDZ 001"]),
               (data[0] || {}).name ],
             [ 1, "lTdz", true, true, "Base TDZ" ]);
        } finally {
          delete mem["spk_suivi_optimisation_v1"];
          global.localStorage = lsAvant;
          [lignes, activeLigneId, activeReferenceId, activeOpId, data, config, activeId, catalogue, conso2025] = etatAv;
        }
      }""",
"3. porte TDZ dans runTests")

# ── 4. version + NOUVEAUTES ──────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.112.0";', 'const TOOL_VERSION = "4.112.1";', "4a. TOOL_VERSION")

remplace(
"""const NOUVEAUTES = [
  { version:"4.112.0", date:"26/10/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.112.1", date:"26/10/2026", points:[
    "<b>Correctif silencieux mais critique</b> — trouvé en répétition générale avant la mise en prod : depuis le 21/10, l'ouverture de l'outil avec des données existantes pouvait <b>retomber par erreur sur le jeu d'exemple</b> (quatre réglages internes se lisaient trop tôt ; la moindre saisie ultérieure aurait alors écrasé les vraies données). Corrigé et désormais <b>gardé par un test</b> : un état présent au chargement se charge toujours en entier."
  ]},
  { version:"4.112.0", date:"26/10/2026", points:[""",
"4b. entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch 4.112.1 posé :", n0, "->", len(s))
