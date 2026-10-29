# -*- coding: utf-8 -*-
# Tour 109 — 4.130.0 — patch E : la porte « coque 4.100 » recalée.
# La porte décrivait le rail de colonne (z-index du rail, left:248px,
# poignée de repli) : le rail n'existe plus — l'en-tête du design system le
# remplace. Les points toujours vrais sont gardés (build, polices brand
# guide, cache SW) ; les points rail deviennent leurs équivalents en-tête :
# .spk-head présent dans les deux fichiers, plus AUCUNE construction du
# rail, z-index de l'en-tête au-dessus des écrans plein écran, les écrans
# posés sous --spk-head-h, la poignée de repli neutralisée (plus de repli).
import io

F = "build_harness.py"
src = io.open(F, encoding="utf-8").read()

DEBUT = """    // (3) la coque est complete
    if (css.indexOf('.spk-rail') === -1) echecs.push('spk-app.css ne definit pas le rail');
    if (shell.indexOf('spk-rail') === -1) echecs.push('spk-shell.js ne construit pas le rail');"""
n = src.count(DEBUT)
assert n == 1, "ancre (3) : %d occurrences (attendu 1)" % n

FIN = """    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'coque 4.100 : la coque est dans le repo git, le rail reste visible et repliable (12 points verifies dans les fichiers reels)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));"""
n = src.count(FIN)
assert n == 1, "ancre fin coque : %d occurrences (attendu 1)" % n

i = src.find(DEBUT)
j = src.find(FIN) + len(FIN)

NOUVEAU = """    // (3) la coque est complete — v4.130 : l EN-TETE remplace le rail
    if (css.indexOf('.spk-head') === -1) echecs.push('spk-app.css ne definit pas l en-tete');
    if (shell.indexOf('spk-head') === -1) echecs.push('spk-shell.js ne construit pas l en-tete');
    if (shell.indexOf('spk-head-r2') === -1) echecs.push('la rangée 2 de l en-tête (onglets + fil) est absente');
    if (shell.indexOf('spk-head-actions') === -1) echecs.push('les actions de la rangée 1 sont absentes');
    if (shell.indexOf('hdTitle') === -1) echecs.push('le titre de la référence n est pas déplacé dans l en-tête');
    /* le rail de colonne ne doit PLUS être construit : l en-tête le remplace */
    if (shell.indexOf('className = "spk-rail"') !== -1) echecs.push('spk-shell.js construit encore le rail de colonne');
    /* v4.109 (brand guide SPK, Tour 91) : les polices de la coque sont
       Open Sans Condensed / Open Sans — Barlow/Public Sans de
       l'auto-designer sont retirées. La porte suit : la déclaration
       doit être là, et la police retirée ne doit pas revenir. */
    if (css.indexOf("'Open Sans Condensed'") === -1) echecs.push('les polices de la coque ne sont pas au brand guide (Open Sans Condensed absente)');
    if (css.indexOf('Barlow Condensed') !== -1) echecs.push('la police retirée Barlow Condensed est de retour dans la coque');
    /* le SW : on verifie le TABLEAU SHELL, pas le fichier entier — la
       chaine peut apparaitre dans un commentaire sans etre en cache. */
    const iShell = sw.indexOf('const SHELL = [');
    const shellSw = iShell < 0 ? '' : sw.slice(iShell, iShell + 900);
    if (shellSw.indexOf('spk-app.css') === -1) echecs.push('le service worker ne met pas la coque en cache');
    if (shellSw.indexOf('spk-shell.js') === -1) echecs.push('le service worker ne met pas le shell en cache');

    // (4) l en-tete reste VISIBLE : z-index superieur aux surfaces plein ecran.
    //     C est LE point du bug d origine (le rail 60 sous les panneaux 80) :
    //     la meme exigence vaut pour l en-tete (90) — lire le z-index DANS la
    //     regle .spk-head, par decoupage de chaine (pas de regex : le harnais
    //     est du JS dans une chaine Python non-raw).
    function lireZIndexApres(texte, apres, fenetre){
      const i = texte.indexOf(apres);
      if (i < 0) return null;
      const tranche = texte.slice(i, i + (fenetre || 200));
      const j = tranche.indexOf('z-index:');
      if (j < 0) return null;
      const reste = tranche.slice(j + 9).replace(/^[^0-9]+/, '');
      const chiffres = (reste.match(/[0-9]+/) || [''])[0];
      return chiffres ? Number(chiffres) : null;
    }
    const zHead = lireZIndexApres(css, '.spk-head{', 160);
    const zPanneau = lireZIndexApres(css, '.panel.panel-large,', 700);
    if (zHead === null || zPanneau === null || isNaN(zHead) || isNaN(zPanneau)) echecs.push('impossible de lire les z-index de l en-tete et des panneaux');
    else if (zHead <= zPanneau) echecs.push('l en-tete (z ' + zHead + ') passe sous les panneaux (z ' + zPanneau + ') : il disparait de l ecran');
    /* les ecrans plein ecran se posent SOUS l en-tete (hauteur mesurée) */
    if (css.indexOf('top:var(--spk-head-h)') === -1) echecs.push('les ecrans plein ecran ne se posent pas sous l en-tete');
    /* la poignee de repli du rail est neutralisee : le repli n existe plus */
    if (css.indexOf('#spkRailToggle{ display:none !important; }') === -1) echecs.push('la poignee de repli du rail n est pas neutralisee');

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'coque 4.130 : l en-tete du design system remplace le rail (barre navy, onglets, actions, hauteur mesurée) (12 points verifies dans les fichiers reels)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));"""

src = src[:i] + NOUVEAU + src[j:]
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("porte coque recalée sur l'en-tête (4.130)")
