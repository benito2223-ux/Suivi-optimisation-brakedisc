# -*- coding: utf-8 -*-
"""Patch v4.88.0 partie A : LE BASCULEUR — consommation theorique vs reelle extrapolee.

Benjamin : « construis le basculeur ». Source REELLE = les feuilles « Pareto
conso » de SES classeurs (lecture locale, constitution 4.2), une semaine de
consommation reelle par article, x 52 — avec l'avertissement affiche.
"""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

def rep(av, ap):
    global s
    assert av in s, "ANCRE INTROUVABLE : " + av[:100]
    s = s.replace(av, ap, 1)

# ── 1. l'etat de session + le parseur, poses devant planLignes ──────────────
rep("const PLAN_ETATS = [",
'''/* ═══ v4.88 — LE BASCULEUR DE CONSOMMATION : theorique vs REELLE ════════════
   Benjamin, en voyant les quantites du Plan : « j'ai de tres gros doutes sur
   tes quantites de plaquettes annuelles » — il a raison : elles sont
   THEORIQUES (production / (aretes x DDV classeur)), et l'historique de ses
   propres classeurs dit un reel ~7,5 fois plus gros. Le basculeur permet de
   calculer les gains sur la consommation REELLE : les feuilles « Pareto
   conso » des classeurs donnent une semaine de consommation reelle par
   article, extrapolee x 52 — avec l'avertissement affiche (regime suppose
   constant). Lecture LOCALE uniquement (constitution 4.2) ; etat de session,
   comme la lecture Classeur Matis : jamais ecrit dans le suivi. */
let consoReelle = null;   /* { lueLe, fichiers: [], parArticle: { ART: { qtySemaine, lignes: [] } } } */
let planSource = "theo";  /* "theo" | "reel" */

function consoDepuisFeuille(nomFeuille, cells){
  /* parse une feuille « Pareto conso » : sections EMAG n / PCI n / HESSAPP,
     articles en dessous, quantites en colonne B. Rend { article: { qtySemaine,
     lignes:Set } } ou null si la feuille n'est pas une conso quantifiee. */
  if(!/pareto/i.test(nomFeuille || "") || !/conso/i.test(nomFeuille || "")) return null;
  const lignesNum = [...new Set(Object.keys(cells).map(r => parseInt(r.replace(/\\D/g, ""), 10)))].sort((a, b) => a - b);
  let enteteQte = false;
  for(const rn of lignesNum.slice(0, 4)){
    const h = cells["A" + rn];
    if(typeof h === "string" && /somme de qt/i.test(h) ) enteteQte = true;
  }
  if(!enteteQte) return null;   /* un pareto de COUT ne doit jamais passer pour des quantites */
  let section = null;
  const out = {};
  for(const rn of lignesNum){
    const a = cells["A" + rn], b = cells["B" + rn];
    if(typeof a !== "string") continue;
    const label = a.trim();
    if(/^total g/i.test(label)){ section = null; continue; }
    if(/(somme de qt|etiquettes de lignes|\\u00e9tiquettes de lignes)/i.test(label)) continue;
    const m = label.match(/^(EMAG\\s*\\d|PCI\\s*\\d|HESSAP\\w*)$/i);
    if(m && typeof b === "number"){ section = m[1].toUpperCase().replace(/\\s+/g, " "); continue; }
    if(section && typeof b === "number" && b > 0){
      const art = label.toUpperCase().replace(/\\s+/g, " ");
      out[art] = out[art] || { qtySemaine: 0, lignes: new Set() };
      out[art].qtySemaine += b;
      out[art].lignes.add(section);
    }
  }
  return Object.keys(out).length ? out : null;
}

/* lit UN classeur : toutes les feuilles, fusionne les sections Pareto conso */
async function consoLireClasseur(file){
  const entries = await _zipOpen(file);
  const shared = await _xlSharedStrings(entries);
  const map = await _xlSheetMap(entries);
  const parArticle = {};
  const feuillesLues = [];
  for(const nom of Object.keys(map)){
    if(!entries[map[nom]]) continue;
    const xml = new TextDecoder("utf-8").decode(await _zipRead(entries[map[nom]]));
    const lu = consoDepuisFeuille(nom, _xlCells(xml, shared));
    if(!lu) continue;
    feuillesLues.push(nom);
    for(const [art, v] of Object.entries(lu)){
      const e = parArticle[art] = parArticle[art] || { qtySemaine: 0, lignes: new Set() };
      e.qtySemaine += v.qtySemaine;
      v.lignes.forEach(x => e.lignes.add(x));
    }
  }
  return { fichier: file.name, feuilles: feuillesLues, parArticle };
}

const PLAN_ETATS = [''')

# ── 2. planLignes : le basculeur dans le calcul ──────────────────────────────
rep('''function planLignes(){
  const d = plaquettesCommunes();
  const parMabec = {};
  plan.forEach(p => { parMabec[p.mabec] = p; });
  return d.groupes.map(g => {
    const art = catalogue.find(a => a.mabec === g.mabec && a.prix !== "" && a.prix > 0);
    const prixA = art ? art.prix : (g.usages[0] ? g.usages[0].prix : 0);
    const piecesAn = prixA > 0 ? g.coutAnnuel / prixA : 0;''',
'''function planLignes(){
  const d = plaquettesCommunes();
  const parMabec = {};
  plan.forEach(p => { parMabec[p.mabec] = p; });
  const reel = (planSource === "reel") && consoReelle && consoReelle.parArticle;
  return d.groupes.map(g => {
    const art = catalogue.find(a => a.mabec === g.mabec && a.prix !== "" && a.prix > 0);
    const prixA = art ? art.prix : (g.usages[0] ? g.usages[0].prix : 0);
    const piecesAnTheo = prixA > 0 ? g.coutAnnuel / prixA : 0;
    /* v4.88 — le basculeur : en mode REEL, la consommation vient des feuilles
       Pareto conso des classeurs (qty semaine x 52). Un article sans donnee
       reelle n'est pas complete en silence : il perd son gain (null). */
    const conso = reel ? consoReelle.parArticle[g.mabec] : null;
    const sourceConso = reel ? (conso ? "reelle" : "sans") : "theo";
    const piecesAn = reel ? (conso ? conso.qtySemaine * 52 : 0) : piecesAnTheo;''')

rep('''    const gain = (actif && ciblePrix !== "" && ciblePrix !== null && prixA > 0)
      ? piecesAn * (prixA - Number(ciblePrix)) : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel,
             piecesAn, cibleIso, ciblePrix, etat: p.etat || "", actif, gain, auto: !!sugg };''',
'''    const gain = (actif && ciblePrix !== "" && ciblePrix !== null && prixA > 0 && sourceConso !== "sans")
      ? piecesAn * (prixA - Number(ciblePrix)) : null;
    return { mabec: g.mabec, isos: [...g.isos], prixA, coutAnnuel: g.coutAnnuel,
             piecesAn, piecesAnTheo, sourceConso, cibleIso, ciblePrix, etat: p.etat || "", actif, gain, auto: !!sugg };''')

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch A applique : parseur + etat + basculeur dans planLignes")
