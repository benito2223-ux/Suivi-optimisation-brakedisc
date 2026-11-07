/* Serveur factice du cloud — POUR LES TESTS LOCAUX UNIQUEMENT (jamais déployé : dist/ ne le contient pas).
   Il reproduit la logique des fonctions SQL de supabase/migrations/20261108_suivi_sync_v2.sql (mêmes règles :
   équipe par code, concurrence par révision, curseur, suppression logique, pièces adressées par empreinte), et
   un interrupteur de panne pour éprouver le hors ligne.
   Usage : node outils/serveur_factice_supabase.mjs [port]      (défaut 8935 ; code d'équipe de test : TEST-CODE)
   Les pages locales le visent via localStorage : spk_cloud_url_test = http://localhost:8935 */
import http from 'node:http';

const PORT = parseInt(process.argv[2] || '8935', 10);
const CODE = 'TEST-CODE';
const shards = new Map();      // "espace|id" -> {id, kind, body, rev, seq, supprime, modifie_par}
const blobs = new Map();
const membres = new Set();
let seq = 0, panne = false, nbRequetes = 0, octetsSortis = 0;
const journal = [];

const cors = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'apikey, authorization, content-type, prefer, x-client-info', 'Access-Control-Allow-Methods': 'GET, POST, PATCH, OPTIONS' };
const envoyer = (res, code, obj) => { const txt = obj === null ? '' : JSON.stringify(obj); octetsSortis += txt.length; res.writeHead(code, { 'Content-Type': 'application/json', ...cors }); res.end(txt); };
const utilisateur = (req) => { const m = /^Bearer tok_(.+)$/.exec(req.headers.authorization || ''); return m ? decodeURIComponent(m[1]) : null; };

const rpc = {
  suivi_statut: (u) => ({ membre: membres.has(u), email: u }),
  suivi_rejoindre: (u, a) => { if (membres.has(u)) return { ok: true, deja: true }; if (a.p_code !== CODE) return { ok: false, raison: 'code incorrect' }; membres.add(u); return { ok: true, deja: false }; },
  sync_pull: (u, a) => { exiger(u); return [...shards.values()].filter(s => s.espace === a.p_espace && s.seq > (a.p_depuis || 0)).sort((x, y) => x.seq - y.seq).slice(0, Math.min(a.p_limite || 100, 500)).map(({ id, kind, body, rev, seq, supprime, modifie_par }) => ({ id, kind, body, rev, seq, supprime, modifie_par })); },
  sync_push: (u, a) => {
    exiger(u);
    return a.p_items.map(it => {
      const cle = a.p_espace + '|' + it.id, cur = shards.get(cle), base = it.base_rev || 0, sup = !!it.supprime;
      if (!cur) { const n = { espace: a.p_espace, id: it.id, kind: it.kind || '', body: it.body, rev: 1, seq: ++seq, supprime: sup, modifie_par: u }; shards.set(cle, n); return { id: n.id, ok: true, rev: 1, seq: n.seq }; }
      if (cur.rev === base) { cur.body = it.body; cur.kind = it.kind || cur.kind; cur.supprime = sup; cur.rev++; cur.seq = ++seq; cur.modifie_par = u; return { id: cur.id, ok: true, rev: cur.rev, seq: cur.seq }; }
      return { id: cur.id, ok: false, conflit: true, rev: cur.rev, seq: cur.seq, body: cur.body, supprime: cur.supprime, modifie_par: cur.modifie_par };
    });
  },
  sync_blobs_manquants: (u, a) => { exiger(u); return a.p_shas.filter(s => !blobs.has(s)); },
  sync_blob_put: (u, a) => { exiger(u); if (!blobs.has(a.p_sha)) blobs.set(a.p_sha, a.p_data); return true; },
  sync_blob_get: (u, a) => { exiger(u); return blobs.get(a.p_sha) ?? null; },
};
function exiger(u) { if (!membres.has(u)) { const e = new Error('accès refusé'); e.http = 403; throw e; } }

http.createServer((req, res) => {
  if (req.method === 'OPTIONS') { res.writeHead(204, cors); return res.end(); }
  const url = new URL(req.url, 'http://x');
  let corps = '';
  req.on('data', c => corps += c);
  req.on('end', () => {
    nbRequetes++;
    // administration des tests
    if (url.pathname === '/__admin/panne') { panne = url.searchParams.get('mode') === 'offline'; return envoyer(res, 200, { panne }); }
    if (url.pathname === '/__admin/etat') {
      return envoyer(res, 200, { shards: shards.size, blobs: blobs.size, membres: [...membres], requetes: nbRequetes, octetsSortis,
        parEspace: Object.fromEntries([...new Set([...shards.values()].map(s => s.espace))].map(e => [e, [...shards.values()].filter(s => s.espace === e).length])),
        revs: Object.fromEntries([...shards.values()].map(s => [s.id, s.rev])), journal: journal.slice(-30) });
    }
    if (url.pathname === '/__admin/raz') { shards.clear(); blobs.clear(); membres.clear(); seq = 0; nbRequetes = 0; octetsSortis = 0; journal.length = 0; return envoyer(res, 200, { ok: true }); }
    if (url.pathname === '/__admin/shard') { const s = [...shards.values()].find(x => x.id === url.searchParams.get('id')); return envoyer(res, 200, s || null); }
    if (panne) { res.writeHead(503, cors); return res.end('panne simulée'); }
    // authentification (accepte tout, l'identité est l'email)
    if (url.pathname === '/auth/v1/token' || url.pathname === '/auth/v1/signup') {
      const a = corps ? JSON.parse(corps) : {};
      const email = a.email || (a.refresh_token ? decodeURIComponent(String(a.refresh_token).replace(/^ref_/, '')) : 'inconnu');
      return envoyer(res, 200, { access_token: 'tok_' + encodeURIComponent(email), refresh_token: 'ref_' + encodeURIComponent(email), expires_in: 3600, user: { email } });
    }
    if (url.pathname === '/auth/v1/logout') return envoyer(res, 204, null);
    const m = /^\/rest\/v1\/rpc\/(.+)$/.exec(url.pathname);
    if (m && rpc[m[1]]) {
      const u = utilisateur(req);
      if (!u) return envoyer(res, 401, { message: 'jeton absent' });
      try {
        const args = corps ? JSON.parse(corps) : {};
        const r = rpc[m[1]](u, args);
        journal.push(m[1] + ' ' + u + (args.p_items ? ' x' + args.p_items.length : ''));
        return envoyer(res, 200, r);
      } catch (e) { return envoyer(res, e.http || 400, { message: e.message }); }
    }
    envoyer(res, 404, { message: 'inconnu : ' + url.pathname });
  });
}).listen(PORT, () => console.log('serveur factice sur http://localhost:' + PORT + ' — code d\'équipe de test : ' + CODE));
