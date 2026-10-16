# -*- coding: utf-8 -*-
"""Patch v4.53 (3) : UI livraisons (créer/lister/imprimer/supprimer) + tests + version."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ── 1. creerLivraison + imprimer + section UI dans renderCarte ──
# insérer les fonctions après ouvrirCarte
avant = """/* l'entrée : le bouton de la barre d'outils ouvre la carte (v4.51.2) */
function ouvrirCarte(){ renderCarte(); ouvrirPanneau("cartePanel"); }"""
apres = """/* l'entrée : le bouton de la barre d'outils ouvre la carte (v4.51.2) */
function ouvrirCarte(){ renderCarte(); ouvrirPanneau("cartePanel"); }

/* ── v4.53 — LIVRAISONS : l'objet que la hiérarchie lit (décision 3) ──────────
   Une livraison = un instantané FIGÉ des gains du plan, daté et nommé. Elle ne se
   recalcule jamais : les chiffres sont copiés à la création — c'est le document que
   Matis montre à sa hiérarchie (« livré en date du…, X €/an actés »). Source unique :
   creerLivraison consomme cartePostes(), exactement comme l'affichage de la carte. */
function creerLivraison(nom){
  const postes = cartePostes().filter(t => t.etat !== "opportunite");
  const plan = postes.map(t => ({
    ligne: t.ligne.nom || "", code: t.code, nom: t.nomMachine || t.code,
    refDominante: (t.poste.refDominante && (t.poste.refDominante.ref ? t.poste.refDominante.ref.nom : t.poste.refDominante.nom)) || "",
    gainActe: t.poste.gainActe || 0, gainProjete: t.poste.gainProjete || 0, etat: t.etat
  }));
  const cibles = lignes.flatMap(l => l.references.map(r => ({ ref: r.nom, cible: r.cibleCPP || null }))).filter(x => x.cible);
  return normalizeLivraison({
    id: "lv" + Date.now().toString(36), nom: nom || "Livraison",
    date: new Date().toISOString().slice(0, 10), creePar: auteurNom || "",
    gainsActes: plan.reduce((a, x) => a + x.gainActe, 0),
    gainsProjetes: plan.reduce((a, x) => a + x.gainProjete, 0),
    plan, cibles,
    essais: postes.reduce((a, t) => a + ((t.poste.essaiOuvert) ? 1 : 0), 0)
  });
}
function livraisonImpressionHTML(l){
  const eur = v => fmtEuroCourt(Math.abs(v || 0)) + "/an";
  const planRows = (l.plan || []).map(x =>
    `<div class="m4-row"><span class="m4-date">${escapeAttr(x.ligne)}</span>` +
    `<span class="m4-titre">${escapeAttr(x.nom)} — ${escapeAttr(x.refDominante || "")}</span>` +
    `<span class="m4-stat">${x.gainActe > 0 ? "acté " + eur(x.gainActe) : x.gainProjete > 0 ? "en cours " + eur(x.gainProjete) : "à chiffrer"}</span></div>`).join("");
  const cibles = (l.cibles || []).map(c => escapeAttr(c.ref) + " " + fmt(c.cible, 3) + " €").join(" · ");
  return `<div class="m4">
    <div class="m4-entete">
      <div><div class="m4-sur">Livraison — ${escapeAttr(l.nom)}</div>
      <div class="m4-titre2">Suivi d'optimisation SPK by CeramTec × Sept Fons — pilote : Matis Hernu · partenaire outillage : SPK by CeramTec (Benjamin Rouquette)</div></div>
      <div class="m4-date2">Livré le ${escapeAttr(l.date || "")} — figé, ne se recalcule pas</div>
    </div>
    <div class="m4-blocs">
      <div class="m4-bloc ok"><div class="n">${eur(l.gainsActes)}</div><div class="l">Gains ACTÉS — en production</div></div>
      <div class="m4-bloc encours"><div class="n">${eur(l.gainsProjetes)}</div><div class="l">EN COURS — validés ou en essai</div></div>
    </div>
    <h4 class="m4-h">Le plan livré — poste par poste</h4>
    ${planRows || `<div class="m4-row"><span class="m4-titre">aucun poste</span></div>`}
    <h4 class="m4-h">Cibles du site</h4>
    <div class="m4-row"><span class="m4-titre">${cibles || "non renseignées"}</span></div>
    <div class="m4-proto">${escapeAttr(l.protocole || "")}</div>
  </div>`;
}
function livraisonsSectionHTML(){
  const rows = (livraisons || []).slice().sort((a, b) => (b.date || "").localeCompare(a.date || "")).map(l =>
    `<div class="lv-row">
      <span class="lv-nom">📦 ${escapeAttr(l.nom)}</span>
      <span class="lv-date">${escapeAttr(l.date || "")} · ${l.creePar || "—"}</span>
      <span class="lv-gains">${l.gainsActes > 0 ? eurTxt(l.gainsActes) + " actés" : ""}${l.gainsActes > 0 && l.gainsProjetes > 0 ? " · " : ""}${l.gainsProjetes > 0 ? eurTxt(l.gainsProjetes) + " en cours" : ""}</span>
      <button class="ghost small lv-print" data-lv="${escapeAttr(l.id)}" title="Imprimer l'A4 de cette livraison">🖨</button>
      <button class="ghost small lv-del" data-lv="${escapeAttr(l.id)}" title="Supprimer cette livraison (les données des scénarios ne sont pas touchées)">🗑</button>
    </div>`).join("");
  return `<div class="lv-bloc">
    <div class="lv-tete">
      <b>📦 Livraisons — le dossier hiérarchie</b>
      <button class="primary small" id="lvCreer">📦 Nouvelle livraison — figer les gains du jour</button>
    </div>
    ${rows || `<p class="panel-hint">Aucune livraison : clique ci-dessus pour figer les gains du jour dans un document daté — celui que la hiérarchie lit.</p>`}
  </div>`;
}
function eurTxt(v){ return fmtEuroCourt(Math.abs(v || 0)) + "/an"; }

