import io, re, subprocess, os

P = 'bilan_economique.html'
s = io.open(P, encoding='utf-8').read()

# les vraies fonctions, extraites du fichier
def grab(src, nom):
    a = src.find('function ' + nom)
    return src[a:src.find('\n}', a) + 2] if a >= 0 else ''

JS = r"""
let lignes, data, config, activeLigneId, activeReferenceId, activeOpId;
let signalerAppele = 0;
function signalerContextePerime(){ signalerAppele++; }
""" + grab(s, 'syncActiveOp') + r"""
function getActiveOp(){
  const l = lignes.find(x => x.id === activeLigneId);
  if(!l) return null;
  const r = l.references.find(x => x.id === activeReferenceId);
  if(!r) return null;
  return r.ops.find(x => x.id === activeOpId) || null;
}
const L = (nom, ref, ops) => ({ id:'l'+nom, nom, references:[{ id:'r'+ref, nom:ref,
  ops: ops.map(o => ({ id:'o'+ref+o, nom:o, scenarios:[{ id:'s'+ref+o, name:'sc '+o }] })) }] });

const T = (t, r) => { console.log('   ' + (r?'OK  ':'KO  <<< ') + t); return r; };
let ko = 0; const T2 = (t, r) => { if(!r) ko++; T(t, r); };

console.log('=== A. le cas NORMAL : rien ne doit bouger ===');
lignes = [L('EMAG 1','a',['10','40']), L('EMAG 3','b',['10','40'])];
activeLigneId='lEMAG 1'; activeReferenceId='ra'; activeOpId='oa40';
data = getActiveOp().scenarios; config = {};
syncActiveOp();
T2('le scenario de l OP active reste affiche', data[0].id === 'sa40');
T2('aucun signalement', signalerAppele === 0);

console.log();
console.log('=== B. LE CAS DE BENJAMIN : le contexte EMAG 3 montre un scenario de EMAG 1 ===');
lignes = [L('EMAG 1','a',['10','40']), L('EMAG 3','b',['10','40'])];
// le contexte annonce EMAG 3 ...
activeLigneId='lEMAG 3'; activeReferenceId='rb'; activeOpId='ob10';
// ... mais data contient le scenario d EMAG 1 OP40 : la fuite
data = [ { id:'sa40', name:'Process actuel KY3500' } ];
signalerAppele = 0;
syncActiveOp();
const op3 = getActiveOp();
T2('le scenario etranger NE REMPLACE PAS l operation', !op3.scenarios.some(s => s.id === 'sa40'));
T2('la vraie liste de l operation est revenue', data.some(s => s.id === 'sb10'));
T2('le scenario EMAG 1 est intact la ou il est',
   lignes[0].references[0].ops[1].scenarios.some(s => s.id === 'sa40'));
T2('rien n a ete perdu : la liste d EMAG 1 OP40 est intacte',
   lignes[0].references[0].ops[1].scenarios.length === 1);
T2('le derangement a ete signale', signalerAppele === 1);

console.log();
console.log('=== C. une RESTAURATION : un tampon legitime ne doit PAS etre refuse ===');
lignes = [L('EMAG 1','a',['10'])];
activeLigneId='lEMAG 1'; activeReferenceId='ra'; activeOpId='oa10';
const tampon = [ { id:'sTMP1', name:'restaure' }, { id:'sTMP2', name:'restaure 2' } ];
data = tampon; signalerAppele = 0;
syncActiveOp();
T2('un tampon sans scenario etranger est accepte', signalerAppele === 0);
T2('et il est bien ecrit dans l operation', getActiveOp().scenarios === tampon);

console.log();
console.log(ko === 0 ? 'TOUT EST VERT' : ko + ' ECHEC(S)');
process.exit(ko ? 1 : 0);
"""
io.open('_ctx.js', 'w', encoding='utf-8').write(JS)
r = subprocess.run(['node', '_ctx.js'], capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print(r.stdout or ('ERREUR\n' + r.stderr[:800]))
os.unlink('_ctx.js')
