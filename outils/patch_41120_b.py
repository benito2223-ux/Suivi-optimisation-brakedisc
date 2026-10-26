# -*- coding: utf-8 -*-
"""Tour 95 — v4.112.0 — tests runTests + version + NOUVEAUTES. Les fixtures
du complément : renommage pur (zéro sortie+ajout, secours tracé), compteurs
inégaux (pas de repli), groupe avec poste sorti (mention + non réparti)."""
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


# ── 1. les tests, dans le bloc v4.111 juste après le test anti-secondes ──────
remplace(
"""        ok("verdict par outil : sans chrono, la tuile n'invente AUCUNE seconde — tout en % et en €/an, dégradé posé",
           [new RegExp("[0-9](?:,[0-9]+)? s[^a-zà-ÿ]").test(tuileHtml),
            tuileHtml.indexOf("hors temps machine") > -1,
            tuileHtml.indexOf("data-gain") > -1,
            tuileHtml.indexOf("Levier technique") > -1],
           [false, true, true, true]);
      }""",
"""        ok("verdict par outil : sans chrono, la tuile n'invente AUCUNE seconde — tout en % et en €/an, dégradé posé",
           [new RegExp("[0-9](?:,[0-9]+)? s[^a-zà-ÿ]").test(tuileHtml),
            tuileHtml.indexOf("hors temps machine") > -1,
            tuileHtml.indexOf("data-gain") > -1,
            tuileHtml.indexOf("Levier technique") > -1],
           [false, true, true, true]);
        /* v4.112 — le SECOURS intra-outil (complément §1, décision Benjamin) :
           renommage pur = zéro paire fantôme, secours tracé, jamais entre
           outils ; compteurs inégaux = pas de repli, le déséquilibre visible. */
        const baseR = mkV("sRB2", "Base renommage", true, [
          { tid: "rb1", numero: "T548", logements: [ { gid: "rb1a", nom: "D1", prix: 9.56, aretes: 8, charn: 50, vc: 220, f: 0.3 } ] },
          { tid: "rb2", numero: "T549", logements: [ { gid: "rb2a", nom: "D1", prix: 9.56, aretes: 8, charn: 30, vc: 220, f: 0.3 } ] } ]);
        const candR = mkV("sRC2", "Cand renommage", false, [
          { tid: "rc1", numero: "T548", logements: [ { gid: "rc1a", nom: "Piste extérieure", prix: 9.56, aretes: 8, charn: 50, vc: 260, f: 0.3 } ] },
          { tid: "rc2", numero: "T549", logements: [ { gid: "rc2a", nom: "Piste intérieure", prix: 9.56, aretes: 8, charn: 50, vc: 260, f: 0.3 } ] } ]);
        const apR = appariementOutils(baseR, candR);
        ok("secours : renommage pur (« D1 » → « Piste extérieure ») — ZÉRO paire fantôme sortie+ajout, deux secours tracés",
           [apR.sorties.length, apR.ajouts.length, apR.paires.length, apR.nbParSecours,
            apR.paires.every(x => x.parSecours === true)],
           [0, 0, 2, 2, true]);
        ok("secours : le repli reste DANS l'outil apparié par numéro — jamais entre outils",
           apR.paires.every(x => String(x.a.o.numero) === String(x.b.o.numero)), true);
        const candR3 = mkV("sRC3", "Cand renommage déséquilibré", false, [
          { tid: "re1", numero: "T548", logements: [ { gid: "re1a", nom: "Piste extérieure", prix: 9.56, aretes: 8, charn: 50, vc: 260, f: 0.3 },
                                                     { gid: "re1b", nom: "Piste intérieure", prix: 9.56, aretes: 8, charn: 50, vc: 260, f: 0.3 } ] },
          { tid: "re2", numero: "T549", logements: [ { gid: "re2a", nom: "D1", prix: 9.56, aretes: 8, charn: 30, vc: 220, f: 0.3 } ] } ]);
        const apR3 = appariementOutils(baseR, candR3);
        ok("secours : compteurs de logements INÉGAUX → PAS de repli, le déséquilibre reste visible (sortie + ajout nommés)",
           [apR3.nbParSecours, apR3.sorties.length, apR3.ajouts.length, apR3.paires.length],
           [0, 1, 2, 1]);
        /* le groupe qui a perdu un membre : la mention sur le badge, le non
           réparti garde le temps machine du sorti (complément §2) */
        const baseGrp = mkV("sGB2", "Base groupe", true, [
          { tid: "gb1", numero: "T541", logements: [ { gid: "gb1a", nom: "D1", prix: 40, aretes: 8, charn: 100, vc: 200, f: 0.3, tps: 60 } ] },
          { tid: "gb2", numero: "T543", sim: true, logements: [ { gid: "gb2a", nom: "D1", prix: 38, aretes: 4, charn: 700, vc: 180, f: 0.25, tps: 120 } ] },
          { tid: "gb3", numero: "T548", sim: true, logements: [ { gid: "gb3a", nom: "D1", prix: 30, aretes: 8, charn: 100, vc: 220, f: 0.3, tps: 60 } ] } ]);
        const candGrp = mkV("sGC2", "Cand groupe", false, [
          { tid: "gc1", numero: "T541", logements: [ { gid: "gc1a", nom: "D1", prix: 40, aretes: 8, charn: 100, vc: 240, f: 0.3, tps: 50 } ] },
          { tid: "gc3", numero: "T548", sim: true, logements: [ { gid: "gc3a", nom: "D1", prix: 30, aretes: 8, charn: 100, vc: 260, f: 0.3, tps: 50 } ] } ]);
        const lGrp = normalizeLigne({ id: "lGrp", nom: "EMAG 1", references: [ normalizeReference({ id: "rGrp", nom: "356x26",
          productionAnnuelle: 10000, ops: [ normalizeOp({ id: "oGrp", nom: "OP40", opCode: "OP40",
            config: Object.assign({}, defaultConfig, { volumeActif: true, coutMachineActif: true }),
            scenarios: [ baseGrp, candGrp ] }) ] }) ] });
        lGrp.coutHoraire = "45";
        const lAvGrp = lignes, activeLAv = activeLigneId, refLAv = activeReferenceId, opLAv = activeOpId, cfgAv = config, dataAv = data, idAv = activeId;
        lignes = [ lGrp ]; activeLigneId = "lGrp"; activeReferenceId = "rGrp"; activeOpId = "oGrp";
        config = lGrp.references[0].ops[0].config; data = [ baseGrp, candGrp ]; activeId = candGrp.id;
        try {
          const vpoGrp = verdictParOutil(candGrp, config, lGrp, lGrp.references[0], baseGrp);
          ok("groupe : chaque outil apparié connaît son poste sorti (T543, simultané de la base)",
             vpoGrp.outils.map(g => g.sortisGroupe), [1, 1]);
          ok("groupe : le non réparti garde le temps machine du poste sorti — 120 s × 45 €/h × 10 000 = 6 250 €/an, au centime",
             Math.round(vpoGrp.nonReparti), 6250);
          ok("groupe : le badge du groupe porte la mention « dont 1 poste sorti », visible sans déplier",
             compositionApercuHTML(candGrp).indexOf("dont 1 poste sorti") > -1, true);
        } finally {
          lignes = lAvGrp; activeLigneId = activeLAv; activeReferenceId = refLAv; activeOpId = opLAv;
          config = cfgAv; data = dataAv; activeId = idAv;
        }
      }""",
"1. tests runTests v4.112")

