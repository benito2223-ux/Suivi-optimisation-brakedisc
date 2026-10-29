# -*- coding: utf-8 -*-
# Tour 108 — 4.129.1 — patch B : le harnais
# La porte « lot 5 4.129 » s'étend aux points 4.129.1 :
#   - `global.localStorage` (Node-only) BANNI du source — l'exception
#     « global is not defined » interrompait la suite au navigateur ;
#   - la sonde de substitution (lsSubstitue) et la porte globalThis présentes ;
#   - les sélecteurs atelier 56 px étendus (textarea, summary, .pcb-op,
#     case à cocher 56/28 par background-clip:content-box).
# Règle du tour : aucun backslash littéral dans les motifs.
import io

F = "build_harness.py"
src = io.open(F, encoding="utf-8").read()

AVANT = """      if (html.indexOf('step="500"') !== -1) echecs.push('le step 500 fauteur d invalid est encore la');"""
APRES = """      if (html.indexOf('step="500"') !== -1) echecs.push('le step 500 fauteur d invalid est encore la');
      /* v4.129.1 — la suite #tests est navigable : plus de `global.localStorage`
         (Node-only, l exception interrompait la suite entière au navigateur) ;
         la sonde de substitution dit quand la porte ne peut pas tourner ici ;
         le plancher atelier 56 px couvre tout élément saisissable ou cliquable. */
      if (html.indexOf('global.localStorage') !== -1) echecs.push('global.localStorage (Node-only) est de retour — la suite plante au navigateur');
      [['globalThis.localStorage = lsFaux', 'la porte TDZ ne passe plus par globalThis'],
       ['lsSubstitue', 'la sonde de substitution localStorage est absente'],
       ['textarea{ min-height:56px', 'les zones de texte atelier ne font pas 56 px'],
       ['summary{ min-height:56px', 'les résumés dépliables atelier ne font pas 56 px'],
       ['.pcb-op{ min-height:56px', 'les lignes d opération atelier ne font pas 56 px'],
       ['background-clip:content-box', 'la case à cocher atelier (56/28 par content-box) est absente']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });"""
n = src.count(AVANT)
assert n == 1, "ancre porte lot 5 : %d occurrences (attendu 1)" % n
src = src.replace(AVANT, APRES)

VIEUX_LIBELLE = "'lot 5 4.129 : tests hors livré (botte secrete préservée), sécurité à l import, charnière step any, lint css du livré'"
NOUVEAU_LIBELLE = "'lot 5 4.129 (étendue 4.129.1) : tests hors livré, sécurité à l import, charnière step any, lint css du livré, suite navigable (globalThis), atelier 56 px tout interactif'"
n = src.count(VIEUX_LIBELLE)
assert n == 1, "libellé porte lot 5 : %d occurrences (attendu 1)" % n
src = src.replace(VIEUX_LIBELLE, NOUVEAU_LIBELLE)

io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch B (4.129.1) appliqué.")
