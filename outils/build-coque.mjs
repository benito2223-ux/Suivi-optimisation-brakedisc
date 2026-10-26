/* ============================================================================
   Suivi_optimisation_SPK — build de la coque UI
   ----------------------------------------------------------------------------
   QUE FAIT CE SCRIPT
   Il prend le monolithe `bilan_economique.html` du repo git et lui ajoute la
   COQUE de navigation : le rail graphite à gauche (bureau), la barre d'onglets
   en bas (mobile), les écrans de travail en plein écran, et la direction
   visuelle « Console d'atelier » (papier chaud, graphite, un seul orange).

   POURQUOI UN SCRIPT, ET PAS UN HTML ÉCRIT À LA MAIN
   La coque vit dans deux fichiers à part — `spk-app.css` (le thème) et
   `spk-shell.js` (le comportement) — pour que la retouche visuelle se fasse
   SANS toucher au monolithe. Le script ne fait que brancher ces deux fichiers
   sur le HTML et y appliquer quelques ajustements de texte.

   LE PIÈGE QU'IL ÉVITE
   Le monolithe se termine par `</script>` SANS `</body>`. Un script qui
   injecte sur `</body>` ne trouve pas d'ancre et echoue (ou, pire, injecte au
   mauvais endroit). On injecte donc APRÈS le dernier `</script>`.

   LE PIÈGE N° 2 — LES ANCRES
   Chaque transformation est vérifiée : si l'ancre n'est pas trouvée, le build
   ÉCHOUE bruyamment (code de sortie ≠ 0) au lieu de livrer un fichier
   silencieusement incomplet. C'est le principe « fail loudly ».

   LE PIÈGE N° 3 — LES FINS DE LIGNE
   Le fichier du repo est en CRLF (Windows), le snapshot de prod peut être en
   LF. Toutes les ancres multi-lignes ci-dessous sont écrites en `\n`. On
   normalise donc le HTML avant de chercher les ancres, puis on restitue CRLF
   en sortie pour ne pas créer un diff de 20 000 lignes dans git.

   RÉFÉRENCE : la coque a été construite le 20/10/2026 par l'agent
   `auto-designer` dans son workspace (`.openclaw-autoclaw/.../dev-build`).
   Le 20/10 au soir, elle a été PORTÉE ici pour que le repo git redevienne
   l'unique source — deux workflow déployaient sur le même domaine dev, et le
   repo git avait écrasé la coque. Voir ECHANGES.md, Tour 76 et 77.

   OU EST ECRIT LE RESULTAT
   IMPORTANT : le build n'ecrit PAS dans le monolithe versionne. Il assemble
   un fichier de DEPLOIEMENT (`dist/bilan_economique.html`), qui est le seul
   a etre publie sur Surge. Pourquoi :

   - le monolithe versionne reste le LOGICIEL METIER, seul, sans la coque :
     un tour de Z Code ne doit pas se retrouver avec un diff de 1,5 Mo parce
     que la coque a ete reinjectee ;
   - la coque se retouche dans `spk-app.css` / `spk-shell.js`, SANS toucher
     au monolithe ;
   - `dist/` est reconstruit a chaque deploiement, il n'est pas versionne
     (voir .gitignore).

   Le deploiement publie donc `dist/`, pas la racine.

   USAGE :  node outils/build-coque.mjs
   ============================================================================ */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const RACINE = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HTML = path.join(RACINE, 'bilan_economique.html');
const CSS = path.join(RACINE, 'spk-app.css');
const SHELL = path.join(RACINE, 'spk-shell.js');
const DIST = path.join(RACINE, 'dist');

// CRLF ou LF ? On note, on normalise en LF pour les ancres, on restitue à la fin.
const brut = fs.readFileSync(HTML, 'utf8');
const crlf = brut.includes('\r\n');
let html = crlf ? brut.replace(/\r\n/g, '\n') : brut;

/* Le monolithe versionne ne doit PAS porter la coque : si elle y est, on la
   retire avant d'assembler, pour que le resultat ne depende pas de l etat du
   fichier. C'est ce qui rend le build reproductible d'une tour a l'autre. */
