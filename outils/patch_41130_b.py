# -*- coding: utf-8 -*-
"""Tour 97 — v4.113.0 — tests recalés + le test du cas OP40 réel + porte."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. renommage pur : la donnée identique se paire AVANT le secours ────────
remplace(
"""        const apR = appariementOutils(baseR, candR);
        ok("secours : renommage pur (« D1 » → « Piste extérieure ») — ZÉRO paire fantôme sortie+ajout, deux secours tracés",
           [apR.sorties.length, apR.ajouts.length, apR.paires.length, apR.nbParSecours,
            apR.paires.every(x => x.parSecours === true)],
           [0, 0, 2, 2, true]);""",
"""        const apR = appariementOutils(baseR, candR);
        ok("secours : renommage pur — zéro paire fantôme ; la donnée identique se paire par DONNÉES, l'autre par secours",
           [apR.sorties.length, apR.ajouts.length, apR.paires.length, apR.nbParDonnees, apR.nbParSecours,
            apR.paires.every(x => String(x.a.o.numero) === String(x.b.o.numero))],
           [0, 0, 2, 1, 1, true]);""",
"1. renommage pur : données d'abord")

# ── 2. compteurs inégaux : le surplus reste un ajout nommé ───────────────────
remplace(
"""        const apR3 = appariementOutils(baseR, candR3);
        ok("secours : compteurs de logements INÉGAUX → PAS de repli, le déséquilibre reste visible (sortie + ajout nommés)",
           [apR3.nbParSecours, apR3.sorties.length, apR3.ajouts.length, apR3.paires.length],
           [0, 1, 2, 1]);""",
"""        const apR3 = appariementOutils(baseR, candR3);
        ok("secours : compteurs inégaux → PAS de repli positionnel ; la donnée identique se paire, le surplus reste un ajout nommé",
           [apR3.nbParSecours, apR3.nbParDonnees, apR3.sorties.length, apR3.ajouts.length, apR3.paires.length],
           [0, 1, 0, 1, 2]);""",
"2. compteurs inégaux recalés")

# ── 3. le test du CAS OP40 RÉEL (le bug vu par Benjamin) ─────────────────────
remplace(
"""        ok("groupe : le badge du groupe porte la mention « dont 1 poste sorti », visible sans déplier",
             compositionApercuHTML(candGrp).indexOf("dont 1 poste sorti") > -1, true);""",
"""        ok("groupe : le badge du groupe porte la mention « dont 1 poste sorti », visible sans déplier",
             compositionApercuHTML(candGrp).indexOf("dont 1 poste sorti") > -1, true);
        /* v4.113 — LE CAS OP40 RÉEL (bug vu par Benjamin en prod 4.112.1) :
           la migration 4.93 reloge les données dans « Plaquette », D1/D2 ne
           portent que la mesure. Apparier par nom les logements sans données
           masquait la vraie sortie T543·D1 (9,8 k€/an — l'incident exact du
           26/10) et flaggait « Plaquette » comme ajoutée. */
        const baseO = mkV("sOB2", "Classeur Matis OP40", true, [
          { tid: "ob1", numero: "T546", logements: [ { gid: "ob1a", nom: "D1", prix: 3.68, aretes: 4, charn: 60 } ] },
          { tid: "ob2", numero: "T548", logements: [ { gid: "ob2a", nom: "D1", prix: 9.56, aretes: 8, charn: 50 } ] },
          { tid: "ob3", numero: "T549", logements: [ { gid: "ob3a", nom: "D1", prix: 9.56, aretes: 8, charn: 30 } ] },
          { tid: "ob4", numero: "T543", logements: [ { gid: "ob4a", nom: "D2", prix: 10.97, aretes: 8, charn: 300 },
                                                     { gid: "ob4b", nom: "D1", prix: 11.87, aretes: 6, charn: 30 } ] } ]);
        const candO = mkV("sOC2", "SL500 OP40", false, [
          { tid: "oc1", numero: "T548", logements: [ { gid: "oc1a", nom: "Piste extérieure", prix: 9.56, aretes: 8, charn: 30 } ] },
          { tid: "oc2", numero: "T549", logements: [ { gid: "oc2a", nom: "Piste intérieure", prix: 9.56, aretes: 8, charn: 30 } ] },
          { tid: "oc3", numero: "T546 D1", logements: [ { gid: "oc3a", nom: "Plaquette", prix: 3.68, aretes: 4, charn: 60 },
                                                        { gid: "oc3b", nom: "D1" } ] },
          { tid: "oc4", numero: "T543", logements: [ { gid: "oc4a", nom: "Plaquette", prix: 10.97, aretes: 8, charn: 300 },
                                                     { gid: "oc4b", nom: "D2" },
                                                     { gid: "oc4c", nom: "D1" } ] } ]);
        const apO = appariementOutils(baseO, candO);
        ok("OP40 réel : les logements SANS données (D1/D2 de mesure) ne sont ni paire, ni sortie, ni ajout",
           [apO.paires.length, apO.sorties.length, apO.ajouts.length,
            apO.paires.every(x => posCost(x.a.l) !== null && posCost(x.b.l) !== null)],
           [4, 1, 0, true]);
        ok("OP40 réel : « Plaquette » (10,97/8/300) se paire avec D2 par DONNÉES identiques — plus de faux « ajouté 681 € »",
           [apO.paires.filter(x => x.parDonnees).map(x => x.a.l.nom + "↔" + x.b.l.nom).join("|"),
            apO.ajouts.some(f => /Plaquette/.test(f.l.nom || ""))],
           ["D2↔Plaquette", false]);
        ok("OP40 réel : la VRAIE sortie refait surface — T543·D1 (11,87/6/30) sans pendant = 9,8 k€/an, l'incident exact du 26/10",
           [apO.sorties[0].o.numero + "·" + apO.sorties[0].l.nom,
            Math.round(11.87 / (6 * 30) * 148942 / 100) * 100,
            Math.round(11.87 / (6 * 30) * 148942)],
           ["T543·D1", 9800, 9821]);""",
"3. le test du cas OP40 réel")

io.open(p, "w", encoding="utf-8").write(s)
print("tests recalés")
