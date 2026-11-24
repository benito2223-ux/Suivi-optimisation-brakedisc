import io, subprocess, os

P = 'bilan_economique.html'
s = io.open(P, encoding='utf-8').read()
i = s.find('v4.71.0 — LA RÉPARATION')
if i < 0:
    i = s.find('function reparerOutilsD1D2(')
i = s.rfind('/*', 0, i)
j = s.find('/* v4.58', s.find('function matisPorteOutilPosition('))
bloc = s[i:j]
assert 'function reparerOutilsD1D2(' in bloc, 'la fonction de reparation n est pas dans le bloc'
assert 'function matisPorteOutilPosition(' in bloc

JS = r"""
%s
const D = (id,n,m,p) => ({ id:id, nom:n||"Logement 1", mabec:m||"", prix:p||0 });
const L = a => a.map(o => o.numero + ' [' + (o.logements||[]).map(l=>l.nom+(l.mabec?'/'+l.mabec:'')).join(' , ') + ']').join('   |   ');
const T = (t,r) => console.log('   ' + (r?'OK  ':'KO  <<< ') + t);
let ko = 0; const T2 = (t,r) => { if(!r) ko++; T(t,r); };

console.log('=== 1. LE CAS DE BENJAMIN : EMAG1 OP40, T543 avec 2 correcteurs ===');
console.log('   L atelier cree T543, puis saisit T543 D1, puis T543 D2.');
let o = [{ id:'a', numero:'T543', logements:[D('g1')] }];
o.push({ id:'b', numero:'T543 D1', logements:[D('h1','Logement 1','MAB-1',12)] });
let p = proposerFusionLogement('T543 D1', o, 'b');
T2('la saisie T543 D1 propose la fusion', !!p);
if (p) o = fusionnerOutils(o, 'b', p);
console.log('   -> ' + L(o));
o.push({ id:'c', numero:'T543 D2', logements:[D('i1','Logement 1','MAB-2',14)] });
p = proposerFusionLogement('T543 D2', o, 'c');
T2('la saisie T543 D2 propose la fusion', !!p);
if (p) o = fusionnerOutils(o, 'c', p);
console.log('   -> ' + L(o));
console.log();
T2('UN SEUL outil T543', o.length === 1 && o[0].numero === 'T543');
T2('DEUX logements, pas trois', (o[0].logements||[]).length === 2);
T2('ils s appellent D1 et D2', (o[0].logements||[]).map(l=>l.nom).sort().join(',') === 'D1,D2');
T2('aucun logement fantome', !o[0].logements.some(l=>/^\s*logement\s*\d*\s*$/i.test(l.nom||'')));
T2('le MABEC-1 et son prix survivent', !!o[0].logements.find(l=>l.mabec==='MAB-1' && l.prix===12));
T2('le MABEC-2 et son prix survivent', !!o[0].logements.find(l=>l.mabec==='MAB-2' && l.prix===14));

console.log();
console.log('=== 2. LES ESPACES : "T 513 D1" et "T513 D1" sont le meme porte-outil ===');
T2('la cle ignore les espaces', matisClePorteOutil('T 513 D1') === matisClePorteOutil('T513 D1'));
T2('la cle ignore les tirets',   matisClePorteOutil('T-513')     === matisClePorteOutil('T513'));
T2('deux portes differents restent distincts', matisClePorteOutil('T513') !== matisClePorteOutil('T517'));

console.log();
console.log('=== 3. REPARER CE QUI EST DEJA SAISI EN DOUBLE ===');
const avant = [
  { id:'x1', numero:'T 543 D1', logements:[D('h1','Logement 1','MAB-1',12)] },
  { id:'x2', numero:'T543 D2',  logements:[D('h2','Logement 1','MAB-2',14)] },
  { id:'y1', numero:'T 513 D1', logements:[D('k1','Logement 1','MAB-3',20)] },
  { id:'y2', numero:'T513 D2',  logements:[D('k2','Logement 1','MAB-4',22)] },
  { id:'z1', numero:'T600',     logements:[D('m1','Piste exterieur','MAB-9',9)] },
];
console.log('   avant : ' + L(avant));
const apres = reparerOutilsD1D2(avant);
console.log('   apres : ' + L(apres));
console.log();
T2('5 outils deviennent 3', apres.length === 3);
T2('T543 a bien 2 logements D1,D2', (apres[0].logements||[]).map(l=>l.nom).sort().join(',') === 'D1,D2');
T2('T513 a bien 2 logements D1,D2', (apres[1].logements||[]).map(l=>l.nom).sort().join(',') === 'D1,D2');
T2('le numero garde les espaces de l atelier ("T 543")', /T\s?543/.test(apres[0].numero) && !/[Dd]\d$/.test(apres[0].numero));
T2('AUCUN MABEC perdu', ['MAB-1','MAB-2','MAB-3','MAB-4','MAB-9'].every(m => apres.some(o => (o.logements||[]).some(l => l.mabec===m))));
T2('AUCUN prix perdu', [12,14,20,22,9].every(p => apres.some(o => (o.logements||[]).some(l => l.prix===p))));
T2('T600, avec son nom d atelier, est INTACT', (apres[2].logements||[])[0].nom === 'Piste exterieur');
T2('la fonction est PURE : l entree n a pas ete modifiee', avant.length === 5 && avant[0].numero === 'T 543 D1' && avant[0].logements[0].nom === 'Logement 1');
T2('rien n est fusionne par erreur avec un autre porte-outil', !apres.some(o => (o.logements||[]).some(l => l.mabec==='MAB-1') && (o.logements||[]).some(l => l.mabec==='MAB-3')));

/* La panne qu'un contre-regard a laissee passer : fusionner DEUX PORTE-OUTILS
   DIFFERENTS parce que la cle de rapprochement est abimee. C'est la faute la plus
   grave possible ici — elle melange deux outillages et perd la correspondance avec
   le classeur de Matis. Elle doit etre attrapee. */
const deuxPortes = [
  { id:'p1', numero:'T543 D1', logements:[D('a1','Logement 1','MAB-A',1)] },
  { id:'p2', numero:'T543 D2', logements:[D('a2','Logement 1','MAB-B',2)] },
  { id:'p3', numero:'T517 D1', logements:[D('b1','Logement 1','MAB-C',3)] },
  { id:'p4', numero:'T517 D2', logements:[D('b2','Logement 1','MAB-D',4)] },
];
const r2 = reparerOutilsD1D2(deuxPortes);
console.log('   -> ' + r2.map(o=>o.numero+' ['+(o.logements||[]).map(l=>l.mabec).join(',')+']').join('  |  '));
T2('T543 et T517 restent DEUX outils distincts', r2.length === 2);
T2('aucun outil ne porte les MABEC d un autre porte-outil',
   r2.every(o => { const ms=(o.logements||[]).map(l=>l.mabec).join(','); return ms==='MAB-A,MAB-B' || ms==='MAB-C,MAB-D'; }));
T2('chaque groupe garde exactement 2 logements', r2.every(o => (o.logements||[]).length === 2));

console.log();
console.log('=== 4. LE RAPPORT PARLE, il ne compte pas en silence ===');
const rap = reparerOutilsRapport(avant, apres);
rap.forEach(l => console.log('   · ' + l));
T2('le rapport nomme chaque fusion', rap.length === 2);
T2('il dit combien de logements', rap.every(l => /logements/.test(l)));

console.log();
console.log('=== 5. L OUTIL NU EST SIGNE, PAS FUSIONNE ===');
const mix = [ {id:'p',numero:'T543',logements:[D('g1')]},
              {id:'q',numero:'T543 D1',logements:[D('h1')]},
              {id:'r',numero:'T543 D2',logements:[D('i1')]} ];
const rx = reparerOutilsD1D2(mix);
T2('l outil nu reste separe', rx.some(o => o.numero === 'T543' && !(o.logements||[]).some(l=>l.nom==='D1')));
T2('mais il est signale', (rx._orphelins||[]).length === 1);
if (rx._orphelins && rx._orphelins[0]) console.log('   · ' + rx._orphelins[0]);

console.log();
console.log(ko === 0 ? 'TOUT EST VERT' : ko + ' ECHEC(S)');
process.exit(ko === 0 ? 0 : 1);
""" % bloc

io.open('_g.js', 'w', encoding='utf-8').write(JS)
r = subprocess.run(['node', '_g.js'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout or r.stderr[:1500])
os.unlink('_g.js')
