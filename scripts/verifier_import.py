import io, re, subprocess, os, json

REPO = r'C:\Users\Admin\Desktop\Stellantis_SeptFons'
P = 'bilan_economique.html'
BAK = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'bak_import.html')
s = io.open(os.path.join(REPO, P), encoding='utf-8').read()

# on prend les VRAIES fonctions de migration de l'app et on y fait passer le fichier
i = s.find('function migrerArbre')
j = s.find('/* ── 4.', i)
if j < 0:
    j = i + 9000
# normalizeLigne/Reference/Op : on les cherche
def grab(nom):
    a = s.find('function ' + nom)
    if a < 0:
        return ''
    b = s.find('\n}', a)
    return s[a:b + 2]

# defaultConfig n'est pas une fonction : on le prend tel quel
_dc = s.find('const defaultConfig = {')
_dc_fin = s.find('\n};', _dc) + 3
defaultConfig = s[_dc:_dc_fin]

blocs = defaultConfig + '\n' + '\n'.join(grab(n) for n in
                  ['normalizeLigne', 'normalizeReference', 'normalizeOp', 'normalizeScenario',
                   'normalizeOutil', 'normalizeLogement', 'normalizePieceDetachee',
                   'normalizeProjet', 'normalizeTag', 'normalizeLivraison',
                   'finaliserProjetsEtResponsables', 'purgerTagsMorts', 'migrerArbre'])
manquants = [n for n in ['normalizeLigne', 'normalizeReference', 'normalizeOp', 'migrerArbre']
             if 'function ' + n not in blocs]
print('fonctions non trouvees :', manquants or 'aucune')

donnees = json.load(io.open(os.path.join(REPO, 'IMPORT_MATIS.json'), encoding='utf-8'))

JS = r"""
%s
const data = %s;
const r = migrerArbre(data);
console.log('=== l ARBORESCENCE A SURVECU A L IMPORT ? ===');
const T = (t, ok) => console.log('   ' + (ok ? 'OK  ' : 'KO  <<< ') + t);
let ko = 0; const T2 = (t, ok) => { if (!ok) ko++; T(t, ok); };

const lignes = r.lignes, rf = lignes.flatMap(l => l.references);
const ops = rf.flatMap(x => x.ops);
const scs = ops.flatMap(o => o.scenarios);
const outils = scs.flatMap(s2 => (s2.outils || []));
const logs = outils.flatMap(t => (t.logements || []));
T2('4 lignes EMAG 1/2/3 + HESSAPP', lignes.length === 4 && lignes.map(l=>l.nom).join(',') === 'EMAG 1,EMAG 2,EMAG 3,HESSAPP');
T2('12 references', rf.length === 12);
T2('les 4 operations de chaque reference sont la', ops.length === 44);
T2('129 outils, 192 logements', outils.length === 129 && logs.length === 192);
T2('aucun outil sans numero', outils.every(t => String(t.numero||'').trim().length > 0));
T2('aucun logement sans identifiant', logs.every(g => !!g.id));
T2('les identifiants sont uniques', new Set(ops.map(o=>o.id)).size === ops.length && new Set(outils.map(t=>t.id)).size === outils.length);
T2('chaque logement a un MABEC ou le dit', logs.filter(g=>!g.mabec).length === 7);
T2('le MABEC a SURVECU a la normalisation (v4.72.0)', logs.filter(g=>g.mabec).length === 185);
T2('l ISO est recuperee (colonne fusionnee)', logs.filter(g=>g.ref).length > 150);
T2('aucune production mise a zero', ops.every(o => o.config.volumeAnnuel !== 0));
T2('15 references ont une production reelle', ops.filter(o => o.config.volumeAnnuel).length === 15);
T2('les productions sont les bonnes', JSON.stringify([2490,4180,6781,8149]) === JSON.stringify([...new Set(ops.map(o=>o.config.volumeAnnuel).filter(Boolean))].sort((a,b)=>a-b)));
T2('les prix survivent', logs.filter(g => g.prix !== "" && g.prix !== undefined).length > 180);
T2('les aretes survivent', logs.every(g => Number.isFinite(g.aretes)));
T2('le scenario de reference est en serie', scs.every(s2 => s2.statut === 'serie'));

/* LE CONTROLE QUI COMPTE : un porte-outil ne peut apparaitre qu UNE fois
   par scenario, avec ses logarithmes. C est le bug de Benjamin. */
console.log();
console.log('=== le controle anti-doublon, apres import ===');
let doublons = 0, outilsMulti = 0;
for (const s2 of scs) {
  const vus = new Set();
  for (const t of (s2.outils || [])) {
    const k = String(t.numero).toUpperCase().replace(/[^A-Z0-9]/g,'');
    if (vus.has(k)) doublons++;
    vus.add(k);
    if ((t.logements||[]).length > 1) outilsMulti++;
  }
}
T2('aucun porte-outil en double dans un scenario', doublons === 0);
T2('des outils portent bien plusieurs logements', outilsMulti > 40);

const t543 = [];
for (const s2 of scs) for (const t of (s2.outils||[])) if (t.numero === 'T543') t543.push(t);
T2('T543 existe, sans doublon a l interieur', t543.length > 0 && t543.every(t => new Set(t.logements.map(g=>g.nom)).size === t.logements.length));
const avec2 = t543.filter(t => t.logements.length === 2);
T2('T543 a bien deux logements D1 et D2', avec2.length > 0);
if (avec2[0]) {
  const noms = avec2[0].logements.map(g=>g.nom).sort().join(',');
  T2('ses deux logements s appellent D1 et D2', noms === 'D1,D2');
  T2('ils ont deux MABEC distincts', avec2[0].logements.every(g=>g.mabec) && avec2[0].logements[0].mabec !== avec2[0].logements[1].mabec);
}
console.log();
console.log(ko === 0 ? 'IMPORT : TOUT EST VERT' : 'IMPORT : ' + ko + ' ECHEC(S)');
process.exit(ko ? 1 : 0);
""" % (blocs, json.dumps(donnees, ensure_ascii=False))

io.open(os.path.join(REPO, '_imp.js'), 'w', encoding='utf-8').write(JS)
r = subprocess.run(['node', os.path.join(REPO, '_imp.js')], capture_output=True, text=True,
                   encoding='utf-8', errors='replace', cwd=REPO)
print(r.stdout or ('ERREUR:\n' + r.stderr[:900]))
os.unlink(os.path.join(REPO, '_imp.js'))
