# -*- coding: utf-8 -*-
"""Tour 88 (4.106.0) — tests harnais : codification + dossier de visite."""
import io

p = "bilan_economique.html"
src = io.open(p, encoding="utf-8").read()
ancre = "      } finally { lignes = lAvX; }"
assert ancre in src, "ancre tests introuvable"

bloc = '''      } finally { lignes = lAvX; }
    }
    {
      /* v4.106 — LA CODIFICATION (sémantique Benjamin 23/10) : DEUX dates par
         article, dérivées au scénario (posé sur l'ARTICLE — Hermes Q2) ; la
         couche « base excel » est hors exigence. Et le dossier de visite :
         agrégation pure (essais, gains qualifiés BADP/cycle standard, bloqués,
         projets ouverts tous âges). */
      ok("codification : trois états par article — non demandée, demandée (âge), codifiée",
         [etatCodification(null).etat,
          etatCodification({ codificationDemandeeLe: "2026-10-01" }).etat,
          etatCodification({ codificationDemandeeLe: "2026-10-01" }).jours === joursDepuis("2026-10-01"),
          etatCodification({ codifieLe: "2026-08-01" }).etat,
          etatCodification({ codifieLe: "2026-08-01" }).le],
         ["nonDemandee", "demandee", true, "codifie", "2026-08-01"]);
      const scExcel = { name: "Prod actuelle (base excel)", outils: [ { logements: [ { codeArticle: "IM02 000 001" } ] } ] };
      const scTous = { name: "Candidat", outils: [ { logements: [ { codeArticle: "A1" }, { codeArticle: "A2" } ] } ] };
      const catTst = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "A2", codificationDemandeeLe: "2026-07-01" } ];
      const catAvT = catalogue; catalogue = catTst;
      try {
        ok("codification : la couche « base excel » est hors exigence (jamais d'article fantôme à coder)",
           codificationScenario(scExcel).etat, "sansExigence");
        ok("codification : un scénario n'est codifié que si TOUS ses articles le sont — l'écran dit lequel manque, l'âge est celui du plus vieux",
           [codificationScenario(scTous).etat,
            codificationScenario(scTous).jours === joursDepuis("2026-07-01"),
            codificationScenario(scTous).manquants.join("|").indexOf("A2") > -1],
           ["attente", true, true]);
        catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "A2", codifieLe: "2026-02-01" } ];
        ok("codification : tous les articles codifiés = scénario codifié",
           codificationScenario(scTous).etat, "codifie");
        catalogue = [ { mabec: "A1", codifieLe: "2026-01-01" }, { mabec: "INCONNU" } ];
        ok("codification : un article hors catalogue est un manquant déclaré (jamais inventé)",
           [codificationScenario(scTous).etat, codificationScenario(scTous).manquants.join("|").indexOf("hors catalogue") > -1],
           ["nonDemandee", true]);
        ok("dates : dateIsoMax garde la plus récente et tolère les vides",
           [dateIsoMax(null, "2026-01-02"), dateIsoMax("2026-01-02", "2026-03-04"), dateIsoMax(null, null)],
           ["2026-01-02", "2026-03-04", null]);
      } finally { catalogue = catAvT; }
      /* le dossier de visite sur un mini-arbre : un acté via BADP, un essai
         conforme, un projet ancien toujours ouvert */
      const lD = normalizeLigne({ id: "lD", nom: "EMAG 1", references: [ normalizeReference({ id: "rD", nom: "356x26",
        productionAnnuelle: 10000, cibleCPP: 0.2, ops: [ normalizeOp({ id: "oD", nom: "OP10", opCode: "OP10",
          config: Object.assign({}, defaultConfig, { volumeActif: true }),
          scenarios: [
            normalizeScenario({ id: "sDbase", name: "Base", baseline: true, outils: [ { id: "tDb", numero: "T5", logements: [ { id: "gDb", nom: "D1", codeArticle: "IM02 999 110", prix: 40, aretes: 8, charniere: 100 } ] } ] }),
            normalizeScenario({ id: "sDserie", name: "Candidat en série", statut: "serie", outils: [ { id: "tDs", numero: "T5", logements: [ { id: "gDs", nom: "D1", codeArticle: "IM02 999 111", prix: 30, aretes: 8, charniere: 100 } ] } ],
              essais: [ { id: "eDs", titre: "Essai serie", date: "2026-10-14", equipe: "Matin", operateur: "Matis",
                params: { logements: [ { outilId: "tDs", logementId: "gDs", outilNumero: "T5", logementNom: "D1", vc: 200, f: 0.3, charniere: 100, suivi: true } ] },
                prelevements: [ { id: "pDs", piece: 100, batt: "0.050", logementId: "gDs" } ] } ] }) ] }) ] }) ] });
      const pjD = { id: "pjD", nom: "Projet ancien ouvert", statut: "encours", creeLe: "2026-01-01T10:00:00Z", dateCible: "2026-12-01", responsableId: "", tags: [] };
      const lAvD = lignes, pjAvD = projets, catAvD = catalogue;
      lignes = [ lD ]; projets = [ pjD ];
      catalogue = [ normalizeArticleCat({ mabec: "IM02 999 111", iso: "CNMX LKT640", prix: 30, codificationDemandeeLe: "2026-07-01" }) ];
      try {
        const d = dossierVisite("2026-10-01");
        ok("dossier de visite : les essais de la fenêtre, leur résultat, le scénario en série visible",
           [d.essais.length, d.essais[0].titre, d.essais[0].etat, d.series.length, d.series[0].statut],
           [1, "Essai serie", "ok", 1, "serie"]);
        ok("dossier de visite : le gain ACTÉ sous BADP est qualifié (article demandé, non codifié) — jamais compté comme cycle standard",
           [d.gains.actes.length, d.gains.actes[0].qualif,
            d.gains.actes[0].codifJours === joursDepuis("2026-07-01"),
            d.gains.totalActeBadp > 0, d.gains.totalActeStandard, d.gains.totalPossible],
           [1, "BADP", true, true, 0, 0]);
        ok("dossier de visite : la codification en attente porte son âge, et le projet ancien est marqué",
           [d.codifAttente.length, d.codifAttente[0].mabec,
            d.codifAttente[0].jours === joursDepuis("2026-07-01"),
            d.projetsOuverts.length, d.projetsOuverts[0].ancien, d.bloques.clotures.length],
           [1, "IM02 999 111", true, 1, true, 0]);
        const dTout = dossierVisite("");
        ok("dossier de visite : sans date posée, la fenêtre couvre tout l'historique",
           dTout.essais.length >= d.essais.length, true);
      } finally { lignes = lAvD; projets = pjAvD; catalogue = catAvD; }
    }'''
src = src.replace(ancre, bloc, 1)
io.open(p, "w", encoding="utf-8").write(src)
print("tests 4.106 insérés")
