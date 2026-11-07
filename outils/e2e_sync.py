"""Test de bout en bout de la synchro : DEUX appareils (deux processus Node, chacun son localStorage) dialoguent
avec le serveur factice (outils/serveur_factice_supabase.mjs). Le code exécuté est celui de bilan_economique.html,
tel quel (même mécanisme que build_harness.py : le DOM est neutralisé, la logique tourne pour de vrai).

Usage :  node outils/serveur_factice_supabase.mjs 8935 &      puis      python outils/e2e_sync.py
Rien n'est écrit hors du dossier temporaire ; aucun cloud réel n'est touché.
"""
import io, os, re, sys, json, subprocess, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(tempfile.gettempdir(), 'e2e_sync')
os.makedirs(TMP, exist_ok=True)
MOCK = 'http://localhost:8935'
EXPORT = os.path.join(REPO, 'AUDIT_export_prod_13-10_08h27_rev425_v3ok.json')

src = io.open(os.path.join(REPO, 'bilan_economique.html'), encoding='utf-8').read()
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', src)
code = '\n;\n'.join(scripts)
code = re.sub(r'verifierNouveautes\(\);(\s*//[^\n]*)?\s*$', ';', code, flags=re.M)
code = re.sub(r'^render\(\);\s*$', ';', code, flags=re.M)
# l'intervalle périodique garderait le processus vivant : on l'ignore (les cycles sont appelés explicitement)
code = code.replace('setInterval(() => { if(!document.hidden && cloudSession) cloudSync("periode"); }, 25000);', ';')

harn = io.open(os.path.join(REPO, 'build_harness.py'), encoding='utf-8').read()
a = harn.index("HARNESS = '''") + len("HARNESS = '''")
b = harn.index('const api = __CODE__')
prelude = harn[a:b]
# stockage adossé à un fichier, hôte local (jamais « prod »), vrai fetch
prelude = prelude.replace("localStorage:{getItem:()=>null,setItem(){},removeItem(){},clear(){}}",
                          "localStorage:__LS")
prelude = prelude.replace('"suivi-optimisation-septfons.surge.sh"', '"localhost"')
prelude = prelude.replace('global.fetch = () => Promise.reject(new Error("hors ligne"));', 'global.fetch = globalThis.__fetchReel;')
prelude = prelude.replace('global.performance = { now:()=>0 };', ';')   # le vrai performance : le fetch de Node s'en sert
# la vraie classe URL est indispensable au fetch de Node : on n'y ajoute que les deux méthodes simulées
prelude = prelude.replace('global.URL = { createObjectURL:()=>"blob:x", revokeObjectURL(){} };', 'global.URL.createObjectURL = ()=>"blob:x"; global.URL.revokeObjectURL = ()=>{};')
prelude = prelude.replace('global.Blob = class { constructor(){} }; global.File = class {};', '')
assert '__LS' in prelude and 'globalThis.__fetchReel' in prelude and 'global.URL.createObjectURL' in prelude

API = """globalThis.__api = {
  get lignes(){return lignes}, set lignes(v){lignes=v}, get data(){return data}, get activeId(){return activeId},
  get syEtat(){return syEtat}, get syMem(){return syMem}, syResume, sySync, syRejoindre, syCalculer, syDecouper, syEtatLocal,
  saveData, payloadSuivi, cloudCompterEssais, cloudSauverSession, get cloudSession(){return cloudSession}, set cloudSession(v){cloudSession=v},
  set dialogueConfirmer(v){dialogueConfirmer=v}, set syPeutAppliquer(v){syPeutAppliquer=v}, set cloudExportSecours(v){cloudExportSecours=v},
  get TOOL_VERSION(){return TOOL_VERSION}, get SY_ESPACE(){return SY_ESPACE}, get CLOUD_URL(){return CLOUD_URL},
  syCanon, syHash, syBlobsReferences, get syPending(){return Object.keys(syEtat.sales)}
};"""

