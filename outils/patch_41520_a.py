# -*- coding: utf-8 -*-
"""Tour 135 (4.152.0) — vue plaquette globale : usages par ISO + extrapolation à trois leviers.
Idempotent, écriture en TOUTE FIN."""
import io, re

P = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/bilan_economique.html"
src = io.open(P, "r", encoding="utf-8", newline="").read()
orig_len = len(src)
deja = []

def repl(s, old, new, label):
    for attempt in (old, old.replace("\n", "\r\n")):
        n = s.count(attempt)
        if n == 1:
            return s.replace(attempt, new)
        if n != 0:
            raise SystemExit("ANCRE '%s' : %d occurrences" % (label, n))
    raise SystemExit("ANCRE INTROUVABLE : %s" % label)

def sonde(motif, label):
    if motif in src:
        deja.append(label)
        return True
    return False

# ── A : fonctions pures + panneau + délégations ─────────────────────────────────
BLOC = r"""/* ═══ Tour 135 (4.152.0) — LA VUE PLAQUETTE GLOBALE ═════════════════════════════
   Spec SPEC_VUE_PLAQUETTE_GLOBALE_2026-11-10.md (décisions Benjamin) :
   · clé de regroupement = la DÉSIGNATION ISO (la plaquette physique), MABEC confondus ;
   · usagesPlaquette : où elle sert (scénario de production de chaque OP, règle 4.114 :
     série du jour sinon ★), avec plaquettes/an et coût annuel par usage ;
   · extrapoleGlobale : SIMULATION prospective à trois leviers cumulables — le prix en
     variable de départ, puis la charnière, puis le temps de cycle (chiffré seulement là
     où temps de coupe ET taux horaire existent ; sinon nommé « cycle non chiffré ») ;
   · un usage sans volume/prix/arêtes/charnière est LISTÉ avec ce qui manque, jamais
     compté pour 0 (constitution §5.6) ; le total porte l'étiquette SIMULATION et ne se
     mélange jamais aux gains actés/projetés (§3.4). */

function normIso(s){
  return String(s || "").trim().toUpperCase().replace(/\s+/g, " ");
}
/* le scénario de production d'une OP : la série du jour, sinon la ★, sinon la base
   excel (règle du bandeau 4.114 — la prod du jour, pas l'archive de comparaison). */
function scenarioProductionOp(op){
  const scs = (op && op.scenarios) || [];
  return scs.find(x => x.statut === "serie" && !x.baseline)
      || scs.find(x => x.baseline)
      || scs.find(x => /base excel/i.test(x.name || ""))
      || null;
}
/* tous les usages d'une plaquette (une désignation ISO, ou une liste — les lignes
   du Plan regroupent plusieurs ISO sous un même MABEC). Accepte string ou tableau. */
function usagesPlaquette(isos){
  const cible = new Set((Array.isArray(isos) ? isos : [isos]).map(normIso).filter(Boolean));
  const usages = [], exclus = [];
  (lignes || []).forEach(lg => (lg.references || []).forEach(rf => (rf.ops || []).forEach(op => {
    const prod = scenarioProductionOp(op);
    if(!prod) return;
    (prod.outils || []).forEach(o => (o.logements || []).forEach(l => {
      if(!cible.has(normIso(l.ref))) return;
      const vol = volumeAnnuel(rf, op.config);
      const prix = parseFloat(l.prix), ar = parseFloat(l.aretes), ch = parseFloat(l.charniere);
      const pAn = plaquettesParAn(l, vol);
      const manques = [];
      if(!(vol > 0)) manques.push("volume annuel");
      if(isNaN(prix) || !(prix > 0)) manques.push("prix");
      if(isNaN(ar) || !(ar > 0)) manques.push("arêtes");
      if(isNaN(ch) || !(ch > 0)) manques.push("charnière");
      const u = { ligne: lg.nom || "?", ligneId: lg.id, reference: rf.nom || "?",
        opCode: op.opCode || op.nom || "?", scenario: prod.name || "",
        outil: o.numero || "?", logement: l.nom || "?",
        mabec: l.codeArticle || l.mabec || "", designation: l.ref || "",
        prix: isNaN(prix) ? null : prix, aretes: isNaN(ar) ? null : ar, charniere: isNaN(ch) ? null : ch,
        tempsCoupe: parseFloat(l.tempsCoupe), tauxHoraire: parseFloat(lg.coutHoraire),
        volume: (vol > 0) ? vol : null, plaquettesAn: pAn,
        coutAnnuel: (pAn !== null && !isNaN(prix)) ? pAn * prix : null };
      if(manques.length) exclus.push({ usage: u, manques });
      else usages.push(u);
    }));
  })));
  usages.sort((a, b) => (b.coutAnnuel || 0) - (a.coutAnnuel || 0));
  return { usages, exclus, totalActuel: usages.reduce((a, u) => a + (u.coutAnnuel || 0), 0) };
}
/* la SIMULATION : ce que vaudrait la plaquette déployée au global, levier par levier.
   Prix (variable de départ) → charnière → temps de coupe. Le cycle n'est compté que là
   où temps de coupe et taux horaire existent : ailleurs il est NOMMÉ, jamais inventé. */
function extrapoleGlobale(uv, leviers){
  const lv = leviers || {};
  const prixL = parseFloat(lv.prix), charnL = parseFloat(lv.charniere), tempsL = parseFloat(lv.tempsCoupe);
  const uPrix = !isNaN(prixL) && prixL > 0;
  const uCharn = !isNaN(charnL) && charnL > 0;
  const uTemps = !isNaN(tempsL) && tempsL > 0;
  const usages = [], cyclesNonChiffres = [];
  uv.usages.forEach(u => {
    const prixSim = uPrix ? prixL : u.prix;
    const plqSim = uCharn ? u.volume / (u.aretes * charnL) : u.plaquettesAn;
    let coutSim = plqSim * prixSim;
    const lev = [];
    if(uPrix) lev.push("prix " + fmt(u.prix, 2) + " → " + fmt(prixL, 2) + " €");
    if(uCharn) lev.push("charnière " + fmt(u.charniere, 0) + " → " + fmt(charnL, 0) + " p");
    let cycleAn = null;
    if(uTemps){
      if(!isNaN(u.tempsCoupe) && u.tauxHoraire > 0){
        cycleAn = (u.tempsCoupe - tempsL) * (u.tauxHoraire / 3600) * u.volume;
        coutSim += cycleAn;
        lev.push("cycle " + fmt(u.tempsCoupe, 1) + " → " + fmt(tempsL, 1) + " s");
      } else {
        cyclesNonChiffres.push({ usage: u, raison: "cycle non chiffré (temps de coupe ou taux horaire manquant) — non compté pour cet usage" });
      }
    }
    usages.push(Object.assign({}, u, { coutSimule: coutSim, ecart: u.coutAnnuel - coutSim, cycleAn, leviers: lev }));
  });
  const totalSimule = usages.reduce((a, u) => a + u.coutSimule, 0);
  return { usages, cyclesNonChiffres, exclus: uv.exclus,
           totalActuel: uv.totalActuel, totalSimule, totalEcart: uv.totalActuel - totalSimule,
           leviersActifs: { prix: uPrix, charniere: uCharn, temps: uTemps } };
}
function extrapoleTotalHTML(ex){
  const nLev = ["prix", "charniere", "temps"].filter(k => ex.leviersActifs[k]).length;
  if(!nLev){
    return `<p class="panel-hint">Renseigne au moins un levier (prix, charnière ou temps de coupe) : le total « si déployée au global » se calcule à la frappe.</p>`;
  }
  const ecart = ex.totalEcart;
  return `<div style="border:1px dashed var(--border); border-radius:var(--radius-sm); padding:8px 10px; background:var(--surface);">
    <div style="font-size:12px; color:var(--ink-soft);">SIMULATION — si cette plaquette était déployée au global, à conditions égales · ${nLev} levier${nLev > 1 ? "s" : ""}</div>
    <div style="font-size:19px; font-weight:800; color:${ecart > 0 ? "var(--green)" : ecart < 0 ? "var(--red)" : "var(--ink)"};">${ecart >= 0 ? "−" : "+"}${fmtEuroCourt(Math.abs(Math.round(ecart)))}/an</div>
    <div style="font-size:12px; color:var(--ink-soft);">coût actuel ${fmtEuroCourt(Math.round(ex.totalActuel))}/an → simulé ${fmtEuroCourt(Math.round(ex.totalSimule))}/an · ${ex.usages.length} usage(s) chiffré(s)</div>
    ${ex.cyclesNonChiffres.length ? `<div style="font-size:12px; color:var(--amber);">${ex.cyclesNonChiffres.map(x => escapeAttr(x.usage.ligne + " · " + x.usage.opCode + " — " + x.raison)).join("<br>")}</div>` : ""}
    <div style="font-size:11px; color:var(--ink-faint);"> Simulation prospective : jamais additionnée aux gains actés ou projetés.</div>
  </div>`;
}
/* le panneau « Où sert cette plaquette ? » — table d'usages + trois leviers live.
   Ouvert depuis le Catalogue, le Plan de conversion et « Ailleurs dans l'usine ». */
function panneauUsagesHTML(isos, prefill){
  const pf = prefill || {};
  const isoListe = (Array.isArray(isos) ? isos : [isos]).filter(Boolean);
  const uv = usagesPlaquette(isoListe);
  const ex = extrapoleGlobale(uv, { prix: pf.prix || "", charniere: pf.charniere || "", tempsCoupe: pf.tempsCoupe || "" });
  const libelleDe = u => { const a = catalogue.find(x => normIso(x.iso) === normIso(u.designation)); return (a && a.libelle) || u.designation; };
  const rows = uv.usages.map(u => `<tr>
      <td><b>${escapeAttr(u.ligne)}</b><br><small>${escapeAttr(u.opCode)} · ${escapeAttr(u.outil)} · ${escapeAttr(u.logement)}</small></td>
      <td>${escapeAttr(u.reference)}</td>
      <td class="mono">${escapeAttr(u.mabec || "—")}<br><small>${escapeAttr(libelleDe(u))}</small></td>
      <td class="num">${fmt(u.plaquettesAn, 0)}</td>
      <td class="num">${fmt(u.prix, 2)} €</td>
      <td class="num">${escapeAttr(String(u.charniere))} p</td>
      <td class="num">${fmtEuroCourt(Math.round(u.coutAnnuel))}/an</td>
    </tr>`).join("");
  const exlus = uv.exclus.map(x => `<li>${escapeAttr(x.usage.ligne + " · " + x.usage.opCode + " · " + x.usage.reference)} — manque : ${escapeAttr(x.manques.join(", "))}</li>`).join("");
  return `<div data-extrapole="${escapeAttr(isoListe.join("|"))}">
    <p class="panel-hint">Tous les usages de <b>${escapeAttr(isoListe.join(" / "))}</b> dans l'usine — scénario de production de chaque OP. MABEC et désignation affichés pour chaque usage.</p>
    ${uv.usages.length ? `<table class="simul-table"><thead><tr><th>Ligne · OP · outil</th><th>Référence</th><th>Plaquette (MABEC + désignation)</th><th class="num">Plaquettes/an</th><th class="num">Prix</th><th class="num">Charnière</th><th class="num">Coût</th></tr></thead><tbody>${rows}</tbody></table>
      <p class="panel-hint">Coût actuel de cette plaquette, tous usages : <b>${fmtEuroCourt(Math.round(uv.totalActuel))}/an</b>.</p>`
      : `<p class="panel-hint">Aucun usage de cette plaquette dans les scénarios de production (elle n'existe que dans des essais, ou sa désignation n'est pas saisie).</p>`}
    ${exlus ? `<p class="panel-hint" style="color:var(--amber);">Usages non chiffrés (exclus du total, données à compléter) :</p><ul class="fusion-conflits">${exlus}</ul>` : ""}
    <div class="extrapole-lev" style="display:flex; gap:10px; flex-wrap:wrap; margin:10px 0 6px;">
      <label style="font-size:12px;">Prix cible (€) <input class="cg-input" type="number" step="0.1" min="0" data-lev="prix" value="${pf.prix ?? ""}" title="Levier de départ : le prix de la plaquette partout où elle sert."></label>
      <label style="font-size:12px;">Charnière cible (p/arête) <input class="cg-input" type="number" step="1" min="1" data-lev="charniere" value="${pf.charniere ?? ""}" title="La durée de vie cible remplace la visée de chaque usage (ex. le mesuré d'un essai validé)."></label>
      <label style="font-size:12px;">Temps de coupe cible (s) <input class="cg-input" type="number" step="0.1" min="0" data-lev="tempsCoupe" value="${pf.tempsCoupe ?? ""}" title="Chiffré seulement où le temps de coupe et le taux horaire de la ligne existent ; ailleurs nommé, jamais inventé."></label>
    </div>
    <div class="extrapole-out">${extrapoleTotalHTML(ex)}</div>
  </div>`;
}
/* ouverture depuis le Catalogue, le Plan et « Ailleurs dans l'usine » ; recalcul live */
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-usages-iso]");
  if(!b) return;
  const isos = String(b.getAttribute("data-usages-iso") || "").split("|").filter(Boolean);
  if(!isos.length) return;
  const pf = {};
  const ch = parseFloat(b.getAttribute("data-usages-charniere"));
  if(!isNaN(ch) && ch > 0) pf.charniere = ch;
  ouvrirDialogue({ titre: "Où sert cette plaquette ?", html: panneauUsagesHTML(isos, pf), sansAnnuler: true });
});
document.addEventListener("input", (e) => {
  if(!e.target.closest) return;
  const bloc = e.target.closest("[data-extrapole]");
  if(!bloc) return;
  const lire = (n) => { const el = bloc.querySelector('[data-lev="' + n + '"]'); return (el && el.value !== "") ? parseFloat(el.value) : ""; };
  const ex = extrapoleGlobale(usagesPlaquette(String(bloc.getAttribute("data-extrapole")).split("|")),
    { prix: lire("prix"), charniere: lire("charniere"), tempsCoupe: lire("tempsCoupe") });
  const out = bloc.querySelector(".extrapole-out");
  if(out) out.innerHTML = extrapoleTotalHTML(ex);
});

function logementBlocHTML(sc, o, l, showFrFa, showCycleDetail){"""
if not sonde("function usagesPlaquette(", "A"):
    src = repl(src, "function logementBlocHTML(sc, o, l, showFrFa, showCycleDetail){", BLOC, "A")

