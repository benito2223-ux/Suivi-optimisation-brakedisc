# -*- coding: utf-8 -*-
"""Tour 89 (4.107.0) — tests harnais de la décomposition des leviers."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
ancre = "      } finally { lignes = lAvD; projets = pjAvD; catalogue = catAvD; }"
assert ancre in src, "ancre tests introuvable"

bloc = '''      } finally { lignes = lAvD; projets = pjAvD; catalogue = catAvD; }
    }
    {
      /* v4.107 — LA DÉCOMPOSITION DES LEVIERS (brique A) : gain vie seul /
         gain prix seul / interaction, sur le poste plaquettes SEUL, sur les
         TOTAUX (jamais un appariement logement à logement — Hermes). */
      const baseL = { outils: [ { logements: [ { prix: 10, aretes: 8, charniere: 150 } ] } ] };
      const candL = { outils: [ { logements: [ { prix: 5, aretes: 8, charniere: 300 } ] } ] };
      const dA = decompositionLeviers(baseL, candL, 450);
      /* P_base = 10/1200 × 450 = 3,75 ; P_cand = 5/2400 × 450 = 0,9375 ;
         prix seul = 50 % de P_base ; vie seule = 50 % ; combiné = 75 % ;
         interaction = 450 × 5 × (1/1200 − 1/2400) = 0,9375 — le cas 4.92 retrouvé. */
      ok("leviers : vie seule et prix seule tombent chacun à 50 % du coût de base (le cas prix ÷2 / vie ×2)",
         [Math.abs(dA.gainPrixSeul - 1.875) < 1e-9, Math.abs(dA.gainVieSeul - 1.875) < 1e-9,
          Math.abs(dA.gainPlaquettes - 2.8125) < 1e-9, Math.abs(dA.interaction - 0.9375) < 1e-9,
          Math.abs(dA.gainPrixSeul + dA.gainVieSeul - dA.interaction - dA.gainPlaquettes) < 1e-9],
         [true, true, true, true, true]);
      ok("leviers : les % parlent à Matis — +100 % de durée de vie, −50 % de prix",
         [Math.abs(dA.viePct - 100) < 1e-9, Math.abs(dA.prixBaissePct - 50) < 1e-9,
          Math.abs(dA.PBase - 3.75) < 1e-9, Math.abs(dA.PCand - 0.9375) < 1e-9],
         [true, true, true, true]);
      /* D3 : la décomposition s'aligne sur coutsDetail (le même filtre de logements) */
      const scD3 = normalizeScenario({ id: "sD3", name: "Cand", outils: [ { id: "tD3", numero: "T5", logements: [ { id: "gD3a", nom: "D1", prix: 12, aretes: 6, charniere: 80 }, { id: "gD3b", nom: "D2", prix: 38, aretes: 4, charniere: 700 } ] } ] });
      const baseD3 = normalizeScenario({ id: "sD3b", name: "Base", baseline: true, outils: [ { id: "tD3b", numero: "T5", logements: [ { id: "gD3c", nom: "D1", prix: 9.56, aretes: 8, charniere: 50 } ] } ] });
      const dD3 = decompositionLeviers(baseD3, scD3, 8000);
      ok("leviers : cohérence D3 — le gain plaquettes décomposé = l'écart coutsDetail.plaquettes × volume, au centime",
           Math.abs((dD3.gainPlaquettes) - (coutsDetail(baseD3).plaquettes - coutsDetail(scD3).plaquettes) * 8000) < 1e-9, true);
      /* OUTILS DIFFÉRENTS base/candidat : le cas où l'appariement logement à
         logement est impossible — la décomposition marche sur les totaux. */
      const dMulti = decompositionLeviers(
        { outils: [ { logements: [ { prix: 10, aretes: 8, charniere: 150 }, { prix: 38, aretes: 4, charniere: 700 } ] } ] },
        { outils: [ { logements: [ { prix: 7, aretes: 6, charniere: 90 } ] } ] }, 5000);
      ok("leviers : outils DIFFÉRENTS de part et d'autre — l'identité vie + prix − interaction = gain plaquettes tient encore (totaux, pas appariement)",
           Math.abs(dMulti.gainPrixSeul + dMulti.gainVieSeul - dMulti.interaction - dMulti.gainPlaquettes) < 1e-9, true);
      ok("leviers : condition 4 — base sans prix/DDV exploitables = non chiffrable (null, jamais 0)",
           [decompositionLeviers({ outils: [ { logements: [ { prix: "", aretes: 8, charniere: 150 } ] } ] }, candL, 450),
            decompositionLeviers(baseL, { outils: [ { logements: [ { prix: 5, aretes: 8, charniere: "" } ] } ] }, 450),
            decompositionLeviers(baseL, candL, 0)],
           [null, null, null]);
      ok("leviers : leviers qui se CONTREDISENT (prix plus cher, vie plus longue) — l'interaction devient négative, l'identité tient",
           (() => { const d = decompositionLeviers(
               { outils: [ { logements: [ { prix: 10, aretes: 8, charniere: 300 } ] } ] },
               { outils: [ { logements: [ { prix: 15, aretes: 8, charniere: 600 } ] } ] }, 900);
             return [d.interaction < 0, Math.abs(d.gainPrixSeul + d.gainVieSeul - d.interaction - d.gainPlaquettes) < 1e-9]; })(),
           [true, true]);
    }'''
src = src.replace(ancre, bloc, 1)
io.open(p, "w", encoding="utf-8").write(src)
print("tests leviers insérés")
