#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET3 — L'ASSEMBLEUR
Couture les sources en un index.html unique, déployable, zéro dépendance.
Pose l'empreinte SHA-256 de chaque source dans le fichier produit : le harnais
(test_app.js) la recalcule — modifier une source et oublier l'assemblage fait
échouer la suite au lieu de valider du code qui n'est plus dans le fichier.

Usage : python assembler.py
"""

import hashlib
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.abspath(__file__))

SOURCES_JS = [
    "src/coeur.js",
    "src/import.js",
    "src/donnees.js",
    "src/ui.js",
    "src/app.js",
    "src/app_edition.js",
    "src/app_panneaux.js",
]
SOURCES_CSS = [
    "src/fonts.css",
    "src/styles.css",
]
COQUILLE = "src/shell.html"
SORTIE = "index.html"


def lire(chemin):
    p = os.path.join(RACINE, chemin)
    if not os.path.exists(p):
        sys.exit("ASSEMBLEUR : source manquante : " + chemin)
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def empreinte(chemin, contenu):
    h = hashlib.sha256()
    h.update(chemin.encode("utf-8"))
    h.update(contenu.encode("utf-8"))
    return h.hexdigest()[:16]


def echapper_js(js):
    """Pour poser le JS dans un <script> inline sans risque de </script>."""
    return js.replace("</script", "<\\/script")


def main():
    css = "\n".join(lire(c) for c in SOURCES_CSS)
    js_parts = []
    empreintes = []
    # les CSS entrent dans l'empreinte : une source modifiée sans ré-assemblage
    # doit être vue, quelle qu'elle soit
    for c in SOURCES_CSS + SOURCES_JS:
        contenu = lire(c)
        empreintes.append("%s %s" % (empreinte(c, contenu), c))
    for j in SOURCES_JS:
        js_parts.append("/* ======== %s ======== */\n%s" % (j, lire(j)))
    js = "\n\n".join(js_parts)

    coquille = lire(COQUILLE)
    bloc_css = "<style>\n%s\n</style>" % css
    bloc_js = "<script>\n%s\n</script>" % echapper_js(js)
    html = coquille.replace("<!-- @CSS@ -->", bloc_css).replace("<!-- @SCRIPTS@ -->", bloc_js)

    # l'empreinte de l'assemblage, lisible en tête de fichier et vérifiable
    global_hash = hashlib.sha256("\n".join(empreintes).encode("utf-8")).hexdigest()[:16]
    bandeau = (
        "<!--\n  PROJET3 — assemblé par assembler.py, NE PAS ÉDITER : éditer les sources.\n"
        "  Empreinte de l'assemblage : %s\n%s\n-->\n"
        % (global_hash, "\n".join("  " + e for e in empreintes))
    )
    html = html.replace("<!doctype html>", "<!doctype html>\n" + bandeau, 1)

    sortie = os.path.join(RACINE, SORTIE)
    with io.open(sortie, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)

    taille = os.path.getsize(sortie)
    print("ASSEMBLEUR : %s écrit (%d octets)" % (SORTIE, taille))
    print("  empreinte de l'assemblage : %s" % global_hash)
    for e in empreintes:
        print("  " + e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