/* Filtre du tableau de bord (v4.1) : null = tous les scenarios, sinon l'id d'un projet --"""
assert s.count(avant) == 1, "ancre UI"
s = s.replace(avant, apres)

# ── 2. section livraisons dans renderCarte + wiring ──
avant = """    <div class="panel-actions"><button class="ghost" id="missionA4Btn">🖨 A4 Mission</button><button class="primary" id="carteClose">Fermer</button></div>"""
apres = """    ${livraisonsSectionHTML()}
    <div class="panel-actions"><button class="ghost" id="missionA4Btn">🖨 A4 Mission</button><button class="primary" id="carteClose">Fermer</button></div>"""
assert s.count(avant) == 1, "panneau actions"
s = s.replace(avant, apres)

avant = """  const mBtn = document.getElementById("missionA4Btn");"""
apres = """  /* v4.53 — livraisons : créer, imprimer, supprimer */
  const creer = document.getElementById("lvCreer");
  if(creer) creer.addEventListener("click", () => {
    const defaut = "Livraison 2026/2027 — " + new Date().toLocaleDateString("fr-FR");
    dialogueDemander("Nom de la livraison (elle fige les gains du jour et ne se recalcule plus) :", defaut, { titre: "Nouvelle livraison" }).then(nom => {
      if(nom === null) return;
      livraisons = (livraisons || []).concat([creerLivraison(String(nom).trim() || defaut)]);
      saveData(); renderCarte();
    });
  });
  wrap.querySelectorAll(".lv-print").forEach(b => b.addEventListener("click", () => {
    const l = (livraisons || []).find(x => x.id === b.getAttribute("data-lv"));
    if(!l) return;
    const el = document.getElementById("livraisonImpression") || document.body.appendChild(Object.assign(document.createElement("div"), { id: "livraisonImpression", hidden: true }));
    el.innerHTML = livraisonImpressionHTML(l);
    document.body.classList.add("print-livraison");
    const nettoie = () => { document.body.classList.remove("print-livraison"); window.removeEventListener("afterprint", nettoie); };
    window.addEventListener("afterprint", nettoie);
    window.print();
    setTimeout(nettoie, 2000);
  }));
  wrap.querySelectorAll(".lv-del").forEach(b => b.addEventListener("click", () => {
    const l = (livraisons || []).find(x => x.id === b.getAttribute("data-lv"));
    if(!l) return;
    dialogueConfirmer("Supprimer la livraison « " + (l.nom || "") + " » ?\\n\\nLes données des scénarios, essais et cibles ne sont pas touchées — seule la copie figée disparaît.",
      { titre: "Supprimer la livraison ?", okLabel: "Supprimer" }).then(ok => {
      if(!ok) return;
      livraisons = (livraisons || []).filter(x => x.id !== l.id);
      saveData(); renderCarte();
    });
  }));

  const mBtn = document.getElementById("missionA4Btn");"""
assert s.count(avant) == 1, "wiring missionA4Btn"
s = s.replace(avant, apres)

# ── 3. CSS livraisons + impression livraison (fin de feuille) ──
idx = s.rfind("</style>")
apres_css = """
<style>
/* ── v4.53 — livraisons : le dossier hiérarchie (bloc carte + impression A4) ── */
.lv-bloc{ margin-top:16px; border-top:2px solid var(--border); padding-top:12px; }
.lv-tete{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; margin-bottom:8px; }
.lv-tete b{ font-family:var(--font-disp); font-weight:700; font-size:14px; }
.lv-row{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:6px 2px; border-bottom:1px solid var(--border); font-size:12.5px; }
.lv-nom{ font-family:var(--font-disp); font-weight:700; color:var(--ink); flex:0 0 auto; }
.lv-date{ font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint); }
.lv-gains{ margin-left:auto; font-family:var(--font-mono); font-size:10.5px; color:var(--green); }
#livraisonImpression{ display:none; }
body.print-livraison > *{ display:none !important; }
body.print-livraison > #livraisonImpression{ display:block !important; }
body.print-livraison #livraisonImpression .m4{ font-family:'Public Sans',Arial,sans-serif; color:#111; }
body.print-livraison #livraisonImpression .m4-entete{ display:flex; justify-content:space-between; border-bottom:3px solid #1B5EA6; padding-bottom:8px; margin-bottom:14px; }
body.print-livraison #livraisonImpression .m4-sur{ font-family:'IBM Plex Mono',monospace; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#1B5EA6; font-weight:600; }
body.print-livraison #livraisonImpression .m4-titre2{ font-size:12px; color:#333; margin-top:4px; }
body.print-livraison #livraisonImpression .m4-date2{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:#555; }
body.print-livraison #livraisonImpression .m4-blocs{ display:flex; gap:12px; margin:14px 0; }
body.print-livraison #livraisonImpression .m4-bloc{ flex:1; border-radius:6px; padding:10px 14px; border:2px solid #1a7a3f; background:#edf7f1; }
body.print-livraison #livraisonImpression .m4-bloc.encours{ border-color:#b45309; background:#fdf6ec; }
body.print-livraison #livraisonImpression .m4-bloc .n{ font-family:'Manrope','Open Sans',Arial,sans-serif; font-weight:700; font-size:22px; }
body.print-livraison #livraisonImpression .m4-bloc .l{ font-size:10.5px; color:#444; text-transform:uppercase; }
body.print-livraison #livraisonImpression .m4-h{ font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:#555; margin:14px 0 6px; }
body.print-livraison #livraisonImpression .m4-row{ display:flex; gap:10px; font-size:11.5px; padding:4px 0; border-bottom:1px solid #eee; }
body.print-livraison #livraisonImpression .m4-date{ font-family:'IBM Plex Mono',monospace; min-width:80px; color:#555; }
body.print-livraison #livraisonImpression .m4-titre{ flex:1; color:#222; }
body.print-livraison #livraisonImpression .m4-stat{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:#1a7a3f; }
body.print-livraison #livraisonImpression .m4-proto{ font-size:10.5px; color:#555; margin-top:12px; border-top:1px solid #ccc; padding-top:8px; }
</style>
</head>"""
idx = s.find("</head>")
assert idx > 0
s = s[:idx] + apres_css + s[idx + len("</head>"):]

# ── 4. version ──
s = s.replace('const TOOL_VERSION = "4.52.0";', 'const TOOL_VERSION = "4.53.0";')

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("UI livraisons + impression OK")
