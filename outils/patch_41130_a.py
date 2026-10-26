# -*- coding: utf-8 -*-
"""Tour 97 — v4.113.0 — le bug OP40 vu par Benjamin en prod (4.112.1).

SYMPTÔME : sur EMAG 1 / 356x26 RPI / OP40, les badges « ajouté — absent de
la référence » nommaient T543·Plaquette et T546 D1·D1 — qui ne correspondent
pas au Classeur Matis — pendant que la VRAIE sortie (T543·D1, 11,87 €/6 ar/
30 = 9,8 k€/an, l'incident EXACT du 26/10) était masquée par une paire
nom D1↔D1 vide-contre-vide.

CAUSE : la migration 4.93 a restructuré les scénarios récents en
[Plaquette (porteuse de données)] + [D1/D2 (contexte de mesure, sans
prix/charnière)]. Le base (Classeur Matis) garde ses données sur D1/D2
directement. Apparier par nom appariait donc des logements SANS données —
qui ne sont pas des porteurs de coût — et flaggait la porteuse réelle comme
« ajoutée ».

FIX (fidèle à la demande §4.4 : « absent OU SANS PRIX/CHARNIÈRE chiffrables »
= absent) :
  1. seuls les PORTEURS DE COÛT (prix×arêtes×charnière exploitables) entrent
     dans l'appariement — un logement sans données n'est ni paire, ni sortie,
     ni ajout (sa tuile dit déjà « Manque : … ») ;
  2. à l'intérieur d'un outil apparié par numéro, SECOURS PAR DONNÉES
     identiques (prix, arêtes, charnière) — tracé (« apparié par données »,
     compté dans la réconciliation) — AVANT le secours positionnel ;
  3. les porteurs restants sortent nommés : base sans pendant = SORTIE (le
     signal T543·D1 9,8 k€/an refait surface), candidat sans pendant = ajout.
"""
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


# ── 1. l'univers de l'appariement = les porteurs de coût seulement ──────────
remplace(
"""function appariementOutils(scRef, scCand){
  const flats = sc => (sc.outils || []).flatMap(o => (o.logements || []).map(l => ({ o, l })));
  const A = flats(scRef), B = flats(scCand);
  const numDe = f => String((f.o && f.o.numero) || "").trim().toUpperCase();
  const nomDe = f => String((f.l && f.l.nom) || "").trim().toUpperCase();""",
"""function appariementOutils(scRef, scCand){
  const flats = sc => (sc.outils || []).flatMap(o => (o.logements || []).map(l => ({ o, l })));
  /* v4.113 (bug OP40 vu par Benjamin en prod) — seuls les PORTEURS DE COÛT
     (prix × arêtes × charnière exploitables) entrent dans l'appariement. La
     migration 4.93 a restructuré les scénarios récents en [Plaquette
     (porteuse)] + [D1/D2 (mesure, sans données)] : apparier par nom des
     logements sans données masquait la vraie sortie (T543·D1, 9,8 k€/an —
     l'incident exact du 26/10) et flaggait la porteuse comme « ajoutée ».
     La demande §4.4 le disait déjà : « sans prix/charnière chiffrables » =
     absent. Un logement sans données n'est ni paire, ni sortie, ni ajout —
     sa tuile dit déjà « Manque : … ». */
  const porteur = f => posCost(f.l) !== null;
  const A = flats(scRef).filter(porteur), B = flats(scCand).filter(porteur);
  const numDe = f => String((f.o && f.o.numero) || "").trim().toUpperCase();
  const nomDe = f => String((f.l && f.l.nom) || "").trim().toUpperCase();""",
"1. porteurs de coût seulement")

# ── 2. le secours par DONNÉES identiques, avant le secours positionnel ──────
remplace(
"""  const paires = [], prisA = new Set(), prisB = new Set();
  let nbParSecours = 0;""",
"""  const paires = [], prisA = new Set(), prisB = new Set();
  let nbParSecours = 0, nbParDonnees = 0;
  const signature = f => { const pr = parseFloat(f.l.prix), a = parseFloat(f.l.aretes), c = parseFloat(f.l.charniere);
    return (pr > 0 && a > 0 && c > 0) ? pr + "|" + a + "|" + c : null; };""",
"2a. nbParDonnees + signature")

remplace(
"""    const restesA = coteA.filter(({ i }) => !prisA.has(i));
    const restesB = coteB.filter(({ j }) => !prisB.has(j));
    if(restesA.length && restesA.length === restesB.length){
      for(let k = 0; k < restesA.length; k++){
        paires.push({ a: restesA[k].fa, b: restesB[k].fb, parPosition: false, parSecours: true });
        prisA.add(restesA[k].i); prisB.add(restesB[k].j);
        nbParSecours++;
      }
    }
  });""",
"""    const restesA = coteA.filter(({ i }) => !prisA.has(i));
    const restesB = coteB.filter(({ j }) => !prisB.has(j));
    /* v4.113 — secours par DONNÉES identiques (prix, arêtes, charnière) :
       le cas réel OP40 — la base porte ses coûts sur D1/D2, les scénarios
       récents les relogent dans « Plaquette » — se pair par identité de
       données, tracé, avant tout repli positionnel. */
    restesA.forEach(({ fa, i }) => {
      const sig = signature(fa);
      if(sig === null || prisA.has(i)) return;
      const m = restesB.findIndex(({ fb, j }) => !prisB.has(j) && signature(fb) === sig);
      if(m > -1){
        paires.push({ a: fa, b: restesB[m].fb, parPosition: false, parDonnees: true });
        prisA.add(i); prisB.add(restesB[m].j);
        nbParDonnees++;
      }
    });
    const restesA2 = coteA.filter(({ i }) => !prisA.has(i));
    const restesB2 = coteB.filter(({ j }) => !prisB.has(j));
    if(restesA2.length && restesA2.length === restesB2.length){
      for(let k = 0; k < restesA2.length; k++){
        paires.push({ a: restesA2[k].fa, b: restesB2[k].fb, parPosition: false, parSecours: true });
        prisA.add(restesA2[k].i); prisB.add(restesB2[k].j);
        nbParSecours++;
      }
    }
  });""",
"2b. secours par données avant le positionnel")

