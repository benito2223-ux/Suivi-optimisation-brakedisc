const fs = require('fs');
const html = fs.readFileSync('bilan_economique.html', 'utf8');
const i = html.indexOf('/* v4.163 — CHECKUP'), j = html.indexOf('/* v4.161 — MOTEUR');
let code = html.slice(i, j).replace(/\(function\(\)\{\n  let wrap = null;[\s\S]*$/, '');
code += '\nglobalThis.__x = { checkupXlsx };';
eval(code);
const ts = (jr, h, m) => new Date(2026, 10, jr, h, m, 5).toISOString();
const rows = [
  { id: 1, ts: ts(24, 6, 10), equipe: 'Matin', ligne: 'EMAG 1', reference: '356x26 RPI', op: 'OP10', type: 'charniere', element: 'T517·D2', attendu: '600', releve: '300', statut: 'ecart', commentaire: 'réglage changé & à vérifier <urgent> "ok"', version_reference: 1 },
  { id: 2, ts: ts(24, 14, 0), equipe: 'Après-midi', ligne: 'EMAG 1', reference: '356x26 RPI', op: 'OP10', type: 'charniere', element: 'T517·D2', attendu: '600', releve: '600', statut: 'ok', commentaire: '', version_reference: 1 },
  { id: 3, ts: ts(24, 6, 15), equipe: 'Matin', ligne: 'EMAG 1', reference: '356x26 RPI', op: 'OP10', type: 'potentiometre', element: 'pot', attendu: '120', releve: '100', statut: 'ecart', commentaire: 'à 100 %', version_reference: 2 }
];
fs.writeFileSync('.test_checkup.xlsx', Buffer.from(globalThis.__x.checkupXlsx(rows)));
console.log('écrit');
