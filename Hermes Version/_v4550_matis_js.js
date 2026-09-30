/* ════════════════════════════════════════════════════════════════════════════
   v4.55.0 — LE CLASSEUR MATIS, source de production RÉELLE (option C de l'analyse
   du 29/09). Règle constitution §4.2 : rien ne quitte le poste — la lecture est
   OPTIONNELLE, manuelle, sur un fichier que l'utilisateur choisit lui-même.

   Ce que ce bloc apporte, et pourquoi c'est un changement de nature :
   · jusqu'ici la production était un SCÉNARIO déguisé (un booléen `baseline` posé
     sur un scénario d'essai) ; chaque calcul cherchait « ★ d'abord, excel en repli » ;
   · le classeur de Matis donne la production RÉELLE, chiffrée, par couple
     ligne × référence (volume en case B1 de chaque feuille « Cout pièce »), avec
     le CPP réel consommé et l'écart à la théorie ;
   · donc : le scénario-★ reste la RÉFÉRENCE DE COMPARAISON (son rôle historique,
     intact), et la production réelle devient une DONNÉE à part, importable, datée.

   Décision C (Benjamin) : on importe et on MESURE l'écart théorie/réel avant de
   décider si la production doit devenir une entité de premier niveau. Rien ici ne
   change le format des données : c'est un bloc d'observation, pas une migration.

   Un .xlsm est une archive ZIP. On lit son XML directement — aucune bibliothèque,
   aucun réseau, rien à installer. La décompression utilise DecompressionStream
   (natif Chrome/Edge, donc « un seul fichier » reste vrai).
   ────────────────────────────────────────────────────────────────────────── */

function _xmlUnescape(s){
  return String(s).replace(/&lt;/g, "<").replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"').replace(/&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, n) => String.fromCharCode(parseInt(n, 10)))
    .replace(/&amp;/g, "&");
}

/* décompresse une entrée ZIP (deflate-raw ou stored) → Uint8Array */
async function _zipRead(ent){
  if(ent.method === 0) return ent.data;
  if(typeof DecompressionStream === "undefined"){
    throw new Error("Ce navigateur ne sait pas lire un classeur Excel. Utilise Chrome ou Edge.");
  }
  const ds = new DecompressionStream("deflate-raw");
  const buf = await new Response(new Blob([ent.data]).stream().pipeThrough(ds)).arrayBuffer();
  return new Uint8Array(buf);
}

/* inventaire des entrées ZIP + accès par nom de feuille */
async function _zipOpen(file){
  const bytes = new Uint8Array(await file.arrayBuffer());
  const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
  const u16 = o => dv.getUint16(o, true), u32 = o => dv.getUint32(o, true);
  let eocd = -1;
  for(let i = bytes.length - 22; i >= Math.max(0, bytes.length - 66000); i--){
    if(u32(i) === 0x06054b50){ eocd = i; break; }
  }
  if(eocd < 0) throw new Error("Ce fichier n'est pas un classeur Excel (archive illisible).");
  const count = u16(eocd + 10);
  let off = u32(eocd + 16);
  const entries = {};
  for(let i = 0; i < count; i++){
    if(u32(off) !== 0x02014b50) break;
    const method = u16(off + 10), csize = u32(off + 20);
    const nlen = u16(off + 28), elen = u16(off + 30), clen = u16(off + 32);
    const lho = u32(off + 42);
    const name = new TextDecoder("utf-8").decode(bytes.subarray(off + 46, off + 46 + nlen));
    const lnlen = u16(lho + 26), lelen = u16(lho + 28);
    const start = lho + 30 + lnlen + lelen;
    entries[name] = { method, csize, data: bytes.subarray(start, start + csize) };
    off += 46 + nlen + elen + clen;
  }
  return entries;
}

