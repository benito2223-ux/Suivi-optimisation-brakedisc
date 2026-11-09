# -*- coding: utf-8 -*-
"""Tour 134 (4.151.0) — Étape 2 : conditions de coupe par groupe simultané.
Patch idempotent : sonde ce qui est déjà appliqué, écrit en TOUTE FIN uniquement."""
import io, sys, re

P = r"C:/Users/Admin/Desktop/Stellantis_SeptFons/bilan_economique.html"
src = io.open(P, "r", encoding="utf-8", newline="").read()
orig_len = len(src)
applique = []
deja = []

def repl(s, old, new, label, expected=1):
    """Remplace old par new (essai LF puis CRLF). Assert exactement `expected` occurrence(s)."""
    for attempt in (old, old.replace("\n", "\r\n")):
        n = s.count(attempt)
        if n == expected:
            return s.replace(attempt, new, expected)
        if n != 0:
            raise SystemExit("ANCRE '%s' : %d occurrences (attendu %d)" % (label, n, expected))
    raise SystemExit("ANCRE INTROUVABLE : %s" % label)

def sonde(motif, label):
    if motif in src or motif.replace("\n", "\r\n") in src:
        deja.append(label)
        return True
    return False

# ── E-decl : le Set de session « différent sur cet outil » ──────────────────────
if not sonde("condOutilsDivergents = new Set()", "E-decl"):
    src = repl(src,
"""let configOuverts = new Set(); /* v4.121 acte II : la configuration nait repliee ; l'ensemble porte les scenarios DEPLIES par l'utilisateur */""",
"""let configOuverts = new Set(); /* v4.121 acte II : la configuration nait repliee ; l'ensemble porte les scenarios DEPLIES par l'utilisateur */
/* Tour 134 — les logements dont l'utilisateur a rouvert le champ « différent sur cet outil » :
   état de SESSION seulement (jamais écrit dans le suivi) — une divergence demandée n'est pas une donnée. */
const condOutilsDivergents = new Set();""", "E-decl")

