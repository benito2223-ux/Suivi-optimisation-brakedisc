import io, subprocess, os

P = 'bilan_economique.html'
s = io.open(P, encoding='utf-8').read()

def grab(src, nom):
    a = src.find('function ' + nom)
    return src[a:src.find('\n}', a) + 2] if a >= 0 else ''

JS = r"""
let lignes = [];
""" + '\n'.join(grab(s, n) for n in
    ['matisPorteOutilPosition', 'matisClePorteOutil', 'normalizeLogement',
     'positionDeOutil', 'renseignerCorrecteur', 'dedoublonnerLogements',
     'reparerOutilsD1D2']) + r"""
function signalerContextePerime(){}

const T = (t, r) => { console.log('   ' + (r?'OK  ':'KO  <<< ') + t); return r; };
let ko = 0; const T2 = (t, r) => { if(!r) ko++; T(t, r); };
const P4 = (id, nom) => ({ id, nom, prix: 0, aretes: 8 });

console.log('=== 1. BENJAMIN : T2D1, l outil est T2, le correcteur D1 ===');
const outils1 = [ { id:'a', numero:'T2D1', logements:[ P4('g1','Logement 1') ] } ];
const r1 = reparerOutilsD1D2(outils1);
T2('le numero reste ce que l atelier a ecrit', r1[0].numero === 'T2D1');
T2('le CORRECTEUR est desormais rempli : D1', r1[0].correcteur === 'D1');
T2('et il y a un logement qui le porte', r1[0].logements.some(g => g.nom === 'D1'));

console.log();
console.log('=== 2. T5D1, pareil ===');
const r2 = reparerOutilsD1D2([ { id:'b', numero:'T5D1', logements:[ P4('g2','Logement 1') ] } ]);
T2('T5D1 : correcteur D1 rempli', r2[0].correcteur === 'D1');
T2('T5D1 : le numero est intact', r2[0].numero === 'T5D1');

console.log();
console.log('=== 3. BENJAMIN : T1 avec SEPT logements du meme nom ===');
const sept = [ { id:'t1', numero:'T1', correcteur:'D1', logements:[
  P4('p1','Plaquette'), P4('p2','Plaquette'), P4('p3','Plaquette'), P4('p4','Plaquette'),
  P4('p5','Plaquette'), P4('p6','Plaquette'), P4('p7','Plaquette') ] } ];
const r3 = reparerOutilsD1D2(sept);
/* les 7 « Plaquette » ne portent AUCUNE position : on n'en invente pas. Elles
   se réduisent donc à un seul emplacement non nommé, et le correcteur D1 vient
   s'ajouter à côté avec SON logement. Deux logements : un provisoire, un D1. */
T2('les 7 deviennent 2 : un provisoire + D1', r3[0].logements.length === 2);
T2('le provisoire garde son nom — on n invente pas de position',
   r3[0].logements.some(g => g.nom === 'Plaquette'));
T2('et le correcteur D1 a bien son logement', r3[0].logements.some(g => g.nom === 'D1'));
T2('le porte-outil est toujours T1', r3[0].numero === 'T1');
T2('le correcteur est toujours D1', r3[0].correcteur === 'D1');

console.log();
console.log('=== 4. et si les 7 portent des noms de positions ? ===');
const sept2 = [ { id:'t1', numero:'T1', correcteur:'D1, D2, D3', logements:[
  P4('q1','D1'), P4('q2','D2'), P4('q3','D3'),
  P4('q4','D1'), P4('q5','D2'), P4('q6','D3'), P4('q7','D1') ] } ];
const r4 = reparerOutilsD1D2(sept2);
T2('les doublons de position disparaissent', r4[0].logements.length === 3);
T2('il reste D1, D2, D3', r4[0].logements.map(g=>g.nom).sort().join(',') === 'D1,D2,D3');

console.log();
console.log('=== 5. la DONNEE la plus renseignee est conservee, pas la premiere ===');
const gA = { id:'z1', nom:'D1', prix:'', aretes:8, mabec:'' };
const gB = { id:'z2', nom:'D1', prix:11.87, aretes:6, mabec:'Z000 519 285' };
const r5 = reparerOutilsD1D2([ { id:'t', numero:'T1', correcteur:'D1', logements:[gA, gB] } ]);
T2('le MABEC le plus informe est garde', r5[0].logements[0].mabec === 'Z000 519 285');
T2('le prix aussi', r5[0].logements[0].prix === 11.87);
T2('et il n y a toujours qu un logement', r5[0].logements.length === 1);

console.log();
console.log('=== 6. la fonction reste PURE ===');
const src = [ { id:'t1', numero:'T1', correcteur:'D1', logements:[P4('p1','D1'),P4('p2','D1')] } ];
const copie = JSON.parse(JSON.stringify(src));
reparerOutilsD1D2(src);
T2('l entree n a pas ete modifiee', JSON.stringify(src) === JSON.stringify(copie));

console.log();
console.log('=== 7. on ne casse pas la regle qui compte ===');
const r7 = reparerOutilsD1D2([ { id:'a', numero:'T543 D1', logements:[P4('m1','Logement 1')] },
                               { id:'b', numero:'T543 D2', logements:[P4('m2','Logement 1')] } ]);
T2('T543 D1 + T543 D2 = UN outil', r7.length === 1);
T2('avec deux logements D1 et D2', r7[0].logements.map(g=>g.nom).sort().join(',') === 'D1,D2');
T2('et son correcteur porte les deux', r7[0].correcteur === 'D1, D2');

console.log();
console.log('=== 8. le PROVISOIRE est RECLAME, pas double (contre-regard) ===');
/* deux jeux DOIVENT produire le meme nombre de logements : si le provisoire etait
   ajoute au lieu d etre renomme, il y en aurait deux. */
const c8a = reparerOutilsD1D2([ { id:'a', numero:'T2D1', logements:[ P4('g','Logement 1') ] } ]);
T2('T2D1 + un provisoire = UN logement, pas deux', c8a[0].logements.length === 1);
T2('et c est bien D1 (le provisoire a ete renomme)', c8a[0].logements[0].nom === 'D1');

console.log();
console.log('=== 9. le dedoublonnage vaut aussi pour PLUSIEURS outils (contre-regard) ===');
/* le chemin de fin de reparerOutilsD1D2 n est atteint qu avec 2 outils et plus :
   les cas precedents ne le couvraient pas du tout, et une panne y passait. */
const neuf = [
  { id:'a', numero:'T1 D1', correcteur:'D1', logements:[ P4('x1','D1'), P4('x2','D1'), P4('x3','D1') ] },
  { id:'b', numero:'T1 D2', correcteur:'D2', logements:[ P4('y1','D2'), P4('y2','D2') ] },
];
const c9 = reparerOutilsD1D2(neuf);
T2('les deux outils sont regroupes en UN', c9.length === 1);
T2('il ne reste que D1 et D2', c9[0].logements.map(g=>g.nom).sort().join(',') === 'D1,D2');
T2('les 5 logements de depart sont tombes a 2', c9[0].logements.length === 2);

console.log();
console.log(ko === 0 ? 'TOUT EST VERT' : ko + ' ECHEC(S)');
process.exit(ko ? 1 : 0);
"""
io.open('_d77.js', 'w', encoding='utf-8').write(JS)
r = subprocess.run(['node', '_d77.js'], capture_output=True, text=True,
                   encoding='utf-8', errors='replace')
print(r.stdout or ('ERREUR\n' + r.stderr[:900]))
os.unlink('_d77.js')