/* les chaînes partagées (le classeur les utilise pour tous les libellés) */
async function _xlSharedStrings(entries){
  const key = Object.keys(entries).find(k => /^xl\/sharedStrings\.xml$/.test(k));
  if(!key) return [];
  const xml = new TextDecoder("utf-8").decode(await _zipRead(entries[key]));
  const out = [];
  const re = /<si>([\s\S]*?)<\/si>/g;
  let m;
  while((m = re.exec(xml))){
    out.push(_xmlUnescape([...m[1].matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join("")));
  }
  return out;
}

/* <c r="A1" t="s"><v>3</v></c> → { A1: valeur } */
function _xlCells(xml, shared){
  const cells = {};
  const re = /<c r="([A-Z]+\d+)"([^>]*?)(?:\/>|>([\s\S]*?)<\/c>)/g;
  let m;
  while((m = re.exec(xml))){
    const ref = m[1], attrs = m[2] || "", inner = m[3] || "";
    const t = (attrs.match(/t="([^"]+)"/) || [])[1];
    if(t === "inlineStr"){
      cells[ref] = _xmlUnescape([...inner.matchAll(/<t[^>]*>([\s\S]*?)<\/t>/g)].map(x => x[1]).join(""));
      continue;
    }
    const vm = inner.match(/<v>([\s\S]*?)<\/v>/);
    if(!vm) continue;
    const raw = _xmlUnescape(vm[1]);
    if(t === "s") cells[ref] = shared[parseInt(raw, 10)] ?? "";
    else if(t === "b") cells[ref] = raw === "1";
    else { const n = parseFloat(raw); cells[ref] = isNaN(n) ? raw : n; }
  }
  return cells;
}

/* le lien nom-de-feuille → fichier XML (workbook.xml + rels) */
async function _xlSheetMap(entries){
  const wbKey = "xl/workbook.xml", relKey = "xl/_rels/workbook.xml.rels";
  if(!entries[wbKey] || !entries[relKey]) return {};
  const wb = new TextDecoder("utf-8").decode(await _zipRead(entries[wbKey]));
  const rels = new TextDecoder("utf-8").decode(await _zipRead(entries[relKey]));
  const relMap = {};
  for(const m of rels.matchAll(/<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"[^>]*\/?>/g)){
    relMap[m[1]] = m[2].replace(/^\/?xl\//, "").replace(/^\.\//, "");
  }
  const map = {};
  for(const m of wb.matchAll(/<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"[^>]*\/?>/g)){
    const target = relMap[m[2]];
    if(target) map[_xmlUnescape(m[1])] = "xl/" + target;
  }
  return map;
}

/* une feuille « Cout pièce » = un couple ligne × référence */
function _matisFeuille(nomFeuille, cells){
  const m = nomFeuille.match(/^Co[uû]t\s+pi[eè]ce\s+([EH])(\d)\s+(.+)$/i);
  if(!m) return null;
  const numOp = r => String(r || "").trim();
  const outils = [];
  for(let row = 4; row <= 140; row++){
    const numOutil = numOp(cells["A" + row]);
    if(!numOutil) continue;
    const op = numOp(cells["B" + row]);
    const mOp = op.match(/^OP\s?(\d+)/i);
    if(!mOp) continue;                     // ligne de garde : seuls les outils comptent
    const f = k => { const v = parseFloat(cells[k + row]); return isNaN(v) ? null : v; };
    outils.push({
      numero: numOutil, opCode: "OP" + mOp[1],
      article: numOp(cells["C" + row]), mabec: numOp(cells["D" + row]),
      aretes: f("F"), prix: f("G"), ddv: f("H"),
      cppTheorique: f("I"), qteTheorique: f("J"),
      coutReelAnnuel: f("L"), cppReel: f("M"), qteReelle: f("N"), ecart: f("O")
    });
  }
  const prod = parseFloat(cells["B1"]);
  return {
    codeLigne: m[1].toUpperCase() + m[2],
    ref: m[3].trim(),
    refComplete: (numOp(cells["C2"])) || m[3].trim(),
    production: isNaN(prod) ? null : prod,
    outils
  };
}

/* ═══ La fonction pure : le récapitulatif, testable sans fichier ═══════════
   Elle prend les feuilles déjà lues et rend ce que l'écran affiche. Aucun accès
   disque ici — c'est ce qui permet de la tester (constitution : source unique). */
function matisRecap(feuilles){
  const couples = {};
  feuilles.forEach(f => {
    if(!f) return;
    const key = f.codeLigne + "·" + f.ref;
    if(!couples[key]) couples[key] = { key, codeLigne: f.codeLigne, ref: f.ref, refComplete: f.refComplete,
      production: 0, aProduction: false, outils: [], cppTheorique: 0, cppReel: 0 };
    const c = couples[key];
    if(f.production !== null && f.production > 0){ c.production = f.production; c.aProduction = true; }
    c.outils = c.outils.concat(f.outils);
  });
  const liste = Object.keys(couples).map(k => couples[k]);
  liste.forEach(c => {
    c.outils.forEach(o => {
      if(o.cppTheorique) c.cppTheorique += o.cppTheorique;
      if(o.cppReel) c.cppReel += o.cppReel;
    });
    c.ecart = (c.cppReel && c.cppTheorique) ? c.cppReel - c.cppTheorique : null;
    c.ecartPct = (c.ecart !== null && c.cppTheorique) ? (c.ecart / c.cppTheorique) * 100 : null;
    c.coutAnnuelReel = c.aProduction && c.cppReel ? c.cppReel * c.production : null;
    c.coutAnnuelTheorique = c.aProduction && c.cppTheorique ? c.cppTheorique * c.production : null;
    c.gapAnnuel = (c.coutAnnuelReel !== null && c.coutAnnuelTheorique !== null)
      ? c.coutAnnuelReel - c.coutAnnuelTheorique : null;
  });
  return liste.sort((a, b) => (b.production || 0) - (a.production || 0));
}

/* l'écart, dit en atelier — jamais un chiffre nu sans sa raison (constitution §3.5) */
function libelleEcartMatis(c){
  if(c.ecart === null) return "non mesurable — pas de CPP réel relevé sur ce couple";
  if(Math.abs(c.ecart) < 0.0005) return "consommation conforme au budget-outillage";
  if(c.ecart > 0) return `surconsommation de ${fmt(Math.abs(c.ecart), 4)} €/pièce`;
  return `sous-consommation de ${fmt(Math.abs(c.ecart), 4)} €/pièce`;
}

/* ═══ La lecture du fichier (asynchrone, manuelle, locale) ═════════════════ */
async function matisLireClasseur(file){
  const entries = await _zipOpen(file);
  const shared = await _xlSharedStrings(entries);
  const map = await _xlSheetMap(entries);
  const feuilles = [];
  for(const nom of Object.keys(map)){
    if(!entries[map[nom]]) continue;
    const xml = new TextDecoder("utf-8").decode(await _zipRead(entries[map[nom]]));
    const f = _matisFeuille(nom, _xlCells(xml, shared));
    if(f) feuilles.push(f);
  }
  return { fichier: file.name, luLe: new Date().toISOString().slice(0, 10),
           feuilles, couples: matisRecap(feuilles) };
}