# ── E1 : les fonctions du groupe, avant logementBlocHTML ────────────────────────
BLOC_FONCTIONS = """/* ═══ Tour 134 (4.151.0) — ÉTAPE 2 : les conditions de coupe se tapent une fois ════
   Demande Claude Tour 133 (DEMANDE_ETAPE_2_CONDITIONS_DE_COUPE_A_HERMES_ZCODE.md).
   Le rangement des données NE CHANGE PAS : vc, f, kappaR, rayonBec, apPiste, tempsCoupe
   restent sur chaque logement, format 8 inchangé. Ce qui change : le bloc « Conditions
   de coupe » du GROUPE simultané écrit, à la saisie, dans tous les logements du groupe.
   Un scénario existant divergent s'ouvre SANS qu'aucune valeur ne bouge : l'écrasement
   n'arrive que quand l'utilisateur retouche le bloc. Aucune conversion automatique. */

/* les groupes simultanés : un groupe = un outil et tous les suivants cochés « simultané
   avec le précédent ». Accepte un scénario OU une liste d'outils. Une seule définition —
   elle remplace les quatre copies locales (cycle, verdict, référence, aperçu). */
function groupesSimultanes(scOuOutils){
  const outils = Array.isArray(scOuOutils) ? scOuOutils : ((scOuOutils && scOuOutils.outils) || []);
  const groupes = [];
  let courant = null;
  outils.forEach(o => {
    if(o.simultaneAvecPrecedent && courant) courant.push(o);
    else { courant = [o]; groupes.push(courant); }
  });
  return groupes;
}
function groupeDeOutil(sc, outilId){
  return groupesSimultanes(sc).find(g => g.some(o => o.id === outilId)) || null;
}
/* l'état des conditions du groupe : uniforme = tous les logements du groupe portent la
   même valeur (ou tous vides). Divergent = le bloc prévient et les champs restent sur
   chaque logement : rien n'est écrasé en silence. Ne rien écrire ici — jamais. */
function conditionsUniformes(membres){
  const logs = membres.flatMap(o => (o.logements || []));
  const uni = (cle) => {
    const vals = logs.map(l => l[cle]);
    const premier = String(vals[0] ?? "");
    const uniforme = logs.length > 0 && vals.every(v => String(v ?? "") === premier);
    return { uniforme, valeur: uniforme ? vals[0] : null };
  };
  const modeVitesse = uni("modeVitesse");
  const champVitesse = modeVitesse.valeur === "G97" ? "sBroche" : "vc";
  return { logs, modeVitesse, champVitesse,
           vitesse: uni(champVitesse),
           f: uni("f"), kappaR: uni("kappaR"),
           rayonBec: uni("rayonBec"), apPiste: uni("apPiste") };
}
/* la saisie du groupe est RECOPIÉE dans tous les logements — le seul endroit où
   l'outil écrit une condition de coupe au niveau du groupe. */
function ecrireConditionsGroupe(membres, champ, val){
  let n = 0;
  membres.forEach(o => (o.logements || []).forEach(l => { l[champ] = val; n++; }));
  return n;
}
/* le mode décide du champ et de l'unité : G96 → Vc (m/min), G97 → S (tr/min).
   En G97 la valeur vit dans sBroche : aucun calcul ne peut lire des tr/min comme des m/min. */
function condLabelVitesse(mode){ return mode === "G97" ? "S <span>tr/min</span>" : "Vc <span>m/min</span>"; }
function condChampVitesse(mode){ return mode === "G97" ? "sBroche" : "vc"; }
/* un essai avec relevés ne propose plus « Aligner sur le scénario » (Tour 134) */
function alignerDisponible(essai){ return !(((essai && essai.prelevements) || []).length); }

/* le bloc « Conditions de coupe » du groupe : une fois, en tête du groupe */
function conditionsGroupeHTML(sc, membres, showFrFa){
  const un = conditionsUniformes(membres);
  const noms = membres.map(o => o.numero || "sans n°").join(" + ");
  const titre = membres.length > 1
    ? "Conditions de coupe — groupe simultané (" + escapeAttr(noms) + ") : tapées une fois pour tous les logements"
    : "Conditions de coupe (" + escapeAttr(noms) + ") : tapées une fois pour tous les logements";
  const valDe = (u) => u.uniforme ? (u.valeur ?? "") : "";
  const plDe = (u) => u.uniforme ? "" : "diffère selon l'outil";
  const divergence = [un.modeVitesse, un.vitesse, un.f, un.kappaR]
    .concat(showFrFa ? [un.rayonBec, un.apPiste] : [])
    .some(u => !u.uniforme);
  const vitesse = champHTML(condLabelVitesse(un.modeVitesse.valeur),
    `<input class="cg-input" type="number" step="10" data-cond-groupe="vitesse" value="${valDe(un.vitesse)}" placeholder="${plDe(un.vitesse)}" title="${un.modeVitesse.valeur === "G97" ? "Rotation broche fixe (tr/min), rangée dans sBroche — jamais lue comme une Vc" : "Vitesse de coupe (m/min)"}">`, "oc-num");
  const mode = champHTML("Mode", `<select class="cg-input" data-cond-groupe="modeVitesse">
      <option value="" ${un.modeVitesse.valeur ? "" : "selected"}>— (non renseigné)</option>
      <option value="G96" ${un.modeVitesse.valeur === "G96" ? "selected" : ""}>G96 — vitesse de coupe constante</option>
      <option value="G97" ${un.modeVitesse.valeur === "G97" ? "selected" : ""}>G97 — rotation broche fixe</option>
    </select>`, "oc-moyen");
  const nombre = (cle, label, step) => champHTML(label,
    `<input class="cg-input" type="number" step="${step}" data-cond-groupe="${cle}" value="${valDe(un[cle])}" placeholder="${plDe(un[cle])}">`, "oc-num");
  return `<div class="cond-groupe" data-sc="${sc.id}" data-groupe="${membres[0].id}">
    <div class="cg-legende">⇉ ${titre}</div>
    <div class="cg-champs">
      ${mode}
      ${vitesse}
      ${nombre("f", "f <span>mm/tr</span>", "0.01")}
      ${nombre("kappaR", "κr <span>°</span>", "1")}
      ${showFrFa ? nombre("rayonBec", "rε <span>mm</span>", "0.1") : ""}
      ${showFrFa ? nombre("apPiste", "ap <span>mm</span>", "0.1") : ""}
    </div>
    ${divergence ? `<div class="cg-avert">Valeurs différentes selon l'outil : les champs restent sur chaque logement, rien n'est écrasé. Retoucher un champ ici applique la valeur à tout le groupe.</div>` : ""}
  </div>`;
}
/* les conditions figées de l'essai, lues PAR GROUPE (Tour 134, demande §3.4) :
   une ligne par groupe simultané quand l'instantané est homogène — sinon rien de plus
   que les puces par logement, qui restent la vérité logement par logement. */
function conditionsEssaiGroupeHTML(sc, essai){
  const snap = (essai.params && essai.params.logements) || [];
  if(!snap.length) return "";
  const aff = v => (v === "" || v == null) ? "—" : v;
  const lignes = [];
  groupesSimultanes(sc).forEach(g => {
    const lps = g.flatMap(o => snap.filter(lp => lp.outilId === o.id));
    if(!lps.length) return;
    const mode = lps[0].modeVitesse || "";
    const vitCh = condChampVitesse(mode);
    const vitesse = lps[0][vitCh];
    const meme = lps.every(lp => String(lp.modeVitesse || "") === String(mode)
      && String(lp[vitCh] ?? "") === String(vitesse ?? "")
      && String(lp.f ?? "") === String(lps[0].f ?? ""));
    if(!(meme && (vitesse || lps[0].f || mode))) return;
    const vit = mode === "G97" ? "S " + aff(vitesse) + " tr/min" : "Vc " + aff(vitesse) + " m/min";
    lignes.push(escapeAttr(g.map(o => o.numero || "?").join(" + ")
      + " — " + (mode ? mode + " · " : "") + vit + " · f " + aff(lps[0].f)));
  });
  if(!lignes.length) return "";
  return `<span class="essai-cond-groupe">${lignes.join("</span><span class=\\"essai-cond-groupe\\">")}</span>`;
}
/* les scénarios dont le NOM porte G97/S+chiffres, sans mode confirmé — proposés UNE fois
   (demande §3.3) : l'utilisateur valide ligne par ligne, la valeur tapée n'est jamais modifiée. */
function scenariosAConfirmerMode(){
  const rx = /G97|S\\d{3,4}/;
  const out = [];
  (lignes || []).forEach(l => (l.references || []).forEach(r => (r.ops || []).forEach(op => {
    (op.scenarios || []).forEach(sc => {
      if(!rx.test(sc.name || "")) return;
      const porte = (sc.outils || []).some(o => (o.logements || []).some(lg => lg.modeVitesse));
      if(!porte) out.push({ sc, ou: (l.nom || "?") + " · " + (op.nom || op.opCode || "?") });
    });
  })));
  return out;
}
function renderG97AConfirmer(){
  const cont = document.getElementById("optG97Liste");
  if(!cont) return;
  const items = scenariosAConfirmerMode();
  if(!items.length){ cont.innerHTML = "Rien à confirmer : aucun scénario n'attend de mode G96/G97."; return; }
  cont.innerHTML = items.map(x => `<div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin:4px 0;">
      <span>« ${escapeAttr(x.sc.name || "sans nom")} » — ${escapeAttr(x.ou)}</span>
      <button type="button" class="ghost small" data-cond-mode-sc="${x.sc.id}" data-cond-mode="G97">confirmer G97 (tr/min)</button>
      <button type="button" class="ghost small" data-cond-mode-sc="${x.sc.id}" data-cond-mode="G96">confirmer G96 (m/min)</button>
    </div>`).join("");
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("[data-cond-mode-sc]");
  if(!b) return;
  const sc = data.find(s => s.id === b.getAttribute("data-cond-mode-sc"));
  const mode = b.getAttribute("data-cond-mode");
  if(!sc || (mode !== "G96" && mode !== "G97")) return;
  sc.outils.forEach(o => (o.logements || []).forEach(lg => { lg.modeVitesse = mode; }));
  saveData(); render();
});

function logementBlocHTML(sc, o, l, showFrFa, showCycleDetail){"""
if not sonde("function groupesSimultanes(", "E1"):
    src = repl(src, "function logementBlocHTML(sc, o, l, showFrFa, showCycleDetail){", BLOC_FONCTIONS, "E1")

