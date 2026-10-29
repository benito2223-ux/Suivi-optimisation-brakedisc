# -*- coding: utf-8 -*-
# Tour 109 — 4.130.0 — patch D : les corrections du premier rendu.
# 1. La règle du filigrane au coin était tombée DANS le @media print (le
#    piège du parseage, rejoué — elle n'existait qu'à l'impression) :
#    retirée de là, reposée dans le bloc principal d'écran.
# 2. CSS coque : fil d'Ariane compacté (les étiquettes 01 · LIGNE MACHINE
#    partent, la ligne des valeurs reste), « + Créer un projet » passe au
#    niveau tertiaire dans la rangée 2 (un seul bouton principal par écran),
#    l'onglet Tableau repart à sa place de la 4.124 (le brief ne le liste
#    pas), l'ordre des onglets suit le brief (Atelier en dernier), la
#    scrollbar des onglets est masquée.
import io

# --- 1. la règle filigrane : sortie du @media print --------------------------
F = "bilan_economique.html"
src = io.open(F, encoding="utf-8").read()

MAL_PLACE = """/* v4.130 : le code ligne au coin, en DEV seulement (jamais sur la prod) */
body[data-env="dev"][data-filigrane-code]:not([data-filigrane-code=""])::after{
  content:attr(data-filigrane-code);
  position:fixed; top:8px; right:16px; z-index:0; pointer-events:none;
  font-family:'Open Sans Condensed',Arial,sans-serif; font-size:54px; font-weight:800;
  color:var(--filigrane-encre, var(--ink)); opacity:.1; line-height:1;
}
@media print{ body[data-env="dev"][data-filigrane-code]::after{ content:none; } }
/* v4.27 : la teinte et le filigrane de ligne ne s'impriment pas */"""
n = src.count(MAL_PLACE)
assert n == 1, "bloc filigrane mal placé : %d occurrences (attendu 1)" % n
src = src.replace(MAL_PLACE, "/* v4.27 : la teinte et le filigrane de ligne ne s'impriment pas */")
print("ok  règle filigrane sortie du @media print")

BIEN_PLACE = """/* ── v4.130.0 · passe design — LA HIÉRARCHIE DE BOUTONS ────────────────────"""
n = src.count(BIEN_PLACE)
assert n == 1, "ancre charter : %d (attendu 1)" % n
BON = """/* v4.130 : le code ligne au coin, en DEV seulement (jamais sur la prod).
   Posé DANS le bloc d'écran — le parseage du head a déjà avalé une règle
   posée dans le @media print (la règle n'existait qu'à l'impression). */
body[data-env="dev"][data-filigrane-code]:not([data-filigrane-code=""])::after{
  content:attr(data-filigrane-code);
  position:fixed; top:8px; right:16px; z-index:0; pointer-events:none;
  font-family:'Open Sans Condensed',Arial,sans-serif; font-size:54px; font-weight:800;
  color:var(--filigrane-encre, var(--ink)); opacity:.1; line-height:1;
}
@media print{
  body[data-env="dev"][data-filigrane-code]::after{ content:none; }
}

/* ── v4.130.0 · passe design — LA HIÉRARCHIE DE BOUTONS ────────────────────"""
src = src.replace(BIEN_PLACE, BON)
print("ok  règle filigrane reposée dans le bloc d'écran")

io.open(F, "w", encoding="utf-8", newline="\n").write(src)

# --- 2. les compactages de la rangée 2 ---------------------------------------
F2 = "spk-app.css"
css = io.open(F2, encoding="utf-8").read()

ANCRE = """/* le bandeau bleu de la fiche et la toolbar du monolithe : leurs éléments
   vivent dans l'en-tête maintenant — les cadres vides disparaissent. */"""
n = css.count(ANCRE)
assert n == 1, "ancre coque : %d (attendu 1)" % n

AJOUT = """/* rangée 2 compactée (rendu regardé) : le fil d'Ariane tient sur la ligne
   des valeurs seules — les étiquettes numérotées partent ; « + Créer un
   projet » passe au niveau tertiaire (un seul bouton principal par écran) ;
   les onglets suivent l'ordre du brief (Atelier en dernier) et l'onglet
   Tableau reste dans la Vue d'ensemble (décision 4.124, le brief ne le
   liste pas) ; la scrollbar des onglets ne se montre pas. */
.spk-head-contexte .fil-ariane .fil-meta{ display:none; }
.spk-head-contexte .fil-ariane{ gap:6px; }
.spk-head-onglets{ scrollbar-width:none; }
.spk-head-onglets::-webkit-scrollbar{ display:none; }
.spk-head-links #dashboardBtn{ display:none; }
.spk-head-links #carteBtn{ order:4; }
.spk-head-contexte #projetsBandeau button.primary,
.spk-head-contexte #projetsBandeau #addProjetBtn{
  background:none; border:none; color:var(--blue); padding:6px 4px;
  font-weight:600; font-size:13px;
}
.spk-head-contexte #projetsBandeau .pj-aide-btn{
  background:none; border:none; color:var(--blue); padding:4px; min-width:0;
}

""" + ANCRE
css = css.replace(ANCRE, AJOUT)
io.open(F2, "w", encoding="utf-8", newline="\n").write(css)
print("ok  compactages rangée 2 posés")
