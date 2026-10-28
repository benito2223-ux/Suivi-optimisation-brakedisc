# -*- coding: utf-8 -*-
"""Tour 101 — v4.125.0 — version + NOUVEAUTES + la porte harnais « lot 4.125 ».
Le piège du double const NOUVEAUTES (trois fois vu) est désamorcé : l'insertion
se fait APRÈS la ligne const, pas en réémettant l'entête suivant."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()

# ── 1. version ───────────────────────────────────────────────────────────────
assert s.count('const TOOL_VERSION = "4.124.1";') == 1
s = s.replace('const TOOL_VERSION = "4.124.1";', 'const TOOL_VERSION = "4.125.0";', 1)
print("ok : TOOL_VERSION")

# ── 2. NOUVEAUTES : insertion APRÈS le const existant (pas d'entête recopié) ─
ancre = 'const NOUVEAUTES = [\n'
assert s.count(ancre) == 1
entree = (
    '  { version:"4.125.0", date:"28/10/2026", points:[\n'
    '    "<b>La navigation se resserre (lot 2 de la revue).</b> L\\u2019outil s\\u2019ouvre sur <b>l\\u2019écran de travail</b> — la Vue d\\u2019ensemble reste à un clic (ou #accueil), elle ne se pose plus en plein écran au démarrage. La rangée <b>« Je cherche… »</b> quitte la fiche (Ctrl+K reste). <b>Transmettre passe en fin de barre</b>, près de + Scénario, et y ajoute <b>Importer un suivi</b> (l\\u2019import et l\\u2019export au même endroit ; le bouton de la barre et celui du rail disparaissent). La <b>tuile ouverte se réduit à une ligne</b> — le nom et le statut sont ceux de la fiche en dessous — et le bandeau de coût à l\\u2019état vide (cible non renseignée) devient une <b>ligne grise</b> au lieu d\\u2019une grande carte. Et l\\u2019anneau de focus ne se pose plus sur « Postes » à l\\u2019ouverture de la Vue d\\u2019ensemble."\n'
    '  ]},\n'
)
s = s.replace(ancre, ancre + entree, 1)
print("ok : entrée NOUVEAUTES (après le const)")

io.open(p, "w", encoding="utf-8").write(s)

# ── 3. la porte harnais ──────────────────────────────────────────────────────
p = "build_harness.py"
s = io.open(p, encoding="utf-8").read()

avant = "  /* ── v4.124.1 — L'ÉQUILIBRE CSS (leçon de la 4.124.0) ──────────────────"
apres = """  /* ── v4.125 — LE LOT NAVIGATION ET DOUBLONS ───────────────────────────
     Brief externe P1-1/P1-2/P1-3, feu vert Benjamin : ouverture sur l'écran
     de travail (Vue d'ensemble sur clic ou #accueil), boussole retirée de la
     fiche, Transmettre en fin de barre avec Importer dans son groupe
     « L'archive », tuile ouverte à une ligne, état vide en ligne grise,
     anneau de focus retiré de l'ouverture de la Vue d'ensemble. */
  (function lot4125(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const lire = function(f){ try { return fs.readFileSync(path.join(REPO, f), 'utf8'); } catch (e) { return ''; } };
    const html = lire('bilan_economique.html');
    const shell = lire('spk-shell.js');
    if (!html) echecs.push('bilan_economique.html introuvable');
    else {
      /* (1) l'ouverture : la Vue d'ensemble ne s'ouvre plus toute seule */
      const mOpen = html.match(/if\\([^)]*\\)\\s*ouvrirAccueil\\(\\);/);
      if (!mOpen) echecs.push('la condition d ouverture de la Vue d ensemble est introuvable');
      else if (mOpen[0].indexOf('#accueil') === -1 || mOpen[0].indexOf('!location.hash') !== -1)
        echecs.push('la Vue d ensemble s ouvre encore sans #accueil');
      /* (2) la boussole n'est plus rendue dans la fiche */
      const iFiche = html.indexOf("el.innerHTML = ");
      const zone = html.slice(html.indexOf('boussoleHTML'), html.indexOf('boussoleHTML') + 200);
      if (zone.indexOf('boussoleHTML() +') !== -1)
        echecs.push('la boussole est encore rendue en tête de fiche');
      /* (3) Transmettre APRÈS + Scénario dans le DOM (fin de barre) */
      const iT = html.indexOf('id="transmettreBtn"');
      const iA = html.indexOf('id="addBtn"');
      if (iT < 0 || iA < 0) echecs.push('Transmettre ou + Scénario introuvable');
      else if (iT < iA) echecs.push('Transmettre est encore AVANT + Scénario (fin de barre attendue)');
      /* (4) Importer dans le menu Transmettre ; plus de bouton de barre ni de rail */
      if (html.indexOf('id="importMenuBtn"') === -1)
        echecs.push('l item Importer a disparu du menu Transmettre');
      if (html.indexOf('id="importBtn"') !== -1)
        echecs.push('le bouton Importer de la barre est de retour');
      if (shell.indexOf('spkRailImport') !== -1)
        echecs.push('le bouton Importer du rail est de retour');
      /* (5) la tuile ouverte à une ligne (pas de badges sur l'actif) */
      const iCarte = html.indexOf('if(sc.id === activeId) return `');
      if (iCarte < 0) echecs.push('la réduction de la tuile ouverte a disparu');
      else {
        const bloc = html.slice(iCarte, iCarte + 500);
        if (bloc.indexOf('tc-badges') !== -1 || bloc.indexOf('tag-pill') !== -1)
          echecs.push('la tuile ouverte porte encore badges ou tags');
      }
      /* (6) la ligne grise d'état vide */
      if (html.indexOf('pcb-vide') === -1)
        echecs.push('la ligne grise d état vide a disparu');
      /* (7) la Vue d'ensemble ne vole plus le focus */
      if (html.indexOf('data-sans-focus') === -1)
        echecs.push('le mécanisme sans-focus a disparu');
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'lot 4.125 : ouverture sur la fiche, boussole retiree, Transmettre en fin avec Importer, tuile a une ligne, etat vide gris' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.124.1 — L'ÉQUILIBRE CSS (leçon de la 4.124.0) ──────────────────"""

assert s.count(avant) == 1, s.count(avant)
s = s.replace(avant, apres, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("porte lot 4.125 posée")