# ── E2 : outilCarteHTML — le bloc du groupe en tête du groupe ───────────────────
if not sonde('conditionsGroupeHTML(sc, groupeMien, showFrFa)', "E2"):
    src = repl(src,
"""  const aDesCouts = o.logements.some(l => posCost(l) !== null);
  return `""",
"""  const aDesCouts = o.logements.some(l => posCost(l) !== null);
  /* Tour 134 — le bloc « Conditions de coupe » du groupe, rendu UNE FOIS par groupe,
     en tête (le premier outil du groupe est sa tête ; un outil seul est un groupe d'un). */
  const groupeMien = groupesSimultanes(sc).find(g => g[0] === o) || [o];
  const estTete = groupeMien[0] === o;
  return `""", "E2")
    src = repl(src,
"""        ${planOutilHTML(sc, o)}
        ${o.logements.map(l => logementBlocHTML(sc, o, l, showFrFa, showCycleDetail)).join("")}""",
"""        ${estTete ? conditionsGroupeHTML(sc, groupeMien, showFrFa) : ""}
        ${planOutilHTML(sc, o)}
        ${o.logements.map(l => logementBlocHTML(sc, o, l, showFrFa, showCycleDetail)).join("")}""", "E2b")

# ── E3 : logementBlocHTML — champs masqués tant qu'ils valent la valeur du groupe ─
if not sonde("cacheSiGroupe", "E3"):
    src = repl(src,
"""  const coupe = [
    num("vc", "Vc <span>m/min</span>", "10"),
    num("f", "f <span>mm/tr</span>", "0.01"),
    num("kappaR", "κr <span>°</span>", "1", 'min="0" max="90"', "Angle de direction d'arête : alimente le rapport Fr/Fa et le suivi thermique."),
    showFrFa ? num("rayonBec", "rε <span>mm</span>", "0.1", 'min="0"', "Rayon de bec — affine le κr effectif quand la coupe se fait sur le bec.") : "",
    showFrFa ? num("apPiste", "ap <span>mm</span>", "0.1", 'min="0"', "Profondeur de passe — affine le κr effectif.") : "",
    num("tempsCoupe", "Temps de coupe <span>s</span>", "0.1", 'min="0"')
  ].filter(Boolean).join("");""",
"""  /* Tour 134 — les conditions portées par le bloc du groupe disparaissent ici tant
     qu'elles valent la valeur du groupe ; le lien « différent sur cet outil » rouvre le
     champ (session seule). tempsCoupe reste toujours ici : il dépend de la longueur
     usinée, pas de la broche. Un groupe divergent laisse tout visible. */
  const grp = groupeDeOutil(sc, o.id);
  const un = (grp && grp.length) ? conditionsUniformes(grp) : null;
  const cleDiverg = (field) => sc.id + "|" + o.id + "|" + l.id + "|" + field;
  const cacheSiGroupe = (field) => {
    if(!un || !un[field] || !un[field].uniforme) return false;
    return !condOutilsDivergents.has(cleDiverg(field));
  };
  const lienDiff = (field) => `<button class="cond-divergence ghost small" data-divergence="${cleDiverg(field)}" title="Saisir une valeur propre à CE logement : possible et visible ; le bloc du groupe ne l'écrase que si tu le retouches">différent sur cet outil</button>`;
  const champLog = (field, maker) => cacheSiGroupe(field) ? lienDiff(field) : maker();
  const vitCh = un ? un.champVitesse : "vc";
  const vitLab = condLabelVitesse(un ? un.modeVitesse.valeur : "");
  const coupe = [
    champLog("vitesse", () => num(vitCh, vitLab, "10")),
    champLog("f", () => num("f", "f <span>mm/tr</span>", "0.01")),
    champLog("kappaR", () => num("kappaR", "κr <span>°</span>", "1", 'min="0" max="90"', "Angle de direction d'arête : alimente le rapport Fr/Fa et le suivi thermique.")),
    showFrFa ? champLog("rayonBec", () => num("rayonBec", "rε <span>mm</span>", "0.1", 'min="0"', "Rayon de bec — affine le κr effectif quand la coupe se fait sur le bec.")) : "",
    showFrFa ? champLog("apPiste", () => num("apPiste", "ap <span>mm</span>", "0.1", 'min="0"', "Profondeur de passe — affine le κr effectif.")) : "",
    num("tempsCoupe", "Temps de coupe <span>s</span>", "0.1", 'min="0"')
  ].filter(Boolean).join("");""", "E3")

