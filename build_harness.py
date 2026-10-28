"""Génère un harnais Node pour exécuter les fonctions du suivi hors navigateur.



Usage : python build_harness.py [sortie.js]

Puis :  node sortie.js   (depuis la racine du repo)



Le harnais neutralise le DOM (le suivi est un fichier unique sans build) et

supprime les deux entrées de fin de script qui ne concernent pas la logique

(le rendu initial et la fenêtre Nouveautés). Tout le reste — y compris runTests —

est exécuté tel quel, sur le vrai code.

"""

import io, re, json, sys, os



REPO = os.path.dirname(os.path.abspath(__file__))

SRC = os.path.join(REPO, 'bilan_economique.html')

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(

    os.environ.get('LOCALAPPDATA', 'C:/Users/Admin/AppData/Local'), 'Temp', 'h451.js')



src = io.open(SRC, encoding='utf-8').read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', src)

code = '\n;\n'.join(scripts)

# neutraliser les deux entrees DOM de fin de script (hors logique testee)

code = re.sub(r'verifierNouveautes\(\);(\s*//[^\n]*)?\s*$', ';', code, flags=re.M)

code = re.sub(r'^render\(\);\s*$', ';', code, flags=re.M)



API = ("get TOOL_VERSION(){return TOOL_VERSION;}, normalizeLigne, normalizeReference, "

       "normalizeOp, normalizeScenario, normalizeProjet, runTests, lignesDuProjet, "

       "projetContientScenario, toggleTagScenario, resoudreTag, matisRecap, libelleEcartMatis, "

       "matisPorteOutilPosition, matisClePorteOutil, reparerOutilsD1D2, reparerOutilsRapport, "

       "detecterOutilsD1D2, migrerOutilsD1D2, compterOutilsD1D2, detecterInversionMabec, migrerInversionMabec, compterInversionsMabec, "

       "_matisFeuille, "

       "getActiveLigne, preparerImportDepuis, axesActifs, reattribuerEssai, opContenantScenario, brancheDeScenario, destinationsEssai, remapperLogementsEssai, normeCleLogement, etatCodification, articlesScenario, codificationScenario, badgeCodifScenario, dossierVisite, dateIsoMax, joursDepuis, decompositionLeviers, planPrioritesData, plaquettesCommunes, simulCSV, catalogueSeed, catalogueAppliquer, catalogueCSV, catalogueDepuisCSV, planLignes, catalogueSuggestion, catalogueParIso, suggestionDepuisArbre, valeurModale, appliquerSuggestionCatalogue, conso2025DepuisFeuille, normalizeConso2025, conso2025SectionsActives, conso2025Somme, planCoutCible, get conso2025(){return conso2025}, set conso2025(v){conso2025=v}, get conso2025SectionsOn(){return conso2025SectionsOn}, set conso2025SectionsOn(v){conso2025SectionsOn=v}, get planSource(){return planSource}, set planSource(v){planSource=v}, get plan(){return plan}, set plan(v){plan=v}, get lignes(){return lignes}, set lignes(v){lignes=v}, "

       "get projets(){return projets}, set projets(v){projets=v}, "

       "get activeProjetId(){return activeProjetId}, set activeProjetId(v){activeProjetId=v}, "

       "get config(){return config}, set config(v){config=v}, "

       "get data(){return data}, set data(v){data=v}")



