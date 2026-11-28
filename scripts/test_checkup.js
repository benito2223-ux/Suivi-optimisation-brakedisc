/* Tests du « Contrôle de prise de poste » (checkup.html) — logique pure, sans navigateur.
   Lancé seul :  node scripts/test_checkup.js     (depuis la racine du dépôt)
   Lancé aussi par build_harness.py (verdict global).
   Principe : le script du fichier réel est exécuté dans un contexte isolé (vm) avec un faux DOM,
   un faux localStorage et un faux fetch. Rien ne sort : aucun accès réseau, aucune écriture. */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const RACINE = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(RACINE, 'checkup.html'), 'utf8');
const m = /<script[^>]*>([\s\S]*?)<\/script>/.exec(html);
if (!m) { console.log('  ECHEC checkup : aucun <script> dans checkup.html'); process.exit(1); }
const css = (/<style>([\s\S]*?)<\/style>/.exec(html) || [, ''])[1];
const code = m[1];

let echecs = 0, ok = 0;
function t(nom, cond, detail) {
  if (cond) { ok++; console.log('  ok  checkup : ' + nom); }
  else { echecs++; console.log('  ECHEC checkup : ' + nom + (detail ? ' — ' + detail : '')); }
}

/* ---------- faux navigateur ---------- */
function creerContexte(reponses) {
  const stock = new Map();
  const appels = [];
  const noeud = () => {
    const n = { innerHTML: '', textContent: '', value: '', style: {}, dataset: {}, children: [], className: '',
      classList: { toggle() {}, add() {}, remove() {}, contains: () => false },
      getAttribute: () => null, setAttribute() {}, appendChild() {}, remove() {}, focus() {}, click() {},
      addEventListener() {}, removeEventListener() {}, querySelector: () => noeud(), querySelectorAll: () => [],
      closest: () => null, getBoundingClientRect: () => ({ top: 0, bottom: 0, height: 0, left: 0, right: 0, width: 0 }) };
    return n;
  };
  const els = {};
  const document = { getElementById: id => els[id] || (els[id] = noeud()), querySelector: () => noeud(), querySelectorAll: () => [],
    createElement: noeud, addEventListener() {}, body: noeud(), documentElement: noeud(), hidden: false };
  const fenetre = {};
  const ctx = {
    document, console: { log() {}, error() {}, warn() {} },
    localStorage: { getItem: k => (stock.has(k) ? stock.get(k) : null), setItem: (k, v) => stock.set(k, String(v)), removeItem: k => stock.delete(k) },
    navigator: { onLine: true, userAgent: 'node', serviceWorker: { register: () => Promise.resolve(), addEventListener() {} } },
    location: { search: '', href: 'http://test/checkup.html', reload() {} },
    history: { state: null, length: 1, pushState() {}, replaceState() {}, back() {}, go() {} },
    matchMedia: () => ({ matches: false, addEventListener() {}, addListener() {} }),
    addEventListener() {}, removeEventListener() {}, confirm: () => true, alert() {},
    setTimeout: (f, ms) => { const h = setTimeout(f, ms); if (h.unref) h.unref(); return h; }, clearTimeout,
    setInterval: () => 0, clearInterval() {},
    Date, Math, JSON, Promise, Set, Map, Array, Object, String, Number, Boolean, RegExp, Error, isNaN, isFinite, parseInt, parseFloat,
    encodeURIComponent, decodeURIComponent, URLSearchParams, URL, Intl, Blob: function () {}, TextEncoder,
    atob: s => Buffer.from(s, 'base64').toString('binary'), btoa: s => Buffer.from(s, 'binary').toString('base64'),
    fetch: async (url, opts) => {
      appels.push({ url: String(url), corps: opts && opts.body ? String(opts.body) : '' });
      return reponses(String(url), opts || {});
    },
    requestAnimationFrame: f => setTimeout(f, 0), getComputedStyle: () => ({ getPropertyValue: () => '' }),
    innerWidth: 390, innerHeight: 844,
  };
  ctx.window = Object.assign(fenetre, ctx); ctx.self = ctx.window; ctx.globalThis = ctx.window;
  ctx.window.addEventListener = () => {};
  vm.createContext(ctx);
  vm.runInContext(code, ctx, { filename: 'checkup.html' });
  return { ctx, appels, stock, ev: s => vm.runInContext(s, ctx) };
}
const reponse = (status) => ({ ok: status >= 200 && status < 300, status, json: async () => ({}), text: async () => '' });
const entree = (id, element, extra) => Object.assign({ localId: id, ts: '2026-11-25T08:00:00Z', equipe: 'Matin', ligne: 'EMAG 1', reference: '356x26 RPI',
  op: 'OP10', type: 'charniere', element, attendu: '150', releve: '150', statut: 'ok', commentaire: '', version_reference: 1 }, extra || {});