# ── E4 : snapshotLogements fige le mode et la rotation ──────────────────────────
if not sonde("modeVitesse: l.modeVitesse, sBroche: l.sBroche", "E4"):
    src = repl(src,
"""    vc: l.vc, f: l.f, charniere: l.charniere, ref: l.ref, prix: l.prix""",
"""    vc: l.vc, f: l.f, charniere: l.charniere, ref: l.ref, prix: l.prix,
    modeVitesse: l.modeVitesse, sBroche: l.sBroche  /* Tour 134 : le mode et la rotation figent avec l'essai */""", "E4")

# ── E5 : paramsDivergences nomme le mode et la rotation ─────────────────────────
if not sonde('mode " + aff(s.modeVitesse', "E5"):
    src = repl(src,
"""    if(!memeVal(s.charniere, cur.charniere)) champs.push("charnière " + aff(s.charniere) + "→" + aff(cur.charniere));""",
"""    if(!memeVal(s.charniere, cur.charniere)) champs.push("charnière " + aff(s.charniere) + "→" + aff(cur.charniere));
    if(!memeVal(s.modeVitesse, cur.modeVitesse)) champs.push("mode " + aff(s.modeVitesse || "—") + "→" + aff(cur.modeVitesse || "—"));
    if(!memeVal(s.sBroche, cur.sBroche)) champs.push("S " + aff(s.sBroche) + "→" + aff(cur.sBroche));""", "E5")