# ── 2. la version ────────────────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.111.0";', 'const TOOL_VERSION = "4.112.0";', "2. TOOL_VERSION")

# ── 3. l'entrée NOUVEAUTES ───────────────────────────────────────────────────
remplace(
"""const NOUVEAUTES = [
  { version:"4.111.0", date:"26/10/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.112.0", date:"26/10/2026", points:[
    "<b>Les renommages de logements ne font plus de bruit.</b> Un logement renommé (« D1 » → « Piste extérieure ») dans un outil par ailleurs identique s'apparie désormais <b>par secours</b> avec son pendant — plus de fausses lignes « sortie + ajout » qui s'annulent. Le repli est <b>tracé</b> (« apparié par secours — noms divergents », compté dans la réconciliation) et ne s'applique <b>jamais entre outils</b> ; si le nombre de logements diffère, aucun repli : le déséquilibre reste visible. Et le badge d'un groupe simultané qui a perdu un poste porte la mention <b>« dont 1 poste sorti »</b> — le coût du poste sorti reste dans le « non réparti » de la réconciliation. Au passage : <b>retrait des 8 fichiers de polices morts</b> (Barlow/Public Sans/IBM Plex des débuts de la coque — l'app embarque déjà ses polices en base64, zéro téléchargement en plus)."
  ]},
  { version:"4.111.0", date:"26/10/2026", points:[""",
"3. entrée NOUVEAUTES")

# note : le premier passage avait collé « points": » (guillemet parasite) dans
# le bloc inséré — corrigé à la main immédiatement, vu par node --check.

io.open(p, "w", encoding="utf-8").write(s)
print("patch B posé :", n0, "->", len(s))
