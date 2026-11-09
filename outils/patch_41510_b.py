# -*- coding: utf-8 -*-
"""Tour 134 (4.151.0) — tests d'acceptation étape 2 (insertion dans la suite intégrée)."""
import io

P = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/bilan_economique.html"
src = io.open(P, "r", encoding="utf-8", newline="").read()
orig_len = len(src)

def repl(s, old, new, label):
    for attempt in (old, old.replace("\n", "\r\n")):
        n = s.count(attempt)
        if n == 1:
            return s.replace(attempt, new)
        if n != 0:
            raise SystemExit("ANCRE '%s' : %d occurrences" % (label, n))
    raise SystemExit("ANCRE INTROUVABLE : %s" % label)

TESTS = r"""  /* Tour 134 (4.151.0) — ÉTAPE 2 : les conditions de coupe se tapent une fois.
     Acceptation (demande Claude Tour 133 §4) : 1 saisie → tous les logements ;
     divergent s'ouvre sans écrire ; décocher « simultané » sépare ; G97 jamais
     lu comme des m/min ; Aligner retiré dès qu'un relevé existe. */
  {
    const mkLog = (id, nom, extras) => Object.assign({ id, nom, prix:"5", aretes:8, charniere:"50",
      vc:"", f:"", kappaR:"", rayonBec:"", apPiste:"", tempsCoupe:"" }, extras || {});
    const mkSc = (defs) => ({ id:"sTour134", name:"test etape2", outils: defs.map(d => ({
      id:d.id, numero:d.numero, simultaneAvecPrecedent:!!d.sim, logements:d.logs.map(l => mkLog(l.id, l.nom, l.x)) })) });
    const scT = mkSc([
      { id:"tA", numero:"T10", logs:[{id:"gA1", nom:"D1"}] },
      { id:"tB", numero:"T20", sim:true, logs:[{id:"gB1", nom:"D1"}, {id:"gB2", nom:"D2"}] },
      { id:"tC", numero:"T30", sim:true, logs:[{id:"gC1", nom:"D1"}] }
    ]);
    const g = groupesSimultanes(scT);
    ok("etape2 : groupes simultanes — 1 outil + 2 simultanes = 2 groupes", [g.length, g[0].length, g[1].length], [2, 1, 2]);
    scT.outils[1].simultaneAvecPrecedent = false;
    ok("etape2 : decocher « simultané » sépare le groupe, chacun garde ses valeurs", [groupesSimultanes(scT).length, groupesSimultanes(scT)[1].length], [2, 2]);
    scT.outils[1].simultaneAvecPrecedent = true;
    const membres = groupesSimultanes(scT)[1];
    const avant = JSON.stringify(membres);
    const uni = conditionsUniformes(membres);
    ok("etape2 : lire l'état du groupe n'écrit rien", [JSON.stringify(membres) === avant, uni.f.uniforme], [true, true]);
    ok("etape2 : UNE saisie remplit tous les logements du groupe (4 logements ici)", [ecrireConditionsGroupe(membres, "f", 0.25), membres.flatMap(o => o.logements).every(l => l.f === 0.25)], [4, true]);
    ecrireConditionsGroupe(groupesSimultanes(scT)[0], "vc", 800);
    ok("etape2 : l'outil hors groupe garde ses propres valeurs", [scT.outils[0].logements[0].vc, scT.outils[1].logements[0].vc], [800, ""]);
    ecrireConditionsGroupe(membres, "modeVitesse", "G97");
    ecrireConditionsGroupe(membres, condChampVitesse("G97"), 700);
    ok("etape2 : G97 — S rangée dans sBroche, vc jamais touché, libellé tr/min", [membres[0].logements[0].sBroche, membres[0].logements[0].vc, membres[1].logements[0].sBroche, condLabelVitesse("G97")], [700, "", 700, "S <span>tr/min</span>"]);
    ok("etape2 : G96 — la vitesse vit dans Vc (m/min)", [condChampVitesse("G96"), condChampVitesse(""), condLabelVitesse("G96")], ["vc", "vc", "Vc <span>m/min</span>"]);
    const scD = mkSc([
      { id:"tX", numero:"T40", logs:[{id:"gX1", nom:"D1", x:{vc:"700", f:"0.25"}}, {id:"gX2", nom:"D2", x:{vc:"900", f:"0.25"}}] }
    ]);
    const snapAvant = JSON.stringify(scD);
    const unD = conditionsUniformes(groupesSimultanes(scD)[0]);
    logementBlocHTML(scD, scD.outils[0], scD.outils[0].logements[0], true, false);
    conditionsGroupeHTML(scD, groupesSimultanes(scD)[0], false);
    ok("etape2 : un groupe divergent s'ouvre SANS écrire (octet pour octet)", [JSON.stringify(scD) === snapAvant, unD.vitesse.uniforme, unD.f.uniforme], [true, false, true]);
    scT.outils[1].logements[0].modeVitesse = "G97";
    const lpB = snapshotLogements(scT).find(lp => lp.logementId === "gB1");
    ok("etape2 : l'instantané d'essai fige le mode et la rotation", [lpB.modeVitesse, lpB.sBroche], ["G97", 700]);
    ok("etape2 : « Aligner » — proposé sans relevé, retiré dès qu'un relevé existe", [alignerDisponible({ prelevements: [] }), alignerDisponible({ prelevements: [{ id:"p1" }] })], [true, false]);
    const scP = mkSc([{ id:"tP", numero:"T50", logs:[{id:"gP1", nom:"D1"}] }]);
    scP.outils[0].logements[0].vc = "700";
    const esP = { params:{ logements:[{ outilId:"tP", logementId:"gP1", vc:"700", f:"", charniere:"" }] } };
    scP.outils[0].logements[0].modeVitesse = "G97";
    scP.outils[0].logements[0].sBroche = "700";
    const dv = paramsDivergences(scP, esP);
    ok("etape2 : une divergence de mode est nommée (mode —→G97)", dv.length === 1 && /mode/.test(dv[0]), true);
    const bloc96 = conditionsGroupeHTML(scT, groupesSimultanes(scT)[0], false);
    const bloc97 = conditionsGroupeHTML(mkSc([{ id:"tZ", numero:"T60", sim:false, logs:[{id:"gZ1", nom:"D1", x:{modeVitesse:"G97", sBroche:"500"}}] }]), groupesSimultanes(scT)[1], false);
    ok("etape2 : le bloc du groupe affiche Vc (m/min) hors G97, jamais des tr/min en m/min", [/Vc <span>m\/min<\/span>/.test(bloc96), /S <span>tr\/min<\/span>/.test(bloc96)], [true, false]);
    ok("etape2 : un groupe en G97 affiche S (tr/min)", /S <span>tr\/min<\/span>/.test(bloc97), true);
  }
"""

ANCRE = '    ok("pièces : les références d\'un enregistrement se listent", [...syPjReferences({ a:{ dataUrl:"§pj§s1" }, b:[{ dataUrl:"§pj§s2" }, { dataUrl:"data:x" }] }, new Set())].sort(), ["s1", "s2"]);\n  }'

if "etape2 : UNE saisie remplit" in src:
    print("déjà appliqué")
else:
    src = repl(src, ANCRE, ANCRE + "\n" + TESTS, "tests-etape2")
    io.open(P, "w", encoding="utf-8", newline="").write(src)
    print("TESTS OK : %d -> %d octets (+%d)" % (orig_len, len(src), len(src) - orig_len))