# ── E6a : l'essai affiche ses conditions par groupe ─────────────────────────────
if not sonde("conditionsEssaiGroupeHTML(sc, essai)}${chips}", "E6a"):
    src = repl(src, "      ${chips}${lpAdd}",
              "      ${conditionsEssaiGroupeHTML(sc, essai)}${chips}${lpAdd}", "E6a")

# ── E6b : Aligner seulement sans relevé ; sinon information + nouvel essai ──────
if not sonde("essai-refaire", "E6b"):
    src = repl(src,
"""      ${diverge.length ? `<span class="essai-diverge">⚠ modifié depuis : ${escapeAttr(diverge.join(" · "))}${interactive ? ` <button class="params-sync" data-id="${sc.id}" data-essai="${essai.id}">Aligner sur le scénario</button>` : ""}</span>` : ""}""",
"""      ${diverge.length
        ? (interactive && alignerDisponible(essai)
            ? `<span class="essai-diverge">⚠ modifié depuis : ${escapeAttr(diverge.join(" · "))} <button class="params-sync" data-id="${sc.id}" data-essai="${essai.id}">Aligner sur le scénario</button></span>`
            : `<span class="essai-diverge essai-diverge-info">ℹ le scénario a changé depuis cet essai (${escapeAttr(diverge.join(" · "))}) — l'essai garde ses conditions${interactive ? ` <button class="ghost small essai-refaire" data-id="${sc.id}" data-essai="${essai.id}" title="Créer un nouvel essai, dans ce scénario, avec les conditions actuelles">Nouvel essai avec les conditions actuelles</button>` : ""}</span>`)
        : ""}""", "E6b")

