# -*- coding: utf-8 -*-
"""Tour 99 — v4.124.0 — P0-2 : le popup « Bienvenue dans la base 2026/2027 »
devient un BANDEAU non bloquant, fermable, affiché une seule fois (même clé de
stockage). Plus aucune couche modale avant le travail. Le texte tient en
deux lignes : la base est en place + le geste de mise à jour.
NB : l'écran d'ouverture (Vue d'ensemble auto, décision Q11 de Benjamin du
30/09) N'EST PAS changé — le brief externe le demande, mais Q11 est un
arbitrage explicite de Benjamin ; il se tranche à la voix, pas en silence."""
import io

p = "bilan_economique.html"
s = io.open(p, encoding="utf-8").read()


def remplace(avant, apres, label):
    global s
    nb = s.count(avant)
    assert nb == 1, "ANCRE %s : %d occurrences (attendu 1)" % (label, nb)
    s = s.replace(avant, apres, 1)
    print("ok :", label)


# ── 1. le popup devient un bandeau en flux (côté HTML : l'ancrage existe) ────
remplace(
"""  <div class="reprise-bandeau" id="repriseBandeau" hidden></div>""",
"""  <div class="reprise-bandeau" id="repriseBandeau" hidden></div>
  <div class="bandeau-premiere" id="bandeauPremiere" hidden></div>""",
"1. l'ancrage du bandeau")

# ── 2. le CSS du bandeau (dans le bloc qui porte reprise-bandeau) ────────────
remplace(
""".reprise-bandeau{display:flex; align-items:center; gap:12px; flex-wrap:wrap; background:var(--gray-50); border:1px solid var(--blue); border-radius:var(--radius); padding:10px 14px; margin-bottom:14px;}""",
""".bandeau-premiere{display:flex; align-items:flex-start; gap:10px; margin:0 14px 10px; padding:9px 12px;
  border:1px solid var(--border); border-left:4px solid var(--blue); border-radius:var(--radius-sm);
  background:var(--surface); font-size:12.5px; line-height:1.45; color:var(--ink-soft);}
.bandeau-premiere b{color:var(--ink);}
.bandeau-premiere .bp-close{margin-left:auto; flex:0 0 auto; border:1px solid var(--border); background:var(--surface);
  border-radius:var(--radius-sm); padding:2px 9px; font-size:11px; cursor:pointer; color:var(--ink-soft);}
.bandeau-premiere .bp-close:hover{border-color:var(--blue); color:var(--blue);}
.reprise-bandeau{""",
"2. le style du bandeau")

# ── 3. le popup modale devient le poseur du bandeau ──────────────────────────
remplace(
"""/* v4.49.3 — message de première ouverture après la mise en place de la base 2026/2027.
   Une fois par poste (drapeau local). Dit le geste critique : une version ancienne de
   l'application efface les cibles de coût au partage — vérifier la version en bas. */
(async function messagePremiereOuverture(){
  const CLE = "spk_msg_base_2026";
  let dejaVu = false;
  try{ dejaVu = localStorage.getItem(CLE) === "1"; }catch(e){}
  if(dejaVu) return;
  const ok = await ouvrirDialogue({
    titre: "Bienvenue dans la base 2026/2027",
    html: dlgTexte(
      "La base de départ est en place : les 6 références de l'atelier, avec leurs outils de prod complets (OP par OP), les références plaquettes ISO, les codes article MABEC et les cibles de coût pièce du site." +
      "\\n\\nLes nouveaux écrans : le coût pièce complet et la feuille de route prod → cible (vue de synthèse), les scénarios d'essai complétés depuis la prod, les outils simultanés en ambre." +
      "\\n\\nGeste important : regarde la version en bas de page — elle doit indiquer v" + TOOL_VERSION + ". Si une version plus ancienne s'affiche, ferme complètement l'application et rouvre-la connectée à Internet (elle se met à jour toute seule). Une version ancienne peut effacer les cibles de coût au moment du partage."),
    sansAnnuler: true, okLabel: "Compris"
  });
  try{ localStorage.setItem(CLE, "1"); }catch(e){}
})();""",
"""/* v4.49.3 — message de première ouverture après la mise en place de la base 2026/2027.
   Une fois par poste (drapeau local). v4.124 (P0-2 du brief externe) : ce n'est plus
   une fenêtre MODALE empilée au démarrage — un bandeau non bloquant, fermable,
   deux lignes. Le geste critique reste dit : une version ancienne peut effacer les
   cibles de coût au partage. */
(function messagePremiereOuverture(){
  const CLE = "spk_msg_base_2026";
  let dejaVu = false;
  try{ dejaVu = localStorage.getItem(CLE) === "1"; }catch(e){}
  if(dejaVu) return;
  const el = document.getElementById("bandeauPremiere");
  if(!el) return;
  el.innerHTML =
    '<span><b>Base 2026/2027 en place</b> : références de l\\'atelier, outils de prod, MABEC, cibles site. ' +
    'Vérifie la version en bas de page (v' + TOOL_VERSION + ') — une version ancienne peut effacer les cibles de coût au partage.</span>' +
    '<button class="bp-close" type="button" title="Fermer (ne s\\'affichera plus)">Compris</button>';
  el.hidden = false;
  el.querySelector(".bp-close").addEventListener("click", () => {
    el.hidden = true;
    try{ localStorage.setItem(CLE, "1"); }catch(e){}
  });
})();""",
"3. le popup devient bandeau non bloquant")

io.open(p, "w", encoding="utf-8").write(s)
print("patch B posé")
