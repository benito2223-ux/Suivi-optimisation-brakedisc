# -*- coding: utf-8 -*-
"""Patch v4.85.0 partie B : remplace-branch catalogue + fonctions pures + panneau + porte + tests."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()

# ── 1. branche « remplace » : le fichier recu fait autorite ─────────────────
av = '''    // le fichier reçu fait autorité : ses specs usine et sa note de synchro remplacent les locales
    specsUsine = normaliserSpecsUsine(parsed.specsUsine);
    synchroNote = parsed.synchroNote || null;'''
ap = '''    // le fichier reçu fait autorité : ses specs usine et sa note de synchro remplacent les locales
    specsUsine = normaliserSpecsUsine(parsed.specsUsine);
    synchroNote = parsed.synchroNote || null;
    catalogue = (parsed.catalogue || []).map(normalizeArticleCat);'''
assert av in s, "ancre remplace"
s = s.replace(av, ap, 1)

# ── 2. les fonctions pures + le panneau, poses avant renderSimul ────────────
av2 = "function renderSimul(){"
bloc = '''/* ═══ v4.85 — LE CATALOGUE PLAQUETTES : socle, seed, propagation, CSV ═══════
   La vérité prix/article : une ligne = UN MABEC = UN prix (décision Benjamin —
   Matis vérifie le fichier ; 209 560 = 38 €). Le fichier d'échange est un CSV
   standalone édité dans Excel. La propagation aux logements se fait AVEC
   rapport et consentement — jamais en silence (§3.2). */

function catalogueSeed(){
  /* regroupe TOUS les logements de l'outil par MABEC : le prix retenu est le
     plus FRÉQUENT (à égalité, le plus élevé — décision Benjamin pour 209 560),
     et chaque divergence est signalée, pas aplatie. Les ISO vus se cumulent. */
  const parMabec = {};
  lignes.forEach(l => (l.references || []).forEach(r => (r.ops || []).forEach(o =>
    (o.scenarios || []).forEach(sc => (sc.outils || []).forEach(ou => (ou.logements || []).forEach(g => {
      const mabec = String(g.codeArticle || g.mabec || "").trim().toUpperCase();
      const prix = parseFloat(g.prix);
      if(!mabec || isNaN(prix) || prix <= 0) return;
      const e = parMabec[mabec] = parMabec[mabec] || { mabec, iso: new Set(), prixVus: {} };
      if(String(g.ref || "").trim()) e.iso.add(String(g.ref).trim());
      e.prixVus[prix] = (e.prixVus[prix] || 0) + 1;
    }))))));
  return Object.values(parMabec).map(e => {
    const entrees = Object.entries(e.prixVus);
    entrees.sort((a, b) => (b[1] - a[1]) || (b[0] - a[0]));
    const prix = Number(entrees[0][0]);
    const divergent = entrees.length > 1;
    return normalizeArticleCat({ mabec: e.mabec, iso: [...e.iso].join(" | "),
      prix, aretes: "", ddv: "", divergent,
      prixVus: entrees.map(e2 => Number(e2[0])) });
  }).sort((a, b) => a.mabec.localeCompare(b.mabec));
}

function catalogueAppliquer(cat){
  /* propage les prix du catalogue dans TOUS les logements correspondants.
     Rend le rapport : MABEC changés, logements touchés, avant/après. */
  const parMabec = {};
  (cat || catalogue).forEach(a => { if(a.prix !== "" && a.prix > 0) parMabec[a.mabec] = a.prix; });
  const rapport = { logementsTouches: 0, mabecs: [] };
  lignes.forEach(l => (l.references || []).forEach(r => (r.ops || []).forEach(o =>
    (o.scenarios || []).forEach(sc => (sc.outils || []).forEach(ou => (ou.logements || []).forEach(g => {
      const mabec = String(g.codeArticle || g.mabec || "").trim().toUpperCase();
      const nouveau = parMabec[mabec];
      if(nouveau === undefined) return;
      const avant = parseFloat(g.prix);
      if(!isNaN(avant) && Math.abs(avant - nouveau) < 1e-9) return;
      g.prix = nouveau;
      rapport.logementsTouches++;
      const deja = rapport.mabecs.find(x => x.mabec === mabec);
      if(deja) deja.n++;
      else rapport.mabecs.push({ mabec, avant, apres: nouveau, n: 1 });
    }))))));
  return rapport;
}

function catalogueCSV(cat){
  const num = v => String(v === "" || v == null ? "" : v).replace(".", ",");
  const cell = v => /[";\\r\\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v);
  const L = ["sep=;", "Catalogue plaquettes - " + new Date().toLocaleDateString("fr-FR"), "",
    "MABEC;Libelle ISO;Prix EUR;Aretes;DDV (pieces)"];
  (cat || catalogue).forEach(a => L.push([a.mabec, a.iso, num(a.prix), num(a.aretes), num(a.ddv)].map(cell).join(";")));
  return "\\uFEFF" + L.join("\\r\\n");
}

function catalogueDepuisCSV(texte){
  /* tolérant : BOM, ligne sep=; optionnelle, ; ou , en séparateur, décimales
     point ou virgule, en-têtes reconnus par mot-clé. Rend { cat, erreurs }. */
  const brut = String(texte || "").replace(/^\\uFEFF/, "").replace(/^sep=;\\r?\\n/i, "").replace(/^sep=,\\r?\\n/i, "");
  const lignesTxt = brut.split(/\\r?\\n/).filter(x => x.trim());
  if(!lignesTxt.length) return { cat: [], erreurs: ["Fichier vide."] };
  const sep = (lignesTxt[0].split(";").length >= lignesTxt[0].split(",").length) ? ";" : ",";
  const entetes = lignesTxt[0].split(sep).map(x => x.trim().toLowerCase());
  const col = cles => entetes.findIndex(h => cles.some(k => h.includes(k)));
  const iM = col(["mabec", "article"]), iI = col(["iso", "libell", "libellé"]), iP = col(["prix"]),
        iA = col(["ar\u00eate", "arete", "arête"]), iD = col(["ddv", "charni\u00e8", "dur\u00e9e", "duree"]);
  if(iM === -1 || iP === -1) return { cat: [], erreurs: ["Colonnes MABEC et Prix introuvables. En-t\u00eates attendus : MABEC ; Libelle ISO ; Prix EUR ; Aretes ; DDV (pieces)."] };
  const cat = [], erreurs = [];
  lignesTxt.slice(1).forEach((ligne, idx) => {
    const c = ligne.split(sep).map(x => x.trim());
    const mabec = (c[iM] || "").toUpperCase().replace(/\\s+/g, " ").trim();
    const prix = parseFloat(String(c[iP] || "").replace(",", "."));
    if(!mabec) return;
    if(isNaN(prix) || prix <= 0){ erreurs.push("Ligne " + (idx + 2) + " : prix illisible (" + (c[iP] || "vide") + ")"); return; }
    const n = v => { const f = parseFloat(String(v || "").replace(",", ".")); return isNaN(f) ? "" : f; };
    cat.push(normalizeArticleCat({ mabec, iso: iI > -1 ? (c[iI] || "") : "", prix,
      aretes: iA > -1 ? n(c[iA]) : "", ddv: iD > -1 ? n(c[iD]) : "" }));
  });
  if(!cat.length && !erreurs.length) erreurs.push("Aucune ligne exploitable.");
  return { cat, erreurs };
}

function catalogueRendu(){
  if(!catalogue.length) return `<p class="panel-hint">Le catalogue est vide. Trois fa\u00e7ons de le remplir : le <b>g\u00e9n\u00e9rer depuis l'outil</b> (un MABEC = un prix, le plus fr\u00e9quent, divergences signal\u00e9es), l'<b>importer d'un CSV</b> \u00e9dit\u00e9 dans Excel, ou les deux \u2014 g\u00e9n\u00e9rer, exporter, faire corriger par Matis, r\u00e9importer.</p>
    <div class="simul-actions">
      <button class="ghost small" id="catSeed">🌱 G\u00e9n\u00e9rer depuis l'outil</button>
      <label class="ghost small" for="catFichier" style="cursor:pointer;">\u2934 Importer un CSV\u2026</label>
      <input type="file" id="catFichier" accept=".csv,.txt" hidden>
    </div>`;
  return `
    <div class="simul-actions">
      <button class="primary small" id="catAppliquer" title="Propage les prix du catalogue dans tous les logements correspondants \u2014 avec rapport">\u2705 Appliquer les prix aux logements</button>
      <button class="ghost small" id="catExporter">\u2935 Exporter le CSV</button>
      <label class="ghost small" for="catFichier" style="cursor:pointer;">\u2934 Importer un CSV\u2026</label>
      <input type="file" id="catFichier" accept=".csv,.txt" hidden>
      <button class="ghost small" id="catSeed">🌱 Reg\u00e9n\u00e9rer depuis l'outil</button>
    </div>
    <p class="panel-hint">${catalogue.length} article(s). Un MABEC = un prix \u2014 la propagation remplace les prix des logements correspondants, avec rapport. <b>SIMULATION jusqu'\u00e0 \u00ab Appliquer \u00bb.</b></p>
    <table class="simul-table">
      <thead><tr><th>Article (MABEC)</th><th>Libell\u00e9s ISO vus</th><th>Prix</th></tr></thead>
      <tbody>${catalogue.map(a => `<tr>
        <td class="mono">${escapeAttr(a.mabec)}</td>
        <td style="font-size:12px; color:#888;">${escapeAttr(a.iso || "\u2014")}</td>
        <td class="mono">${a.prix !== "" ? fmt(a.prix, 2) + " \u20ac" : "\u2014"}${a.divergent ? ' <span style="color:#b45309;">(prix divergents dans l\'outil \u2014 Matis v\u00e9rifie)</span>' : ""}</td>
      </tr>`).join("")}</tbody>
    </table>`;
}

function renderCatalogue(){
  const wrap = document.getElementById("cataloguePanel");
  if(!wrap) return;
  wrap.innerHTML = `<h3>📚 Catalogue plaquettes \u2014 la v\u00e9rit\u00e9 prix/article</h3>` + catalogueRendu();
  const seed = document.getElementById("catSeed");
  if(seed) seed.addEventListener("click", () => {
    backupSnapshot("Catalogue : g\u00e9n\u00e9ration depuis l'outil");
    catalogue = catalogueSeed();
    saveData(); renderCatalogue();
  });
  const fich = document.getElementById("catFichier");
  if(fich) fich.addEventListener("change", () => {
    const f = fich.files[0];
    if(!f) return;
    const reader = new FileReader();
    reader.onload = () => {
      const { cat, erreurs } = catalogueDepuisCSV(reader.result);
      if(erreurs.length){ dialogueAlerte(erreurs.join("<br>"), "Import catalogue"); return; }
      backupSnapshot("Catalogue : import CSV");
      const parMabec = {};
      catalogue.forEach(a => { parMabec[a.mabec] = a; });
      cat.forEach(a => { parMabec[a.mabec] = a; });
      catalogue = Object.values(parMabec).map(normalizeArticleCat);
      saveData(); renderCatalogue();
    };
    reader.readAsText(f, "utf-8");
  });
  const exp = document.getElementById("catExporter");
  if(exp) exp.addEventListener("click", () => {
    const blob = new Blob([catalogueCSV()], { type: "text/csv;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = "Catalogue_plaquettes.csv";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });
  const appl = document.getElementById("catAppliquer");
  if(appl) appl.addEventListener("click", () => {
    const avant = JSON.stringify(catalogue);
    const rapport = catalogueAppliquer();
    if(!rapport.logementsTouches){ dialogueAlerte("Tous les logements correspondants portent d\u00e9j\u00e0 le prix du catalogue.", "Rien \u00e0 mettre \u00e0 jour"); return; }
    backupSnapshot("Catalogue : propagation des prix");
    saveData(); render();
    dialogueAlerte(`<b>${rapport.logementsTouches} logement(s) mis(s) \u00e0 jour.</b><br>` +
      rapport.mabecs.slice(0, 12).map(x => `${escapeAttr(x.mabec)} : ${escapeAttr(String(x.avant))} \u2192 ${escapeAttr(String(x.apres))} \u20ac (${x.n})`).join("<br>") +
      (rapport.mabecs.length > 12 ? "<br>\u2026" : ""), "Prix propag\u00e9s");
  });
}
function ouvrirCatalogue(){
  fermerPanneaux();
  ouvrirPanneau("cataloguePanel");
  renderCatalogue();
}

function renderSimul(){'''
assert av2 in s, "ancre 2"
s = s.replace(av2, bloc, 1)

# ── 3. conteneur + bouton + wiring ──────────────────────────────────────────
av3 = '<div class="panel panel-large" id="simulPanel" hidden></div>'
assert av3 in s, "ancre 3"
s = s.replace(av3, av3 + '\n  <div class="panel panel-large" id="cataloguePanel" hidden></div>', 1)

av4 = '''      <button class="primary small" id="pfSimul" title="Que vaut une baisse de prix sur les plaquettes utilis\u00e9es par plusieurs productions ? \u00c9conomie annuelle \u20ac et % \u2014 SIMULATION, rien n'\u00e9crit">💰 Simulateur prix</button>'''
ap4 = av4 + '''
      <button class="primary small" id="pfCatalogue" title="La v\u00e9rit\u00e9 prix/article : un MABEC = un prix. Export/import CSV, propagation aux logements avec rapport">📚 Catalogue</button>'''
assert av4 in s, "ancre 4"
s = s.replace(av4, ap4, 1)

av5 = '''  const cSimul = document.getElementById("pfSimul");
  if(cSimul) cSimul.addEventListener("click", ouvrirSimul);'''
ap5 = '''  const cSimul = document.getElementById("pfSimul");
  if(cSimul) cSimul.addEventListener("click", ouvrirSimul);
  const cCat = document.getElementById("pfCatalogue");
  if(cCat) cCat.addEventListener("click", ouvrirCatalogue);'''
assert av5 in s, "ancre 5"
s = s.replace(av5, ap5, 1)

# ── 4. porte de clic ─────────────────────────────────────────────────────────
av6 = '''  { porte:"\u21c4 R\u00e9attribuer un essai", fns:["reattribuerEssai"] },'''
ap6 = av6 + '''
  { porte:"📚 Catalogue (accueil)", fns:["ouvrirCatalogue", "renderCatalogue", "catalogueSeed", "catalogueAppliquer", "catalogueCSV", "catalogueDepuisCSV"] },'''
assert av6 in s, "ancre 6"
s = s.replace(av6, ap6, 1)

# ── 5. version + nouveautes ──────────────────────────────────────────────────
s = s.replace('const TOOL_VERSION = "4.84.0";', 'const TOOL_VERSION = "4.85.0";', 1)
av7 = '''const NOUVEAUTES = [
  { version:"4.84.0", date:"13/10/2026", points:['''
ap7 = '''const NOUVEAUTES = [
  { version:"4.85.0", date:"13/10/2026", points:[
    "<b>📚 Le catalogue plaquettes.</b> La v\u00e9rit\u00e9 prix/article : un MABEC = un prix. G\u00e9n\u00e9rez-le depuis l'outil (divergences signal\u00e9es \u00e0 faire v\u00e9rifier par Matis), exportez-le en CSV pour l'\u00e9diter dans Excel, r\u00e9importez-le quand les prix bougent \u2014 puis <b>\u2705 Appliquez</b> : chaque logement concern\u00e9 est mis \u00e0 jour, avec le rapport de ce qui a chang\u00e9."
  ]},
  { version:"4.84.0", date:"13/10/2026", points:['''
assert av7 in s, "ancre 7"
s = s.replace(av7, ap7, 1)

open('bilan_economique.html', 'w', encoding='utf-8', newline='').write(s)
print("patch B applique : remplace + fonctions + panneau + porte + version")