# ── B : le catalogue — « Où ? » sur chaque article ──────────────────────────────
if not sonde('data-usages-iso="${escapeAttr(a.iso || "")}"', "B"):
    src = repl(src,
"""        <td class="mono">${escapeAttr(a.mabec)}</td>""",
"""        <td class="mono">${escapeAttr(a.mabec)}${a.iso ? `<br><button type="button" class="ghost small" style="margin-top:3px;" data-usages-iso="${escapeAttr(a.iso)}" title="Où cette plaquette est utilisée dans l'usine (ligne, OP, quantité), et l'économie si elle était déployée au global">Où ?</button>` : ""}</td>""", "B")

# ── C : le Plan de conversion — « usages » par ligne d'article ──────────────────
if not sonde('data-usages-iso="${escapeAttr(l.isos.join("|"))}"', "C"):
    src = repl(src,
"""          <td style="font-size:11.5px; color:#888;">${l.isos.map(x => escapeAttr(x)).join("<br>")}</td>""",
"""          <td style="font-size:11.5px; color:#888;">${l.isos.map(x => escapeAttr(x)).join("<br>")}${l.isos.length ? `<br><button type="button" class="ghost small" style="margin-top:3px;" data-usages-iso="${escapeAttr(l.isos.join("|"))}" title="Où ces plaquettes sont utilisées dans l'usine, et l'économie si elles étaient déployées au global">usages</button>` : ""}</td>""", "C")

