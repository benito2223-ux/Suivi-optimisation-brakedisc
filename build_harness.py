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
       "_matisFeuille, "
       "getActiveLigne, get lignes(){return lignes}, set lignes(v){lignes=v}, "
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
  if (typeof (__DIAG__) !== 'undefined') (__DIAG__)(A);
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
               .replace('__DIAG__', os.environ.get('HARNESS_DIAG', 'undefined'))
io.open(OUT, 'w', encoding='utf-8').write(HARNESS)
print('harnais écrit :', OUT, '(%d Ko)' % (len(HARNESS) // 1024))
