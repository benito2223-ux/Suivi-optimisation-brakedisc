# -*- coding: utf-8 -*-
"""Repare la trace PROD 4.88.0 : backticks mangés par bash + omission Projet."""

s = open('ECHANGES.md', encoding='utf-8', newline='').read()
q = chr(39)
av = ("curl HTTP 200, **1 477 865 o**, , SW 200 ; empreinte **identique octet pour octet** au local ; "
      "Projet re-v\u00e9rifi\u00e9 4.88.0 inchang\u00e9 (Z Code, Tour 71 bis) |")
ap = ("curl HTTP 200, **1 496 294 o**, " + q + "TOOL_VERSION = " + chr(34) + "4.88.0" + chr(34) + q +
      ", SW 200 ; empreinte **identique octet pour octet** au local ; Projet re-d\u00e9ploy\u00e9 "
      "4.88.0 (il avait \u00e9t\u00e9 OUBLI\u00c9 au tour 71 \u2014 omission vue et corrig\u00e9e au m\u00eame moment) "
      "(Z Code, Tour 71 bis) |")
assert av in s, "trace introuvable"
s = s.replace(av, ap, 1)
open('ECHANGES.md', 'w', encoding='utf-8', newline='').write(s)
print("trace corrigee (TAILLE + TOOL_VERSION + omission Projet declaree)")
