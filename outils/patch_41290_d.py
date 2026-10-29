# -*- coding: utf-8 -*-
# Tour 107 — 4.129.0, LOT 5 (hygiène) — patch D : le harnais
# 1. Porte « lot 5 4.129 » : le build porte l'étape de retrait des tests (et
#    préserve la botte secrete), le test de sécurité à l'import vit dans la
#    suite, la charnière accepte tout nombre, le lint CSS du livré existe ;
#    et si un dist est construit, il ne porte PAS la suite intégrée.
# 2. La porte « equilibre css 4.124.1 » s'étend au dist (fichier livré).
# Règle des Tours 82/104/105 : aucun backslash littéral dans les motifs,
# aucun commentaire de porte contenant les séquences de commentaire bloc.
import io

F = "build_harness.py"
src = io.open(F, encoding="utf-8").read()

# --- 1. la porte lot 5, insérée avant la porte equilibre css ----------------
ANCRE_EQ = """  /* ── v4.124.1 — L'ÉQUILIBRE CSS (leçon de la 4.124.0) ──────────────────"""
n = src.count(ANCRE_EQ)
assert n == 1, "ancre equilibre : %d occurrences (attendu 1)" % n

PORTE_LOT5 = """  /* ── v4.129.0 — LOT 5 : L'HYGIÈNE ──────────────────────────────────────
     Le livré maigrit : la suite intégrée ne voyage plus (étape de build,
     la botte secrete v4.42 qui vivait dans son bloc est préservée — sinon
     la partie K de l aide serait livrée à tous). Le test de sécurité à
     l import vit dans la suite ; la charnière accepte tout nombre
     (step any : un 1250 saisi ne passe plus invalid) ; le lint CSS du
     livré existe. Si un dist est déjà construit : il ne porte pas la
     suite intégrée. */
  (function lot54129(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    const build = (function(){ try { return fs.readFileSync(path.join(REPO, 'outils', 'build-coque.mjs'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) echecs.push('bilan_economique.html introuvable');
    if (!build) echecs.push('outils/build-coque.mjs introuvable');
    if (html && build) {
      [['data-field="charniere" type="number" step="any" inputmode="numeric"', 'la charniere n accepte pas tout nombre (step any attendu)'],
       ['step="500"', 'le step 500 fauteur d invalid est encore la'],
       ['sécurité import : AUCUN innerHTML ni rendu', 'le test de sécurité à l import est absent de la suite'],
       ['__xssPwned=1', 'le payload hostile du test de sécurité est absent']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });
      [['Tests du moteur economique', 'le build ne repère plus le bloc des tests'],
       ['botte secrete', 'le build ne préserve plus la botte secrete (la partie K de l aide partirait en clair)'],
       ['porte encore la suite intégrée', 'le contrôle du livré (suite intégrée absente) est absent du build'],
       ['déséquilibré dans le livré', 'le lint CSS du livré est absent du build']]
      .forEach(function(m){ if (build.indexOf(m[0]) === -1) echecs.push(m[1]); });
    }
    const dist = (function(){ try { return fs.readFileSync(path.join(REPO, 'dist', 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (dist && dist.indexOf('runTests') !== -1) echecs.push('le dist construit porte encore la suite intégrée — relancer le build');
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'lot 5 4.129 : tests hors livré (botte secrete préservée), sécurité à l import, charnière step any, lint css du livré' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

"""
src = src.replace(ANCRE_EQ, PORTE_LOT5 + ANCRE_EQ)
print("ok  porte lot 5 4.129")

# --- 2. equilibre css s'étend au dist ---------------------------------------
ANCRE_MREP = """      /* la règle fautive, gardée complète (celle de la 4.123) */
      const mRep = html.match(/\\.reprise-bandeau\\{[^}]*display:flex[^}]*\\}/);"""
n = src.count(ANCRE_MREP)
assert n == 1, "ancre mRep : %d occurrences (attendu 1)" % n

CTRL_DIST = """      /* v4.129.0 (LOT 5) — le même contrôle sur le FICHIER LIVRÉ quand il
         est construit : le dist est ce que le navigateur reçoit vraiment. */
      const dist = (function(){ try { return fs.readFileSync(path.join(REPO, 'dist', 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
      if (dist) {
        let i = 0;
        while (i < dist.length) {
          const d = dist.indexOf('<style', i);
          if (d < 0) break;
          const f = dist.indexOf('</style>', d);
          if (f < 0) { echecs.push('dist : bloc style non fermé'); break; }
          const corps = dist.slice(dist.indexOf('>', d) + 1, f);
          const o = corps.split('{').length - 1;
          const c = corps.split('}').length - 1;
          if (o !== c) echecs.push('dist : bloc style déséquilibré (octet ' + d + ') : ' + o + ' ouvrantes, ' + c + ' fermantes');
          i = f + 8;
        }
      }
"""
src = src.replace(ANCRE_MREP, CTRL_DIST + ANCRE_MREP)
print("ok  equilibre css étendue au dist")

VIEUX_LIBELLE = "'equilibre css 4.124.1 : chaque bloc style a ses accolades fermees, la regle reprise-bandeau est complete'"
NOUVEAU_LIBELLE = "'equilibre css 4.124.1 (étendue 4.129 au dist) : chaque bloc style a ses accolades fermees, la regle reprise-bandeau est complete'"
n = src.count(VIEUX_LIBELLE)
assert n == 1, "libellé equilibre : %d occurrences (attendu 1)" % n
src = src.replace(VIEUX_LIBELLE, NOUVEAU_LIBELLE)
print("ok  libellé equilibre mis à jour")

assert src != io.open(F, encoding="utf-8").read()
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch D appliqué.")