(async () => {
  /* ---- 1. Équipes : horaires confirmés par Benjamin le 25/11/2026 (5 h, 13 h, 21 h) ---- */
  {
    const { ev } = creerContexte(() => reponse(201));
    const nom = (h, mi) => ev('equipe(new Date(2026, 10, 25, ' + h + ', ' + (mi || 0) + ')).nom');
    t('équipe de nuit jusqu\'à 4 h 59', nom(4, 59) === 'Nuit' && nom(0, 0) === 'Nuit', nom(4, 59));
    t('équipe du matin de 5 h à 12 h 59', nom(5, 0) === 'Matin' && nom(12, 59) === 'Matin', nom(5, 0) + '/' + nom(12, 59));
    t('équipe de l\'après-midi de 13 h à 20 h 59', nom(13, 0) === 'Après-midi' && nom(20, 59) === 'Après-midi', nom(13, 0) + '/' + nom(20, 59));
    t('équipe de nuit dès 21 h', nom(21, 0) === 'Nuit' && nom(23, 59) === 'Nuit', nom(21, 0));
  }

  /* ---- 2. Envoi du journal : un relevé refusé ne bloque plus les autres ---- */
  {
    const { ctx, ev, appels } = creerContexte((url, opts) => {
      if (!/checkup_journal/.test(url)) return reponse(200);
      const corps = JSON.parse(opts.body || '[]');
      return reponse(corps.some(x => x.element === 'T999 · D9') ? 400 : 201);
    });
    ctx.__q = [entree('a1', 'T500 · D1'), entree('a2', 'T500 · D2'), entree('a3', 'T999 · D9', { commentaire: 'x'.repeat(2000) }), entree('a4', 'T517 · D2'), entree('a5', 'T521 · D1')];
    ev('queue = __q.slice(); journal = __q.map(e => Object.assign({}, e)); prochainEssai = 0;');
    await ev('flusherJournal(true)');
    const restant = ev('queue.map(e => e.localId)');
    const envoyes = ev('journal.filter(e => e.sent).map(e => e.localId)');
    const refuses = ev('journal.filter(e => e.refuse).map(e => e.localId)');
    t('un relevé refusé n\'empêche plus les 4 autres de partir', envoyes.length === 4 && envoyes.indexOf('a3') === -1, 'envoyés=' + envoyes);
    t('le relevé refusé est repéré et sorti de la file', refuses.length === 1 && refuses[0] === 'a3' && restant.length === 0, 'refusés=' + refuses + ' file=' + restant);
    t('l\'écran dit qu\'un relevé est refusé (plus de blocage silencieux)', /1 relevé refusé/.test(ev('infoJournal()')), ev('infoJournal()'));
    t('l\'isolement reste borné (moins de 25 envois pour 5 relevés)', appels.filter(a => /checkup_journal/.test(a.url)).length < 25, String(appels.length));
  }

  /* ---- 3. Réseau coupé ou serveur en panne : rien n'est perdu, rien n'est marqué refusé ---- */
  {
    for (const [nom, rep] of [['serveur 503', () => reponse(503)], ['réseau coupé', () => { throw new Error('Failed to fetch'); }], ['trop de requêtes 429', () => reponse(429)]]) {
      const { ctx, ev } = creerContexte((url) => (/checkup_journal/.test(url) ? rep() : reponse(200)));
      ctx.__q = [entree('b1', 'T500 · D1'), entree('b2', 'T500 · D2')];
      ev('queue = __q.slice(); journal = __q.map(e => Object.assign({}, e)); prochainEssai = 0;');
      await ev('flusherJournal(true)');
      t('« ' + nom + ' » : les 2 relevés restent en file, aucun n\'est déclaré refusé',
        ev('queue.length') === 2 && ev('journal.filter(e => e.refuse || e.sent).length') === 0, 'file=' + ev('queue.length'));
    }
    const { ctx, ev } = creerContexte((url) => (/checkup_journal/.test(url) ? reponse(404) : reponse(200)));
    ctx.__q = [entree('c1', 'T500 · D1')];
    ev('queue = __q.slice(); journal = __q.map(e => Object.assign({}, e)); prochainEssai = 0;');
    await ev('flusherJournal(true)');
    t('table du journal absente (404) : relevé conservé et message affiché', ev('queue.length') === 1 && /conserv/.test(ev('infoJournal()')), ev('infoJournal()'));
  }

  /* ---- 4. Tout le lot refusé (droits) : rien n'est jeté, l'écran le dit ---- */
  {
    const { ctx, ev } = creerContexte((url) => (/checkup_journal/.test(url) ? reponse(403) : reponse(200)));
    ctx.__q = [entree('d1', 'T500 · D1'), entree('d2', 'T500 · D2')];
    ev('queue = __q.slice(); journal = __q.map(e => Object.assign({}, e)); prochainEssai = 0;');
    await ev('flusherJournal(true)');
    t('droits refusés (403) : les relevés restent en file et ne sont pas perdus', ev('queue.length') === 2 && ev('journal.filter(e => e.refuse).length') === 0, 'file=' + ev('queue.length'));
  }

  /* ---- 5. Contrôles statiques du fichier livré ---- */
  {
    const decl = (code.match(/^(?:async )?function ([A-Za-z0-9_$]+)/gm) || []).map(s => s.replace(/^(?:async )?function /, ''));
    const doublons = decl.filter((n, i) => decl.indexOf(n) !== i);
    t('aucune fonction déclarée deux fois', doublons.length === 0, doublons.join(', '));
    let o = 0, f = 0; for (const c of css) { if (c === '{') o++; if (c === '}') f++; }
    t('feuille de style équilibrée (accolades)', o === f, o + ' / ' + f);
    const build = (/const BUILD = "([^"]+)"/.exec(code) || [])[1];
    const ver = JSON.parse(fs.readFileSync(path.join(RACINE, 'checkup-version.json'), 'utf8')).build;
    t('BUILD du fichier = checkup-version.json (sinon la mise à jour ne se déclenche pas)', build === ver, build + ' / ' + ver);
    const sansPolice = html.replace(/base64,[A-Za-z0-9+\/=]{200,}/g, '');
    t('aucune mention de la marque ni de la maison mère', !/ceramtec|\bspk\b/i.test(sansPolice));
    t('aucune puissance, aucun coût, aucun prix à l\'écran', !/p_req|puissance|coût|\bprix\b/i.test(sansPolice));
    t('l\'encre des boutons ✓ et ≠ suit le thème (lisible en mode nuit)', /--on-accent/.test(css) && /\.bok\{[^}]*color:var\(--on-accent\)/.test(css) && /\.bec\{[^}]*color:var\(--on-accent\)/.test(css));
    t('le bouton retour d\'Android est géré (historique)', /addEventListener\("popstate"/.test(code) && /history\.pushState/.test(code));
    t('un glisser interrompu est rattrapé (pointercancel)', /"pointercancel"/.test(code));
    t('l\'app relit les références au retour au premier plan', /visibilitychange/.test(code) && /synchroniser\(true\)/.test(code));
    t('motifs rapides et boutons secondaires à 72 px (gants)', /\.motif\{[^}]*min-height:72px/.test(css) && /header \.hbtn\{[^}]*min-height:72px/.test(css));
  }

  console.log((echecs ? '  ECHEC ' : '  ok  ') + 'checkup : ' + ok + ' vérifications passées, ' + echecs + ' échec(s)');
  process.exit(echecs ? 1 : 0);
})().catch(e => { console.log('  ECHEC checkup : le test a planté — ' + (e && e.stack || e)); process.exit(1); });
