# -*- coding: utf-8 -*-
"""Patch v4.52 (2/2) : missionA4HTML + CSS d'impression + version."""
p = "bilan_economique.html"
s = open(p, encoding="utf-8").read()

# ── missionA4HTML : construit le contenu de l'A4 Mission (toute l'usine) ──
# inséré juste avant le filtre du tableau de bord (contexte global dispo)
avant = """/* Filtre du tableau de bord (v4.1) : null = tous les scenarios, sinon l'id d'un projet --"""
apres = """/* ── v4.52 — A4 MISSION : le livrable hiérarchie, imprimable ─────────────────
   Une page : qui pilote, qui accompagne, ce qui est GAGNÉ (acté), ce qui est EN COURS,
   le plan (les machines et leurs OPs), le protocole. Une seule source de vérité :
   gainPoste() par ligne et par poste — la carte, le bandeau et cet A4 disent la même
   chose, toujours (A3). Consomme les mêmes règles de périmètre que le reste (4.45). */
function missionA4HTML(){
  const postes = [];
  const essais = [];
  lignes.forEach(ligne => {
    postesLigne(ligne, LIGNES_SEPT_FONS).forEach(m => {
      const p = gainPoste(ligne, m.code, LIGNES_SEPT_FONS);
      if((p.refs || []).length) postes.push({ ligne, code: m.code, nom: m.nom || p.nom, p });
    });
    (ligne.references || []).forEach(r => r.ops.forEach(o => o.scenarios.forEach(sc => {
      (sc.essais || []).forEach(es => essais.push({
        ligne: ligne.nom, ref: r.nom, op: (o.nom || "").trim(),
        titre: es.titre || "Essai", date: es.date || "",
        statut: sc.statut, scId: sc.id, prels: (es.prelevements || []).length
      }));
    })));
  });
  if(!postes.length && !essais.length) return "";
  const acte = postes.reduce((a, x) => a + (x.p.gainActe || 0), 0);
  const projete = postes.reduce((a, x) => a + (x.p.gainProjete || 0), 0);
  essais.sort((a, b) => (b.date || "").localeCompare(a.date || ""));
  const pilote = (responsables || [])[0];
  const timeline = (essais.length ? essais.slice(0, 10) : []).map(e =>
    `<div class="m4-row"><span class="m4-date">${escapeAttr(e.date || "—")}</span>` +
    `<span class="m4-titre">${escapeAttr(e.ligne)} · ${escapeAttr(e.ref)} · ${escapeAttr(e.op)} — <b>${escapeAttr(e.titre)}</b> (${e.prels} prél.)</span>` +
    `<span class="m4-stat">${e.statut === "serie" ? "en série" : e.statut === "valide" ? "validé 5×" : "en cours"}</span></div>`).join("")
    || `<div class="m4-row"><span class="m4-date">—</span><span class="m4-titre">Aucun essai enregistré</span></div>`;
  const plan = postes.filter(x => (x.p.refs || []).length).map(x =>
    `<div class="m4-row"><span class="m4-date">${escapeAttr(x.ligne.nom)} · ${escapeAttr(x.code)}</span>` +
    `<span class="m4-titre">${x.p.gainActe > 0 ? "gain acté " + fmtEuroCourt(x.p.gainActe) + "/an" : ""}` +
    `${x.p.gainActe > 0 && x.p.gainProjete > 0 ? " · " : ""}` +
    `${x.p.gainProjete > 0 ? "potentiel " + fmtEuroCourt(x.p.gainProjete) + "/an" : ""}</span></div>`).join("")
    || `<div class="m4-row"><span class="m4-titre">Aucun poste chiffré — la carte atelier indique les postes à compléter</span></div>`;
  return `<div class="m4">
    <div class="m4-entete">
      <div><div class="m4-sur">Mission 2026/2027 — optimisation du coût de revient</div>
      <div class="m4-titre2">Pilote : Matis Hernu · Partenaire outillage : SPK by CeramTec (Benjamin Rouquette)</div></div>
      <div class="m4-date2">${new Date().toLocaleDateString("fr-FR")}</div>
    </div>
    <div class="m4-blocs">
      <div class="m4-bloc ok"><div class="n">${fmtEuroCourt(acte)}/an</div><div class="l">Gains ACTÉS — passés en production</div></div>
      <div class="m4-bloc encours"><div class="n">${fmtEuroCourt(projete)}/an</div><div class="l">EN COURS — validés ou en essai</div></div>
    </div>
    <h4 class="m4-h">Essais — les plus récents</h4>
    ${timeline}
    <h4 class="m4-h">Le plan — poste par poste (rendement : gains annuels)</h4>
    ${plan}
    <div class="m4-proto">Méthode : tout essai concluant est répété 5× ; validé 5× et viable économiquement, il passe en production. Chaque gain est comparé à périmètre identique (référence contre référence).</div>
  </div>`;
}

/* Filtre du tableau de bord (v4.1) : null = tous les scenarios, sinon l'id d'un projet --"""
assert s.count(avant) == 1, "missionA4HTML"
s = s.replace(avant, apres)