# ── D : « Ailleurs dans l'usine » — les plaquettes du scénario + extrapolation mesurée ─
if not sonde("Plaquettes de ce scénario — où servent-elles ailleurs", "D"):
    src = repl(src,
"""    ${sansVolume ? `<p class="dm-p">Volume annuel manquant sur ${sansVolume} poste${sansVolume > 1 ? "s" : ""} concerné${sansVolume > 1 ? "s" : ""} : non compté${sansVolume > 1 ? "s" : ""} dans l'estimation.</p>` : ""}
  </section>`;""",
"""    ${sansVolume ? `<p class="dm-p">Volume annuel manquant sur ${sansVolume} poste${sansVolume > 1 ? "s" : ""} concerné${sansVolume > 1 ? "s" : ""} : non compté${sansVolume > 1 ? "s" : ""} dans l'estimation.</p>` : ""}
    ${(() => { /* Tour 135 : les plaquettes du scénario — où servent-elles ailleurs ? */
      const isosSc = [];
      (sc && sc.outils || []).forEach(o => (o.logements || []).forEach(l => {
        const k = normIso(l.ref);
        if(k && !isosSc.some(x => normIso(x) === k)) isosSc.push(l.ref);
      }));
      if(!isosSc.length) return "";
      const cr = charniereReelle(sc);
      const crMin = (cr && cr.min > 0) ? cr.min : null;
      const boutons = isosSc.map(r => `<button type="button" class="ghost small" style="margin:2px 2px;" data-usages-iso="${escapeAttr(r)}">${escapeAttr(r)}</button>`).join(" ");
      const extrap = crMin ? ` <button type="button" class="ghost small" data-usages-iso="${escapeAttr(isosSc.join("|"))}" data-usages-charniere="${crMin}" title="Ouvrir la simulation « déployée au global » avec la durée de vie mesurée par cet essai (${crMin} p/arête) — à confirmer, essai arrêté avant la charnière si ≥">Extrapoler avec la vie mesurée (${crMin} p)</button>` : "";
      return `<p class="dm-p">Plaquettes de ce scénario — où servent-elles ailleurs : ${boutons}${extrap}</p>`;
    })()}
  </section>`;""", "D")

