# -*- coding: utf-8 -*-
"""Tour 90 (4.108.0) — tests harnais de la matrice « Où investir »."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
ancre = "      } finally { lignes = lAvD; projets = pjAvD; catalogue = catAvD; }"
assert ancre in src, "ancre tests introuvable"

bloc = '''      } finally { lignes = lAvD; projets = pjAvD; catalogue = catAvD; }
    }
    {
      /* v4.108 — LA MATRICE « OÙ INVESTIR » : cinq paniers, deux axes jamais
         fondus en un score. Un arbre à cinq OP calibrées : valide / positif /
         jamais travaillé / insuffisant (pas de volume) / arrêté (motif). */
      const cfgD = { volumeActif: true };
      const mkRefD = (refNom, opCode, prodPrix, vol, extra) => normalizeReference({ id: uid("r"), nom: refNom,
        productionAnnuelle: vol, cibleCPP: 0.2, ops: [ normalizeOp({ id: uid("o"), nom: opCode, opCode, config: Object.assign({}, defaultConfig, cfgD),
          scenarios: [ normalizeScenario(Object.assign({ id: uid("s"), name: "Base " + refNom, baseline: true, statut: "serie",
            outils: [ { id: uid("t"), numero: "T5", logements: [ { id: uid("g"), nom: "D1", codeArticle: "IM02 000 001", prix: prodPrix, aretes: 8, charniere: 100 } ] } ],
            essais: [], scrapLog: [] }, extra || {})) ] }) ] });
      const lP = normalizeLigne({ id: "lP", nom: "EMAG 1", references: [
        mkRefD("DV1", "OP10", 40, 10000, {}),
        mkRefD("DV2", "OP20", 40, 10000, {}),
        mkRefD("DV3", "OP30", 40, 10000, {}),
        mkRefD("DV4", "OP40", 40, 0, {}),
        mkRefD("DV5", "OP15", 40, 10000, {})
      ] });
      // OP10 : candidat VALIDÉ moins cher
      const op10 = lP.references[0].ops[0];
      op10.scenarios.push(normalizeScenario({ id: uid("s"), name: "Candidat validé", statut: "valide",
        outils: [ { id: uid("t"), numero: "T5", logements: [ { id: uid("g"), nom: "D1", codeArticle: "IM02 000 002", prix: 30, aretes: 8, charniere: 100 } ] } ], essais: [], scrapLog: [] }));
      // OP20 : candidat avec un ESSAI CONFORME (positif, pas validé)
      const op20 = lP.references[1].ops[0];
      const sPos = normalizeScenario({ id: uid("s"), name: "Candidat positif", statut: "essai",
        outils: [ { id: uid("t"), numero: "T5", logements: [ { id: uid("g"), nom: "D1", codeArticle: "IM02 000 003", prix: 30, aretes: 8, charniere: 100 } ] } ], essais: [], scrapLog: [] });
      const gPos = sPos.outils[0].logements[0];
      sPos.essais.push({ id: uid("e"), titre: "Essai ok", date: "2026-10-20", params: { logements: [ { outilId: sPos.outils[0].id, logementId: gPos.id, outilNumero: "T5", logementNom: "D1", vc: 200, f: 0.3, charniere: 100, suivi: true } ] },
        prelevements: [ { id: uid("p"), piece: 100, batt: "0.050", logementId: gPos.id } ] });
      op20.scenarios.push(sPos);
      // OP40 : pas de volume (insuffisant)
      // OP15 : candidat ARRÊTÉ avant charnière (échec, hors course)
      const op15 = lP.references[4].ops[0];
      const sArret = normalizeScenario({ id: uid("s"), name: "Candidat arrêté", statut: "essai",
        outils: [ { id: uid("t"), numero: "T5", logements: [ { id: uid("g"), nom: "D1", codeArticle: "IM02 000 004", prix: 30, aretes: 8, charniere: 100 } ] } ],
        essais: [ { id: uid("e"), titre: "Essai cassé", date: "2026-10-18", cloture: { motif: "casse_insert" },
          params: { logements: [ { outilId: uid("t"), logementId: uid("g"), outilNumero: "T5", logementNom: "D1", vc: 200, f: 0.3, charniere: 100, suivi: true } ] },
          prelevements: [ { id: uid("p"), piece: 40, batt: "0.200", logementId: uid("g") } ] } ], scrapLog: [] });
      op15.scenarios.push(sArret);
      const lAvP2 = lignes, pjAvP2 = projets, catAvP2 = catalogue;
      lignes = [ lP ]; projets = []; catalogue = [];
      try {
        const recap = planRecapGains();
        const d = planPrioritesData(recap);
        const parCle = cle => d.items.filter(x => x.cle === cle);
        ok("priorités : les cinq paniers trient les cinq postes calibrés — aucun poste hors panier, la production en série est hors course à courir",
           [parCle("valide").length, parCle("positifs").length, parCle("jamais").length,
            parCle("insuffisant").length, parCle("arrete").length, d.dejaEnSerie.nb],
           [1, 1, 1, 1, 1, 1]);
        ok("priorités : le panier VALIDÉ porte son potentiel et sa prochaine étape ; la FACILITÉ dit le geste",
           [parCle("valide")[0].scenario, parCle("valide")[0].potentiel > 0, parCle("valide")[0].step.indexOf("série") > -1],
           ["Candidat validé", true, true]);
        ok("priorités : le panier POSITIF compte les essais conformes contre le protocole",
           [parCle("positifs")[0].step.indexOf("1 essai(s) conforme(s)") > -1, parCle("positifs")[0].step.indexOf("5×") > -1],
           [true, true]);
        ok("priorités : le panier INSUFFISANT nomme ce qui manque (le volume), jamais un zéro",
           parCle("insuffisant")[0].manques.join("|").indexOf("volume annuel") > -1, true);
        ok("priorités : le panier ARRÊTÉ porte le motif en toutes lettres (Hermes — le cas SN60)",
           parCle("arrete")[0].motifs.join("|").indexOf("arrêté avant sa charnière") > -1, true);
        ok("priorités : le panier JAMAIS TRAVAILLÉ porte la dépense comme axe potentiel",
           [parCle("jamais").length, parCle("jamais")[0].depense > 0], [1, true]);
        /* l'univers plaquettes : un article de la base 2025 sans lien outillage
           sort sur la ligne explicite, jamais dans un panier */
        const cAv = conso2025;
        conso2025 = normalizeConso2025({ lueLe: "24/10/2026", fichier: "test.xlsx",
          parMabec: { "IM02 000 001": { parSection: { "OP 10": 5000 } }, "EMBOUT D13": { parSection: { "OP 10": 1831 } } } });
        const d2 = planPrioritesData(recap);
        conso2025 = cAv;
        ok("priorités : l'univers plaquettes — l'EMBOUT (sans lien outillage) sort sur la ligne explicite, l'article outillé reste dedans",
           [d2.horsArticles.length, d2.horsArticles[0].mabec, d2.horsTotal > 0], [1, "EMBOUT D13", true]);
      } finally { lignes = lAvP2; projets = pjAvP2; catalogue = catAvP2; }
    }'''
src = src.replace(ancre, bloc, 1)
io.open(p, "w", encoding="utf-8").write(src)
print("tests priorités insérés")