const A_SUPPRIMER = [
  /\n<link rel="stylesheet" href="spk-app\.css">/g,
  /\n<script src="spk-shell\.js" defer><\/script>/g
];
for (const motif of A_SUPPRIMER) html = html.replace(motif, '');

const remplacements = [];
const dejaFaits = [];

function remplacer(avant, apres, label) {
  // IDEMPOTENCE : le build doit pouvoir etre relance sur un monolithe qui
  // porte deja la coque (tour suivant de Z Code, par exemple). Si la
  // transformation est deja appliquee, on ne la rejoue pas.
  const dejaApplique = html.includes(apres);
  const occurrences = html.split(avant).length - 1;
  if (occurrences === 0 && dejaApplique) {
    dejaFaits.push(label);
    return;
  }
  if (occurrences === 0) {
    throw new Error(
      'ancre introuvable : ' + label + '\n' +
      'Le monolithe a change depuis le dernier build. Reprendre l ancre ici, ' +
      'ou faire disparaitre la transformation si elle n a plus lieu d etre.'
    );
  }
  if (occurrences !== 1) {
    throw new Error('ancre ambigue (' + occurrences + ' occurrences) : ' + label);
  }
  html = html.replace(avant, apres);
  remplacements.push(label);
}

/* --------------------------------------------------------------------------
   1. Le thème du navigateur suit le graphite de la coque (le monolithe est
      encore en bleu #1a1ea6 de l'ancienne charte).
   -------------------------------------------------------------------------- */
remplacer(
  '<meta name="theme-color" content="#1a1a1a">',
  '<meta name="theme-color" content="#23282b">',
  'theme-color du navigateur'
);

/* --------------------------------------------------------------------------
   2. (RETIRÉ en 4.101.1) — l'amener au haut de la Synthèse vit désormais
      DANS le monolithe : le handler de syntheseBtn ferme proprement les
      panneaux (voile modal inclus) et scrolle vers le haut. La coque ne
      transforme plus ce handler — le build doit rester reproductible.
   -------------------------------------------------------------------------- */

/* --------------------------------------------------------------------------
   3. Le Plan de conversion devient un espace de travail : meme sans ligne
      chiffree, il explique la suite au lieu d afficher une phrase vide.
   -------------------------------------------------------------------------- */
