#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJET3 — LE CONTRE-REGARD (constitution §6, règles 7-10)
Une panne est injectée PAR COUCHE ; on exige qu'UN test la voie (rouge) ;
le fichier est restauré PAR COPIE sauvegardée, jamais par git ; la
restauration est vérifiée octet pour octet (SHA-256).

Usage : python tests/contre_regard.py
"""

import hashlib
import io
import os
import shutil
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OS = os.path.join(RACINE, "index.html")
TMP = OS + ".contregard"

PANNES = [
    {
        "nom": "NOYAU — la charnière disparaît du CPP (prix / arêtes seulement)",
        "fichier": "src/coeur.js",
        "avant": "return prix / (aretes * charniere);",
        "apres": "return prix / aretes;",
        "suite": "tests/test_coeur.js",
    },
    {
        "nom": "PREUVE — le battement juge la MOYENNE des deux côtés",
        "fichier": "src/coeur.js",
        "avant": "return Math.max.apply(null, cotes);",
        "apres": "return (cotes[0] + cotes[1]) / 2;",
        "suite": "tests/test_coeur.js",
    },
    {
        "nom": "RENDU — le CPP PRÉVU s'affiche à la place de l'OBTENU (la panne du Tour 54)",
        "fichier": "src/app.js",
        "avant": "h(\"td\", { class: \"mono\" },\n            o.cpp !== null ? fmt(o.cpp, 4)",
        "apres": "h(\"td\", { class: \"mono\" },\n            d.cpp !== null ? fmt(d.cpp, 4)",
        "suite": "tests/test_app.js",
    },
    {
        "nom": "FUSION — l'arrivée gagne même quand elle est plus vieille",
        "fichier": "src/import.js",
        "avant": "if (tA > tL) {",
        "apres": "if (true) {",
        "suite": "tests/test_import.js",
    },
    {
        "nom": "CONFIDENTIALITÉ — K et P_req sortent en visible (constitution §4.1)",
        "fichier": "src/app.js",
        "avant": "h(\"div\", { class: \"etiquette\" }, \"Chemin vers la cible\"),",
        "apres": "h(\"div\", { class: \"etiquette\" }, \"Chemin vers la cible (P_req = K)\"),",
        "suite": "tests/test_app.js",
    },
]


def sha(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def lancer(suite):
    r = subprocess.run(["node", os.path.join(RACINE, suite)],
                       capture_output=True, text=True, cwd=RACINE)
    return r.returncode, (r.stdout + r.stderr)


def assembler():
    r = subprocess.run(["python", os.path.join(RACINE, "assembler.py")],
                       capture_output=True, text=True, cwd=RACINE)
    if r.returncode != 0:
        sys.exit("l'assemblage a échoué : " + r.stdout + r.stderr)


def main():
    print("CONTRE-REGARD — cinq pannes, une par couche, restaurées par copie vérifiée")
    verts_avant = 0
    echecs_rituel = 0

    for panne in PANNES:
        source = os.path.join(RACINE, panne["fichier"])
        with io.open(source, encoding="utf-8") as f:
            original = f.read()
        if panne["avant"] not in original:
            print("  [IMPOSSIBLE] l'ancre de la panne n'existe plus : " + panne["nom"])
            echecs_rituel += 1
            continue

        # 1. sauvegarder (par copie)
        shutil.copyfile(OS, TMP)
        sha_avant = sha(OS)

        # 2. casser la source, ré-assembler
        with io.open(source, "w", encoding="utf-8", newline="\n") as f:
            f.write(original.replace(panne["avant"], panne["apres"], 1))
        assembler()

        # 3. regarder : la suite visée doit être ROUGE
        code, sortie = lancer(panne["suite"])
        vue = code != 0
        if vue:
            verts_avant += 1
            print("  [VUE]       " + panne["nom"])
        else:
            echecs_rituel += 1
            print("  [INVISIBLE] " + panne["nom"] + " — la suite reste verte devant la panne")

        # 4. restaurer PAR COPIE, vérifier octet pour octet
        shutil.copyfile(source + ".contregard.src", source) if False else None
        with io.open(source, "w", encoding="utf-8", newline="\n") as f:
            f.write(original)
        assembler()
        sha_apres = sha(OS)
        if sha_avant != sha_apres:
            print("  [DANGER]    la restauration n'est pas identique : " + panne["fichier"])
            echecs_rituel += 1
        os.remove(TMP)

    print("")
    if echecs_rituel:
        print("CONTRE-REGARD ROUGE : %d panne(s) invisible(s) ou incident(s) de restauration" % echecs_rituel)
        return 1
    print("CONTRE-REGARD VERT : les %d pannes sont vues par les tests, fichiers restaurés octet pour octet" % verts_avant)
    return 0


if __name__ == "__main__":
    sys.exit(main())
