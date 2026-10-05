#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""2resume — l'assembleur.

Quatre sources lisibles + les polices, un seul fichier déployable.

L'ordre est imposé par le cahier §8 : noyau, jeu, projection, puis l'écran.
`index.html` n'est pas la vérité — il est RECONSTITUÉ à chaque couture, et son
empreinte (SHA-256 des quatre sources) est posée dans le fichier produit pour
que le harnais refuse de tourner sur une couture périmée.

Deux détails qui ont déjà coûté une version à quelqu'un d'autre :

* lecture en `newline=''` — en mode texte, Python convertit les CRLF en LF,
  l'assembleur et le harnais Node ne verraient alors plus le même octet ;
* écriture en `newline='\\n'` — l'assembleur du proto réécrivait les CR du noyau
  en CRCRLF (2364 lignes du fichier produit qui ne correspondaient à aucune
  source). Le fichier produit DOIT être la concaténation octet pour octet.
"""

import hashlib
import io
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))

SOURCES = ["coeur.js", "donnees.js", "import.js", "app.html"]
MARQUEURS = ["__COEUR__", "__DONNEES__", "__IMPORT__"]


def lire(nom):
    with io.open(os.path.join(BASE, nom), "r", encoding="utf-8", newline="") as f:
        return f.read()


def ecrire(nom, texte):
    with io.open(os.path.join(BASE, nom), "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)


def empreinte(contenus):
    return hashlib.sha256("\x00".join(contenus).encode("utf-8")).hexdigest()[:16]


def main():
    for nom in SOURCES + ["polices.css"]:
        if not os.path.exists(os.path.join(BASE, nom)):
            sys.exit("ASSEMBLAGE KO : la source %s est absente." % nom)

    polices = lire("polices.css")
    contenus = [lire(n) for n in SOURCES]
    html = contenus[-1]

    # L'empreinte est calculée sur les quatre sources AVANT injection : elle est
    # donc reproductible par le harnais, qui relit les mêmes fichiers sur disque.
    sig = empreinte(contenus)
    html = html.replace("__POLICES__", polices)
    html = html.replace("__ASSEMBLAGE__", sig)
    for marqueur, contenu in zip(MARQUEURS, contenus[:-1]):
        if marqueur not in html:
            sys.exit("ASSEMBLAGE KO : le marqueur %s est absent de app.html" % marqueur)
        html = html.replace(marqueur, contenu)

    restes = re.findall(r"__[A-Z]+__", html)
    if restes:
        sys.exit("ASSEMBLAGE KO : marqueur résiduel en sortie : %s" % ", ".join(sorted(set(restes))))

    ecrire("index.html", html)
    taille = os.path.getsize(os.path.join(BASE, "index.html"))
    print("ASSEMBLAGE OK — empreinte %s — index.html : %d octets" % (sig, taille))


if __name__ == "__main__":
    main()