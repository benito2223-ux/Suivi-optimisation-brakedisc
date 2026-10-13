# -*- coding: utf-8 -*-
"""Patch v4.84.0 : export Excel (CSV-FR) + plein ecran du simulateur."""

s = open('bilan_economique.html', encoding='utf-8').read()

# 1. simulCSV (pure, testable) + les deux handlers, poses avant simulHTML
av = "function simulHTML(){"
fonctions = '''/* v4.83/4.84 — l'export : CSV-FR (BOM + sep=; + decimales a virgule) — Excel
   francais l'ouvre sans avertissement, et la regle maison tient : zero SDK.
   PURE : la donnee, le taux et les articles inclus passent en argument —
   testable hors DOM. La chaine commence par le BOM ; la ligne sep=; force le
   separateur quelle que soit la configuration d'Excel. */
function simulCSV(d, tauxPct, inclus){
  const num = v => String(Math.round(v * 10000) / 10000).replace(".", ",");
  const cell = v => /[";\\r\\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v);
  const plagePrix = g => {
    const mn = Math.min(...g.usages.map(u => u.prix)), mx = Math.max(...g.usages.map(u => u.prix));
    return mn === mx ? num(mn) : num(mn) + " a " + num(mx);
  };
  const L = [];
  L.push("sep=;");
  L.push("Simulation prix plaquettes - " + new Date().toLocaleDateString("fr-FR"));
  L.push("Taux de baisse applique;" + String(tauxPct).replace(".", ",") + " %");
  L.push("");
  L.push("Article (MABEC);Libelles ISO;Usages;Lignes;Prix constates (EUR);Cout annuel (EUR);Economie annuelle (EUR)");
  let inclu = 0;
  d.groupes.forEach(g => {
    const actif = !inclus.size || inclus.has(g.mabec);
    const ec = actif ? g.coutAnnuel * tauxPct / 100 : 0;
    inclu += ec;
    L.push([g.mabec, [...g.isos].join(" | "), g.usages.length,
            [...new Set(g.usages.map(u => u.ligne))].join(" | "),
            plagePrix(g), num(g.coutAnnuel), num(ec)].map(cell).join(";"));
  });
  L.push(["TOTAL", "", "", "", "", num(d.totalAnnuel), num(inclu)].map(cell).join(";"));
  L.push("");
  L.push("Budget outillage annuel par reference");
  L.push("Ligne;Reference;Volume annuel;Cout annuel (EUR);% du budget");
  d.parReference.forEach(x => L.push([x.ligne, x.ref, num(x.prod), num(x.coutAnnuel),
    num(d.totalAnnuel ? x.coutAnnuel / d.totalAnnuel * 100 : 0)].map(cell).join(";")));
  return "\\uFEFF" + L.join("\\r\\n");
}

function simulExporter(){
  const d = plaquettesCommunes();
  const taux = parseFloat(document.getElementById("simulTaux")?.value) || 0;
  const inclus = new Set(Array.from(document.querySelectorAll(".simul-inc"))
    .filter(cb => cb.checked).map(cb => cb.getAttribute("data-mabec")));
  const csv = simulCSV(d, taux, inclus);
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const t = new Date();
  const stamp = t.getFullYear() + String(t.getMonth() + 1).padStart(2, "0") + String(t.getDate()).padStart(2, "0")
              + "-" + String(t.getHours()).padStart(2, "0") + String(t.getMinutes()).padStart(2, "0");
  a.href = url;
  a.download = "Simulation_prix_plaquettes_" + stamp + ".csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

/* v4.84 — plein ecran : le panneau passe par-dessus tout (CSS maxi), et le
   mode natif est tente par-dessus (reunion projetee). ESC rend la main. */
function simulMaxi(){
  const p = document.getElementById("simulPanel");
  if(!p) return;
  const on = !p.classList.contains("simul-maxi");
  p.classList.toggle("simul-maxi", on);
  try{
    if(on && p.requestFullscreen) p.requestFullscreen().catch(() => {});
    else if(!on && document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(() => {});
  }catch(e){}
  const b = document.getElementById("simulMaxiBtn");
  if(b) b.textContent = on ? "\\u2922 Quitter le plein ecran" : "\\u26f6 Plein ecran";
}

function simulHTML(){'''
assert av in s, "ancre 1"
s = s.replace(av, fonctions, 1)

# 2. la barre d'actions dans simulHTML (au-dessus de la note)
av2 = '''  return `
    <div class="simul-note">SIMULATION'''
ap2 = '''  return `
    <div class="simul-actions">
      <button class="ghost small" id="simulExporterBtn" title="T\u00e9l\u00e9charge les deux tableaux en CSV \u2014 s'ouvre dans Excel">\u2935 Exporter Excel (CSV)</button>
      <button class="ghost small" id="simulMaxiBtn" title="Projection en r\u00e9union">\u26f6 Plein \u00e9cran</button>
    </div>
    <div class="simul-note">SIMULATION'''