# ── 3. le rendu porte le compte ──────────────────────────────────────────────
remplace(
'  return { paires, sorties, ajouts, nbParPosition: paires.filter(p => p.parPosition).length, nbParSecours };',
'  return { paires, sorties, ajouts, nbParPosition: paires.filter(p => p.parPosition).length, nbParSecours, nbParDonnees };',
"3a. rendu : nbParDonnees")

remplace(
"""    const g = parCle.get(cle);
    g.paires.push(pr);
    if(pr.parPosition) g.parPosition = true;
    if(pr.parSecours) g.parSecours = true;
  });""",
"""    const g = parCle.get(cle);
    g.paires.push(pr);
    if(pr.parPosition) g.parPosition = true;
    if(pr.parSecours) g.parSecours = true;
    if(pr.parDonnees) g.parDonnees = true;
  });""",
"3b. le groupe trace parDonnees")

remplace(
"""      return { lRef: lB, lSc: lS, parPosition: pr.parPosition, parSecours: !!pr.parSecours, indice,""",
"""      return { lRef: lB, lSc: lS, parPosition: pr.parPosition, parSecours: !!pr.parSecours, parDonnees: !!pr.parDonnees, indice,""",
"3c. le logement porte parDonnees")

remplace(
"""  outils.forEach(g => g.logements.forEach(x => parLogement.set(x.lSc.id, {
    indice: x.indice, pctCycle: x.pctCycle, vfSc: x.vfSc, parPosition: x.parPosition, parSecours: x.parSecours,""",
"""  outils.forEach(g => g.logements.forEach(x => parLogement.set(x.lSc.id, {
    indice: x.indice, pctCycle: x.pctCycle, vfSc: x.vfSc, parPosition: x.parPosition, parSecours: x.parSecours, parDonnees: x.parDonnees,""",
"3d. parLogement porte parDonnees")

remplace(
'           outils, sorties, ajouts, nbParPosition: appar.nbParPosition, nbParSecours: appar.nbParSecours,',
'           outils, sorties, ajouts, nbParPosition: appar.nbParPosition, nbParSecours: appar.nbParSecours, nbParDonnees: appar.nbParDonnees,',
"3e. verdictParOutil rend nbParDonnees")

# ── 4. le dépliant et la réconciliation nomment le secours par données ──────
remplace(
'      ${vpLog.parSecours ? `<div class="ap-detail-l"><span>Appariement</span><b>par secours — noms divergents (même outil, même nombre de logements)</b></div>` : ""}',
'      ${vpLog.parSecours ? `<div class="ap-detail-l"><span>Appariement</span><b>par secours — noms divergents (même outil, même nombre de logements)</b></div>` : ""}\n      ${vpLog.parDonnees ? `<div class="ap-detail-l"><span>Appariement</span><b>par données identiques — prix, arêtes et charnière égaux (même outil)</b></div>` : ""}',
"4a. dépliant : la ligne par données")

remplace(
'outil(s) apparié(s) par position (numéro absent ou en doublon)` : ""}${vp.nbParSecours ? ` · ${vp.nbParSecours} logement(s) apparié(s) par secours (noms divergents)` : ""}',
'outil(s) apparié(s) par position (numéro absent ou en doublon)` : ""}${vp.nbParSecours ? ` · ${vp.nbParSecours} logement(s) apparié(s) par secours (noms divergents)` : ""}${vp.nbParDonnees ? ` · ${vp.nbParDonnees} logement(s) apparié(s) par données identiques` : ""}',
"4b. réconciliation : les secours par données comptés")

# ── 5. version + NOUVEAUTES ──────────────────────────────────────────────────
remplace('const TOOL_VERSION = "4.112.1";', 'const TOOL_VERSION = "4.113.0";', "5a. TOOL_VERSION")

remplace(
"""const NOUVEAUTES = [
  { version:"4.112.1", date:"26/10/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.113.0", date:"26/10/2026", points:[
    "<b>Le verdict par outil parle le vrai langage des fiches.</b> Vu sur EMAG 1 OP40 : les scénarios récents relogent les données de plaquette dans un logement « Plaquette » (D1/D2 ne portant que la mesure), et l'appariement comparait des logements <b>sans données</b> — d'où des badges « ajouté » qui ne correspondaient pas au Classeur Matis, pendant que la <b>vraie</b> disparition (T543 · D1, <b>9,8 k€/an</b> — l'incident exact du 26/10) restait muette. Désormais : seuls les logements <b>porteurs de coût</b> (prix, arêtes, charnière) sont comparés ; un logement relogé à l'identique se paire <b>par données identiques</b> (tracé) ; et un porteur de la référence sans pendant sort <b>nommément</b> dans « dont sorties du scénario ». Vérifié sur OP40 : la ligne montre bien <b>−9,8 k€/an (T543 · D1)</b>."
  ]},
  { version:"4.112.1", date:"26/10/2026", points:[""",
"5b. entrée NOUVEAUTES")

io.open(p, "w", encoding="utf-8").write(s)
print("patch 4.113.0 posé :", n0, "->", len(s))
