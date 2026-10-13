# -*- coding: utf-8 -*-
"""Assemble DOSSIER_REVUE_CLAUDE.md : extraits choisis du code pour une revue
par Claude web (version gratuite, pas d'acces dossier). Objectif : <= 120 Ko."""

s = open('bilan_economique.html', encoding='utf-8', newline='').read()
lignes = s.split('\n')

def extrait_fonction(nom, max_lignes=130):
    """extrait la fonction `nom` jusqu'a la fonction suivante (cap inclus)."""
    ancre = 'function ' + nom
    i = s.find(ancre)
    if i == -1:
        return f"/* [fonction {nom} introuvable] */\n"
    dept = s[:i].count('\n')
    # fin = prochaine declaration de fonction top-level
    j = dept + 1
    fin = len(lignes)
    for k in range(dept + 1, min(dept + max_lignes + 1, len(lignes))):
        if lignes[k].startswith('function ') or lignes[k].startswith('async function '):
            fin = k
            break
    else:
        fin = min(dept + max_lignes, len(lignes))
    bloc = '\n'.join(lignes[dept:fin])
    if fin == dept + max_lignes and fin < len(lignes):
        bloc += f"\n/* [...extrait coupe a {max_lignes} lignes] */"
    return bloc + '\n'

def grepcss(motifs, max_par_motif=6):
    out = []
    bas = motifs if isinstance(motifs, list) else [motifs]
    for m in bas:
        n = 0
        for ligne in lignes:
            t = ligne.strip()
            if t.startswith(m) and n < max_par_motif:
                out.append(t)
                n += 1
    return '\n'.join(out)

parties = []
parties.append("""# DOSSIER DE REVUE — suivi SPK Sept Fons (extrait auto-contenu)

Tu es un relecteur critique EXTERIEUR. Cet outil a ete construit par deux IA
(Z Code + Hermes) qui sont fieres de leur travail — ne le sois pas a leur place.
Ton travail : trouver ce qui cloche, ce qui va casser, ce qui fera fuir
l'utilisateur. Tu PROPOSES, tu ne codes pas.

LE PROJET : suivi d'optimisation du cout de revient des disques de frein
(usinage ceramique, Stellantis Sept Fons). UN SEUL fichier HTML (~19 200 lignes),
zero build, zero SDK, offline-first, PWA. Trois publics : l'atelier (Matis,
operateurs, GANTS + TABLETTE, saisie rapide et bruyante), le pilote, la
hierarchie (documents imprimables). L'outil est AUSSI un outil commercial : il
doit demontrer a Matis l'economie du passage sur les plaquettes SPK.

VERSION COURANTE : 4.89.0 — 551 tests verts (harnais maison dans build_harness.py).

REGLES DU JEU (extrait de la constitution, a respecter dans tes directives) :
- aucun chiffre mensonger : un absent se NOMME, jamais un zero qui pretend ;
- cout plaquette et temps machine = DEUX AXES, jamais sommes ;
- ne pas additionner des gains de natures differentes ;
- K (Vc x Hex) et P_req n'apparaissent JAMAIS dans les sorties visibles (secret
  interne SPK) — verifie qu'aucun extrait ne les expose ;
- les donnees reelles ne sortent jamais du poste.

Ce dossier contient des EXTRAITS choisis, pas tout le fichier : declare ce que
tu n'as pas pu evaluer. Format de ta reponse : verdict en 5 lignes (sans
complaisance), puis 5 a 10 directives PRIORISEES (P1/P2/P3) — chacune avec
probleme, pourquoi, directive concrete pour Z Code, effort S/M/L. Termine par
ce qui est bien fait (court) et ce qui t'a manque.

Axes imposes : (A) ergonomie de saisie atelier (gants, tablette, bruit),
(B) hierarchie visuelle (Benjamin dit : « tout est ton sur ton, trop petit »),
(C) le monolithe de 19 200 lignes (ou est la limite ?), (D) la coherence du
socle commercial (catalogue, plan de conversion, basculeur, simulateur),
(E) les angles morts (etats globaux, hors ligne, deux postes en parallelle).

=== EXTRAITS ===

--- 1. CSS (regles cles : tokens, conteneur, panneaux, tuiles, champs, tables) ---

""")

css_motifs = [':root{', '.wrap{', '.hd ', 'body{', '.panel', '.tuile', '.acc-', '.btn', '.cell',
              '.oc-', '.at-', '.lb-', '.simul-', '.os-', '.foot-cell', '.status-badge', 'input[type="number"]']
parties.append(grepcss(css_motifs, 8))
parties.append("\n--- 2. L'ECRAN D'ACCUEIL (rendu) ---\n")
parties.append(extrait_fonction('renderAccueil', 120))
parties.append(extrait_fonction('accueilBandeauHTML', 90))
parties.append(extrait_fonction('accueilPiedHTML', 40))
parties.append("\n--- 3. LA SAISIE ATELIER (gants + tablette) ---\n")
parties.append(extrait_fonction('atelierHTML', 130))
parties.append("\n--- 4. LE PLAN DE CONVERSION (vitrine commerciale) ---\n")
parties.append(extrait_fonction('planHTML', 110))
parties.append(extrait_fonction('planLignes', 60))
parties.append("\n--- 5. LE SIMULATEUR ---\n")
parties.append(extrait_fonction('simulHTML', 90))
parties.append("\n--- 6. LE CATALOGUE ---\n")
parties.append(extrait_fonction('catalogueRendu', 50))
parties.append("\n--- 7. L'ECRITURE DES CHAMPS (le chemin de la saisie) ---\n")
parties.append(extrait_fonction('writeFieldValue', 70))
parties.append("\n--- 8. HISTORIQUE RECENT (CHANGELOG, 3 dernieres versions) ---\n")

c = open('CHANGELOG.md', encoding='utf-8').read()
parties.append('\n'.join(c.split('\n')[:90]))

parties.append("\n--- 9. JOURNAL (2 derniers tours) ---\n")
e = open('ECHANGES.md', encoding='utf-8').read()
le = e.split('\n')
parties.append('\n'.join(le[:100]))

sortie = '\n'.join(parties)
open('DOSSIER_REVUE_CLAUDE.md', 'w', encoding='utf-8', newline='\n').write(sortie)
print("dossier ecrit :", len(sortie.encode('utf-8')), "octets |", sortie.count('\n'), "lignes")
print("estimation tokens ~", len(sortie)//4)