assert av2 in s, "ancre 2"
s = s.replace(av2, ap2, 1)

# 3. le wiring dans renderSimul
av3 = '''  const taux = document.getElementById("simulTaux");
  if(taux) taux.addEventListener("input", simulRecalcul);
  wrap.querySelectorAll(".simul-inc").forEach(cb => cb.addEventListener("change", simulRecalcul));
  simulRecalcul();'''
ap3 = '''  const taux = document.getElementById("simulTaux");
  if(taux) taux.addEventListener("input", simulRecalcul);
  wrap.querySelectorAll(".simul-inc").forEach(cb => cb.addEventListener("change", simulRecalcul));
  const ex = document.getElementById("simulExporterBtn");
  if(ex) ex.addEventListener("click", simulExporter);
  const mx = document.getElementById("simulMaxiBtn");
  if(mx) mx.addEventListener("click", simulMaxi);
  simulRecalcul();'''
assert av3 in s, "ancre 3"
s = s.replace(av3, ap3, 1)

# 4. le CSS complet du simulateur — ACCROC ASSUME : le bloc 4.83 n'avait JAMAIS
#    ete insere (garde conditionnel trop malin, insertion sautee en silence).
#    Insertion inconditionnelle devant le premier </style> (le style principal),
#    garde par une porte hors-suite dans le harnais.
av4 = ".simul-note {"
ap4 = '''/* v4.83/4.84 — le simulateur de baisse de prix (bloc CSS complet) */
.simul-note { background:#eef4fb; border:1px solid #cfe0f3; border-radius:4px; padding:9px 13px; font-size:13px; color:#1b5ea6; margin-bottom:14px; }
.simul-controles { display:flex; align-items:center; gap:10px; margin-bottom:12px; font-size:14px; }
.simul-controles input { width:80px; font-family:var(--font-mono); }
.simul-table { width:100%; border-collapse:collapse; font-size:13.5px; }
.simul-table th, .simul-table td { padding:7px 9px; border-bottom:1px solid #e4e6ea; text-align:left; }
.simul-table th { font-size:12px; color:#666; font-weight:600; text-transform:uppercase; letter-spacing:.03em; }
.simul-table td.mono, .simul-table tfoot td { font-family:var(--font-mono); }
.simul-table tfoot td { font-weight:600; border-top:2px solid #d6d9de; }
.simul-actions { display:flex; gap:8px; margin-bottom:10px; }
.simul-resultat { margin-top:16px; padding:13px 16px; background:#f0f7ee; border:1px solid #cfe3c8; border-radius:4px; font-size:15px; }
#simulPanel.simul-maxi { position:fixed; inset:0; max-width:none; width:100vw; height:100vh; max-height:none; z-index:260; overflow:auto; border-radius:0; margin:0; }
'''
if av4 not in s:
    i = s.find('</style>')
    assert i > 0, "aucun </style>"
    s = s[:i] + ap4 + s[i:]
    print("CSS simulateur insere (il manquait depuis la 4.83 !)")
else:
    print("CSS deja present, maxi seul ajoute")
    s = s.replace(".simul-resultat {", ".simul-actions { display:flex; gap:8px; margin-bottom:10px; }\n#simulPanel.simul-maxi { position:fixed; inset:0; max-width:none; width:100vw; height:100vh; max-height:none; z-index:260; overflow:auto; border-radius:0; margin:0; }\n.simul-resultat {", 1)

# 5. REPARATION : la restauration par copie a rejoue une copie perimee — le
#    fichier porte encore l'ANCIEN test de porte (comptage, aveugle a la faute
#    cle-par-nom). On remet la porte honnete (attribution verifiee).
av_old = '''ok("simulateur : deux r\u00e9f\u00e9rences de M\u00caME NOM (deux lignes) restent deux lignes du budget \u2014 la cl\u00e9 est l'ID",
           d2.parReference.length, 3);'''
porte_bonne = '''ok("simulateur : deux r\u00e9f\u00e9rences de M\u00caME NOM (deux lignes) restent attribu\u00e9es \u00e0 CHACUNE des machines \u2014 la cl\u00e9 est l'ID, pas le nom",
           [d2.parReference.length, d2.parReference.filter(x => x.ref === "330x14").length,
            (d2.parReference.find(x => x.ligne === "PCI 4") || {}).prod,
            d2.parReference.find(x => x.ligne === "EMAG 2") === undefined],
           [3, 1, 2000, true]);'''
if av_old in s:
    s = s.replace(av_old, porte_bonne, 1)
    print("porte honnete remise (la copie perimee avait rendu l'ancienne)")
else:
    print("porte deja honnete, rien a faire")
assert porte_bonne in s, "la porte honnete doit exister"

