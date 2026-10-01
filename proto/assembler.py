#!/usr/bin/env python
"""Assemblage du proto en UN fichier déployable.

Le proto est écrit en trois morceaux (coeur.js, donnees.js, proto.html) parce que
c'est plus lisible et testable ainsi — mais ce qui part sur Surge doit être un seul
fichier, sans dépendance. Ce script fait la couture.

Il remplace aussi les marqueurs __COEUR__ / __DONNEES__ par le contenu réel, et
écrit le fichier à la racine du dossier proto/ pour le déploiement.

Vérification à la fin : le fichier produit ne doit PLUS contenir de marqueur.
"""
import io, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def lire(nom):
    with io.open(os.path.join(BASE, nom), encoding="utf-8") as f:
        return f.read()

coeur = lire("coeur.js")
donnees = lire("donnees.js")
html = lire("proto.html")

for nom, marqueur, contenu in (("coeur", "__COEUR__", coeur),
                               ("donnees", "__DONNEES__", donnees)):
    if marqueur not in html:
        print("ASSEMBLAGE KO : le marqueur %s est absent de proto.html" % marqueur)
        sys.exit(1)
    html = html.replace(marqueur, contenu)

sortie = os.path.join(BASE, "index.html")
with io.open(sortie, "w", encoding="utf-8") as f:
    f.write(html)

restants = re.findall(r"__[A-Z]+__", html)
if restants:
    print("ASSEMBLAGE KO : marqueur residuel %s" % set(restants))
    sys.exit(1)

print("assemblage : %d lignes, %.0f Ko -> %s"
      % (len(html.splitlines()), len(html.encode("utf-8")) / 1024.0, sortie))