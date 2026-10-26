# -*- coding: utf-8 -*-
"""Tour 96 — v4.112.1 — la PORTE structurelle TDZ : toute globale assignée
dans loadAll() doit être déclarée AVANT l'appel initial `loadAll();`. Le test
runtime ne voyait pas le piège (il rejoue loadAll après l'évaluation, quand
la TDZ est levée) — le contre-regard vient de le prouver. Cette porte lit le
fichier réel, comme la constitution le demande (le piège est documenté depuis
le début du cahier, jamais gardé)."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

avant = "  /* ── v4.112 — LES 8 POLICES MORTES SONT RETIRÉES ─────────────────────"
apres = """  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────
     Le bug de la répétition générale pré-prod (26/10) : une globale assignée
     dans loadAll() mais déclarée APRÈS l'appel initial lève ReferenceError,
     avalée par le catch silencieux — les données réelles retombent sur
     l'exemple, et la première saisie écraserait le localStorage. Le test
     runtime ne le voit pas (il rejoue loadAll après l'évaluation complète,
     quand la TDZ est levée) : seule la SÉQUENCE initiale du fichier mord.
     Cette porte lit donc le fichier réel : pour chaque identifiant assigné
     en tête de ligne dans le corps de loadAll, sa déclaration top-level
     `let/const` doit précéder l'appel `loadAll();`. */
  (function porteTdzLoadAll(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const NL = String.fromCharCode(10);
      const iDeb = html.indexOf('function loadAll(){');
      const iFin = html.indexOf(NL + 'function ', iDeb);
      const iAppel = html.indexOf(NL + 'loadAll();');
      if (iDeb < 0 || iAppel < 0) echecs.push('loadAll ou son appel initial introuvable');
      else if (iFin < 0) echecs.push('fin de loadAll introuvable');
      else {
        const corps = html.slice(iDeb, iFin);
        const noms = {};
        corps.split(NL).forEach(function(l){
          const m = l.match(/^\\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\\s*=[^=]/);
          if (m) noms[m[1]] = true;
        });
        Object.keys(noms).sort().forEach(function(n){
          /* déclaration top-level la plus précoce (colonne 0) */
          const re = new RegExp('^(let|const)\\\\s+' + n + '\\\\b', 'm');
          const mDec = re.exec(html);
          if (!mDec) return; /* locale sans déclaration top-level : hors périmètre */
          if (mDec.index > iAppel)
            echecs.push('la globale ' + n + ' est assignée dans loadAll mais déclarée APRÈS son appel — piège TDZ : repli silencieux sur les données d\\u2019exemple');
        });
      }
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'porte TDZ 4.112.1 : toute globale de loadAll se déclare avant son appel (le repli silencieux sur les données d\\u2019exemple ne reviendra pas)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.112 — LES 8 POLICES MORTES SONT RETIRÉES ─────────────────────"""

assert s.count(avant) == 1, s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("porte TDZ structurelle posée")
