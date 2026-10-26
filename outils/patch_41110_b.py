# -*- coding: utf-8 -*-
"""Tour 94 — v4.111.0 — la porte hors-suite « verdict par outil 4.111 ».
Lit le fichier réel : le module existe, la tuile n'apparie plus JAMAIS par
position, la fiche porte la réconciliation et la ligne « dont sorties », le
dégradé a sa garde d'impression, et aucun K ni P_req dans les libellés."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


remplace(
"  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──",
"""  /* ── v4.111.0 — LE VERDICT PAR OUTIL ──────────────────────────────────
     Demande Hermes/Benjamin du 26/10 (incident T543 D1) : le verdict se
     refait en additionnant les tuiles. Portes : le module existe, la tuile
     n'apparie plus JAMAIS par position, la fiche porte la réconciliation et
     la ligne « dont sorties du scénario », le dégradé du gain a sa garde
     d'impression, et aucun K ni P_req dans les libellés (§2.6). */
  (function verdictParOutilGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const code = html;
      ['function appariementOutils(scRef, scCand){',
       'function verdictParOutil(sc, cfg, ligne, ref, baseCmp){',
       'function verdictSortiesHTML(vpo){']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('module absent : ' + m); });

      /* le piège n°1 banni : plus aucun appariement positionnel dans la tuile */
      const iTuile = code.indexOf('function apercuLogementHTML');
      const iCompo = code.indexOf('function compositionApercuHTML');
      if (iTuile < 0 || iCompo < 0) echecs.push('la composition (tuiles) introuvable');
      else {
        const blocTuile = code.slice(iTuile, iCompo);
        if (blocTuile.indexOf('flatsSc.indexOf') !== -1 || blocTuile.indexOf('indexOf(l)') !== -1)
          echecs.push('l appariement positionnel est de retour dans la tuile');
        if (blocTuile.indexOf('vp.parLogement') === -1)
          echecs.push('la tuile ne lit plus l appariement par numéro');
      }

      /* la fiche porte le verdict par outil et sa réconciliation */
      if (iCompo >= 0) {
        const iFinCompo = code.indexOf(String.fromCharCode(10) + '/* ----', iCompo);
        const blocCompo = code.slice(iCompo, iFinCompo > 0 ? iFinCompo : iCompo + 7000);
        if (blocCompo.indexOf('verdictParOutil(') === -1)
          echecs.push('la composition ne calcule plus le verdict par outil');
        if (blocCompo.indexOf('ap-reconcil') === -1)
          echecs.push('la ligne de réconciliation a disparu de la fiche');
      }

      /* la ligne dédiée dans le verdict (l'incident rendu impossible à rater) */
      const iVerdict = code.indexOf('function verdictHTML');
      if (iVerdict < 0) echecs.push('verdictHTML introuvable');
      else {
        const iFinV = code.indexOf(String.fromCharCode(10) + '/* ----', iVerdict);
        const blocV = code.slice(iVerdict, iFinV > 0 ? iFinV : iVerdict + 3500);
        if (blocV.indexOf('verdictSortiesHTML(') === -1)
          echecs.push('le verdict ne porte plus la ligne dont sorties du scénario');
      }

      /* le dégradé du gain ne s'imprime jamais : deux règles data-gain
         (l'une dans @media print), comme les couleurs de ligne */
      const occ = code.split('.ap-tuile[data-gain').length - 1;
      if (occ < 2) echecs.push('le dégradé du gain n a pas sa garde d impression (moins de 2 règles data-gain)');

      /* les libellés du sémantique sont là, sans aucun K ni P_req (§2.6) */
      ['dont sorties du scénario', 'Levier technique', 'Levier productivité', 'Réconciliation']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('libellé absent : ' + m); });
      const iMod = code.indexOf('function verdictParOutil');
      const iFinMod = code.indexOf(String.fromCharCode(10) + 'function ', iMod);
      const blocMod = code.slice(iMod, iFinMod > 0 ? iFinMod : iMod + 6000);
      ['K = Vc', 'P_req', 'coefficient K'].forEach(function(m){
        if (blocMod.indexOf(m) !== -1) echecs.push('le module du verdict expose un interdit : ' + m);
      });
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'verdict par outil 4.111 : appariement par numéro, réconciliation somme des tuiles = verdict, sorties nommées' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──""",
"1. porte hors-suite verdict par outil 4.111")

io.open(p, "w", encoding="utf-8").write(s)
print("patch harnais posé")