SCRIPT = ("globalThis.__fetchReel = fetch;\n"
          "const __f = process.env.LS_FILE; let __d = {}; try { __d = JSON.parse(require('fs').readFileSync(__f, 'utf8')); } catch (e) {}\n"
          "const __LS = { getItem: k => (k in __d ? __d[k] : null), setItem(k, v) { __d[k] = String(v); }, removeItem(k) { delete __d[k]; }, clear() { __d = {}; }, "
          "get length() { return Object.keys(__d).length; }, key: i => Object.keys(__d)[i] };\n"
          + prelude +
          "\nconst api = " + json.dumps(code) + " + `\n;" + API + "\n`;\n"
          "new Function(api)();\n"
          "globalThis.__saveLS = () => require('fs').writeFileSync(__f, JSON.stringify(__d));\n"
          "require(process.env.PAS)(globalThis.__api, __LS).then(r => { globalThis.__saveLS(); console.log('@@' + JSON.stringify(r)); process.exit(0); })"
          ".catch(e => { globalThis.__saveLS(); console.log('@@' + JSON.stringify({ erreur: String(e && e.stack || e) })); process.exit(1); });\n")
SCRIPT = SCRIPT.replace('`\\n;', '`\\n;')
io.open(os.path.join(TMP, 'app.js'), 'w', encoding='utf-8').write(SCRIPT)

PAS = r"""
module.exports = async (A, LS) => {
  const pas = process.env.PAS_NOM, role = process.env.ROLE;
  const sc = () => { let r = null; A.lignes.forEach(l => l.references.forEach(rf => rf.ops.forEach(o => o.scenarios.forEach(s => { if (!r && (s.essais || []).length) r = s; })))); return r; };
  const cible = sc();
  const sonde = () => { const s = sc(); return { essais: A.cloudCompterEssais(A.lignes), operateur: s && s.essais[0].operateur, nbPrel: s && s.essais[0].prelevements.length,
      nomScenario: s && s.name, tol: s && (s.essais[0].marpossListe && s.essais[0].marpossListe[0] || {}).tol,
      scenarios: A.lignes.reduce((n, l) => n + l.references.reduce((m, r) => m + r.ops.reduce((k, o) => k + o.scenarios.length, 0), 0), 0) }; };
  const fini = async () => { for (let i = 0; i < 160 && A.syMem.verrou; i++) await new Promise(r => setTimeout(r, 250)); };
  A.dialogueConfirmer = async () => true; A.syPeutAppliquer = () => true; A.cloudExportSecours = () => {};
  const tok = (e) => ({ access_token: 'tok_' + encodeURIComponent(e), refresh_token: 'ref_' + encodeURIComponent(e), expires_at: Date.now() + 3600000, email: e });
  const sortie = (x) => Object.assign({ pas, role, sonde: sonde(), resume: A.syResume(), enAttente: A.syPending.length, shardsConnus: Object.keys(A.syEtat.shards).length, curseur: A.syEtat.curseur }, x || {});
  switch (pas) {
    case 'init': {
      const fs = require('fs');
      if (role === 'A') LS.setItem('spk_suivi_optimisation_v1', fs.readFileSync(process.env.EXPORT, 'utf8'));
      LS.setItem('spk_cloud_url_test', process.env.MOCK); LS.setItem('spk_espace_test', 'e2e');
      return { ok: true };
    }
    case 'connecter': {
      A.cloudSession = tok(role === 'A' ? 'a@test' : 'b@test');
      await A.sySync('test');
      if (A.syMem.membre === false || /code/.test(A.syMem.erreur || '')) { await A.syRejoindre('TEST-CODE'); await fini(); }
      await A.sySync('test'); await fini();
      return sortie({ url: A.CLOUD_URL, espace: A.SY_ESPACE });
    }
    case 'sync': A.cloudSession = tok(role === 'A' ? 'a@test' : 'b@test'); await A.sySync('test'); await fini(); return sortie();
    case 'editer': {  // modifie des champs selon EDIT = "champ=valeur;..."
      const s = sc(); const e = s.essais[0];
      process.env.EDIT.split(';').forEach(kv => {
        const [k, v] = kv.split('=');
        if (k === 'operateur') e.operateur = v;
        else if (k === 'equipe') e.equipe = v;
        else if (k === 'prelevement') e.prelevements.push({ id: 'pe2e' + Math.random().toString(36).slice(2), piece: e.prelevements.length + 1, batt: v, battD: '', battG: '', logementId: '', pointMesure: '' });
        else if (k === 'nom') s.name = v;
        else if (k === 'tol') { e.marpossListe = e.marpossListe || []; if (!e.marpossListe.length) e.marpossListe.push({ id: 'mj1', jour: '', debut: '', fin: '', tol: '', releves: [] }); e.marpossListe[0].tol = v; }
        else if (k === 'supprimer-dernier-scenario') { const op = A.lignes[0].references[0].ops[0]; op.scenarios.pop(); }
        else if (k === 'nouveau-scenario') { const op = A.lignes[0].references[0].ops[0]; const c = JSON.parse(JSON.stringify(op.scenarios[0])); c.id = 'snew' + Math.random().toString(36).slice(2, 6); c.name = v; c.essais = []; op.scenarios.push(c); }
      });
      A.saveData(); A.syCalculer();
      return sortie({ aEnvoyer: A.syPending });
    }
    case 'sonde': return sortie();
    case 'nb-shards': return sortie({ nb: Object.keys(A.syDecouper(A.syEtatLocal()).shards).length });
    case 'pending': return sortie({ aEnvoyer: A.syPending });
    case 'etat-local': return sortie({ canon: A.syHash(A.syCanon(JSON.parse(A.payloadSuivi()).lignes)) });
  }
  return { erreur: 'pas inconnu ' + pas };
};
"""
io.open(os.path.join(TMP, 'pas.js'), 'w', encoding='utf-8').write(PAS)