# ── E6c : la puce d'essai affiche S tr/min en G97 ───────────────────────────────
if not sonde('"S " + (lp.sBroche === "" || lp.sBroche == null ? "—" : lp.sBroche)', "E6c"):
    src = repl(src,
""" — Vc ${lp.vc === "" || lp.vc == null ? "—" : lp.vc} f ${lp.f === "" || lp.f == null ? "—" : lp.f} charnière""",
""" — ${lp.modeVitesse === "G97" ? "S " + (lp.sBroche === "" || lp.sBroche == null ? "—" : lp.sBroche) + " tr/min" : "Vc " + (lp.vc === "" || lp.vc == null ? "—" : lp.vc)} f ${lp.f === "" || lp.f == null ? "—" : lp.f} charnière""", "E6c")

# ── E7 : handlers du bloc groupe, du lien divergence, du nouvel essai ; garde Aligner ─
if not sonde('root.querySelectorAll(".cond-groupe [data-cond-groupe]")', "E7"):
    src = repl(src,
"""      if(l){ l.suiviTolerance = inp.checked; saveData(); render(); }
    });
  });
  root.querySelectorAll(".params-sync").forEach(el => {""",
"""      if(l){ l.suiviTolerance = inp.checked; saveData(); render(); }
    });
  });
  /* Tour 134 — le bloc « Conditions de coupe » du groupe : une saisie, tous les
     logements du groupe. Le champ vitesse suit le mode (G96 → vc, G97 → sBroche). */
  root.querySelectorAll(".cond-groupe [data-cond-groupe]").forEach(inp => {
    inp.addEventListener("change", () => {
      const bloc = inp.closest(".cond-groupe");
      const teteId = bloc ? bloc.getAttribute("data-groupe") : "";
      const membres = groupesSimultanes(sc).find(g => g[0] && g[0].id === teteId) || [];
      if(!membres.length) return;
      let champ = inp.getAttribute("data-cond-groupe");
      if(champ === "vitesse"){
        const sel = bloc.querySelector('[data-cond-groupe="modeVitesse"]');
        champ = condChampVitesse(sel ? sel.value : "");
      }
      const val = inp.type === "number" ? (inp.value === "" ? "" : parseFloat(inp.value)) : inp.value;
      ecrireConditionsGroupe(membres, champ, val);
      saveData(); render();
    });
  });
  /* le lien « différent sur cet outil » : rouvre le champ au niveau du logement (session seule) */
  root.querySelectorAll(".cond-divergence").forEach(btn => {
    btn.addEventListener("click", () => {
      condOutilsDivergents.add(btn.getAttribute("data-divergence"));
      render();
    });
  });
  /* Tour 134 — « Nouvel essai avec les conditions actuelles » : un essai neuf dans ce
     scénario, avec l'instantané d'aujourd'hui. L'essai d'origine garde les siennes. */
  root.querySelectorAll(".essai-refaire").forEach(el => {
    el.addEventListener("click", () => {
      const today = new Date().toISOString().slice(0,10);
      sc.essais = sc.essais || [];
      const nouvelId = "e" + Math.random().toString(36).slice(2);
      sc.essais.push({ id: nouvelId, titre: "Essai " + (sc.essais.length + 1),
        date: today, equipe: "", operateur: "",
        but: "Reprendre l'essai précédent avec les conditions actuelles du scénario",
        observations: "", conclusion: "", maturiteBruts: "",
        params: { logements: snapshotLogements(sc) },
        marposs: { debut:"", fin:"", releves:[] },
        photos: [],
        prelevements: [],
        modifieLe: new Date().toISOString() });
      essaisOuverts.add(sc.id + "|" + nouvelId);
      saveData(); render();
      const det = document.querySelector(`details.essai-card[data-essai-id="${nouvelId}"]`);
      if(det) det.scrollIntoView({block:"center", behavior:"smooth"});
    });
  });
  root.querySelectorAll(".params-sync").forEach(el => {""", "E7")

# garde : plus d'alignement possible dès qu'un relevé existe (défense en profondeur)
if not sonde("Tour 134 : un essai avec relevés ne s'aligne plus", "E7b"):
    src = repl(src,
"""      const es = sc.essais.find(e => e.id === el.getAttribute("data-essai"));
      if(!es) return;
      dialogueConfirmer("Aligner « " + es.titre + " » sur les conditions actuelles du scénario ?""",
"""      const es = sc.essais.find(e => e.id === el.getAttribute("data-essai"));
      if(!es) return;
      if((es.prelevements || []).length) return; /* Tour 134 : un essai avec relevés ne s'aligne plus */
      dialogueConfirmer("Aligner « " + es.titre + " » sur les conditions actuelles du scénario ?""", "E7b")