HARNESS = '''const fs = require('fs');

const node = ()=>({ getAttribute:()=>null, setAttribute(){}, removeAttribute(){}, hasAttribute:()=>false,

  style:{}, dataset:{}, scrollIntoView(){}, focus(){}, blur(){}, click(){}, setPointerCapture(){},

  classList:{add(){},remove(){},toggle(){},contains:()=>false,replace(){}},

  appendChild(){}, removeChild(){}, insertBefore(){}, contains:()=>true, remove(){}, cloneNode(){return node()},

  addEventListener(){}, removeEventListener(){}, querySelector:()=>node(), querySelectorAll:()=>[],

  getBoundingClientRect:()=>({top:0,left:0,right:0,bottom:0,width:0,height:0}),

  getClientRects:()=>[], toDataURL:()=>"", innerHTML:"", outerHTML:"", textContent:"", value:"",

  checked:false, disabled:false, files:[], parentNode:null, children:[], childNodes:[] });

const doc = { getElementById:(id)=>_els[id]||(_els[id]=node()), querySelector:()=>node(), querySelectorAll:()=>[], createElement:node,

  createTextNode:node, createElementNS:node, documentElement:node(), body:node(), head:node(),

  addEventListener(){}, removeEventListener(){}, location:{hash:""}, cookie:"", readyState:"complete" };

/* v4.60 (tour 16) : getElementById DOIT rendre le même élément d'un appel à

   l'autre -- les tests de rendu écrivent innerHTML puis le relisent ; un stub

   jetable les faisait échouer en node alors qu'ils passent au navigateur. */

const _els = {};

global.document = doc;

global.window = { addEventListener(){}, removeEventListener(){}, matchMedia:()=>({matches:false,addEventListener(){},addListener(){}}),

  localStorage:{getItem:()=>null,setItem(){},removeItem(){},clear(){}}, location:{hash:"",href:"",origin:"",protocol:"http:"},

  open(){}, print(){}, close(){}, alert:()=>{}, confirm:()=>true, prompt:()=>null, setTimeout, clearTimeout, setInterval, clearInterval,

  requestAnimationFrame:f=>setTimeout(f,0), getComputedStyle:()=>({getPropertyValue:()=>""}), devicePixelRatio:1,

  navigator:{userAgent:"node",serviceWorker:{register:()=>Promise.resolve()},clipboard:{}}, screen:{width:1400,height:900},

  crypto:{getRandomValues:a=>a}, innerWidth:1400, innerHeight:900, scrollTo(){}, postMessage(){} };

global.localStorage = global.window.localStorage;

global.location = global.window.location; global.navigator = global.window.navigator;

/* v4.99.0 — le stub `location` porte maintenant un `hostname` explicite.
   Le code livré teste l'hôte pour savoir s'il est sur l'adresse de dev
   (cloud débranché). Sans `hostname` dans le stub, `location.hostname` valait
   `undefined` : le test passait par accident (undefined ne correspond à
   aucun nom) et la branche « cloud débranché » n'était JAMAIS testée en node.
   Ici l'hôte du harnais est explicitement celui de la PRODUCTION : le
   harnais vérifie donc le chemin normal, et la porte dédiée vérifie le
   chemin « débranché » en simulant l'hôte de dev. */
global.window.location.hostname = "suivi-optimisation-septfons.surge.sh";
global.window.location.host = "suivi-optimisation-septfons.surge.sh";
global.location.hostname = "suivi-optimisation-septfons.surge.sh";
global.location.host = "suivi-optimisation-septfons.surge.sh";

global.matchMedia = global.window.matchMedia; global.getComputedStyle = global.window.getComputedStyle;

global.addEventListener = ()=>{}; global.removeEventListener = ()=>{};

global.requestAnimationFrame = global.window.requestAnimationFrame;

global.FileReader = class { readAsDataURL(){} addEventListener(){} readAsText(){} };

global.Image = class { set src(v){} get width(){return 0;} get height(){return 0;} addEventListener(){} };

global.CanvasRenderingContext2D = class {}; global.HTMLCanvasElement = class {}; global.OffscreenCanvas = class {};

global.DOMParser = class { parseFromString(){ return doc; } };

global.Blob = class { constructor(){} }; global.File = class {};

global.URL = { createObjectURL:()=>"blob:x", revokeObjectURL(){} };

global.fetch = () => Promise.reject(new Error("hors ligne"));

global.MutationObserver = class { observe(){} disconnect(){} };

global.IntersectionObserver = class { observe(){} disconnect(){} };

global.ResizeObserver = class { observe(){} disconnect(){} };

global.self = global.window; global.top = global.window; global.parent = global.window;

global.performance = { now:()=>0 }; global.alert = ()=>{}; global.confirm = ()=>true; global.prompt = ()=>null;



const api = __CODE__ + `

;globalThis.__api = { __API__ };

`;

try {

  new Function(api)();

  const A = globalThis.__api;

  const r = A.runTests();

  console.log('VERSION:', A.TOOL_VERSION);

  console.log('RESULTAT:', r.total, 'tests |', r.echecs, 'echecs');

  (r.details||[]).filter(d=>!d.pass).forEach(d=>console.log('  ECHEC:', d.nom, '| recu=', JSON.stringify(d.recu), '| attendu=', JSON.stringify(d.attendu)));

  if(!r.echecs) console.log('TOUT EST VERT');



  /* ── v4.63.3 — CONTRASTE DES TOKENS DE SURFACE ──────────────────────────

     Une suite de fonctions pures ne voit pas une couleur : c'est une mesure,

     pas une logique. Le trou a été trouvé par contre-regard le 30/09 — remettre

     --label à 2,81:1 n'a déclenché AUCUN échec, et c'est exactement pour ça

     que personne ne l'avait vu. Ce bloc ferme la porte (constitution §5.6 :

     « un chiffre qu'on ne peut pas justifier n'est pas affiché » — et de même

     une couleur qu'on ne peut pas lire ne s'affiche pas).

     On lit le CSS réel du fichier, pas une constante du test. */

  (function contrasteTokens(){

    const fs = require('fs');

    const html = fs.readFileSync('bilan_economique.html', 'utf8');

    /* On cherche le BLOC :root de référence, pas la première accolade : il

       commence par un commentaire, donc un regex non gore s'arreterait la

       premiere fois et ne verrait aucun token. On prend le premier :root dont

       le corps contient --ink (les autres sont le @media print et le template

       du rapport, autonomes par construction). */

    let corps = null;

    for (const m of html.matchAll(/:root\s*\{/g)) {

      const debut = m.index + m[0].length;

      let prof = 1, i = debut;

      while (i < html.length && prof > 0) {

        const c = html[i];

        if (c === '{') prof++;

        else if (c === '}') prof--;

        i++;

      }

      const bloc = html.slice(debut, i);

      if (/--ink\s*:/.test(bloc)) { corps = bloc; break; }

    }

    if (!corps) { console.log('  CONTRASTE : bloc :root de reference non trouve — test non joue'); process.exitCode = 2; return; }

    const tokens = {};

    for (const m of corps.matchAll(/(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*[;,]/g)) {

      tokens[m[1]] = m[2];

    }

    if (!tokens['--ink'] || !tokens['--label']) {

      console.log('  CONTRASTE : tokens de surface absents du bloc lu — test non joue');

      process.exitCode = 2; return;

    }

    function lum(h){

      h = h.trim().replace('#','');

      if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];

      if (h.length > 6) h = h.substr(0,6);

      const r = parseInt(h.substr(0,2),16)/255, g = parseInt(h.substr(2,2),16)/255, b = parseInt(h.substr(4,2),16)/255;

      const f = c => c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);

      return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b);

    }

    function cr(a,b){ const la = lum(a), lb = lum(b); return (Math.max(la,lb)+0.05)/(Math.min(la,lb)+0.05); }

    /* seuil AA sur texte normal : 4,5:1. Le texte de l'outil est petit

       (libelles 10-11 px), donc on ne negotiate pas a 3:1. */

    const paires = [

      ['--label','--white',    'les intitulés sur une carte'],

      ['--body','--white',     'les paragraphes sur une carte'],

      ['--ink','--white',      'le texte principal sur le fond de page'],

      ['--body','--white',     'les descriptions sur le fond de page'],

      ['--blue','--white',     "le bleu d'action sur une carte"],

      ['--red','--white',      'le rouge CeramTec sur une carte']

    ];

    let joues = 0, echecs = 0;

    for (const [fg, bg, pourquoi] of paires) {

      if (!tokens[fg] || !tokens[bg]) { console.log('  CONTRASTE : token absent --'+fg+' ou --'+bg+' — non teste'); continue; }

      const v = cr(tokens[fg], tokens[bg]);

      joues++;

      const okc = v >= 4.5;

      if (!okc) echecs++;

      console.log((okc?'  ok  ':'  ECHEC ')+'contraste : '+pourquoi+' — '+fg+' '+tokens[fg]+' sur '+bg+' '+tokens[bg]+' = '+v.toFixed(2)+':1 (seuil 4,5:1)');

    }

    if (joues) console.log('  CONTRASTE : '+joues+' paires verifiees sur le CSS reel du fichier, '+echecs+' sous le seuil');

    /* Le contraste compte comme un echec de la suite : on l'ajoute au total

       plutot que de fixer process.exitCode, que le exit() du harnais ecraserait

       (constat du 30/09 — deux lignes plus bas). */

    r.echecs += echecs;

  })();



  /* ── v4.80 — L'IDENTITÉ SPK, ÉCRITE SOIT QU'ELLE PUISSE REVENIR ───────────

     Constat du Tour 56 : on a restauré la palette v3.15 et surtout la

     hiérarchie de forme (Open Sans Condensed / Open Sans / IBM Plex Mono — brand guide SPK, 4.109). Le contre-regard

     a montré qu'UNE SEULE de ces valeurs était gardée : remettre

     --font-disp sur Roboto — c'est-à-dire annuler exactement la plainte de

     Benjamin, « les polices sont les mêmes » — laissait la suite à 497/0

     sans un seul soupir. Le contrôle de contraste ne l'aurait pas vu : il ne

     contrôle pas la FORME, il ne contrôle que le plancher 4,5:1.



     Ces portes referment l'angle mort. Elles lisent le fichier réel, comme

     le contrôle de contraste ; elles ne vivent pas dans runTests(), donc

     elles ne coûtent aucun octet à l'outil déployé. Elles gardent deux choses

     distinctes : les VALEURS de l'identité, et le FAIT qu'il y ait trois

     formes — une ré-application du Design System B doit les faire échouer. */

  (function identiteTokens(){

    const fs = require('fs');

    const html = fs.readFileSync('bilan_economique.html', 'utf8');

    let corps = null;

    for (const m of html.matchAll(/:root\s*\{/g)) {

      const debut = m.index + m[0].length;

      let prof = 1, i = debut;

      while (i < html.length && prof > 0) {

        const c = html[i];

        if (c === '{') prof++;

        else if (c === '}') prof--;

        i++;

      }

      const bloc = html.slice(debut, i);

      if (/--ink\s*:/.test(bloc)) { corps = bloc; break; }

    }

    if (!corps) { console.log('  IDENTITE : bloc :root de reference non trouve — test non joue'); process.exitCode = 2; return; }

    const tok = {};

    for (const m of corps.matchAll(/(--[a-z0-9-]+)\s*:\s*([^;]+);/g)) tok[m[1]] = m[2].trim();



    let joues = 0, echecs = 0;

    const porte = (nom, obtenu, attendu) => {

      joues++;

      const okc = obtenu === attendu;

      if (!okc) echecs++;

      console.log((okc ? '  ok  ' : '  ECHEC ') + 'identité : ' + nom + ' — attendu « ' + attendu

        + ' », lu « ' + obtenu + ' »');

    };



    /* 1. la palette de l'identité SPK by CeramTec (v3.15, restaurée en 4.80) */

    porte("le bleu d'action", tok['--blue'], '#1B5EA6');

    porte('le rouge CeramTec', tok['--red'], '#E2001A');

    porte('le fond de page est gris, pas blanc', tok['--bg'], '#e8eaed');

    porte('le plein bleu des aplats', tok['--fill'], '#1B5EA6');



    /* 2. les rayons : c'est la signature d'un système « quasi-plat » */

    porte('le rayon des cartes', tok['--radius'], '3px');

    porte('le rayon des grandes surfaces', tok['--radius-lg'], '4px');



    /* 3. LA HIÉRARCHIE DE FORME — la porte qui manquait le 02/10.

       Titres et texte ne doivent PAS être la même famille : c'est exactement

       ce que le Design System B avait fait, et ce que Benjamin a vu. */

    const disp = (tok['--font-disp'] || '').split(',')[0].trim().replace(/^'|'$/g, '');

    const body = (tok['--font-body'] || '').split(',')[0].trim().replace(/^'|'$/g, '');

    porte('les titres ont leur propre famille', disp, 'Open Sans Condensed');  /* v4.109 — brand guide SPK */

    joues++;

    if (disp === body) {

      echecs++;

      console.log('  ECHEC identité : titres et texte partagent la famille « ' + disp

        + " » — c'est exactement l'aplatissement du Design System B");

    } else {

      console.log('  ok  identité : titres « ' + disp + ' » ≠ texte « ' + body + ' » — trois formes');

    }



    /* 4. Open Sans Condensed est RÉELLEMENT embarquée, pas seulement nommée dans un token.

       Un token qui promet une police absente du fichier donne un repli

       silencieux : la page aurait l'air de marcher et serait redevenue plate. */

    joues++;

    if (html.indexOf("@font-face{font-family:'Open Sans Condensed'") < 0) {

      echecs++;

      console.log("  ECHEC identite : Open Sans Condensed est nommee dans le token mais AUCUN @font-face ne l'embarque");

    } else {

      console.log('  ok  identité : Open Sans Condensed est embarquée en base64 (aucun appel réseau — brand guide SPK)');

    }



    /* 5. Les valeurs du Design System B ne doivent plus être là. Une réapplication

       du DS B — par une session qui ne lit pas l'historique — échoue ici. */

    for (const p of [['le bleu du DS B', '#006AB3'], ['le rouge du DS B', '#E30045']]) {

      joues++;

      if (corps.toUpperCase().includes(p[1].toUpperCase())) {

        echecs++;

        console.log('  ECHEC identité : ' + p[0] + ' (' + p[1] + ') est encore dans le bloc :root');

      } else {

        console.log('  ok  identité : ' + p[0] + ' (' + p[1] + ') a bien disparu du bloc :root');

      }

    }



    console.log('  IDENTITE : ' + joues + ' portes verifiees sur le CSS reel du fichier, '

      + echecs + ' en echec');

    r.echecs += echecs;

  })();



  /* ── v4.79 — LE CSS D'IMPRESSION A4 VIT DANS LE DOCUMENT PRINCIPAL ─────────

     Né en 4.53.0 à l'intérieur du template du rapport autonome, le bloc

     body.print-livraison n'a JAMAIS stylé l'outil : l'impression d'une

     livraison rendait l'écran, pas l'A4 (daté au Tour 52, commit a0e4d6e).

     Ce contrôle lit le fichier réel : les règles print-livraison ET

     print-mission doivent exister AVANT le premier <script> — c'est-à-dire

     dans le <head> du document que le navigateur applique vraiment. Une

     question de structure de document, posée au document. */

  (function cssImpression(){

    const fs = require('fs');

    const html = fs.readFileSync('bilan_economique.html', 'utf8');

    const tete = html.slice(0, html.indexOf('<script'));

    const attendus = [

      ['body.print-livraison >', "l'impression A4 d'une livraison"],

      ['body.print-mission >', "l'impression A4 de la mission"],

      ['#missionA4', 'le conteneur de la mission']

    ];

    let vus = 0;

    for (const [a, pourquoi] of attendus) {

      const la = tete.includes(a);

      if (!la) r.echecs++;

      vus++;

      console.log((la ? '  ok  ' : '  ECHEC ') + 'css impression : ' + pourquoi + ' — "' + a + '" ' + (la ? 'present' : 'ABSENT') + ' dans le head du document principal');

    }

    if (vus) console.log('  CSS IMPRESSION : ' + vus + ' regles verifiees dans le head reel du fichier');

  })();

  /* ── v4.89.1 — LE SECRET K NE DORT JAMAIS DANS LE FICHIER LIVRÉ ──────────
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
  /* ── v4.84 — LE SIMULATEUR EST STYLE ET PLEIN ECRAN, DANS LE CSS RÉEL ──

     L'accroc : le bloc CSS de la 4.83 n'avait JAMAIS été inséré — un garde

     conditionnel trop malin avait sauté l'insertion en silence, et le panneau

     a tourné deux versions non stylé (4.83.0 et 4.83.1, les deux domaines).

     La porte lit le fichier réel : les classes du simulateur EXISTENT. */

  (function simulCss(){

    const fs = require('fs');

    const html = fs.readFileSync('bilan_economique.html', 'utf8');

    const manquantes = ['.simul-note {', '.simul-table {', '.simul-resultat {', '.panel.simul-maxi', '.panel.simul-maxi .simul-table', 'function basculerMaxi']

      .filter(sel => html.indexOf(sel) === -1);

    if(manquantes.length) r.echecs += manquantes.length;

    console.log((manquantes.length ? '  ECHEC ' : '  ok  ') + 'simulateur : CSS présent dans le fichier réel (' + (6 - manquantes.length) + '/6 règles)' + (manquantes.length ? ' — MANQUANT : ' + manquantes.join(', ') : ''));

  })();

  /* ── v4.96 — LE SYSTÈME DE PANNEAUX NE RETOMBE PAS ──────────────────────
     Le défaut du lot 1 : .panel.panel-large ne posait qu'un max-width:1120px
     sur une base .panel figée à width:520px — un max-width n'élargit pas, tous
     les grands panneaux tournaient à 520 px. La porte lit le fichier réel :
     (1) panel-large porte un VRAI width min(1120px…), pas un max-width seul ;
     (2) la base .panel ne redescend pas sous 540 px ; (3) le sticky du titre
     et du footer d'actions existe. Sinon échec de la suite. */
  (function panneauxSysteme(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const echecs = [];
    if(!/\.panel\.panel-large\{\s*width:\s*min\(1120px/.test(html))
      echecs.push('panel-large sans vrai width 1120 (max-width seul = panneaux figés)');
    const base = html.match(/\.panel\{[^}]*width:\s*min\((\d+)px/);
    if(!base || parseInt(base[1], 10) < 540)
      echecs.push('base .panel sous 540 px ou introuvable (trouvé : ' + (base ? base[1] : '?') + ')');
    if(html.indexOf('.panel-large > h3{') === -1 || html.indexOf('position:sticky') === -1)
      echecs.push('sticky titre/footer absent');
    if(echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'panneaux 4.96 : largeurs et sticky présents dans le fichier réel' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.82 — LES DATES DE SAISIE SONT BORNÉES ───────────────────────────

     Benjamin : « la date des essais ne peut pas se taper directement il faut

     faire défiler… depuis l'an 1 ». Un input date sans min voit son sélecteur

     d'année démarrer à l'an 1. Le contrôle lit le fichier réel : CHAQUE champ

     date porte ses bornes. Une question de saisie atelier, posée au document. */

  (function datesBornees(){

    const fs = require('fs');

    const html = fs.readFileSync('bilan_economique.html', 'utf8');

    const inputs = html.match(/<input[^>]*type="date"[^>]*>/g) || [];

    const nues = inputs.filter(t => !t.includes('min="') || !t.includes('max="'));

    if(nues.length) r.echecs += nues.length;

    console.log((nues.length ? '  ECHEC ' : '  ok  ') + 'dates de saisie : ' + inputs.length + ' champs, ' + (inputs.length - nues.length) + ' bornés (min/max) — le sélecteur démarre à une année utile');

  })();

  /* ── v4.98 — LA TUILE D'ACCUEIL N'EMBROUILLE PLUS SON TEXTE ───────────────
     Le défaut, vu a l'ecran le 20/10 : dans les tuiles de ligne, le libelle
     « PHOTO MACHINE A FOURNIR » (majuscules, 7,5 px) demandait 4 lignes dans
     un cadre de 56 x 42 px — il en SORTAIT et passait sur « aucune reference
     declaree » juste a cote. Deux causes, deux corrections :
     (1) le libelle est court (« photo a fournir ») et tient dans le cadre ;
     (2) le cadre ne deborde plus (overflow:hidden) — un texte qui deborde ne
         peut plus recouvrir le voisin, meme si le libelle change encore.
     La porte lit le fichier REEL et verifie les DEUX. */
  (function tuileAccueilNEmbrouille(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const echecs = [];
    const bloc = html.match(/\.al-photo\{[^}]*\}/);
    if(!bloc) echecs.push('.al-photo introuvable dans le fichier reel');
    else {
      if(!/overflow:hidden/.test(bloc[0])) echecs.push('.al-photo sans overflow:hidden (le libelle peut deborder sur le voisin)');
      const fs2 = parseFloat((bloc[0].match(/font-size:([\d.]+)px/) || [])[1]);
      if(!(fs2 >= 8)) echecs.push('.al-photo en dessous de 8 px (illisible a l ecran) : ' + fs2);
    }
    if(html.indexOf('photo machine à fournir') !== -1 && /<div class="al-photo"[^>]*>[^<]*machine/i.test(html))
      echecs.push('libelle photo long encore present dans la balise (« photo machine à fournir ») — il deborde dans 56 px');
    if(html.indexOf('photo à fournir') === -1)
      echecs.push('libelle photo court (« photo à fournir ») absent');
    if(echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'tuile 4.98 : le libelle photo tient dans son cadre et ne recouvre plus le texte voisin' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.98 — L'AIDE NE FLOUTE PLUS A COTE D'UNE ACTION (§3.5) ────────────
     Le cahier UX (§3.5) : « le texte explicatif a cote de « + Creer un
     projet » passe en info-bulle ou dans le panneau, pas affiche en
     permanence en corps de texte a cote d'un bouton d'action. » Le texte
     existe toujours (rien ne se perd) mais il est MASQUE par defaut et
     ouvert par un bouton (i). La porte lit le fichier REEL. */
  (function aideProjetConsultee(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const echecs = [];
    if(html.indexOf('pj-aide-btn') === -1) echecs.push('bouton d aide (i) absent — l aide ne peut plus etre consultee');
    if(!/<span class="pj-aide" id="pjAide" hidden>/.test(html))
      echecs.push('le texte d aide n est plus masque par defaut (hidden manquant)');
    if(html.indexOf('id="pjAideBtn"') === -1) echecs.push('le bouton d aide n est pas relie au texte');
    if(echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'aide 4.98 : le texte d aide se consulte, il ne flotte plus a cote du bouton (§3.5)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.99 — LE CLOUD EST DÉBRANCHÉ SUR L'ADRESSE DE DEV ─────────────────
     Le fait : depuis le 20/10/2026, dev et prod servent le MÊME projet Supabase
     (`xlpfwvipdmgslwpbbfxs`). Benjamin : « le cloud est branché sur la branche
     dev alors on le débranche ». Le débranchement porte sur le CODE LIVRÉ, pas
     sur une configuration de poste : c'est la seule façon que la règle soit
     vraie pour tout le monde, y compris pour un lien de dev envoyé à Matis.

     La porte lit le fichier RÉEL et vérifie les SIX points :
     (1) le test d'hôte existe et cite l'adresse de dev ;
     (2) l'écriture d'état est coupée ;
     (3) l'envoi de photo est coupé ;
     (4) l'archivage est coupé ;
     (5) le retrait du bucket est coupé ;
     (6) la connexion est coupée ET le cycle de synchro sort — sans (6), la
         boucle périodique (90 s) continuerait de LIRE le cloud de la prod et
         pourrait y fusionner l'état de Matis par surprise.
     Elle vérifie aussi que la PASTILLE et le PANNEAU Options l'annoncent :
     un débranchement muet laisserait croire que la synchro fonctionne. */
  (function cloudDe_brancheSurDev(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const echecs = [];
    const blocs = {
      test_hote: html.indexOf('CLOUD_ECRITURE_AUTORISEE') !== -1
        && html.indexOf('suivi-optimisation-projet') !== -1
        && html.indexOf('location.hostname') !== -1,
      depot_etat: /async function cloudEcrireEtat\(\)\{[\s\S]{0,400}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      envoi_photo: /async function cloudPhotoEnvoyer\([^)]*\)\{[\s\S]{0,300}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      archivage: /async function cloudArchiverLeCloudActuel\([^)]*\)\{[\s\S]{0,300}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      retrait_bucket: /async function cloudPhotoSupprimer\([^)]*\)\{[\s\S]{0,300}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      connexion: /async function cloudConnexion\([^)]*\)\{[\s\S]{0,300}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      cycle_sort: /async function cloudSync\([^)]*\)\{[\s\S]{0,400}?CLOUD_ECRITURE_BLOQUEE/.test(html),
      pastille_visible: /cloudRenduPastille\(\)\{[\s\S]{0,600}?CLOUD_ECRITURE_BLOQUEE/.test(html) && /☁ débranché/.test(html),
      panneau_visible: /cloudRenduOptions\(\)\{[\s\S]{0,800}?CLOUD_ECRITURE_BLOQUEE/.test(html) && /Cloud débranché/.test(html),
      /* la coupure doit etre CONDITIONNELLE : la prod et le poste local ne
         doivent PAS etre bloques. On verifie que le nom de la prod n'apparait
         jamais dans une liste d'interdits, et que la condition est bien un
         test d'hote (pas une constante « toujours bloque »). */
      prod_pas_bloquee: (html.indexOf('INTERDITS') === -1 || html.indexOf('INTERDITS') > html.indexOf('suivi-optimisation-septfons'))
        && /CLOUD_ECRITURE_AUTORISEE\s*=\s*!/.test(html),
      poste_local_pas_bloque: html.indexOf('suivi-optimisation-septfons') === -1
        || html.indexOf('CLOUD_ECRITURE_AUTORISEE') !== -1
    };
    Object.keys(blocs).forEach(k => { if(!blocs[k]) echecs.push('coupure absente : ' + k); });
    if(echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'cloud 4.99 : le cloud est debranche sur l adresse de dev (11/11 points verifies dans le fichier reel)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.100 — LA COQUE EST DANS LE REPO GIT ──────────────────────────────
     Le 20/10/2026, deux workflow deployaient sur le meme domaine dev : le
     repo git et le build de refonte de l'agent auto-designer (hors git). Le
     repo git a ecrase la coque (Benjamin : « pourquoi on est revenu sur
     l'ancien design !!!!! sans la barre laterale etc »). Option A (Benjamin)
     : la coque est portee dans le repo git.

     Ces portes garentissent que la coque ne peut plus disparaitre du build :
     - le monolithe VERSIONNE ne doit PAS porter la coque (sinon chaque tour
       de Z Code se retrouve avec un diff de 1,5 Mo) ;
     - le build doit l'assembler dans dist/ ;
     - la coque doit etre complete (CSS + shell + les 8 polices) ;
     - le rail doit rester VISIBLE : le bug dorigine etait un z-index, pas
       une regle manquante — un test « la regle existe » ne prouve rien. */
  /* ── v4.100.1 — LE BOUTON RETOUR NE DISPARAIT PLUS SOUS UN DIALOGUE ──
     Benjamin, 20/10 : « dans le plan de conversion quand on lis un classeur
     le bouton retour disparait bro ». La lecture d'un classeur appelle
     dialogueAlerte (bilan_economique.html, ligne ~16307), qui ouvre
     dialogPanel — un `.panel` SANS `panel-large`. La regle calculait
     smallOpen sur TOUT `.panel` non-panel-large visible : le dialogue
     annulait donc l'etat d'espace de travail, le bouton Retour disparaissait
     au milieu du Plan, et le rail redevenait « non repliable » alors que le
     Plan etait toujours ouvert.

     La correction : un surcouche (dialogue, recherche, annotation photo) se
     pose PAR-DESSUS un espace de travail, il ne le remplace pas. Seuls les
     vrais petits panneaux (Options, Import, Nouveau projet...) le remplacent. */
  (function boutonRetourSousDialogue(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const shell = (function(){
      try { return fs.readFileSync(path.join(REPO, 'spk-shell.js'), 'utf8'); } catch (e) { return ''; }
    })();

    if (!shell) echecs.push('spk-shell.js introuvable : la porte ne peut rien verifier');

    if (shell) {
      /* (1) les surcouches doivent etre declarees */
      const iSur = shell.indexOf('const SURCOUCHES = [');
      if (iSur < 0) echecs.push('les surcouches ne sont pas declarees : le dialogue annule encore l espace de travail');
      else {
        const bloc = shell.slice(iSur, iSur + 200);
        ['dialogPanel', 'searchPanel'].forEach(function(id){
          if (bloc.indexOf(id) === -1) echecs.push('la surcouche ' + id + ' n est pas exclue du calcul d espace de travail');
        });
      }

      /* (2) le calcul ne doit PLUS compter tout .panel non-panel-large */
      const iSync = shell.indexOf('function syncWorkspace(');
      if (iSync < 0) echecs.push('syncWorkspace introuvable');
      else {
        const bloc = shell.slice(iSync, iSync + 600);
        if (bloc.indexOf('petitPanneauAuPremierPlan()') === -1)
          echecs.push('syncWorkspace ne passe plus par le filtre des surcouches');
        if (bloc.indexOf('.panel:not(.panel-large):not(#backlogWrap):not([hidden])') !== -1)
          echecs.push('syncWorkspace recompte tout .panel non-panel-large : le dialogue refait disparaitre le bouton');
      }

      /* (3) la liste des petits panneaux doit etre balayee en entier :
             un surcouche peut preceder un vrai panneau dans le document */
      const iFiltre = shell.indexOf('function petitPanneauAuPremierPlan(');
      if (iFiltre < 0) echecs.push('le filtre des surcouches est absent');
      else {
        const bloc = shell.slice(iFiltre, iFiltre + 700);
        if (bloc.indexOf('querySelectorAll') === -1)
          echecs.push('le filtre ne balaie qu un seul panneau : un surcouche peut masquer un vrai panneau');
      }
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'bouton retour 4.100.1 : un dialogue par-dessus un espace de travail ne fait plus disparaitre le bouton Retour' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.100.2 — LE SHELL EST SERVI EN RÉSEAU D'ABORD ──
     Benjamin, 20/10 : « Problème toujours présent bro » — alors que le
     correctif du bouton Retour était déployé, publié et vérifié sur l'URL
     publique. Cause : `spk-shell.js` était servi CACHE D'ABORD. Le cache ne
     se purge que si le service worker change, or c'est le shell qui changeait,
     pas le SW : l'ancien shell restait en cache, invisible et intouchable.
     Le profil de test (Chrome neuf à chaque fois) n'avait jamais de cache —
     il vérifiait le code, pas ce que l'utilisateur voit. */
  (function majAToudPourShell(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const lire = (rel) => { try { return fs.readFileSync(path.join(REPO, rel), 'utf8'); } catch (e) { return ''; } };
    const sw = lire('service-worker.js');
    const html = lire('bilan_economique.html');

    if (!sw) echecs.push('service-worker.js introuvable : la porte ne peut rien verifier');

    if (sw) {
      /* (1) le shell doit etre dans le lot "reseau d'abord" */
      const iEst = sw.indexOf('const estJs = url.pathname.endsWith');
      if (iEst < 0) echecs.push('le shell n est pas reconnu comme ressource du lot reseau-dabord');
      else {
        const bloc = sw.slice(iEst, iEst + 900);
        const iIf = bloc.indexOf('if (estHtml || estCss');
        if (iIf < 0) echecs.push('impossible de lire la condition reseau-dabord');
        else if (bloc.slice(iIf, iIf + 80).indexOf('estJs') === -1) echecs.push('le shell n est PAS dans le lot reseau-dabord : un correctif du shell peut rester invisible');
      }

      /* (2) addAll est tout ou rien : un 404 sur une police fait echouer
             l'installation du SW, et l'ancien continue de servir l'ancien
             shell. Il faut une mise en cache entree par entree. */
      if (sw.indexOf('c.addAll(SHELL)') !== -1) echecs.push('addAll est tout ou rien : une entree manquante empeche le nouveau service worker de prendre la main');
      if (sw.indexOf('SHELL.map') === -1) echecs.push('la mise en cache n est pas entree par entree');

      /* (3) le SW doit signaler sa prise de main aux pages ouvertes */
      if (sw.indexOf('SPK_MAJ') === -1) echecs.push('le service worker ne previent pas les pages ouvertes de sa prise de main');
    }

    if (html) {
      /* (4) l'enregistrement doit forcer la mise a jour et surveiller la
             version. ATTENTION : on cherche dans le CODE ACTIF, pas dans le
             fichier entier — les chaines apparaissent aussi dans les
             COMMENTAIRES (qui expliquent justement la correction), et un
             test « la chaine est presente » passerait donc meme si le code
             avait disparu. C'est ce piege que la porte a deja laisse passer
             deux fois dans ce tour. On retire les commentaires avant. */
      const NL2 = String.fromCharCode(10);
      const htmlCode = html
        .split(NL2).map(function(l){ return l.replace(/\/\/.*$/, ''); }).join(NL2)
        .split(NL2).filter(function(l){ return l.indexOf('*') < 0; }).join(NL2);

      /* On cherche l'OCCURRENCE EXACTE dans une LIGNE DE CODE, pas la
         presence de la chaine. Sans cela, le commentaire de la correction
         (qui cite `updateViaCache` dans une liste a puces) faisait passer
         la porte meme quand le code avait disparu — c'est exactement ce
         qui est arrive : la porte disait verte avec le code mort.
         On exige donc que la ligne contienne ET le mot-cle ET un signe
         d'appel (`(`, `{`, `=`, `;`) — un commentaire ne les a pas. */
      function ligneActive(src, motCle, doitEtreAppel){
        const ls = src.split(NL2);
        for (let i = 0; i < ls.length; i++) {
          if (ls[i].indexOf(motCle) === -1) continue;
          if (ls[i].trim().indexOf('*') === 0) continue;      // ligne de commentaire
          if (ls[i].trim().indexOf('//') === 0) continue;      // ligne de commentaire
          if (doitEtreAppel && ls[i].indexOf(doitEtreAppel) === -1) continue;
          return true;
        }
        return false;
      }
      if (!ligneActive(htmlCode, 'updateViaCache', 'register')) echecs.push('le service worker n est pas enregistre avec updateViaCache : sa nouvelle version peut rester invisible');
      if (!ligneActive(htmlCode, 'navigator.serviceWorker.register', '(')) echecs.push('le service worker n est plus enregistre');
      /* la verification doit etre DECLAREE *et APPELEE : la declaration
         seule ne prouve rien (une fonction jamais appele ne verifie
         jamais rien). On compte les occurrences hors declaration. */
      if (!ligneActive(htmlCode, '_spkVerifierVersion', '(')) echecs.push('la page ne verifie pas si une version plus recente est servie : elle peut rester en retard indefiniment');
      else {
        const lsHtml = htmlCode.split(NL2);
        let appels = 0;
        for (let i = 0; i < lsHtml.length; i++) {
          const t = lsHtml[i].trim();
          if (t.indexOf('*') === 0 || t.indexOf('//') === 0) continue;
          if (lsHtml[i].indexOf('_spkVerifierVersion') === -1) continue;
          if (t.indexOf('function _spkVerifierVersion') !== -1) continue; // la declaration
          appels++;
        }
        if (appels === 0) echecs.push('la verification de version n est jamais APPELEE : la page peut rester en retard indefiniment');
      }
      if (!ligneActive(htmlCode, 'SPK_MAJ', 'type')) echecs.push('la page n ecoute pas le signal de mise a jour du service worker');
      /* la purge des caches doit vraiment avoir lieu, ET partout ou elle est
         prevue. Une seule occurrence saine ne suffit pas : si la purge
         disparait du gestionnaire SPK_MAJ mais reste dans la verification de
         version, le chemin le plus utilise (rechargement par le signal du
         service worker) ne purge plus rien. On verifie donc que CHAQUE
         occurrence utile est presente. */
      function toutesLesOccurrencesUtiles(src, motCle, contexte){
        const ls = src.split(NL2);
        let trouvees = 0, utiles = 0;
        for (let i = 0; i < ls.length; i++) {
          const t = ls[i].trim();
          if (t.indexOf('*') === 0 || t.indexOf('//') === 0) continue;
          if (ls[i].indexOf(motCle) === -1) continue;
          if (contexte && ls[i].indexOf(contexte) === -1) continue;
          trouvees++;
          if (ls[i].indexOf(motCle + '(') !== -1 || ls[i].indexOf('.' + motCle + '(') !== -1) utiles++;
        }
        return { trouvees: trouvees, utiles: utiles };
      }
      const purge = toutesLesOccurrencesUtiles(htmlCode, 'delete', 'caches');
      if (purge.utiles === 0) echecs.push('la page ne purge pas les caches : elle peut rester sur un shell perime');
      const reload = toutesLesOccurrencesUtiles(htmlCode, 'location.reload', 'location');
      if (reload.utiles === 0) echecs.push('la page ne se recharge pas : une version plus recente reste invisible');
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'maj a chaud 4.100.2 : le shell est servi en reseau d abord, un correctif ne peut plus rester invisible en cache (8 points)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.100.3 — L'IMPORT PRÉVIENT QUAND LE FICHIER REÇU RETIRE DES ESSAIS ──
     Benjamin, 20/10 : « je ne retrouve pas tous les essais réalisés (exemple
     PCI 5 OP40) quand j'importe les JSON ». Reproduction : importer plusieurs
     fichiers à la suite avec « Remplacer tout » (le bouton par défaut) ne
     garde que le DERNIER — rev425 après rev431 = 5 essais au lieu de 7, PCI 5
     OP40 disparu. Et le numéro de révision ne protège pas : deux postes
     incrémentent chacun le leur (rev432 recevait MOINS d'essais que rev431).
     Le garde : l'écran de choix compare le NOMBRE D'ESSAIS reçu et local, et
     affiche l'écart AVANT le clic. */
  /* ── v4.100.4 — LES ONGLETS DU RAIL SONT EXCLUSIFS ──
     Benjamin, 21/10 : « les onglets tableau et synthese ne fonctionnent pas ».
     Constat : les écrans du rail s'empilaient au lieu de se remplacer — et la
     Synthèse, bloc en flux de l'app d'avant la coque (aucun z-index),
     s'ouvrait DERRIÈRE l'Accueil ou le Tableau de bord restés ouverts (z 80).
     Mesuré en navigateur : Accueil ouvert -> clic Synthèse -> l'écran reste
     sur l'accueil. Le shell referme maintenant les surfaces voisines en
     phase de capture, marque l'onglet de la Synthèse, et Retour la ferme. */
  (function railExclusif4100_4(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const shell = (function(){ try { return fs.readFileSync(path.join(REPO, 'spk-shell.js'), 'utf8'); } catch (e) { return ''; } })();
    if (!shell) { echecs.push('spk-shell.js introuvable'); }
    else {
      /* (1) la table d'exclusivité couvre les cinq boutons du rail */
      ['accueilBtn: ["accueilPanel"', 'dashboardBtn: ["dashboardPanel"', 'syntheseBtn: ["syntheseWrap"', 'carteBtn: ["cartePanel"', 'matisBtn: ["matisPanel"'].forEach(function(morceau){
        if (shell.indexOf(morceau) === -1) echecs.push('SURFACES_DU_BOUTON ne couvre pas ' + morceau.split(':')[0]);
      });

      /* (2) le refermement se fait en PHASE DE CAPTURE (avant l'app) */
      if (shell.indexOf('}, true); /* capture') === -1) echecs.push('le refermement des surfaces n est pas en phase de capture');

      /* (3) la Synthèse compte comme un espace ouvert (Retour + onglet) */
      if (shell.indexOf('#syntheseWrap:not([hidden])') === -1) echecs.push('workspaceOpen ignore la Synthese');

      /* (4) Retour referme aussi la Synthèse */
      if (shell.indexOf('synthese.hidden = true') === -1) echecs.push('fermerPanneaux ne ferme pas la Synthese');

      /* (5) l onglet actif est pose d apres la surface visible */
      if (shell.indexOf('visible === "syntheseWrap"') === -1) echecs.push('pas de remontee en haut pour la Synthese');
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'rail exclusif 4.100.4 : les onglets du rail se remplacent au lieu de s empiler' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  (function importPrevientSiMoinsDEssais(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const NL = String.fromCharCode(10);
      const code = html.split(NL).map(function(l){ return l.replace(/\/\/.*$/, ''); }).join(NL);

      /* (1) le compteur d'essais existe et marche sur les 4 niveaux */
      if (code.indexOf('nbEssaisDe') === -1) echecs.push('pas de compteur d essais dans l ecran d import');
      const iFn = code.indexOf('const nbEssaisDe =');
      if (iFn < 0) echecs.push('le compteur nbEssaisDe est introuvable');
      else {
        const ligne = code.slice(iFn, code.indexOf(String.fromCharCode(10), iFn));
        ['references','ops','scenarios','essais'].forEach(function(k){
          if (ligne.indexOf(k) === -1) echecs.push('le compteur nbEssaisDe ne compte pas le niveau ' + k);
        });
      }

      /* (2) la comparaison est faite entre le RECU et le LOCAL */
      if (code.indexOf('essaisRecus < essaisLocaux') === -1) echecs.push('la comparaison recu/local est absente');

      /* (3) l'avertissement s affiche dans le panneau, AVANT les boutons */
      const iPanneau = code.indexOf('importPanelBody');
      const iBoutons = code.indexOf('importRemplace');
      if (iPanneau < 0 || iBoutons < 0) echecs.push('le panneau d import est introuvable');
      else {
        const panneau = code.slice(iPanneau, iBoutons);
        if (panneau.indexOf('moinsDEssais') === -1) echecs.push('l avertissement moins-d-essais n est pas affiche dans le panneau (ou apres les boutons)');
        if (panneau.indexOf('de MOINS que vos données actuelles') === -1) echecs.push('le texte de l avertissement est absent');
      }
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'import 4.100.3 : l ecran d import previent quand le fichier recu porte moins d essais que les donnees locales' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  (function planTableauDeBordLive(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const NL = String.fromCharCode(10);
      const code = html.split(NL).map(function(l){ return l.replace(/\/\/.*$/, ''); }).join(NL);

      /* (1) la case PRIX CONFIRME est CABLEE : le listener existe et il ecrit
             dans le champ confirme. Une case presente sans listener est une case
             MORTE (le bug du 21/10) — le test d unitite ne la voit pas, il
             teste le champ, pas le cable. */
      const iConf = code.indexOf('data-planconf');
      if (iConf < 0) echecs.push('la case prix valide n est plus dans le tableau du Plan');
      else {
        const iEcoute = code.indexOf('data-planconf]');
        if (iEcoute < 0) echecs.push('la case prix valide n a aucun listener (elle est MORTE)');
        else {
          const bloc = code.slice(iEcoute, iEcoute + 700);
          if (bloc.indexOf('e.confirme') === -1) echecs.push('le listener de la case prix valide n ecrit pas dans le champ confirme');
          if (bloc.indexOf('saveData') === -1) echecs.push('le listener de la case prix valide ne sauvegarde pas');
        }
      }

      /* (2) les 5 briques du tableau de bord live sont dans le SOURCE */
      ['planRecapGains', 'planChronologieEssais', 'planParetoSVG', 'planBandeauHTML', 'planTableauDeBordHTML']
        .forEach(function(fn){
          if (code.indexOf('function ' + fn) === -1) echecs.push('la fonction ' + fn + ' est absente du source');
        });

      /* (3) les gains actes et possibles ne sont JAMAIS additionnes : pas de
             total unique qui melee les deux (constitution 3.4). Le controle est
             CADE sur le bloc qui CONSTRUIT le recapitulatif (l addition y
             porterait un nom) — chercher dans tout le fichier laisserait passer
             un calcul melee ailleurs. */
      const iRecap = code.indexOf('function planRecapGains');
      if (iRecap < 0) echecs.push('planRecapGains introuvable');
      else {
        /* le bloc va de la fonction a la fonction SUIVANTE (sinon on s arrete a
           la premiere accolade fermante, qui coupe au milieu de la fonction) */
        const iSuivant = code.indexOf('function planChronologieEssais', iRecap);
        const bloc = code.slice(iRecap, iSuivant > 0 ? iSuivant : iRecap + 4000);
        /* tout total qui additionne les deux series est interdit, quel que soit
           le nom qu il porte. SANS REGEX : dans cette chaine Python non-raw, un
           "\\n" Backslash-n devient un VRAI saut de ligne et la regex compile
           mais ne matche plus rien — la porte passerait au vert sans rien voir
           (piege documente : harnais + echappement JS). On travaille donc avec
           des chaines : on decoupe le bloc en LIGNES et on cherche un + entre
           un nom de serie et un nom de projete. */
        const nomsSerie = ['gainActe', 'totalActe', 'actes'];
        const nomsProj = ['gainProjete', 'totalPossible', 'totalProjeteBrut', 'enCoursPositifs'];
        const lignesBloc = bloc.split(String.fromCharCode(10));
        lignesBloc.forEach(function(ligne){
          const posPlus = ligne.indexOf('+');
          if (posPlus < 0) return;
          const avant = ligne.slice(0, posPlus);
          const apres = ligne.slice(posPlus + 1);
          const aSerie = nomsSerie.filter(function(n){ return avant.indexOf(n) !== -1; });
          const aProj = nomsProj.filter(function(n){ return apres.indexOf(n) !== -1; });
          if (aSerie.length && aProj.length)
            echecs.push('les gains actes et possibles sont additionnes dans le recapitulatif : ' + ligne.trim().slice(0, 90));
        });
      }

      /* (4) pas de dependance reseau dans les graphiques (constitution 5.5) */
      const iSvg = code.indexOf('function planParetoSVG');
      if (iSvg >= 0) {
        const bloc = code.slice(iSvg, iSvg + 2600);
        if (bloc.indexOf('http://') !== -1 || bloc.indexOf('https://') !== -1)
          echecs.push('le graphique du Plan depend du reseau');
      }

      /* (5) le tableau de bord est montee DANS le rendu du Plan */
      const iRend = code.indexOf('function renderPlan');
      if (iRend < 0) echecs.push('renderPlan introuvable');
      else {
        const bloc = code.slice(iRend, iRend + 1200);
        if (bloc.indexOf('planTableauDeBordHTML') === -1)
          echecs.push('le tableau de bord live n est pas monte dans le rendu du Plan');
      }
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'plan 4.102.0 : le tableau de bord live est monte, la case prix valide est cablee, les gains ne sont pas melanges' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.111.0 — LE VERDICT PAR OUTIL ──────────────────────────────────
     Demande Hermes/Benjamin du 26/10 (incident T543 D1) : le verdict se
     refait en additionnant les tuiles. Portes : le module existe, la tuile
     n'apparie plus JAMAIS par position, la fiche porte la réconciliation et
     la ligne « dont sorties du scénario », le dégradé du gain a sa garde
     d'impression, et aucun K ni P_req dans les libellés (§2.6). */
  (function verdictParOutilGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const code = html;
      ['function appariementOutils(scRef, scCand){',
       'function verdictParOutil(sc, cfg, ligne, ref, baseCmp){',
       'function verdictSortiesHTML(vpo){']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('module absent : ' + m); });

      /* le piège n°1 banni : plus aucun appariement positionnel dans la tuile */
      const iTuile = code.indexOf('function apercuLogementHTML');
      const iCompo = code.indexOf('function compositionApercuHTML');
      if (iTuile < 0 || iCompo < 0) echecs.push('la composition (tuiles) introuvable');
      else {
        const blocTuile = code.slice(iTuile, iCompo);
        if (blocTuile.indexOf('flatsSc.indexOf') !== -1 || blocTuile.indexOf('indexOf(l)') !== -1)
          echecs.push('l appariement positionnel est de retour dans la tuile');
        if (blocTuile.indexOf('vp.parLogement') === -1)
          echecs.push('la tuile ne lit plus l appariement par numéro');
      }

      /* la fiche porte le verdict par outil et sa réconciliation */
      if (iCompo >= 0) {
        const iFinCompo = code.indexOf(String.fromCharCode(10) + '/* ----', iCompo);
        const blocCompo = code.slice(iCompo, iFinCompo > 0 ? iFinCompo : iCompo + 7000);
        if (blocCompo.indexOf('verdictParOutil(') === -1)
          echecs.push('la composition ne calcule plus le verdict par outil');
        if (blocCompo.indexOf('ap-reconcil') === -1)
          echecs.push('la ligne de réconciliation a disparu de la fiche');
      }

      /* la ligne dédiée dans le verdict (l'incident rendu impossible à rater) */
      const iVerdict = code.indexOf('function verdictHTML');
      if (iVerdict < 0) echecs.push('verdictHTML introuvable');
      else {
        const iFinV = code.indexOf(String.fromCharCode(10) + '/* ----', iVerdict);
        const blocV = code.slice(iVerdict, iFinV > 0 ? iFinV : iVerdict + 3500);
        if (blocV.indexOf('verdictSortiesHTML(') === -1)
          echecs.push('le verdict ne porte plus la ligne dont sorties du scénario');
      }

      /* le dégradé du gain ne s'imprime jamais : deux règles data-gain
         (l'une dans @media print), comme les couleurs de ligne */
      const occ = code.split('.ap-tuile[data-gain').length - 1;
      if (occ < 2) echecs.push('le dégradé du gain n a pas sa garde d impression (moins de 2 règles data-gain)');

      /* les libellés du sémantique sont là, sans aucun K ni P_req (§2.6) */
      ['dont sorties du scénario', 'Levier technique', 'Levier productivité', 'Réconciliation']
        .forEach(function(m){ if (code.indexOf(m) === -1) echecs.push('libellé absent : ' + m); });

      /* v4.112 — le secours intra-outil TRACÉ (complément §1). LE PIÈGE VU
         AU CONTRE-REGARD : le libellé vit AUSSI dans l'annonce NOUVEAUTES —
         chercher dans tout le fichier laissait la porte verte avec un dépliant
         muet. On vérifie donc le libellé DANS le bloc du dépliant (la fonction
         de la tuile), et le compteur DANS le bloc de la composition. */
      const iTuileV = code.indexOf('function apercuLogementHTML');
      const iCompoV = code.indexOf('function compositionApercuHTML');
      if (iTuileV < 0 || iCompoV < 0) echecs.push('v4.112 : les fonctions de rendu introuvables');
      else {
        const blocTuileV = code.slice(iTuileV, iCompoV);
        if (blocTuileV.indexOf('par secours — noms divergents') === -1)
          echecs.push('v4.112 : le tracé « par secours — noms divergents » a quitté le dépliant de la tuile');
        if (blocTuileV.indexOf('parSecours') === -1)
          echecs.push('v4.112 : la tuile ne porte plus le drapeau parSecours');
        /* v4.113 — le secours par DONNÉES identiques (bug OP40 vu par
           Benjamin en prod) : tracé dans le dépliant, filtre des porteurs
           de coût présent dans l'appariement. */
        if (blocTuileV.indexOf('par données identiques') === -1)
          echecs.push('v4.113 : le tracé « par données identiques » a quitté le dépliant de la tuile');
        const iApp2 = code.indexOf('function appariementOutils');
        const iFin2 = code.indexOf(String.fromCharCode(10) + 'function ', iApp2);
        const blocApp2 = code.slice(iApp2, iFin2 > 0 ? iFin2 : iApp2 + 6000);
        if (blocApp2.indexOf('posCost(f.l) !== null') === -1)
          echecs.push('v4.113 : l appariement ne filtre plus les porteurs de coût');
        if (blocApp2.indexOf('parDonnees') === -1)
          echecs.push('v4.113 : le secours par données identiques a disparu de l appariement');
        const iFinC = code.indexOf(String.fromCharCode(10) + '/* ----', iCompoV);
        const blocCompoV = code.slice(iCompoV, iFinC > 0 ? iFinC : iCompoV + 9000);
        if (blocCompoV.indexOf('apparié(s) par secours') === -1)
          echecs.push('v4.112 : la réconciliation ne compte plus les secours');
        if (code.indexOf('sortisGroupe') === -1 || code.indexOf('nbParSecours') === -1)
          echecs.push('v4.112 : la dérivation secours/sortis a disparu du module');
      }
      /* la mention vit DANS le badge du groupe (rendu ap-gs-tete), pas
         ailleurs : ancre sur le helper grpSortis, la fenetre couvre le rendu */
      const iGrpS = code.indexOf('const grpSortis = g =>');
      if (iGrpS < 0) echecs.push('v4.112 : grpSortis introuvable');
      else {
        const blocGs = code.slice(iGrpS, iGrpS + 3600);
        if (blocGs.indexOf('ap-gs-tete') === -1)
          echecs.push('v4.112 : la mention des sortis ne vit plus dans le rendu du groupe');
        if (blocGs.indexOf('poste') === -1)
          echecs.push('v4.112 : le badge du groupe ne porte plus la mention des postes sortis');
      }
      const iMod = code.indexOf('function verdictParOutil');
      const iFinMod = code.indexOf(String.fromCharCode(10) + 'function ', iMod);
      const blocMod = code.slice(iMod, iFinMod > 0 ? iFinMod : iMod + 6000);
      ['K = Vc', 'P_req', 'coefficient K'].forEach(function(m){
        if (blocMod.indexOf(m) !== -1) echecs.push('le module du verdict expose un interdit : ' + m);
      });
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'verdict par outil 4.111 : appariement par numéro, réconciliation somme des tuiles = verdict, sorties nommées' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.114.0 — LA PORTE « LE BANDEAU DIT VRAI » ────────────────────────
     Décision Benjamin 26/10 : le bandeau Coût pièce lit la SÉRIE comme
     production du jour, la ★ reste la base (jamais de re-base automatique),
     trois temporalités affichées séparément, les abandonnés ne nourrissent
     plus le meilleur, et le clic puce OP ouvre le détail des scénarios.
     Le vocabulaire tué ne doit jamais revenir dans le bloc rendu. */
  (function bandeauCPPGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const iA = html.indexOf('function pieceCPPComplet');
      const iB = html.indexOf('function feuilleRouteHTML');
      if (iA < 0 || iB < 0 || iB <= iA) echecs.push('bloc bandeau introuvable');
      else {
        const bloc = html.slice(iA, iB);
        [['meilleur en cours', "le vocabulaire tué est de retour : meilleur en cours"],
         ['passé en série', "le vocabulaire tué est de retour : passé en série"],
         ['€ prod', "le vocabulaire tué est de retour : EUR prod"],
         ['"prod seule"', "le vocabulaire tué est de retour : prod seule"]]
        .forEach(function(m){ if (bloc.indexOf(m[0]) !== -1) echecs.push(m[1]); });
        [['function pcbOuvrirDetail', 'le détail au clic puce OP absent'],
         ['pcbDernier = p', 'état de rendu du bandeau non branché'],
         ['sc.statut !== "serie"', 'la lecture série = production du jour absente'],
         ['sc.statut === "abandonne"', 'le filtre des abandonnés absent'],
         ['ne bouge jamais toute seule', 'engagement anti-ré-base automatique absent'],
         ['réalisé', 'la phrase réalisé absente du bandeau'],
         ['reste possible', 'la phrase reste possible absente du bandeau'],
         ['Ce que coûte la pièce', 'le titre du bandeau non revocabularisé'],
         ['data-pcb-i', 'les puces OP ne sont pas cliquables']]
        .forEach(function(m){ if (bloc.indexOf(m[0]) === -1) echecs.push(m[1]); });
      }
      if (html.indexOf('id="pcbOpPanel"') === -1) echecs.push('le panneau détail OP absent du DOM');
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'bandeau CPP 4.114 : lecture série, trois phrases, abandonnés filtrés, vocabulaire tenu, détail au clic' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.115.0 — LA PORTE « LA CAMPAGNE » ─────────────────────────────────
     La timeline commerciale : seuls les séries actent (§3.4), un jalon sans
     date se dit et va dans « à compléter » (§3.5), la courbe cumule dans
     l'ordre des dates, et la file attrape jalons non datés et coûts incomplets. */
  (function campagneGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      [['function campagneCollecter', 'le collecteur de campagne absent'],
       ['function campagneCourbeSVG', 'la courbe cumulée absente'],
       ['function campagneHTML', 'le rendu de la campagne absent'],
       ['id="campagnePanel"', 'le panneau campagne absent du DOM'],
       ['id="campagneBtn"', 'le bouton de menu absent'],
       ['campagneOuvrirBtn', 'le résumé en tête de Synthèse absent'],
       ['jalon non daté', 'les jalons sans date ne se disent pas'],
       ['OP non chiffrable', 'les OP non chiffrables ne remontent pas'],
       ['manque ', 'les coûts incomplets ne se listent pas'],
       ['sc.statut === "serie" && !sc.baseline', 'la courbe doit ne compter que les séries non-étoile'],
       ['sc.statut === "abandonne"', 'garde-fou abandonné du bandeau disparu ?']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'la campagne 4.115 : jalons, courbe actée seule, à compléter, deux points d entrée' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.115.1 — LA PORTE « LA CASCADE A SES BARRES » ──────────────────────
     Bug v4.31-v4.115.0 : le CSS de la cascade et de la table comparative ne
     vivait que dans le template du rapport de validation. La page doit avoir
     SA copie : chaque règle colorée doit exister DEUX fois (template + page).
     Une seule occurrence = la page est redevenue aveugle. */
  (function cascadeGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      [['.syn2-wf-bar { border-radius', 2, 'le style de barre de cascade n a plus sa copie page'],
       ['.syn2-wf-bar.save { background:var(--green); }', 2, 'la barre verte n a plus sa copie page'],
       ['table.synthese.syn2 { min-width:760px; }', 2, 'la table comparative n a plus sa copie page'],
       ['td.syn2-best', 2, 'la meilleure valeur n a plus sa copie page']]
      .forEach(function(m){ if ((html.split(m[0]).length - 1) < m[1]) echecs.push(m[2]); });
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'cascade 4.115.1 : la page a sa copie du CSS cascade + comparative' + (echecs.length ? ' - ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.116.0 — LA PORTE « LA FUSION NE MENT PAS » ────────────────────────
     La fusion Classeur Matis : le porteur d'histoire garde ses ids, la
     prévision est pure, les conflits bloquent l'application, un numéro
     ambigu n'est jamais fusionné, contrôle des prélèvements AVANT mutation. */
  (function fusionGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      [['function matisPairesDoublons', 'la détection de paires absente'],
       ['function prevoirFusionMatis', 'la prévision pure absente'],
       ['function appliquerFusionMatis', "l'application absente"],
       ['id="fusionMatisPanel"', 'le panneau de fusion absent du DOM'],
       ['fusion-matis-btn', "le bouton d'entrée sur la fiche absent"],
       ['à trancher à la main', 'les numéros ambigus ne sont pas refusés'],
       ['fusionScoreHistoire', "le score d'histoire (plan, pièces, prélèvements) absent"],
       ['contrôle AVANT mutation', 'le contrôle des prélèvements ne se fait pas avant mutation']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'fusion Matis 4.116 : détection, porteur d histoire, prévision pure, conflits bloquants, zéro dangling' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.117.0 — LA PORTE « LE DERNIER LOT » ────────────────────────────────
     Boussole Première Lecture, Ctrl+K, ce qui attend (âges), décliner un
     gagnant (ids neufs), filet undo 30 jours avec instantané AVANT mutation. */
  (function dernierLotGate(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      [['function boussoleHTML', 'la boussole Première Lecture absente'],
       ['boussole-lien', 'les liens de la boussole absents'],
       ['function campagneCeQuiAttendHTML', 'les âges (ce qui attend) absents'],
       ['function declinerScenario', 'la déclinaison de gagnant absente'],
       ['declinerCloneOutils', 'la copie à ids neufs absente'],
       ['const UNDO_CLE', 'le journal undo absent'],
       ['function undoRestaurer', 'la restauration absente'],
       ['undoPousser(', 'la prise d instantané avant mutation absente'],
       ['id="undoPanel"', 'le panneau du filet absent du DOM'],
       ['id="declinerPanel"', 'le panneau de déclinaison absent du DOM'],
       ['id="undoMenuBtn"', 'le bouton de menu du filet absent'],
       ['.decliner-btn', 'le bouton décliner absent de la fiche'],
      ['const BASE_MATIS', 'la base Matis embarquée absente'],
      ['BASE_MATIS.consoArticle', 'les consommations réelles Matis absentes'],
      ['totalPareto: 1004671', 'le total Pareto absent'],
      ['Réel Matis</th>', 'la colonne Réel Matis absente du simulateur']]
      .forEach(function(m){ if (html.indexOf(m[0]) === -1) echecs.push(m[1]); });
      if (html.indexOf('toLowerCase() === "k"') === -1) echecs.push('le raccourci Ctrl+K absent');
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'dernier lot 4.117 : boussole, Ctrl+K, âges, déclinaison, filet undo' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.120 — LE LOT UX (PDF mort, flash, import au rail) ────────────
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
      if (html.indexOf('html:not([data-pret]) body{visibility:hidden') === -1)
        echecs.push('le body n est plus caché pendant le chargement');
      if (html.indexOf(',5000)') === -1)
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

  /* ── v4.112.1 — LA PORTE TDZ DU CHARGEMENT ────────────────────────────
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
      /* v4.120 — Hermes a recollé « }loadAll(); » sans saut de ligne :
         l'ancre n'est plus un saut de ligne mais la PREMIÈRE occurrence de
         l'appel (les mentions en commentaire n'ont pas de point-virgule). */
      const iAppel = html.indexOf('loadAll();');
      if (iDeb < 0 || iAppel < 0) echecs.push('loadAll ou son appel initial introuvable');
      else if (iFin < 0) echecs.push('fin de loadAll introuvable');
      else {
        const corps = html.slice(iDeb, iFin);
        const noms = {};
        corps.split(NL).forEach(function(l){
          const m = l.match(/^\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=[^=]/);
          if (m) noms[m[1]] = true;
        });
        Object.keys(noms).sort().forEach(function(n){
          /* déclaration top-level la plus précoce (colonne 0). PAS DE REGEX
             DYNAMIQUE : la leçon des tours 82/4.100 (échappement Python→JS)
             reprisée ici — une new RegExp en string a déjà laissé cette porte
             aveugle au premier contre-regard. On cherche du TEXTE : une
             déclaration top-level commence par 'let NAME ' en tête de ligne. */
          const iLet = html.indexOf(NL + 'let ' + n + ' ');
          const iConst = html.indexOf(NL + 'const ' + n + ' ');
          const iDec = (iLet < 0) ? iConst : ((iConst < 0) ? iLet : Math.min(iLet, iConst));
          if (iDec < 0) return; /* locale sans déclaration top-level : hors périmètre */
          if (iDec > iAppel)
            echecs.push('la globale ' + n + ' est assignée dans loadAll mais déclarée APRÈS son appel — piège TDZ : repli silencieux sur les données d\u2019exemple');
        });
      }
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'porte TDZ 4.112.1 : toute globale de loadAll se déclare avant son appel (le repli silencieux sur les données d\u2019exemple ne reviendra pas)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.112 — LES 8 POLICES MORTES SONT RETIRÉES ─────────────────────
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
      restants = fs.readdirSync(dirFonts).filter(function(f){ return /\.woff2$/i.test(f); });
    } catch (e) { /* dossier absent : vide, acceptable */ }
    if (restants.length) echecs.push('fonts/ contient encore : ' + restants.join(', '));
    /* le HTML source ne référence aucun fichier fonts/ (déjà vrai avant, le
       garder vrai : une police ne revient qu accompagnée de sa décision) */
    if (html && html.indexOf('fonts/') !== -1) echecs.push('le HTML source référence un fichier fonts/');
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'polices mortes 4.112 : les 8 fichiers retirés (fonts/, SW + CACHE bumpé, build) et le HTML sans référence fonts/' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.110.0 — LE BADGE DE CODIFICATION SUR LES FICHES SCÉNARIO ──
     Brique B (UI) : l'état dérivé de la 4.106 devient visible là où le
     scénario est jugé. La fonction pure est testée dans runTests ; cette
     porte lit le fichier réel : la fonction existe, la fiche l'appelle,
     les trois libellés du sémantique Benjamin (codifié / attente X j /
     non demandée) sont là, et le hors-exigence (base excel / sans
     article) n'a pas fondu. */
  (function badgeCodifFiches(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const html = (function(){ try { return fs.readFileSync(path.join(REPO, 'bilan_economique.html'), 'utf8'); } catch (e) { return ''; } })();
    if (!html) { echecs.push('bilan_economique.html introuvable'); }
    else {
      const code = html;

      /* (1) la fonction pure existe */
      if (code.indexOf('function badgeCodifScenario(sc){') === -1)
        echecs.push('badgeCodifScenario absente du source');

      /* (2) la fiche scénario du Plan appelle le badge : un badge dérivé
             qui n'est pas rendu est une donnée morte (leçon case PRIX). */
      const iFiche = code.indexOf('function planScenariosHTML');
      if (iFiche < 0) echecs.push('planScenariosHTML introuvable');
      else {
        const iSuiv = code.indexOf(String.fromCharCode(10) + 'function ', iFiche);
        const bloc = code.slice(iFiche, iSuiv > 0 ? iSuiv : iFiche + 8000);
        if (bloc.indexOf('badgeCodifScenario(sc)') === -1)
          echecs.push('la fiche scénario n affiche plus l état de codification');
        if (bloc.indexOf('l.codifB') === -1)
          echecs.push('le badge dérivé nest plus rendu dans la cellule État');
      }

      /* (3) les trois libellés du sémantique + le hors-exigence */
      const iBadge = code.indexOf('function badgeCodifScenario');
      if (iBadge >= 0) {
        const iFin = code.indexOf(String.fromCharCode(10) + 'function ', iBadge);
        const bloc = code.slice(iBadge, iFin > 0 ? iFin : iBadge + 3000);
        ['codification attendue', 'codification non demand', '>codifié<', 'pc-stat serie', 'pc-stat attente']
          .forEach(function(m){ if (bloc.indexOf(m) === -1) echecs.push('le badge a perdu « ' + m + ' »'); });
        if (bloc.indexOf('sansExigence') === -1 || bloc.indexOf('sansArticle') === -1)
          echecs.push('le badge ne respecte plus le hors-exigence (base excel / sans article)');
      }
    }
    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'badge codif 4.110 : la fiche scénario porte l état de codification dérivé (codifié / attente X j / non demandée)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  /* ── v4.103.0 — LE PRIX SPK PAR DÉFAUT N'EXISTE PLUS ─────────────────────
     Décision Benjamin du 20/10 (chaque plaquette a son prix) d'abord portée
     par le build SEUL — ce qui faisait diverger les deux mondes : le harnais
     testait des comportements que le fichier servi ne connaissait plus.
     Le retrait vit dans le source ; cette porte l'empêche de revenir, entre
     deux builds (le build-coque a son propre garde, il ne court qu'à lui). */
  (function prixSpkAbsentDuSource(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const n = html.split('prixSpk').length - 1;
    if (n) r.echecs += 1;
    console.log((n ? '  ECHEC ' : '  ok  ') + 'prix SPK défaut : le source ne référence plus prixSpk (décision 20/10 dans la source, plus dans le build)' + (n ? ' — ' + n + ' occurrence(s)' : ''));
  })();

  (function coqueDansLeRepoGit(){
    const fs = require('fs');
    const path = require('path');
    const echecs = [];
    const REPO = __REPO__;
    const lire = (rel) => { try { return fs.readFileSync(path.join(REPO, rel), 'utf8'); } catch (e) { return ''; } };

    const monolithe = lire('bilan_economique.html');
    const css = lire('spk-app.css');
    const shell = lire('spk-shell.js');
    const build = lire(path.join('outils', 'build-coque.mjs'));
    const sw = lire('service-worker.js');

    // (1) le monolithe versionne ne porte PAS la coque
    const monolithePropre = monolithe.indexOf('spk-app.css') === -1
      && monolithe.indexOf('spk-shell.js') === -1;
    if (!monolithePropre) echecs.push('le monolithe versionne porte la coque : chaque tour aurait un diff de 1,5 Mo');

    // (2) le build assemble dans dist/ ET branche la coque.
    //     ATTENTION : on ne cherche pas la chaine n'importe ou dans le
    //     fichier — elle apparait aussi dans les COMMENTAIRES et dans
    //     l'en-tete, ou un build devenu inutile passerait quand meme.
    //     On retire donc les commentaires avant de chercher.
    /* ATTENTION : pas de '\n' litteral ici — le harnais est du JS dans une
       chaine Python NON-raw, un '\n' y devient un vrai saut de ligne et le
       fichier JS ne compile plus. On construit la separation par code. */
    const NL = String.fromCharCode(10);
    const buildCode = build
      .split(NL).map(function(l){ return l.replace(/\/\/.*$/, ''); }).join(NL)
      .split(NL).filter(function(l){ return l.indexOf('*') < 0; }).join(NL);
    if (buildCode.indexOf("path.join(RACINE, 'dist')") === -1) echecs.push('le build n assemble pas dans dist/');
    if (buildCode.indexOf('spk-app.css') === -1) echecs.push('le build ne branche pas le CSS de la coque');
    /* l'injection reelle : le lien doit etre INSERE dans le HTML, pas
       seulement nomme. On cherche le fragment qui construit la balise. */
    /* l'injection reelle : on cherche la ligne qui CONSTRUIT la balise
       (celle qui assemble le HTML), pas la ligne qui la teste. Une
       construction disparue = plus de coque dans le deploiement. */
    if (buildCode.indexOf("html = html.slice(0, insert) +") === -1) echecs.push('le build n insere plus le lien vers le CSS de la coque');
    /* Le shell : on ne cherche pas une chaine dans le source (elle
       apparait aussi dans le test d idempotence) — on verifie que le build
       CONSTRUIT la balise, sur une ligne d affectation. */
    const lignesBuild = buildCode.split(NL);
    const construitShell = lignesBuild.some(function(l){
      const t = l.trim();
      return t.indexOf('+ ') === 0 && t.indexOf('defer></script>') !== -1;
    });
    if (!construitShell) echecs.push('le build n insere plus le shell de la coque');
    if (buildCode.indexOf('spk-shell.js') === -1) echecs.push('le build ne branche pas le shell de la coque');
    if (buildCode.indexOf('fonts') === -1) echecs.push('le build ne copie pas les polices');

    // (3) la coque est complete
    if (css.indexOf('.spk-rail') === -1) echecs.push('spk-app.css ne definit pas le rail');
    if (shell.indexOf('spk-rail') === -1) echecs.push('spk-shell.js ne construit pas le rail');
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
    /* v4.112 : les 8 polices de la coque d'origine sont RETIREES du SW
       (decision Benjamin, complement du 26/10 soir) - ce controle vit
       desormais dans la porte dediee 'polices mortes 4.112', qui exige
       leur ABSENCE et le bump de CACHE. Garder l'ancienne exigence ici
       aurait contredit la decision. */

    // (4) le rail reste VISIBLE : z-index superieur aux surfaces plein ecran.
    //     C est LE point du bug d origine : le rail (60) passait sous les
    //     panneaux (80) et disparaitait de l ecran.
    /* On lit le z-index du rail DANS la regle qui le remonte (celle qui
       suit le repere « LE RAIL DOIT RESTER VISIBLE »), pas la premiere
       occurrence du fichier : le CSS de la coque contient plusieurs
       `.spk-rail { z-index: 60 }` (le rail de base, le rail mobile), et
       lire la premiere ferait passer une regression du z-index de la
       correction. On prend donc la valeur la plus HAUTE appliquee au rail
       dans un media query bureau — c'est elle qui compte a l'ecran. */
    const blocCorrection = css.split('LE RAIL DOIT RESTER VISIBLE')[1] || '';
    /* PAS DE REGEX : le harnais est du JS dans une chaine Python non-raw,
       chaque backslash y est reinterprete. Une regex de z-index ecrit
       ici arrive en JS avec un double backslash et ne matche jamais -
       la porte passerait donc toujours au vert. On lit la valeur par
       decoupage de chaine, qui ne depend d'aucun echappement. */
    function lireZIndexApres(texte, apres, fenetre){
      const i = texte.indexOf(apres);
      if (i < 0) return null;
      const tranche = texte.slice(i, i + (fenetre || 200));
      const j = tranche.indexOf('z-index:');
      if (j < 0) return null;
      /* apres 'z-index:' il y a des espaces puis le nombre : on saute les
         espaces, sinon le nettoyage des non-chiffres ne laisse rien. */
      const reste = tranche.slice(j + 9).replace(/^[^0-9]+/, '');
      /* on ne garde QUE les chiffres : le reste peut contenir un ';' ou
         un retour ligne, et Number() renverrait alors NaN — qui ne vaut ni
         null ni comparable, et la porte passerait au vert sans rien voir. */
      const chiffres = (reste.match(/[0-9]+/) || [''])[0];
      return chiffres ? Number(chiffres) : null;
    }
    /* le rail : on part de la REGLE `.spk-rail {` du bloc de correction, pas
       du premier `z-index:` du bloc (celui-la est dans le commentaire). */
    const zRailMax = lireZIndexApres(blocCorrection, '.spk-rail {', 120);
    /* le panneau : la regle de la coque est longue (position, inset, top,
       left, transform, width, max-width, height...) avant le z-index — on
       ouvre la fenetre largement. */
    const zPanneau = lireZIndexApres(css, '.panel.panel-large,', 700);
    /* un NaN ne vaut ni null ni comparable : il passerait au vert. On le
       traite donc comme une lecture impossible. */
    if (zRailMax === null || zPanneau === null || isNaN(zRailMax) || isNaN(zPanneau)) echecs.push('impossible de lire les z-index du rail et des panneaux');
    else if (zRailMax <= zPanneau) echecs.push('le rail (z ' + zRailMax + ') passe sous les panneaux (z ' + zPanneau + ') : il disparait de l ecran');
    /* le decalage : on le cherche DANS le bloc de correction. La chaine
       'left: 248px !important' existe aussi dans la regle `.wrap` (le
       contenu decale de la meme facon) : chercher dans tout le fichier
       laisserait passer un bloc de correction vide. */
    if (blocCorrection.indexOf('left: 248px !important') === -1) echecs.push('les ecrans plein ecran ne s arretent pas au bord du rail');
    if (blocCorrection.indexOf('width: auto !important') === -1) echecs.push('les ecrans plein ecran gardent width 100% : ils deborderaient');

    // (5) la poignee de repli reste ACTIVE en plein ecran (Benjamin, 20/10) :
    //     le rail est le repere de navigation, un espace de travail ne doit
    //     pas le figer. La regle inverse (poignee masquee) a ete retiree.
    /* meme contrainte : decoupage de chaine, pas de regex (les backslash
       sont reinterpretes par la chaine Python du harnais). */
    const iPoignee = css.indexOf('body.spk-workspace-open #spkRailToggle');
    const poignee = iPoignee < 0 ? '' : css.slice(iPoignee, iPoignee + 260);
    if (!poignee) echecs.push('plus de regle pour la poignee en espace de travail');
    else {
      if (poignee.indexOf('pointer-events: none') !== -1) echecs.push('la poignee est encore neutralisee en espace de travail');
      if (poignee.indexOf('opacity: 0') !== -1) echecs.push('la poignee est encore masquee en espace de travail');
    }

    if (echecs.length) r.echecs += echecs.length;
    console.log((echecs.length ? '  ECHEC ' : '  ok  ') + 'coque 4.100 : la coque est dans le repo git, le rail reste visible et repliable (12 points verifies dans les fichiers reels)' + (echecs.length ? ' — ' + echecs.join(' ; ') : ''));
  })();

  if (typeof (__DIAG__) !== 'undefined') (__DIAG__)(A);

  /* v4.80 — LE VERDICT FINAL TIENT COMPTE DES GARDE-FOUS.

     runTests() imprime son résumé AVANT que les contrôles de hors-suite ne

     tournent (contraste, identité, CSS d'impression) : sur une régression de

     la palette, la console affichait donc « TOUT EST VERT — 497 tests | 0

     echecs » alors que le process sortait en 1. Le code de sortie, lui, disait

     vrai ; l'écran, non. C'est exactement le défaut qu'on reproche à une

     contre-vérification qui passe sans avoir rien vérifié : un verdict

     affiché ne vaut que s'il couvre tout ce qui a été contrôlé. */

  if (r.echecs > 0) {

    console.log('');

    console.log('VERDICT : ECHEC — ' + r.echecs + ' controle(s) hors runTests() ont échoue.');

    console.log('          (le résumé « 497 tests | 0 echecs » ci-dessus ne les compte pas)');

  } else {

    console.log('');

    console.log('VERDICT : tout est vert — y compris les garde-fous de hors-suite.');

  }

  /* v4.60 (tour 16) : le code de l'outil installe des setInterval (synchro cloud,

     debounce) qui gardent la boucle d'événements de node vivante -- sans exit

     explicite, le process ne rend JAMAIS la main et le verdict, déjà imprimé,

     reste invisible derrière un pipe. Exit code = nombre d'échecs (0 = tout vert),

     utilisable tel quel par n'importe quelle revue croisée. */

  process.exit(r.echecs ? 1 : 0);

} catch(e){ console.log('ERREUR EXEC:', e.message); console.log((e.stack||'').split('\\n').slice(0,6).join('\\n')); process.exit(2); }

'''



HARNESS = HARNESS.replace('__CODE__', json.dumps(code)) \
               .replace('__API__', API) \
               .replace('__REPO__', json.dumps(REPO.replace('\\', '/'))) \
               .replace('__DIAG__', os.environ.get('HARNESS_DIAG', 'undefined'))

io.open(OUT, 'w', encoding='utf-8').write(HARNESS)

print('harnais écrit :', OUT, '(%d Ko)' % (len(HARNESS) // 1024))