# ── CSS d'impression A4 Mission (en fin de feuille) ──
avant = "</style>\n</head>" if "</style>\n</head>" in s else None
import re
dernier = s.rfind("</style>")
apres_css = """
<style>
/* ── v4.52 — A4 Mission : à l'impression, seule la mission s'affiche ── */
#missionA4{ display:none; }
@media print{
  body.print-mission > *{ display:none !important; }
  body.print-mission > #missionA4{ display:block !important; }
  .m4{ font-family:'Public Sans',Arial,sans-serif; color:#111; }
  .m4-entete{ display:flex; justify-content:space-between; align-items:flex-end; border-bottom:3px solid #1B5EA6; padding-bottom:8px; margin-bottom:14px; }
  .m4-sur{ font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:#1B5EA6; font-weight:600; }
  .m4-titre2{ font-family:'Public Sans',Arial,sans-serif; font-size:12px; color:#333; margin-top:3px; }
  .m4-date2{ font-family:'IBM Plex Mono',monospace; font-size:10px; color:#555; }
  .m4-blocs{ display:flex; gap:12px; margin-bottom:14px; }
  .m4-bloc{ flex:1; border-radius:6px; padding:10px 14px; border:2px solid #1a7a3f; background:#edf7f1; }
  .m4-bloc.encours{ border-color:#b45309; background:#fdf6ec; }
  .m4-bloc .n{ font-family:'Manrope','Open Sans',Arial,sans-serif; font-weight:700; font-size:22px; color:#111; }
  .m4-bloc .l{ font-size:10.5px; color:#444; text-transform:uppercase; letter-spacing:.04em; }
  .m4-h{ font-family:'IBM Plex Mono',monospace; font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:#555; margin:14px 0 6px; }
  .m4-row{ display:flex; gap:10px; align-items:baseline; font-size:11.5px; padding:4px 0; border-bottom:1px solid #eee; }
  .m4-date{ font-family:'IBM Plex Mono',monospace; color:#555; min-width:78px; }
  .m4-titre{ flex:1; color:#222; }
  .m4-stat{ font-family:'IBM Plex Mono',monospace; font-size:10px; text-transform:uppercase; color:#1a7a3f; }
}
</style>
</head>"""
idx = s.find("</head>")
assert idx > 0
s = s[:idx] + apres_css + s[idx + len("</head>"):]

# ── version + NOUVEAUTES ──
s = s.replace('const TOOL_VERSION = "4.50.0";', 'const TOOL_VERSION = "4.52.0";')
avant = 'const NOUVEAUTES = [\n  { version:"4.50.0", date:"29/09/2026", points:['
apres = '''const NOUVEAUTES = [
  { version:"4.52.0", date:"29/09/2026", points:[
    "<b>L'A4 Mission — le livrable hiérarchie.</b> Un imprimable qui raconte la démarche : les gains ACTÉS en production, les gains EN COURS (validés ou en essai), la timeline des essais récents avec leur statut, et le plan poste par poste. Bouton « 🖨 A4 Mission » dans la carte atelier — même source de vérité que la carte (jamais de chiffre divergent)."
  ]},
  { version:"4.50.0", date:"29/09/2026", points:['''
assert s.count(avant) == 1, "NOUVEAUTES"
s = s.replace(avant, apres)

open(p, "w", encoding="utf-8", newline="\n").write(s)
print("4.52 missionA4 + CSS OK")
