# -*- coding: utf-8 -*-
"""Tour 98 — v4.120.0 — la porte hors-suite « lot UX 4.120 » : (1) ⤓ Imprimer
lit LOGO_SPK_SRC et ne jette plus sur le logo retiré ; (2) l'anti-flash est
posé (cache + révélation + filet) ; (3) le rail câble l'import au file picker
de l'app. Contre-regards prévus : logo retiré→jette, révélation retirée,
câblage coupé."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

avant = "  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────"
apres = """  /* ── v4.120 — LE LOT UX (PDF mort, flash, import au rail) ────────────
     Trois retours de Benjamin du 28/10. (1) « ⤓ Imprimer » ne fait rien :
     printGo lisait le logo de l'en-tête, retiré au dé-branding 4.104 —
     querySelector null, TypeError avant window.print(). (2) « on aperçoit
     l'ancienne page puis la nouvelle » : le squelette statique se peint
     pendant le chargement du script. (3) l'import doit vivre au pied du
     rail. La porte lit les fichiers réels. */
  (function lotUx4120(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const lire = function(f){ try { return fs.readFileSync(path.join(REPO, f), 'utf8'); } catch (e) { return ''; } };
    const html = lire('bilan_economique.html');
    const shell = lire('spk-shell.js');
    if (!html) echecs.push('bilan_economique.html introuvable');
    if (!shell) echecs.push('spk-shell.js introuvable');
    if (html) {
      /* (1) le logo A4 vient de l'embed, plus jamais du header retiré */
      const iPgo = html.indexOf('getElementById("printGo")');
      if (iPgo < 0) echecs.push('printGo introuvable');
      else {
        const bloc = html.slice(iPgo, iPgo + 900);
        if (bloc.indexOf('.hd-left img') !== -1)
          echecs.push('printGo lit encore le logo retiré de l en-tête (TypeError assurée)');
        if (bloc.indexOf('LOGO_SPK_SRC') === -1)
          echecs.push('printGo ne lit pas le logo A4 embarqué (LOGO_SPK_SRC)');
      }
      /* (2) l'anti-flash : le cache, la révélation après le premier rendu,
         et le filet à 5 s (si le rendu meurt, la page doit se montrer quand même) */
      const nbPret = html.split('data-pret').length - 1;
      if (nbPret < 3) echecs.push('l anti-flash est incomplet (cache + révélation + filet attendus, ' + nbPret + ' occurrence(s) de data-pret)');
      if (html.indexOf('html:not([data-pret]) body{visibility:hidden}') === -1)
        echecs.push('le body n est plus caché pendant le chargement');
      if (html.indexOf('setTimeout(function(){document.documentElement.setAttribute("data-pret","1")},5000)') === -1)
        echecs.push('le filet de révélation à 5 s a disparu');
      const iRend = html.indexOf(NL79() + 'render();');
      if (iRend < 0) echecs.push('le premier rendu introuvable');
      else {
        const apresRendu = html.slice(iRend, iRend + 300);
        if (apresRendu.indexOf('data-pret') === -1)
          echecs.push('la révélation ne se pose plus après le premier rendu');
      }
    }
    if (shell) {
      /* (3) le rail câble l'import au file picker de l'app */
      if (shell.indexOf('id="spkRailImport"') === -1)
        echecs.push('le bouton Importer a quitté le pied du rail');
      if (shell.indexOf('getElementById("importInput")') === -1)
        echecs.push('le bouton du rail ne déclenche plus le file picker de l app');
    }
    function NL79(){ return String.fromCharCode(10); }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'lot UX 4.120 : printGo vit (logo A4), anti-flash posé, import au rail' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────"""

assert s.count(avant) == 1, s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("porte lot UX posée")
