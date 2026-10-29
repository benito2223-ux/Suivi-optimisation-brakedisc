# -*- coding: utf-8 -*-
# Tour 109 — 4.130.0 — patch A : le monolithe (passe design, lot 4.130)
# 1. Le charter v4.70 « bouton cercle + chevron » est remplacé par la
#    hiérarchie à trois niveaux du design system : principal bleu plein
#    (un seul par écran), secondaire contour bleu, tertiaire texte.
#    Plus aucun ::before disque — les 128 boutons gardent balises, ids,
#    handlers (le charter ne faisait que du CSS).
# 2. Le filet bicolore 2 px de la toolbar passe au liseré bleu 3 px du
#    design system (le rouge du filet disparaît — le rouge = accent).
# 3. Les chips + Ra / + VE / + Autre critère : le « + » devient un <b> bleu,
#    le style chip (pointillé gris) est posé dans le même patch.
# 4. Le filigrane de ligne : plus de texte répété dans le fond — la teinte
#    reste, le code ligne devient un attribut body affiché AU COIN en DEV
#    seulement (body[data-env=dev]). data-env est posé ici (hostname prod =
#    "prod", tout le reste — localhost, file://, le dev — = "dev").
# 5. La virgule orpheline de la grille Composition : tuileOutil retournait
#    un Array sans join — le cast implicite en string séparait les tuiles
#    par « , » dès qu'un outil portait deux logements.
# 6. TOOL_VERSION 4.130.0 + entrée NOUVEAUTES.
import io

F = "bilan_economique.html"
src = io.open(F, encoding="utf-8").read()

def remplacer(avant, apres, label):
    global src
    n = src.count(avant)
    assert n == 1, "ancre %s : %d occurrences (attendu 1)" % (label, n)
    src = src.replace(avant, apres)
    print("ok  " + label)

# --- 1. le charter boutons ---------------------------------------------------
DEBUT = "/* ── v4.70.0 · L4 — LE BOUTON CERCLE + CHEVRON ─────────────────────────────"
FIN = "button.primary:hover::before, .btn-serie:hover::before{ background:var(--blue); }"
i = src.find(DEBUT)
j = src.find(FIN)
assert i != -1 and j != -1 and i < j, "bornes du charter v4.70 introuvables"
ancien = src[i:j + len(FIN)]
assert ancien.count("::before") >= 4, "le bloc extrait ne ressemble pas au charter"

