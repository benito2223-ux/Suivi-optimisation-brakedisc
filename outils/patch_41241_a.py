# -*- coding: utf-8 -*-
"""Tour 100 — v4.124.1 — le garde-fou structurel qui aurait attrapé le bug :
l'équilibre des accolades de CHAQUE bloc <style> (une accolade ouverte sans
fermeture fait ignorer au navigateur tout ce qui suit, sans AUCUNE erreur
console — leçon de la 4.124.0). Et la règle .reprise-bandeau doit porter ses
déclarations (la règle exacte de la 4.123)."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

avant = "  /* ── v4.124 — LES P0 DU BRIEF EXTERNE ─────────────────────────────────"
apres = """  /* ── v4.124.1 — L'ÉQUILIBRE CSS (leçon de la 4.124.0) ──────────────────
     Mon patch P0-2 avait laissé `.reprise-bandeau{` ouvert sans ses
     déclarations : le navigateur jetait le bloc suivant, la moitié de la
     page perdait sa mise en forme — et AUCUNE erreur console, aucun test
     texte ne le voyait. Benjamin l'a vu au rendu, réparé une ligne dans une
     copie, et posé la règle : NE RIEN LIVRER sans avoir regardé le rendu.
     Ce garde-fou structurel attrape le mécanisme : chaque bloc <style> doit
     avoir autant d'accolades ouvrantes que fermantes. */
  (function equilibreCss41241(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) echecs.push('bilan_economique.html introuvable');
    else {
      const ouvrants = html.split('<style>').length - 1;
      const fermants = html.split('</style>').length - 1;
      if (ouvrants !== fermants) echecs.push('blocs style déséquilibrés : ' + ouvrants + ' ouvrants, ' + fermants + ' fermants');
      let i = 0;
      while (i < html.length) {
        const d = html.indexOf('<style>', i);
        if (d < 0) break;
        const f = html.indexOf('</style>', d);
        if (f < 0) { echecs.push('bloc style non fermé'); break; }
        const corps = html.slice(d + 7, f);
        const o = (corps.match(/\\{/g) || []).length;
        const c = (corps.match(/\\}/g) || []).length;
        if (o !== c) echecs.push('bloc style n° ' + (i + 1) + ' déséquilibré : ' + o + ' accolades ouvrantes, ' + c + ' fermantes — une règle avalera la suivante');
        i = f + 7;
      }
      /* la règle fautive, gardée complète (celle de la 4.123) */
      const mRep = html.match(/\\.reprise-bandeau\\{[^}]*display:flex[^}]*\\}/);
      if (!mRep) echecs.push('.reprise-bandeau a perdu ses déclarations (la règle 4.123 attendue est absente)');
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'equilibre css 4.124.1 : chaque bloc style a ses accolades fermees, la regle reprise-bandeau est complete' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.124 — LES P0 DU BRIEF EXTERNE ─────────────────────────────────"""

assert s.count(avant) == 1, s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("porte équilibre CSS posée")
