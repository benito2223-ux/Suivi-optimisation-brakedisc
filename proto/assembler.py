#!/usr/bin/env python
"""Assemblage du proto en UN fichier déployable.

Le proto est écrit en trois morceaux (coeur.js, donnees.js, proto.html) parce que
c'est plus lisible et testable ainsi — mais ce qui part sur Surge doit être un seul
fichier, sans dépendance. Ce script fait la couture.

Il remplace aussi les marqueurs __COEUR__ / __DONNEES__ par le contenu réel, et
écrit le fichier à la racine du dossier proto/ pour le déploiement.

Vérification à la fin : le fichier produit ne doit PLUS contenir de marqueur.
"""
import io, os, re, sys, hashlib

BASE = os.path.dirname(os.path.abspath(__file__))

def lire(nom):
    """Lecture en octets, pas en mode texte. En mode texte, Python convertit les
    fins de ligne CRLF en LF : l'assembleur et le harnais (Node) ne verraient
    alors plus le MÊME fichier, et l'empreinte calculée ici ne correspondrait à
    rien de ce que le harnais peut recalculer."""
    with io.open(os.path.join(BASE, nom), "rb") as f:
        return f.read().decode("utf-8")

coeur = lire("coeur.js")
donnees = lire("donnees.js")
importjs = lire("import.js")
html = lire("proto.html")

# L'empreinte des trois morceaux, posée DANS le fichier produit.
# Sans elle, le harnais des écrans teste l'assemblage — donc l'état du code au
# moment du dernier assemblage, pas l'état du code. Modifier coeur.js et oublier
# de réassembler laisse tous les tests verts sur du code qui n'existe plus.
# C'est exactement l'illusion que ce harnais est censé interdire.
empreinte = hashlib.sha256(
    ("\x00".join([coeur, donnees, importjs, html])).encode("utf-8")
).hexdigest()[:16]

for nom, marqueur, contenu in (("coeur", "__COEUR__", coeur),
                               ("donnees", "__DONNEES__", donnees),
                               ("import", "__IMPORT__", importjs)):
    if marqueur not in html:
        print("ASSEMBLAGE KO : le marqueur %s est absent de proto.html" % marqueur)
        sys.exit(1)
    html = html.replace(marqueur, contenu)

if "__ASSEMBLAGE__" not in html:
    print("ASSEMBLAGE KO : le marqueur __ASSEMBLAGE__ est absent de proto.html")
    print("                (le harnais des écrans ne peut plus détecter un")
    print("                 assemblage périmé — c'est le garde-fou du Tour 55.)")
    sys.exit(1)
html = html.replace("__ASSEMBLAGE__", empreinte)

sortie = os.path.join(BASE, "index.html")
with io.open(sortie, "w", encoding="utf-8") as f:
    f.write(html)

restants = re.findall(r"__[A-Z]+__", html)
if restants:
    print("ASSEMBLAGE KO : marqueur residuel %s" % set(restants))
    sys.exit(1)

print("assemblage : %d lignes, %.0f Ko -> %s  [empreinte %s]"
      % (len(html.splitlines()), len(html.encode("utf-8")) / 1024.0, sortie, empreinte))