# -*- coding: utf-8 -*-
"""Tour 95 — v4.112.0 — le harnais : (1) la porte « verdict par outil 4.111 »
s'étend aux libellés du secours et de la mention des sortis (complément §1-2) ;
(2) nouvelle porte « polices mortes 4.112 » : les 8 noms absents du SW et du
build, le dossier fonts/ sans .woff2, et la constante CACHE bumpée."""
import io

p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. la porte 4.111 s'étend (libellés du secours + mention des sortis) ─────
remplace(
"""      /* les libellés du sémantique sont là, sans aucun K ni P_req (§2.6) */
      ['dont sorties du scénario', 'Levier technique', 'Levier productivité', 'Réconciliation']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('libellé absent : ' + m); });""",
"""      /* les libellés du sémantique sont là, sans aucun K ni P_req (§2.6) */
      ['dont sorties du scénario', 'Levier technique', 'Levier productivité', 'Réconciliation']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('libellé absent : ' + m); });

      /* v4.112 — le secours intra-outil TRACÉ (complément §1) et la mention
         des postes sortis sur le badge du groupe (complément §2) : un repli
         silencieux ou une mention perdue = la porte tombe. */
      ['apparié par secours — noms divergents', 'logement(s) apparié(s) par secours', 'sortisGroupe', 'nbParSecours', 'parSecours']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('v4.112 : libellé absent : ' + m); });
      /* la mention vit DANS le badge du groupe (ap-gs-tete), pas ailleurs */
      const iGs = code.indexOf('ap-gs-tete');
      if (iGs >= 0) {
        const blocGs = code.slice(iGs - 300, iGs + 1600);
        if (blocGs.indexOf('grpSortis') === -1 || blocGs.indexOf('poste') === -1)
          echecs.push('v4.112 : le badge du groupe ne porte plus la mention des postes sortis');
      }""",
"1. porte 4.111 étendue aux libellés v4.112")

# ── 2. la porte « polices mortes retirées » ──────────────────────────────────
remplace(
"""  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──""",
"""  /* ── v4.112 — LES 8 POLICES MORTES SONT RETIRÉES ─────────────────────
     Décision Benjamin (complément du 26/10 soir) : Barlow/Public Sans/IBM
     Plex de la coque d'origine ne servent jamais (l'app embarque ses
     polices en base64). Le retrait doit être COMPLET : fichiers, cache du
     SW (avec bump de CACHE, sinon les clients installés gardent le vieux
     cache), liste blanche du build — sinon un 404 ou un fichier fantôme
     revient. */
  (function policesMortes4112(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const MORTES = ['barlow-condensed-600', 'barlow-condensed-700',
      'public-sans-400', 'public-sans-500', 'public-sans-600', 'public-sans-700',
      'ibm-plex-mono-400', 'ibm-plex-mono-500'];
    const lire = function(f){ try { return fs.readFileSync(path.join(REPO, f), 'utf8'); } catch (e) { return ''; } };
    const sw = lire('service-worker.js');
    const buildCode = lire(path.join('outils', 'build-coque.mjs'));
    const html = lire('bilan_economique.html');
    if (!sw) echecs.push('service-worker.js introuvable');
    else {
      MORTES.forEach(function(m){ if (sw.indexOf(m) !== -1) echecs.push('le SW référence encore la police morte ' + m); });
      const mCache = sw.match(/const CACHE = "([^"]+)"/);
      if (!mCache) echecs.push('constante CACHE introuvable dans le SW');
      else if (mCache[1] === 'spk-suivi-shell-v6') echecs.push('la constante CACHE n a pas été bumpée (v6 périmée)');
    }
    if (!buildCode) echecs.push('build-coque.mjs introuvable');
    else MORTES.forEach(function(m){ if (buildCode.indexOf(m) !== -1) echecs.push('la liste blanche du build référence encore ' + m); });
    /* le dossier fonts/ : plus aucun .woff2 */
    const dirFonts = path.join(REPO, 'fonts');
    let restants = [];
    try {
      restants = fs.readdirSync(dirFonts).filter(function(f){ return /\\.woff2$/i.test(f); });
    } catch (e) { /* dossier absent : vide, acceptable */ }
    if (restants.length) echecs.push('fonts/ contient encore : ' + restants.join(', '));
    /* le HTML source ne référence aucun fichier fonts/ (déjà vrai avant, le
       garder vrai : une police ne revient qu accompagnée de sa décision) */
    if (html && html.indexOf('fonts/') !== -1) echecs.push('le HTML source référence un fichier fonts/');
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'polices mortes 4.112 : les 8 fichiers retirés (fonts/, SW + CACHE bumpé, build) et le HTML sans référence fonts/' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──""",
"2. porte polices mortes 4.112")

io.open(p, "w", encoding="utf-8").write(s)
print("patch C posé")