# ── E8 : unification des quatre calculs de groupes ──────────────────────────────
if not sonde("const groupes = groupesSimultanes(outils).map(", "E8a"):
    src = repl(src,
"""  const outils = sc.outils || [];
  let filled = 0, total = 0;
  const groupes = [];
  outils.forEach((o, idx) => {
    let s = 0;
    (o.logements||[]).forEach(l => {
      total++;
      const c = parseFloat(l.tempsCoupe);
      if(!isNaN(c)){ filled++; s += c; }
    });
    if(idx > 0 && o.simultaneAvecPrecedent && groupes.length) groupes[groupes.length-1].push(s);
    else groupes.push([s]);
  });""",
"""  const outils = sc.outils || [];
  let filled = 0, total = 0;
  /* Tour 134 : la répartition simultané/série vit dans groupesSimultanes() — une seule définition */
  const tempsParOutil = outils.map(o => {
    let s = 0;
    (o.logements||[]).forEach(l => {
      total++;
      const c = parseFloat(l.tempsCoupe);
      if(!isNaN(c)){ filled++; s += c; }
    });
    return s;
  });
  const groupes = groupesSimultanes(outils).map(g => g.map(o => tempsParOutil[outils.indexOf(o)]));""", "E8a")

if not sonde("    const groupes = groupesSimultanes(sc); /* Tour 134", "E8b"):
    src = repl(src,
"""    const groupes = [];
    sc.outils.forEach((o, i) => {
      if(i > 0 && o.simultaneAvecPrecedent && groupes.length) groupes[groupes.length - 1].push(o);
      else groupes.push([o]);
    });
    groupes.forEach(membres => {""",
"""    const groupes = groupesSimultanes(sc); /* Tour 134 : une seule définition */
    groupes.forEach(membres => {""", "E8b")

if not sonde("  const groupesRef = groupesSimultanes(base.outils || []);", "E8c"):
    src = repl(src,
"""  const groupesRef = [];
  (base.outils || []).forEach((o, i) => {
    if(i > 0 && o.simultaneAvecPrecedent && groupesRef.length) groupesRef[groupesRef.length - 1].push(o);
    else groupesRef.push([o]);
  });""",
"""  const groupesRef = groupesSimultanes(base.outils || []); /* Tour 134 : une seule définition */""", "E8c")

if not sonde("  const groupes = groupesSimultanes(sc).map(g => g.map(o => sc.outils.indexOf(o)));", "E8d"):
    src = repl(src,
"""  const groupes = [];
  let courant = null;
  sc.outils.forEach((o, oi) => {
    if(o.simultaneAvecPrecedent && courant) courant.push(oi);
    else { courant = [oi]; groupes.push(courant); }
  });""",
"""  /* Tour 134 : la répartition vit dans groupesSimultanes() — une seule définition */
  const groupes = groupesSimultanes(sc).map(g => g.map(o => sc.outils.indexOf(o)));""", "E8d")

# ── E9 : la section Options « Conditions de coupe » ─────────────────────────────
if not sonde('id="optG97Liste"', "E9"):
    src = repl(src,
"""    <label class="opt-row">
      <input type="checkbox" id="optCycleDetail">""",
"""    <div class="opt-section">Conditions de coupe</div>
    <div class="opt-field on" style="padding-left:0;">
      <label>Mode de vitesse à confirmer (G96 / G97) <i class="opt-scope">OP</i></label>
      <div id="optG97Liste" style="color:var(--ink); font-size:13px;"></div>
      <span class="opt-note">Scénarios dont le NOM porte « G97 » ou « S » suivi de 3-4 chiffres : confirmer le mode une fois par scénario, ligne par ligne. La valeur saisie n'est jamais modifiée — seule l'étiquette du mode est posée. Liste vide = rien à confirmer.</span>
    </div>

    <label class="opt-row">
      <input type="checkbox" id="optCycleDetail">""", "E9")