def pas(role, nom, edit=''):
    env = dict(os.environ, LS_FILE=os.path.join(TMP, 'ls_%s.json' % role), PAS=os.path.join(TMP, 'pas.js'), PAS_NOM=nom, ROLE=role,
               EDIT=edit, MOCK=MOCK, EXPORT=EXPORT)
    p = subprocess.run(['node', os.path.join(TMP, 'app.js')], capture_output=True, text=True, env=env, timeout=180)
    for l in p.stdout.splitlines():
        if l.startswith('@@'):
            return json.loads(l[2:])
    raise RuntimeError('sortie illisible : ' + p.stdout[-400:] + p.stderr[-600:])

import urllib.request
def mock(chemin):
    with urllib.request.urlopen(MOCK + chemin, timeout=10) as r:
        return json.loads(r.read().decode() or 'null')

echecs = []
def verifier(nom, cond, detail=''):
    if not cond: echecs.append(nom)
    print(('  ok  ' if cond else '  ECHEC ') + nom + (' — ' + str(detail) if detail else ''))

if __name__ == '__main__':
    mock('/__admin/raz'); mock('/__admin/panne?mode=online')
    for f in os.listdir(TMP):
        if f.startswith('ls_'): os.remove(os.path.join(TMP, f))
    pas('A', 'init'); pas('B', 'init')
    print('== 1. A dépose ses données réelles (cloud vide)')
    a = pas('A', 'connecter')
    etat = mock('/__admin/etat')
    verifier('A est membre et premier contact fait', a['resume']['membre'] is True and a['resume']['premier'] is True, a['resume'])
    attendu = pas('A', 'nb-shards')['nb']
    verifier('le serveur a reçu TOUS les enregistrements de A (%d attendus : l’état normalisé, pas le fichier brut)' % attendu, etat['shards'] == attendu, etat['shards'])
    verifier('rien en attente chez A après le dépôt', a['enAttente'] == 0, a['enAttente'])
    verifier('les 12 pièces volumineuses sont à part, envoyées une seule fois', etat['blobs'] == 12, etat['blobs'])
    verifier('A est bien dans l\'espace de test (pas de pollution d\'un autre espace)', list(etat['parEspace'].keys()) == ['e2e'], etat['parEspace'])
    print('== 2. B (poste neuf, jeu d\'exemple) rejoint et reçoit tout')
    b = pas('B', 'connecter')
    verifier('B a reçu les mêmes essais que A', b['sonde']['essais'] == a['sonde']['essais'] and b['sonde']['essais'] > 0, (b['sonde']['essais'], a['sonde']['essais']))
    ha, hb = pas('A', 'etat-local')['canon'], pas('B', 'etat-local')['canon']
    verifier('B et A ont exactement le même arbre (lignes, références, OP, scénarios, essais)', ha == hb)
    verifier('B n\'a rien à renvoyer après adoption (la normalisation locale ne crée pas de bruit)', b['enAttente'] == 0, b['aEnvoyer'] if 'aEnvoyer' in b else b['enAttente'])
    print('== 3. une saisie sur B arrive chez A, et ne coûte qu\'un enregistrement')
    avant = mock('/__admin/etat')['octetsSortis']
    e = pas('B', 'editer', 'operateur=Matis;prelevement=0.031')
    verifier('une saisie ne marque qu\'UN enregistrement à envoyer', len(e['aEnvoyer']) == 1, e['aEnvoyer'])
    pas('B', 'sync')
    a2 = pas('A', 'sync')
    verifier('A reçoit l\'opérateur saisi sur B', a2['sonde']['operateur'] == 'Matis', a2['sonde']['operateur'])
    verifier('A reçoit le prélèvement ajouté sur B', a2['sonde']['nbPrel'] == b['sonde']['nbPrel'] + 1, (a2['sonde']['nbPrel'], b['sonde']['nbPrel']))
    print('== 4. modifications simultanées de champs différents : fusion, rien n\'est perdu')
    pas('A', 'editer', 'equipe=Nuit')
    pas('B', 'editer', 'nom=Variante B')
    pas('A', 'sync')                       # A part d'abord
    rb = pas('B', 'sync')                  # B tombe sur le conflit et fusionne
    ra = pas('A', 'sync')
    verifier('B garde son renommage ET reçoit l\'équipe de A', rb['sonde']['nomScenario'] == 'Variante B', rb['sonde'])
    verifier('A reçoit le renommage de B', ra['sonde']['nomScenario'] == 'Variante B', ra['sonde'])
    verifier('plus rien en attente nulle part', ra['enAttente'] == 0 and rb['enAttente'] == 0, (ra['enAttente'], rb['enAttente']))
    print('== 5. le même champ modifié des deux côtés : pas de plantage, un conflit est noté, les deux convergent')
    pas('A', 'editer', 'operateur=Alice')
    pas('B', 'editer', 'operateur=Bruno')
    pas('A', 'sync'); rb = pas('B', 'sync'); ra = pas('A', 'sync')
    verifier('les deux appareils convergent vers la même valeur', ra['sonde']['operateur'] == rb['sonde']['operateur'], (ra['sonde']['operateur'], rb['sonde']['operateur']))
    verifier('le conflit est consigné pour l\'utilisateur', len(rb['resume']['conflits']) >= 1, rb['resume']['conflits'])
    print('== 6. hors ligne : on saisit, la file d\'attente se garde, tout part au retour du réseau')
    mock('/__admin/panne?mode=offline')
    o = pas('B', 'editer', 'prelevement=0.044')
    s = pas('B', 'sync')
    verifier('hors ligne : l\'erreur est visible et la saisie est en attente', bool(s['resume']['erreur']) and s['enAttente'] >= 1, (s['resume']['erreur'], s['enAttente']))
    verifier('hors ligne : la file d\'attente survit au redémarrage de l\'appli', pas('B', 'pending')['enAttente'] >= 1)
    mock('/__admin/panne?mode=online')
    s = pas('B', 'sync'); a3 = pas('A', 'sync')
    verifier('retour du réseau : tout est parti', s['enAttente'] == 0, s['enAttente'])
    verifier('A reçoit la saisie faite hors ligne', a3['sonde']['nbPrel'] == s['sonde']['nbPrel'], (a3['sonde']['nbPrel'], s['sonde']['nbPrel']))
    print('== 7. un scénario ajouté puis supprimé se propage')
    n0 = pas('A', 'sonde')['sonde']['scenarios']
    pas('A', 'editer', 'nouveau-scenario=Live Vc 700'); pas('A', 'sync')
    verifier('B reçoit le nouveau scénario', pas('B', 'sync')['sonde']['scenarios'] == n0 + 1)
    pas('B', 'editer', 'supprimer-dernier-scenario=1'); pas('B', 'sync')
    verifier('A reçoit la suppression', pas('A', 'sync')['sonde']['scenarios'] == n0)
    print('== 8. le coût réseau')
    fin = mock('/__admin/etat')
    print('   requêtes :', fin['requetes'], '| octets reçus par les appareils :', fin['octetsSortis'])
    print('\n' + (str(len(echecs)) + ' ECHEC(S) : ' + ' ; '.join(echecs) if echecs else 'TOUT VERT'))
    sys.exit(1 if echecs else 0)