const ETAT_VIDE_PLAN = `
<div class="plan-empty">
  <div class="plan-empty-copy">
    <p class="plan-empty-kicker">Le passage à SPK, article par article</p>
    <h2>La production devient une feuille de route.</h2>
    <p class="plan-empty-lead">Dès qu'un scénario est en production, chaque article est chiffré ici : consommation actuelle, cible SPK, seuil de neutralité et gain annuel. Tu décides de l'étape de chaque ligne — le potentiel ne compte que ce que tu as réellement posé.</p>
    <ol class="plan-empty-steps">
      <li><span>01</span><div><b>Chiffrer</b><p>Le plan reprend les articles et leurs volumes de production.</p></div></li>
      <li><span>02</span><div><b>Proposer</b><p>La cible SPK et le prix cible se règlent ligne par ligne.</p></div></li>
      <li><span>03</span><div><b>Gagner</b><p>Le gain annuel se calcule en direct ; le CSV part en réunion.</p></div></li>
    </ol>
    <button class="primary" type="button" onclick="fermerPanneaux(); document.getElementById('addBtn').click();">Créer un scénario de production</button>
  </div>
  <div class="plan-empty-preview" aria-label="Aperçu d'une ligne du plan">
    <div class="pep-top"><span>APERÇU</span><b>KY3500 → LKT640</b></div>
    <div class="pep-line"><span>Prix actuel</span><b>8,40 €</b></div>
    <div class="pep-line"><span>Cible SPK</span><b>5,00 €</b></div>
    <div class="pep-line"><span>Seuil de neutralité</span><b>60 %</b></div>
    <div class="pep-gain"><span>Gain annuel</span><b>− 12 400 €</b></div>
    <p>Exemple de lecture. Les chiffres réels viennent de tes scénarios en production.</p>
  </div>
</div>`;
const ANCRE_PLAN_VIDE = /if\(!lignes\.length\) return `<p class="panel-hint">Aucun article de production chiffré[^`]*`;/;
if (ANCRE_PLAN_VIDE.test(html)) {
  html = html.replace(ANCRE_PLAN_VIDE, 'if(!lignes.length) return ' + JSON.stringify(ETAT_VIDE_PLAN) + ';');
  remplacements.push('etat vide du Plan de conversion (espace de travail)');
} else if (html.includes('plan-empty-copy')) {
  dejaFaits.push('etat vide du Plan de conversion (espace de travail)');
} else {
  throw new Error('ancre introuvable : etat vide du Plan de conversion');
}

/* --------------------------------------------------------------------------
   4. (v4.104) — le titre du Plan est deja posé sans emoji dans le monolithe,
      et les contrôles de consommation sont montés en tête du panneau par
      renderPlan lui-même : plus de transformation ici. Les ancres de cette
      section vivent désormais dans le source ; le build ne les détourne pas.
   -------------------------------------------------------------------------- */

/* --------------------------------------------------------------------------
   5. Le prix SPK par defaut est sorti du code A LA SOURCE (v4.103.0).
      Decision Benjamin du 20/10 (« chaque plaquette a son prix »), d'abord
      appliquee par ce build en detournant le monolithe — ce qui faisait
      DIVERGER les deux mondes : le harnais testait des comportements
      (prix par defaut, suggestion KY3500 a 5 EUR) que le fichier servi ne
      connaissait plus. Le retrait vit maintenant dans bilan_economique.html
      lui-meme ; ce build n'a plus qu'a EMPECHER le retour :
      une seule occurrence de prixSpk quelque part = build en echec.
   -------------------------------------------------------------------------- */
if (html.includes('prixSpk')) {
  throw new Error('prixSpk encore reference — la decision Benjamin du 20/10 (chaque plaquette a son prix, pas de prix par defaut) a ete contournée');
}

/* --------------------------------------------------------------------------
   6. Le theme arrive apres tous les styles inline et avant le script metier :
      il doit pouvoir SURCHARGER le CSS du monolithe, pas l'inverse.
   -------------------------------------------------------------------------- */
const wrapIndex = html.indexOf('<div class="wrap"');
if (wrapIndex < 0) throw new Error('wrap introuvable');
const firstScript = html.indexOf('<script>', wrapIndex);
if (firstScript < 0) throw new Error('script introuvable');
const lastStyle = html.lastIndexOf('</style>', firstScript);
if (lastStyle < 0) throw new Error('style introuvable');
if (html.includes('<link rel="stylesheet" href="spk-app.css">')) {
  dejaFaits.push('injection du lien vers spk-app.css');
} else {
  const insert = lastStyle + '</style>'.length;
  html = html.slice(0, insert) + '\n<link rel="stylesheet" href="spk-app.css">\n' + html.slice(insert);
  remplacements.push('injection du lien vers spk-app.css');
}

/* --------------------------------------------------------------------------
   7. La coque de navigation est chargee APRES le script metier : elle
      deplace les boutons existants dans le rail, sans recreer leurs
      ecouteurs. Le fichier se termine par `</script>` SANS `</body>` : on
      injecte donc apres le dernier `</script>`, jamais sur `</body>`.
   -------------------------------------------------------------------------- */
if (html.includes('<script src="spk-shell.js" defer></script>')) {
  dejaFaits.push('injection du script de coque spk-shell.js');
} else {
  const lastScriptEnd = html.lastIndexOf('</script>');
  if (lastScriptEnd < 0) throw new Error('fin de script introuvable');
  html = html.slice(0, lastScriptEnd + '</script>'.length)
    + '\n<script src="spk-shell.js" defer></script>\n'
    + html.slice(lastScriptEnd + '</script>'.length);
  remplacements.push('injection du script de coque spk-shell.js');
}

/* --------------------------------------------------------------------------
   8. Restitution des fins de ligne d'origine, pour ne pas faire bouffer le
      diff de git de 20 000 lignes.
   -------------------------------------------------------------------------- */
if (crlf) html = html.replace(/\n/g, '\r\n');

/* On assemble dans dist/ : le monolithe versionne reste intact. */
fs.mkdirSync(DIST, { recursive: true });
const SORTIE = path.join(DIST, 'bilan_economique.html');
fs.writeFileSync(SORTIE, html, 'utf8');

/* Les fichiers annexes de la coque vont avec le HTML. */
for (const nom of ['spk-app.css', 'spk-shell.js']) {
  fs.copyFileSync(path.join(RACINE, nom), path.join(DIST, nom));
}
fs.mkdirSync(path.join(DIST, 'fonts'), { recursive: true });
/* v4.112 — purge AVANT copie : le build ne nettoyait pas dist/, et le retrait
   des 8 polices mortes est reparti une fois avec les anciennes encore dans
   dist/ (vues après déploiement, corrigé le jour même). Un dossier fonts/
   source vide reste vide au dist. */
for (const f of fs.readdirSync(path.join(DIST, 'fonts'))) {
  fs.rmSync(path.join(DIST, 'fonts', f), { force: true });
}
if (fs.existsSync(path.join(RACINE, 'fonts'))) {
  for (const f of fs.readdirSync(path.join(RACINE, 'fonts'))) {
    fs.copyFileSync(path.join(RACINE, 'fonts', f), path.join(DIST, 'fonts', f));
  }
}
for (const nom of ['index.html', 'manifest.webmanifest', 'service-worker.js']) {
  const src = path.join(RACINE, nom);
  if (fs.existsSync(src)) fs.copyFileSync(src, path.join(DIST, nom));
}
fs.mkdirSync(path.join(DIST, 'icons'), { recursive: true });
for (const f of fs.readdirSync(path.join(RACINE, 'icons'))) {
  fs.copyFileSync(path.join(RACINE, 'icons', f), path.join(DIST, 'icons', f));
}

/* --------------------------------------------------------------------------
   La liste blanche de publication (`.surgeignore`).
   Surge lit ce fichier DANS le dossier deploye : il doit donc vivre dans
   `dist/`, pas seulement a la racine. Il est strict par defaut (`*` puis
   exceptions) : tout ce qui n'est pas explicitement liste ne part JAMAIS
   sur Surge — donnees d'essais, notes internes, journal, outillage.
   --------------------------------------------------------------------------- */
const SURGEIGNORE = `# Deploiement verrouille (genere par outils/build-coque.mjs).
# Seuls ces fichiers partent sur Surge. Tout le reste reste local :
# donnees d'essais reelles, notes internes, journal, outillage.
*
!bilan_economique.html
!index.html
# La coque de navigation (v4.100.0)
!spk-app.css
!spk-shell.js
# PWA : manifeste reel + service worker + icones
!manifest.webmanifest
!service-worker.js
!icons
!icons/icon-192.png
!icons/icon-512.png
!icons/icon-512-maskable.png
# Polices : v4.112 — les 8 fichiers de la coque d'origine sont retires
# (Barlow/Public Sans/IBM Plex mortes, l'app embarque ses polices en base64).
# La ligne !fonts reste pour le jour ou une police de marque revient.
!fonts
`;
fs.writeFileSync(path.join(DIST, '.surgeignore'), SURGEIGNORE, 'utf8');

console.log('coque assemblee dans dist/');
console.log('  sortie : ' + path.relative(RACINE, SORTIE));
console.log('  transformations appliquees : ' + remplacements.length);
remplacements.forEach((r, i) => console.log('   ' + (i + 1) + '. ' + r));
if (dejaFaits.length) {
  console.log('  deja en place : ' + dejaFaits.length);
  dejaFaits.forEach((r, i) => console.log('   - ' + r));
}
console.log('  taille : ' + fs.statSync(SORTIE).size + ' octets');
console.log('  fins de ligne : ' + (crlf ? 'CRLF (d origine)' : 'LF (d origine)'));
console.log('  css : ' + path.relative(RACINE, CSS));
console.log('  shell : ' + path.relative(RACINE, SHELL));
