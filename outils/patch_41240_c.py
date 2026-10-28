# -*- coding: utf-8 -*-
"""Tour 99 — v4.124.0 — version, NOUVEAUTES, et la porte harnais « P0 du brief »."""
import io, re

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(fichier, avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── version ──────────────────────────────────────────────────────────────────
remplace(p, 'const TOOL_VERSION = "4.123.0";', 'const TOOL_VERSION = "4.124.0";', "1. TOOL_VERSION")

m = re.search(r'const NOUVEAUTES = \[\n  \{ version:"4\.[0-9.]+", date:"[0-9/]+", points:\[\n', s)
assert m, "ancre NOUVEAUTES introuvable"
entree = (
    'const NOUVEAUTES = [\n'
    '  { version:"4.124.0", date:"28/10/2026", points:[\n'
    '    "<b>Les quatre corrections du brief de revue (P0).</b> <b>Un commentaire technique s\\u2019affichait en texte sur les tuiles de scénario</b> — retiré. <b>La fenêtre « Bienvenue » ne bloque plus le démarrage</b> : elle devient un bandeau discret fermable, affiché une seule fois. <b>Le vert du bandeau de fiche dit de nouveau quelque chose</b> : il marque la validation quand le seuil est atteint (plus une couleur de position), et les trois précisions (durée de vie, €/arête, temps de cycle) descendent dans une ligne secondaire — trois chiffres ouvrent la fiche. <b>Le rail se recentre</b> : Atelier et Tableau quittent la navigation (leurs vues vivent dans les onglets de la Vue d\\u2019ensemble) — il reste Vue d\\u2019ensemble · Synthèse · Matis · + Scénario · Transmettre."\n'
    '  ]},\n'
)
s = s[:m.start()] + entree + s[m.start():]
print("ok : entrée NOUVEAUTES")
io.open(p, "w", encoding="utf-8").write(s)

# ── la porte harnais ─────────────────────────────────────────────────────────
p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

avant = "  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────"
apres = """  /* ── v4.124 — LES P0 DU BRIEF EXTERNE ─────────────────────────────────
     La revue externe (chantier_zcode, Benjamin) : un commentaire rendu en
     texte dans les tuiles, un popup modal au démarrage, un vert positionnel,
     un rail qui contredit le changelog. La porte lit les fichiers réels et
     garde chaque correction. */
  (function p0Brief4124(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const lire = function(f){ try { return fs.readFileSync(path.join(REPO, f), 'utf8'); } catch (e) { return ''; } };
    const html = lire('bilan_economique.html');
    if (!html) echecs.push('bilan_economique.html introuvable');
    else {
      const NLX = String.fromCharCode(10);
      /* (1) P0-1 : la chaîne fautive est absente (le contrôle de rendu
         « innerText sans /* » vit dans le test navigateur, pas ici) */
      if (html.indexOf('est supprimee - la fiche en dessous dit tout') !== -1)
        echecs.push('le commentaire fautif est de retour dans le fichier');
      /* (1bis) la règle du cahier est maintenant gardée : aucun commentaire
         /* v4 suivi d'une fin de template */ sur la même ligne qu'un backtick
         dans le bloc des tuiles — contrôle par ligne : une ligne qui contient
         à la fois « `; » (fin de template) et « /* » est suspecte */
      html.split(NLX).forEach(function(l){
        if (l.indexOf('`;') !== -1 && l.indexOf('/* v4') !== -1)
          echecs.push('ligne suspecte (commentaire dans un template) : ' + l.trim().slice(0, 60));
      });
      /* (2) P0-2 : le bienvenue n'est plus une modale */
      const iBien = html.indexOf('Bienvenue dans la base 2026/2027');
      if (iBien < 0) echecs.push('le message de bienvenue a disparu sans remplacement');
      else {
        const zone = html.slice(Math.max(0, iBien - 1500), iBien + 1500);
        if (zone.indexOf('ouvrirDialogue') !== -1)
          echecs.push('le bienvenue s affiche encore dans une fenêtre modale');
        if (zone.indexOf('bandeauPremiere') === -1 && html.indexOf('id="bandeauPremiere"') === -1)
          echecs.push('le bandeau non bloquant de bienvenue est absent');
      }
      /* (3) P0-3 : le vert est un état, plus une position */
      const mLast = html.match(/\\.foot-cell:last-child\\{[^}]*\\}/);
      if (mLast && mLast[0].indexOf('fill-good') !== -1)
        echecs.push('le vert positionnel last-child est de retour');
      if (html.indexOf('.foot-cell.is-ok') === -1)
        echecs.push('la classe explicite is-ok est absente');
      const iValid = html.indexOf('const validationCell');
      if (iValid < 0) echecs.push('validationCell introuvable');
      else {
        const bloc = html.slice(iValid, iValid + 400);
        if (bloc.indexOf('is-ok') === -1)
          echecs.push('la validation ne porte plus le vert explicite');
      }
      if (html.indexOf('class="foot-second"') === -1)
        echecs.push('la ligne secondaire de la fiche a disparu');
      /* (4) P0-4 : Atelier / Tableau masqués du rail */
      const mRail = html.match(/\\.toolbar-ecrans #carteBtn[^}]*\\}/);
      if (!mRail) echecs.push('la règle de masquage Atelier/Tableau a disparu');
      else if (mRail[0].indexOf('display:none') === -1 && mRail[0].indexOf('display: none') === -1)
        echecs.push('Atelier/Tableau ne sont plus masqués');
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'P0 brief 4.124 : tuile sans commentaire rendu, bienvenue non modal, vert explicite, rail recentré' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────"""

assert s.count(avant) == 1, s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("porte P0 posée")
