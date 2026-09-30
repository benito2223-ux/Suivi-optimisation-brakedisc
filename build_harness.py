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
  if (typeof __DIAG__ !== 'undefined') __DIAG__(A);
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
               .replace('__DIAG__', 'undefined')
io.open(OUT, 'w', encoding='utf-8').write(HARNESS)
print('harnais écrit :', OUT, '(%d Ko)' % (len(HARNESS) // 1024))
