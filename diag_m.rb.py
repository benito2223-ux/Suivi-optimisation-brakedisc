import io, re, subprocess, os

P = 'bilan_economique.html'
s = io.open(P, encoding='utf-8').read()

# on extrait les 3 fonctions reelles du fichier et on les fait tourner
i = s.find('function matisPorteOutilPosition')
j = s.find('/* v4.58', i)
bloc = s[i:j]

JS = r"""
%s

const D = n => ({ id: n, nom: "Logement 1" });
const L = a => a.map(o => o.id + '(' + o.numero + ')[' + (o.logements||[]).map(l=>l.nom).join(',') + ']').join('  ');
const T = (t,r) => console.log('   ' + (r?'OK  ':'KO  ') + t);

console.log('=== A. le vocabulaire : quelles saisies sont comprises ? ===');
[['T543 D1','T543','D1'],['T543D1','T543','D1'],['T 543 D1','T 543','D1'],
 ['T543','T543',null],['T543 D','T543','D']].forEach(([e,p,pos]) => {
  const r = matisPorteOutilPosition(e);
  T(JSON.stringify(e) + '  ->  porte=' + JSON.stringify(r.porte) + '  pos=' + JSON.stringify(r.position),
    r.porte===p && r.position===pos);
});

console.log();
console.log('=== B. LE SCENARIO DE BENJAMIN : T543, puis D1, puis D2 ===');
let outils = [{ id:'a', numero:'T543', logements:[D('g1')] }];
console.log('   depart          : ' + L(outils));

let p1 = proposerFusionLogement('T543 D1', outils, 'b');
T('la saisie "T543 D1" propose une fusion', !!p1);
if (p1) outils = fusionnerOutils(outils, 'b', p1);
console.log('   apres D1        : ' + L(outils));
const n1 = (outils[0].logements||[]).length;

let p2 = proposerFusionLogement('T543 D2', outils, 'c');
T('la saisie "T543 D2" propose une fusion', !!p2);
if (p2) outils = fusionnerOutils(outils, 'c', p2);
console.log('   apres D2        : ' + L(outils));

const n2 = (outils[0].logements||[]).length;
console.log();
T('il ne reste QU UN outil (pas deux)', outils.length === 1);
T('il reste 2 logements, pas 3', n2 === 2);
if (n2 !== 2) console.log('       ^^^^^ BUG : ' + (n2===3 ? 'un logement "Logement 1" fantome subsiste a cote de D1 et D2' : 'autre cas'));
T('les logements s appelle D1 et D2',
  (outils[0].logements||[]).map(l=>l.nom).sort().join(',') === 'D1,D2');
T('aucun logement ne garde un nom par defaut',
  !(outils[0].logements||[]).some(l=>/^\s*logement\s*\d*\s*$/i.test(l.nom||'')));

console.log();
console.log('=== C. les espaces : "T 543" et "T543" sont-ils le meme porte-outil ? ===');
const a = matisPorteOutilPosition('T 543').porte, b = matisPorteOutilPosition('T543').porte;
T('"T 543" et "T543" donnent le meme porte', a === b);
if (a !== b) console.log('       ^^^^^ BUG : "' + a + '" vs "' + b + '" -- deux outils distincts pour la meme piece');

console.log();
console.log('=== D. le CAS REEL : les outils sont deja saisis en double ===');
const existant = [
  { id:'x1', numero:'T543 D1', logements:[{id:'h1', nom:'Logement 1', mabec:'M1', prix:12}] },
  { id:'x2', numero:'T543 D2', logements:[{id:'h2', nom:'Logement 1', mabec:'M2', prix:14}] },
];
const presents = existant.map(o => o.numero).join(' / ');
const repair = typeof repairingOutilsD1D2 === 'function' ? repairingOutilsD1D2(existant) : null;
console.log('   donnees actuelles : ' + presents);
T('une fonction de REPARATION existe pour l existant', !!repair);
if (repair) {
  console.log('   apres reparation   : ' + L(repair));
  T('un seul outil', repair.length === 1);
  T('deux logements D1 et D2', (repair[0].logements||[]).length === 2);
  T('les MABEC sont conserves',
    (repair[0].logements||[]).map(l=>l.mabec).sort().join(',') === 'M1,M2');
  T('les prix sont conserves',
    (repair[0].logements||[]).map(l=>l.prix).sort((a,b)=>a-b).join(',') === '12,14');
}
process.exit(0);
""" % bloc

io.open('_diag.js', 'w', encoding='utf-8').write(JS)
r = subprocess.run(['node', '_diag.js'], capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print(r.stdout or r.stderr[:1500])
os.unlink('_diag.js')