# 5 bis. tests : la porte CSV (contenu, BOM, sep, decimales a virgule)
av5 = '''           [3, 1, 2000, true]);'''
ap5 = av5 + '''
        /* v4.84 — l'export : un CSV qu'Excel FR ouvre SANS avertissement ni
           colonnes cass\u00e9es : BOM, sep=; en premiere ligne, decimales a virgule,
           les deux tableaux. La porte lit la chaine PURE, pas le DOM. */
        const csv = simulCSV(d, 10, new Set());
        const lignesCsv = csv.split("\\r\\n");
        ok("export simulateur : BOM + sep=; en t\u00eate \u2014 Excel FR ouvre sans avertissement",
           [csv.charCodeAt(0), lignesCsv[0], lignesCsv[1].indexOf("Simulation")],
           [65279, "sep=;", 0]);
        ok("export simulateur : d\u00e9cimales \u00e0 virgule (jamais de point) et s\u00e9parateur point-virgule partout",
           [csv.indexOf(".5 ") === -1 && csv.indexOf(";0.") === -1, (csv.match(/;/g) || []).length > 30],
           [true, true]);
        ok("export simulateur : les deux tableaux sont l\u00e0, avec TOTAL et \u00e9conomies",
           [lignesCsv.some(x => x.indexOf("Budget outillage annuel par reference") === 0),
            lignesCsv.some(x => x.indexOf("TOTAL;") === 0),
            lignesCsv.some(x => x.indexOf("Economie annuelle (EUR)") > -1)],
           [true, true, true]);'''
assert av5 in s, "ancre 5"
s = s.replace(av5, ap5, 1)

# 6. version + nouveautes
s = s.replace('const TOOL_VERSION = "4.83.1";', 'const TOOL_VERSION = "4.84.0";', 1)
ancien = '''const NOUVEAUTES = [
  { version:"4.83.1", date:"13/10/2026", points:['''
nouveau = '''const NOUVEAUTES = [
  { version:"4.84.0", date:"13/10/2026", points:[
    "<b>Le simulateur sort de l'\u00e9cran.</b> <b>\u2935 Exporter Excel (CSV)</b> : les deux tableaux (articles et budget par r\u00e9f\u00e9rence) partent dans un fichier qui s'ouvre dans Excel sans avertissement \u2014 taux et articles coch\u00e9s inclus. <b>\u26f6 Plein \u00e9cran</b> : le panneau passe par-dessus tout, pour projeter en r\u00e9union. \u00c9chap rend la main."
  ]},
  { version:"4.83.1", date:"13/10/2026", points:['''
assert ancien in s
s = s.replace(ancien, nouveau, 1)

open('bilan_economique.html', 'w', encoding='utf-8', newline='\n').write(s)
print("patch v4.84.0 applique")

# 7. harnais : API + porte hors-suite sur le CSS maxi
h = open('build_harness.py', encoding='utf-8').read()
if "simulCSV" not in h:
    h = h.replace('"getActiveLigne, preparerImportDepuis, axesActifs, reattribuerEssai, plaquettesCommunes, get lignes(){return lignes}, set lignes(v){lignes=v}, "',
                  '"getActiveLigne, preparerImportDepuis, axesActifs, reattribuerEssai, plaquettesCommunes, simulCSV, get lignes(){return lignes}, set lignes(v){lignes=v}, "')
porte_css = """  /* \u2500\u2500 v4.84 \u2014 LE SIMULATEUR EST STYLE ET PLEIN ECRAN, DANS LE CSS R\u00c9EL \u2500\u2500
     L'accroc : le bloc CSS de la 4.83 n'avait JAMAIS \u00e9t\u00e9 ins\u00e9r\u00e9 \u2014 un garde
     conditionnel trop malin avait saut\u00e9 l'insertion en silence, et le panneau
     a tourn\u00e9 deux versions non styl\u00e9 (4.83.0 et 4.83.1, les deux domaines).
     La porte lit le fichier r\u00e9el : les classes du simulateur EXISTENT. */
  (function simulCss(){
    const fs = require('fs');
    const html = fs.readFileSync('bilan_economique.html', 'utf8');
    const manquantes = ['.simul-note {', '.simul-table {', '.simul-resultat {', '#simulPanel.simul-maxi']
      .filter(sel => html.indexOf(sel) === -1);
    if(manquantes.length) r.echecs += manquantes.length;
    console.log((manquantes.length ? '  ECHEC ' : '  ok  ') + 'simulateur : CSS pr\u00e9sent dans le fichier r\u00e9el (' + (4 - manquantes.length) + '/4 r\u00e8gles)' + (manquantes.length ? ' \u2014 MANQUANT : ' + manquantes.join(', ') : ''));
  })();
"""
ancre_g = """  /* \u2500\u2500 v4.82 \u2014 LES DATES DE SAISIE SONT BORN\u00c9ES"""
if ancre_g in h:
    h = h.replace(ancre_g, porte_css + ancre_g, 1)
    print("porte CSS + API ajoutees au harnais")
else:
    print("!! ancre gate harnais introuvable")
open('build_harness.py', 'w', encoding='utf-8').write(h)