# ── E : CSS ─────────────────────────────────────────────────────────────────────
if not sonde(".extrapole-lev input", "E"):
    src = repl(src,
""".essai-diverge-info{color:var(--ink-soft);}""",
""".essai-diverge-info{color:var(--ink-soft);}
/* Tour 135 — vue plaquette globale */
.extrapole-lev input{width:110px;}
[data-extrapole] .simul-table td, [data-extrapole] .simul-table th{font-size:12px; padding:4px 6px;}""", "E")

# ── F : version + NOUVEAUTES ────────────────────────────────────────────────────
if 'const TOOL_VERSION = "4.152.0";' in src:
    deja.append("F")
else:
    src = repl(src, 'const TOOL_VERSION = "4.151.0";', 'const TOOL_VERSION = "4.152.0";', "F")

if not sonde('{ version:"4.152.0"', "G"):
    src = repl(src,
"""const NOUVEAUTES = [
  { version:"4.151.0", date:"10/11/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.152.0", date:"10/11/2026", points:[
    "<b>Une plaquette, tous ses usages, son gain au global.</b> Dans le Catalogue (« Où ? »), dans le Plan de conversion (« usages ») et dans « Ailleurs dans l'usine », chaque plaquette (vue MABEC + désignation) montre où elle sert : ligne, référence, OP, quantité de plaquettes par an, coût annuel. Et la simulation « si elle était déployée au global » se chiffre en direct à trois leviers — prix (le point de départ), puis charnière cible, puis temps de coupe. Ce qui manque est nommé (volume, cycle), jamais inventé ; le total porte l'étiquette SIMULATION et ne se mélange jamais aux gains actés.",
    "<b>« Extrapoler avec la vie mesurée ».</b> Dans « Ailleurs dans l'usine », quand un essai a mesuré une durée de vie, un bouton ouvre la simulation globale pré-remplie avec cette charnière mesurée : l'essai validé sur un poste donne aussitôt ce qu'il vaudrait partout où la même plaquette travaille."
  ]},
  { version:"4.151.0", date:"10/11/2026", points:[""", "G")

# ── Écriture EN TOUTE FIN ───────────────────────────────────────────────────────
if len(src) != orig_len:
    io.open(P, "w", encoding="utf-8", newline="").write(src)
    print("PATCH A OK : %d -> %d (+%d)" % (orig_len, len(src), len(src) - orig_len))
else:
    print("rien à écrire")
print("déjà en place :", deja)