# ── E10 : render() rafraîchit la liste G97 ──────────────────────────────────────
if not sonde("  renderG97AConfirmer();\n", "E10"):
    src = repl(src,
"""function render(){
""",
"""function render(){
  renderG97AConfirmer();
""", "E10", expected=1)

# ── E11 : CSS ───────────────────────────────────────────────────────────────────
if not sonde(".cond-groupe{", "E11"):
    src = repl(src,
""".lb-groupes{display:flex; flex-wrap:wrap; gap:10px;}""",
""".lb-groupes{display:flex; flex-wrap:wrap; gap:10px;}
/* Tour 134 — bloc conditions du groupe simultané */
.cond-groupe{border:1px dashed var(--border); border-radius:var(--radius-sm); padding:8px 10px; margin:6px 0 10px; background:var(--surface);}
.cond-groupe .cg-legende{font-size:12px; color:var(--ink-soft); margin-bottom:6px;}
.cond-groupe .cg-champs{display:flex; flex-wrap:wrap; gap:10px;}
.cg-input{background:var(--bg); border:1px solid var(--border); border-radius:var(--radius-sm); padding:4px 6px; font-family:var(--font-mono); font-size:13px; color:var(--ink); max-width:140px;}
.cond-groupe .cg-avert{margin-top:6px; font-size:12px; color:var(--amber);}
.cond-divergence{font-size:11px; padding:2px 6px;}
.essai-cond-groupe{display:inline-block; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-sm); padding:2px 6px; margin-right:6px; font-size:12px;}
.essai-diverge-info{color:var(--ink-soft);}""", "E11")

# ── E12 : version ───────────────────────────────────────────────────────────────
if 'const TOOL_VERSION = "4.151.0";' in src:
    deja.append("E12")
else:
    src = repl(src, 'const TOOL_VERSION = "4.150.1";', 'const TOOL_VERSION = "4.151.0";', "E12")

# ── E13 : NOUVEAUTES ────────────────────────────────────────────────────────────
if not sonde('{ version:"4.151.0"', "E13"):
    src = repl(src,
"""const NOUVEAUTES = [
  { version:"4.150.1", date:"09/11/2026", points:[""",
"""const NOUVEAUTES = [
  { version:"4.151.0", date:"10/11/2026", points:[
    "<b>Les conditions de coupe se tapent une fois.</b> Un groupe d'outils qui usinent en simultané partage une seule saisie : mode, vitesse, avance, κr, rε et ap se tapent en tête du groupe et remplissent tous les logements d'un coup. Un outil qui diffère garde le droit à sa valeur — le lien « différent sur cet outil » rouvre le champ, et un scénario existant aux valeurs divergentes s'ouvre sans rien changer.",
    "<b>Le mode G96 / G97 existe.</b> Le champ « Mode » précise si la vitesse est une Vc (m/min, G96) ou une rotation broche (tr/min, G97). En G97, la valeur se range à part : aucun écran ne peut plus afficher des tr/min avec l'unité m/min. Les scénarios dont le NOM porte G97 ou S800 se proposent dans Options → « Conditions de coupe » pour confirmer le mode, ligne par ligne — la valeur tapée n'est jamais modifiée.",
    "<b>Un essai garde ses conditions.</b> Le bouton « Aligner sur le scénario » disparaît dès qu'un relevé existe : l'essai figé reste figé, et le scénario changé se signale en information, plus en invitation. À la place : « Nouvel essai avec les conditions actuelles ». En tête d'essai, les conditions figées se lisent par groupe d'outils simultanés."
  ]},
  { version:"4.150.1", date:"09/11/2026", points:[""", "E13")

# ── Écriture EN TOUTE FIN ───────────────────────────────────────────────────────
if len(src) != orig_len:
    io.open(P, "w", encoding="utf-8", newline="").write(src)
    print("PATCH OK : %d -> %d octets (+%d)" % (orig_len, len(src), len(src) - orig_len))
else:
    print("PATCH : rien à écrire (tout déjà appliqué ?)")
print("appliqués :", applique)
print("déjà en place :", deja)