NOUVEAU = """/* ── v4.130.0 · passe design — LA HIÉRARCHIE DE BOUTONS ────────────────────
   Trois niveaux, pas plus (brief design 4.130) :
   · principal : fond bleu plein, texte blanc — UN SEUL par écran ;
   · secondaire : contour bleu 1 px, fond blanc, texte bleu ;
   · tertiaire : texte bleu seul, souligné au survol ; une action
     destructive (danger) garde son texte rouge — le rouge est un
     signal, jamais un grand fond ni un disque.
   Le charter v4.70 (disque noir + chevron › en ::before sur 128 boutons)
   est retiré : tout est un bouton principal, donc rien ne l'est. Les
   balises, ids et handlers ne bougent pas — ce bloc reste du CSS pur. */
button.primary, button.ghost, button.danger, button.pdf, button.save, button.sec,
button.manuel, button.promouvoir, .btn-serie, .btn-valide, .btn-abandon,
.btn-essai, .outil-add, .outils-copier, .outils-completer, .scrap-add, .piece-add,
.logement-add, .marposs-import, .marposs-paste-btn, .prel-add, .backlog-add, .param-add{
  display:inline-flex; align-items:center; gap:8px;
  background:transparent; border:1px solid transparent; box-shadow:none;
  padding:8px 14px; border-radius:3px;
  font-size:14px; font-weight:600; line-height:1.25;
  color:var(--blue); text-align:left;
  transition:background .15s ease, border-color .15s ease, color .15s ease;
}
button.primary{
  background:var(--blue); border-color:var(--blue); color:#fff;
}
button.primary:hover{ background:#154d8a; border-color:#154d8a; }
button.ghost, button.pdf, button.save, button.sec, button.manuel,
.outil-add, .outils-copier, .outils-completer, .scrap-add, .piece-add,
.logement-add, .marposs-import, .marposs-paste-btn, .prel-add,
.backlog-add, .param-add{
  background:#fff; border-color:var(--blue);
}
button.ghost:hover, button.pdf:hover, button.save:hover, button.sec:hover,
button.manuel:hover, .outil-add:hover, .outils-copier:hover,
.outils-completer:hover, .scrap-add:hover, .piece-add:hover,
.logement-add:hover, .marposs-import:hover, .marposs-paste-btn:hover,
.prel-add:hover, .backlog-add:hover, .param-add:hover{
  background:#e8f0fb;
}
button.danger, .btn-abandon, button.promouvoir{
  background:transparent; border-color:transparent; color:var(--red);
  padding:8px 6px;
}
button.danger:hover, .btn-abandon:hover, button.promouvoir:hover{
  background:#fce8ea; color:var(--red);
}
.btn-serie, .btn-valide, .btn-essai{
  background:#fff; border-color:var(--blue); color:var(--blue);
}
.btn-serie:hover, .btn-valide:hover, .btn-essai:hover{ background:#e8f0fb; }

/* ── v4.130.0 — les chips : ajouter un critère est une invitation, pas une
   action : contour pointillé gris, le « + » en bleu (le HTML porte le +
   dans un <b class="chip-plus"> posé au même tour). */
.csup-add{
  background:#fff; border:1px dashed var(--gray-300); border-radius:3px;
  color:var(--ink); font-weight:500; padding:6px 12px;
}
.csup-add:hover{ background:#f3f8fd; border-color:var(--gray-300); }
.chip-plus{ color:var(--blue); font-weight:700; margin-right:4px; }"""

src = src[:i] + NOUVEAU + src[j + len(FIN):]
print("ok  charter v4.70 -> hiérarchie 3 niveaux (0 ::before disque)")

# --- 2. le filet bicolore de la toolbar --------------------------------------
remplacer(""".toolbar::after{
  content:""; position:absolute; left:0; right:0; bottom:-1px; height:2px;
  background:linear-gradient(to right, var(--red) 0 18%, var(--blue) 18% 100%);
  pointer-events:none;
}""",
""".toolbar::after{
  content:""; position:absolute; left:0; right:0; bottom:-1px; height:3px;
  background:var(--blue);
  pointer-events:none;
}""", "filet toolbar : 3 px bleu (le rouge = accent)")

# --- 3. les chips + Ra / + VE / + Autre critère ------------------------------
remplacer('">+ Ra</button>', '"><b class="chip-plus">+</b>Ra</button>', "chip + Ra")
remplacer('">+ VE</button>', '"><b class="chip-plus">+</b>VE</button>', "chip + VE")
remplacer('">+ Autre critère…</button>', '"><b class="chip-plus">+</b>Autre critère…</button>', "chip + Autre critère")

# --- 4. le filigrane : teinte seule dans le fond, code au coin en DEV --------
remplacer("""  const texte = def.sansFiligrane ? "" :
    `<text x='120' y='97' font-family='Open Sans Condensed,Arial,sans-serif' font-size='54' font-weight='800' ` +
    `fill='${encreTexte}' fill-opacity='${opaTexte}' text-anchor='middle'>${code}</text>`;
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='240' height='150'>` +
    `<rect width='240' height='150' fill='${def.encre}' fill-opacity='${def.alpha}'/>` +
    texte + `</svg>`;
  document.body.style.backgroundColor = "";
  document.body.style.backgroundImage = `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;""",
"""  /* v4.130 — plus de filigrane répété dans le fond du travail : la teinte
     seule reste en motif, et le code ligne devient un attribut du body que
     la feuille affiche AU COIN en DEV seulement (body[data-env=dev] posé
     ci-dessous ; sur la prod, jamais). L'encre du coin suit la famille. */
  document.body.dataset.env = /^suivi-optimisation-septfons\\.surge\\.sh$/.test(location.hostname) ? "prod" : "dev";
  document.body.dataset.filigraneCode = def.sansFiligrane ? "" : code;
  document.body.style.setProperty("--filigrane-encre", encreTexte);
  const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='240' height='150'>` +
    `<rect width='240' height='150' fill='${def.encre}' fill-opacity='${def.alpha}'/></svg>`;
  document.body.style.backgroundColor = "";
  document.body.style.backgroundImage = `url("data:image/svg+xml,${encodeURIComponent(svg)}")`;""",
"filigrane : teinte seule + code au coin en DEV")

