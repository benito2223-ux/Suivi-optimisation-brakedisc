# -*- coding: utf-8 -*-
"""Patch v4.89.1 partie 2 : la porte SECRET K dans le harnais + version."""

h = open('build_harness.py', encoding='utf-8', newline='').read()

av = """  /* ── v4.84 — LE SIMULATEUR EST STYLE ET PLEIN ECRAN, DANS LE CSS RÉEL ──"""
porte = """  /* ── v4.89.1 — LE SECRET K NE DORT JAMAIS DANS LE FICHIER LIVRÉ ──────────
     Revue Claude P1 : le fichier est PUBLIC sur deux domaines — un navigateur
     télécharge tout le source, formules et valeurs comprises. L'aide de
     l'outil exposait K = Vc × f × sin(κr), ses points de production et les
     angles validés. Retirés, et la porte lit le fichier réel : la formule, ses
     points et les marqueurs de la section retirée = absents, sinon échec. */
  (function secretK(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const fuites = ['K = Vc', '174 et 448', 'validé le 26/08', 'aideTitreK">Formules']
      .filter(m => html.indexOf(m) !== -1);
    if(fuites.length) r.echecs += fuites.length;
    console.log((fuites.length ? '  ECHEC ' : '  ok  ') + 'secret K : formule, points et angles absents du fichier livré' + (fuites.length ? ' — FUITE : ' + fuites.join(', ') : ''));
  })();
  /* ── v4.84 — LE SIMULATEUR EST STYLE ET PLEIN ECRAN, DANS LE CSS RÉEL ──"""
assert av in h, "ancre harnais introuvable"
h = h.replace(av, porte, 1)
open('build_harness.py', 'w', encoding='utf-8').write(h)
print("porte secret K ajoutee au harnais")

s = open('bilan_economique.html', encoding='utf-8', newline='').read()
s = s.replace('const TOOL_VERSION = "4.89.0";', 'const TOOL_VERSION = "4.89.1";', 1)
av2 = '''  { version:"4.89.0", date:"14/10/2026", points:['''
ap2 = '''  { version:"4.89.1", date:"14/10/2026", points:[
    "<b>Correction de confidentialité.</b> L'aide de l'outil affichait une formule thermique interne et ses points de r\\u00e9f\\u00e9rence production \\u2014 \\u00e7a n'avait rien \\u00e0 faire dans un fichier public. Retir\\u00e9 : l'indice reste affich\\u00e9 comme indice comparatif, sa m\\u00e9thode reste interne SPK."
  ]},
  { version:"4.89.0", date:"14/10/2026", points:['''
assert av2 in s, "ancre nouveautes"
s = s.replace(av2, ap2, 1)
open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("version 4.89.1 + nouveautes")