# le CSS du coin (posé dans le premier bloc style, près du reste)
remplacer("/* v4.27 : la teinte et le filigrane de ligne ne s'impriment pas */",
"""/* v4.130 : le code ligne au coin, en DEV seulement (jamais sur la prod) */
body[data-env="dev"][data-filigrane-code]:not([data-filigrane-code=""])::after{
  content:attr(data-filigrane-code);
  position:fixed; top:8px; right:16px; z-index:0; pointer-events:none;
  font-family:'Open Sans Condensed',Arial,sans-serif; font-size:54px; font-weight:800;
  color:var(--filigrane-encre, var(--ink)); opacity:.1; line-height:1;
}
@media print{ body[data-env="dev"][data-filigrane-code]::after{ content:none; } }
/* v4.27 : la teinte et le filigrane de ligne ne s'impriment pas */""",
"CSS du filigrane au coin (dev-only)")

# --- 5. la virgule orpheline de la grille Composition ------------------------
remplacer("""  const tuileOutil = (o, oi) =>
    o.logements.map(l => apercuLogementHTML(sc, o, l, OUTIL_COLORS[oi % OUTIL_COLORS.length], oi, volume, totalAnnuelSc, partRefSc, vp, ajoutCout.get(o), sortiePar.get(o)));""",
"""  const tuileOutil = (o, oi) =>
    o.logements.map(l => apercuLogementHTML(sc, o, l, OUTIL_COLORS[oi % OUTIL_COLORS.length], oi, volume, totalAnnuelSc, partRefSc, vp, ajoutCout.get(o), sortiePar.get(o))).join("");""",
"virgule orpheline : tuileOutil joint ses tuiles (le cast Array séparait par ,)")

# --- 6. version + NOUVEAUTES -------------------------------------------------
remplacer('const TOOL_VERSION = "4.129.1";',
          'const TOOL_VERSION = "4.130.0";', "TOOL_VERSION")

NOUV_ANCRE = 'const NOUVEAUTES = [\n'
NOUV_ENTREE = '''const NOUVEAUTES = [
  { version:"4.130.0", date:"29/10/2026", points:[
    "<b>L\\u2019outil reprend le design system SPK — boutons et en-tête.</b> Fin des disques noirs à chevron : <b>trois niveaux de bouton</b> — un principal bleu plein par écran, un contour bleu, du texte. <b>L\\u2019en-tête tient en deux rangées</b> : logo, titre de la référence et actions (Rechercher, Transmettre, options, verrou) sur la barre bleu marine, navigation soulignée et fil d\\u2019Ariane en dessous. « + Scénario » quitte la barre pour la zone de travail ; « Créer un projet » et l\\u2019aide quittent les rangées de tête. Le filigrane de ligne quitte le fond du travail (il reste au coin, et seulement sur les adresses de développement). Les chips « + Ra / + VE / + Autre critère » deviennent des invitations pointillées."
  ]},
'''
n = src.count(NOUV_ANCRE)
assert n == 1, "ancre NOUVEAUTES : %d occurrences (attendu 1)" % n
src = src.replace(NOUV_ANCRE, NOUV_ENTREE)
print("ok  NOUVEAUTES 4.130.0")

assert src != io.open(F, encoding="utf-8").read()
io.open(F, "w", encoding="utf-8", newline="\n").write(src)
print("patch A (4.130.0) appliqué.")
